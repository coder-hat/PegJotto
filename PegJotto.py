from enum import Enum, unique
from random import choices

@unique
class Peg(Enum):
    '''
    Pegs serve as both playing pieces and scoring tokens.
    '''
    # Color definition strings from:
    # https://en.wikipedia.org/wiki/Web_colors
    EMPTY = ('#d3d3d3', '000') # X11 LightGray (211, 211, 211)
    RED =  ('red', 'RED')
    GREEN = ('green', 'GRN')
    BLUE = ('blue', 'BLU')
    YELLOW = ('#ffff00', 'YLW') # X11 Yellow (255, 255, 0)
    ORANGE = ('#ff8c00', 'ORN') # X11 DarkOrange (255, 140, 0)
    BROWN = ('#8b4513', 'BRN') # SaddleBrown (139, 69, 19)
    BLACK = ('black', 'BLK')
    WHITE = ('white', 'WHT')

    def __init__(self, color, tla):
        self.color = color  # TkInter-compatible color text string
        self.tla = tla  # Three-Letter-Acronym

    @property
    def short_name(self):
        return self.tla

class GameState:
    '''
    Contains all the data state required for a game of Peg Jotto,
    along with the methods necessary to mutate that state based
    on player guesses.
    '''
    def __init__(self, code_length=4, allowed_guesses=6, score_pegs_as_code=False):
        self.code_length = code_length
        self.allowed_guesses = allowed_guesses
        self.score_pegs_as_code = score_pegs_as_code
        # Each game requires resetting the following properties.
        self.used_guesses = 0
        self.guesses = []
        self.code = []
        self.game_over = False
        self.game_won = False

    def reset(self):
        self.used_guesses = 0
        self.guesses = []
        self.code = []
        self.game_over = False
        self.game_won = False

    def is_code_peg(self, p):
        return False if not self.score_pegs_as_code and (p == Peg.BLACK or p == Peg.WHITE) else True

    def make_random_code(self):
        peg_list = [p for p in Peg if self.is_code_peg(p)]
        return choices(peg_list, k=self.code_length)

    def set_code(self, code=None):
        if code and len(code) != self.code_length:
            raise IndexError('code has wrong number of Pegs')
        self.code = code if code else self.make_random_code()

    def get_code(self):
        return self.code

    def submit_guess(self, guess):
        '''
        Scores the guess tuple of Pegs and appends it and its score tuple
        as a (guess, score) tuple-pair of Peg tuples to this GameState's guesses list.
        Updates game_over and game_won flag values relative to this guess submission.
        '''
        score = self.score_guess(guess)
        self.guesses.append((guess, score))
        self.game_over = len(self.guesses) >= self.allowed_guesses
        self.game_won = sum((1 if p == Peg.BLACK else 0 for p in score))

    def score_guess(self, guess):
        score = []
        misses = []
        remainders = []
        # Collect exact matches (color AND position) first.
        # Anything else is a "miss" at this point.
        for i in range(self.code_length):
            if guess[i] == self.code[i]:
                score.append(Peg.BLACK)
            else:
                misses.append(guess[i])
                remainders.append(self.code[i])
        # Each miss is either partial (color matches) or complete.
        for p in misses:
            try:
                remainders.remove(p)
                score.append(Peg.WHITE)
            except ValueError:
                score.append(Peg.EMPTY)
        return tuple(score)
