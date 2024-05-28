import unittest
from tkinter import Tk
from connect_four import ConnectFour, PLAYER_X, EMPTY, ROWS, COLUMNS, PLAYER_O

class TestConnectFour(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.game = ConnectFour(self.root)

    def tearDown(self):
        self.root.quit()
        self.root.update_idletasks()
        self.root.destroy()

    def test_initialization(self):
        self.assertEqual(self.game.player, PLAYER_X)
        self.assertEqual(len(self.game.board), ROWS)
        self.assertEqual(len(self.game.board[0]), COLUMNS)
        self.assertTrue(all(cell == EMPTY for row in self.game.board for cell in row))

    def test_make_move(self):
        self.game.make_move(0)
        self.assertEqual(self.game.board[ROWS - 1][0], PLAYER_X)
        self.assertEqual(self.game.player, PLAYER_O)
        self.game.make_move(0)
        self.assertEqual(self.game.board[ROWS - 2][0], PLAYER_O)
        self.assertEqual(self.game.player, PLAYER_X)

    def test_winning_condition(self):

        for _ in range(3):
            self.game.make_move(0)
            self.game.make_move(1)
        self.game.make_move(0)
        self.assertTrue(self.game.check_winner(ROWS - 4, 0))


    def test_full_column_outcome(self):
        # Fill the first column
        for _ in range(ROWS):
            self.game.make_move(0)
        # Try to make a move in the full column
        self.assertIsNone(self.game.find_row(0))

if __name__ == "__main__":
    unittest.main()
