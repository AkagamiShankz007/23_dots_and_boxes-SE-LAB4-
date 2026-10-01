import unittest

from board import Board
from game import DotsAndBoxes
from rules import valid_move


class DotsAndBoxesTests(unittest.TestCase):
    def test_valid_horizontal_move(self):
        board = Board()
        self.assertTrue(valid_move(board, "H", 0, 0))

        board.add_line("H", 0, 0)
        self.assertFalse(valid_move(board, "H", 0, 0))

    def test_valid_vertical_move(self):
        board = Board()
        self.assertTrue(valid_move(board, "V", 0, 1))
        self.assertTrue(valid_move(board, "V", 1, 1))

    def test_invalid_repeated_move(self):
        board = Board()
        board.add_line("H", 0, 0)

        with self.assertRaises(ValueError):
            board.add_line("H", 0, 0)

    def test_completion_of_a_box_updates_score_and_turn(self):
        game = DotsAndBoxes()

        for move in [("H", 0, 0), ("V", 0, 0), ("V", 0, 1), ("H", 1, 0)]:
            game.apply_move(*move)

        self.assertEqual(game.scores, [0, 1])
        self.assertEqual(game.current, 1)
        self.assertIn((0, 0), game.board.completed)
        self.assertEqual(game.board.box_owners[(0, 0)], 2)

    def test_undo_last_move_restores_board_and_player_state(self):
        game = DotsAndBoxes()
        game.apply_move("H", 0, 0)
        game.undo_last_move()

        self.assertEqual(game.scores, [0, 0])
        self.assertEqual(game.current, 0)
        self.assertFalse(game.board.horizontal[0][0])

    def test_end_of_game_condition(self):
        board = Board()

        for r in range(board.rows + 1):
            for c in range(board.cols):
                board.add_line("H", r, c)

        for r in range(board.rows):
            for c in range(board.cols + 1):
                board.add_line("V", r, c)

        self.assertTrue(board.is_complete())


if __name__ == "__main__":
    unittest.main()
