from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk

# Board Position [C]ell [V]alues
CV_OFF = 0
CV_EMPTY = 1
CV_PEG = 2

class PegBoard:
    '''
    Coordinate system: zero-based (row, col) with origin in upper-left corner (i.e. board[r=0][c=0])
    '''
    ROW_COUNT = 7
    COL_COUNT = 7

    # Currently, this is the only supported board configuration
    ENGLISH_EMPTY = [(3,3)]
    ENGLISH_OFF = [
        (0,0), (0,1), (0,5), (0,6),
        (1,0), (1,1), (1,5), (1,6),
        (5,0), (5,1), (5,5), (5,6),
        (6,0), (6,1), (6,5), (6,6)
    ]

    def __init__(self):
        self.board = [[CV_PEG] * PegBoard.COL_COUNT for row in range(PegBoard.ROW_COUNT)]
        for r, c in PegBoard.ENGLISH_EMPTY: self.board[r][c] = CV_EMPTY
        for r, c in PegBoard.ENGLISH_OFF: self.board[r][c] = CV_OFF
        self.initial_pegs = self.count_pegs()
        self.current_pegs = self.initial_pegs
        self.turns_taken = 0
        self.selected_peg = None

    def count_pegs(self):
        peg_count = 0
        for row in self.board:
            for cell in row:
                if cell == CV_PEG: peg_count += 1
        return peg_count

    def select_peg(self, select_row, select_column):
        if self.board[select_row][select_column] == CV_PEG:
            if self.selected_peg and self.selected_peg == (select_row, select_column):
                self.selected_peg = None
            else:
                self.selected_peg = (select_row, select_column)
    
    def jump_and_remove(self, landing_row, landing_column):
        '''
        Attempts to jump self's currently selected peg orthogonally over an adjacent peg
        to the board location specified by the landing row, column args.
        Returns the removed (jumped over) cell location pair (removed_row, removed_col) if successful, otherwise None.
        '''
        remove_cell = self.is_legal_jump(landing_row, landing_column)
        if remove_cell:
            removed_row, removed_column = remove_cell
            selected_row, selected_column = self.selected_peg
            self.board[selected_row][selected_column] = CV_EMPTY
            self.board[removed_row][removed_column] = CV_EMPTY
            self.board[landing_row][landing_column] = CV_PEG
            self.current_pegs = self.count_pegs()
            self.turns_taken += 1
            self.selected_peg = None
            return removed_row, removed_column
        return None

    def is_legal_jump(self, landing_row, landing_column):
        if not self.selected_peg:
            return False  # no selected peg means no jump origin
        selected_row, selected_column  = self.selected_peg
        i_between = lambda a, b: a - 1 if a > b else a + 1
        if (landing_row == selected_row):
            if abs(landing_column - selected_column) == 2:
                between_column = i_between(selected_column, landing_column)
                return (landing_row, between_column) if pb.board[landing_row][between_column] == CV_PEG else None
            else:
                return None # wrong column-distance
        elif (landing_column == selected_column):
            if abs(landing_row - selected_row) == 2:
                between_row = i_between(selected_row, landing_row)
                return (between_row, landing_column) if pb.board[between_row][landing_column] == CV_PEG else None
            else:
                return None # wrong row-distance
        else:
            return None # non-orthogonal

    def status_text(self):
        return "Moves={} Pegs={}/{}".format(self.turns_taken, self.current_pegs, self.initial_pegs)

    def print_the_board(self):
        glyph = [" #", " o", " .", " *"]
        for r, row in enumerate(pb.board):
            for c, cell_value in enumerate(row):
                ofs = 1 if self.selected_peg == (r, c) else 0
                s = glyph[cell_value + ofs]
                print(s, end='')
            print()


# def i_between(a, b):
#     return a - 1 if a > b else a + 1
            
#----- GUI functions

def get_photo_image(png_file):
    image = Image.open(str(png_file))
    photo = ImageTk.PhotoImage(image)
    return photo

def click_handler(pb, w, r, c, pgi):
    cell_value = pb.board[r][c]
    if not (cell_value == CV_OFF):
        if cell_value == CV_PEG:
            pb.select_peg(r,c)
        else:
            pb.jump_and_remove(r, c)
    print(pb.status_text())
    update_display(pb, w, pgi)

def update_display(pb, w, pgi):
    # refresh every widget in the PegBoard portion of the display grid
    for r, row in enumerate(pb.board):
        for c, cell_value in enumerate(row):
            if cell_value != CV_OFF:
                widget = w.grid_slaves(row=r, column=c)[0]
                widget.config(image=pgi[cell_value])
                widget.config(highlightbackground="white")
    # highight the selected peg (if a peg is selected)
    if pb.selected_peg:
        r, c = pb.selected_peg
        widget = w.grid_slaves(row=r, column=c)[0]
        widget.config(highlightbackground="green")
    # update the status text label
    widget = w.grid_slaves(row=PegBoard.ROW_COUNT, column=0)[0]
    widget.config(text=pb.status_text())

#----- Program Main

if __name__ == "__main__":

    pb = PegBoard()
    
    window = tk.Tk()
    window.title("Peg Solitaire")

    p_image_root = Path('/Users/ksdj/Pictures/Art/PegSolitaireImages/')
    peg_images = [get_photo_image(p_image_root.joinpath(png_name)) for png_name in ("Null32.png", "BlackRing32.png", "BluePeg32.png")]

    for irow in range(PegBoard.ROW_COUNT):
        for icol in range(PegBoard.COL_COUNT):
            cell_value = pb.board[irow][icol]
            if cell_value == CV_OFF:
                cell_widget = tk.Label(image=peg_images[cell_value])
            else:
                cell_widget = tk.Button(
                    image=peg_images[cell_value], 
                    command=lambda pb=pb, w=window, r=irow, c=icol, pgi=peg_images: click_handler(pb, w, r, c, pgi)
                )
            cell_widget.grid(row=irow, column=icol)
            # button.bind("<Button-1>", button_clicked)
    lbl_status = tk.Label(text=pb.status_text())
    lbl_status.grid(row=PegBoard.ROW_COUNT, column=0, columnspan=PegBoard.COL_COUNT)

    window.mainloop()