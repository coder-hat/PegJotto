import unittest

from PegJotto import GameState
from PegJotto import Peg


class TestGameState(unittest.TestCase):

    def test_set_and_get_code(self):
        gs = GameState()
        self.assertIsNone(gs.get_code(), 'before set_code')
        expect = (Peg.RED, Peg.GREEN, Peg.BLUE, Peg.EMPTY)
        gs.set_code(expect)
        actual = gs.get_code()
        self.assertTupleEqual(actual, expect, 'After set_code')

    def test_score_guess(self):
        gs = GameState(code_length=3)
        code = (Peg.RED, Peg.GREEN, Peg.BLUE)
        gs.set_code(code)
        test_data = {
            '0 exact, 0 partial': ((Peg.YELLOW, Peg.YELLOW, Peg.YELLOW), (Peg.EMPTY, Peg.EMPTY, Peg.EMPTY)),
            '1 exact, 0 partial': ((Peg.YELLOW, Peg.YELLOW, Peg.BLUE), (Peg.BLACK, Peg.EMPTY, Peg.EMPTY)),
            '0 exact, 1 partial': ((Peg.BLUE, Peg.YELLOW, Peg.YELLOW, Peg.YELLOW), (Peg.WHITE, Peg.EMPTY, Peg.EMPTY)),
            '2 exact, 0 partial': ((Peg.RED, Peg.YELLOW, Peg.BLUE), (Peg.BLACK, Peg.BLACK, Peg.EMPTY)),
            '0 exact, 2 partial': ((Peg.GREEN, Peg.YELLOW, Peg.RED), (Peg.WHITE, Peg.WHITE, Peg.EMPTY)),
            '1 exact, 2 partial': ((Peg.BLUE, Peg.GREEN, Peg.RED), (Peg.BLACK, Peg.WHITE, Peg.WHITE)),
            '3 exact, 0 partial': ((Peg.RED, Peg.GREEN, Peg.BLUE), (Peg.BLACK, Peg.BLACK, Peg.BLACK)),
            '0 exact, 3 partial': ((Peg.GREEN, Peg.BLUE, Peg.RED), (Peg.WHITE, Peg.WHITE, Peg.WHITE))
        }
        for msg_key in test_data:
            guess, expect = test_data[msg_key]
            actual = gs.score_guess(guess)
            self.assertCountEqual(actual, expect, msg_key)

if __name__ == '__main__':
    unittest.main()
