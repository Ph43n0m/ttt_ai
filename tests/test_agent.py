import unittest

from pyautogui import Point

from ttt_ai.agent import MiniMaxAgent
from ttt_ai.board import Board
from ttt_ai.field import FieldState


class TestMiniMaxAgent(unittest.TestCase):
    def setUp(self):
        self.agent = MiniMaxAgent()
        self.board = Board()

    def test_get_best_move_empty_board(self):
        self._generate_board(full_board=False)
        best_move = self.agent.get_best_move(self.board)
        self.assertIsNotNone(
            best_move, "Best move should be not None on an empty board."
        )
        self.assertEqual(best_move, 6, "Best move should be 6 on an empty board.")

    def test_get_best_move_full_board(self):
        self._generate_board(full_board=True)
        best_move = self.agent.get_best_move(self.board)
        self.assertIsNone(best_move, "Best move should be None on a full board.")

    def test_get_best_move_winner_exists(self):
        # Simulate a winning condition for X
        self._generate_board(full_board=False, winner=FieldState.X)
        best_move = self.agent.get_best_move(self.board)
        self.assertIsNone(best_move, "Best move should be None when a X winner exists.")
        # Simulate a winning condition for O
        self._generate_board(full_board=False, winner=FieldState.O)
        best_move = self.agent.get_best_move(self.board)
        self.assertIsNone(best_move, "Best move should be None when a O winner exists.")

    def test_get_best_move_for_partial_board(self):
        """
        Test the agent's ability to find the best move on a partially filled board.
        This test assumes that the agent can correctly identify the best move in a non-terminal state.
        """
        target_field = 0
        test_point = Point(100, 100)

        # Simulate a partial board state
        self._generate_board(full_board=False)
        target_field = 2
        self.board[0, 0].state = FieldState.X
        self.board[0, 1].state = FieldState.X
        self.board[1, 1].state = FieldState.O

        self.board.print_board()
        self.board.get_field_by_flat_index(target_field).location = test_point

        self.assert_best_move_for_board(target_field, test_point)

        # Simulate another partial board state
        self._generate_board(full_board=False)
        target_field = 0
        self.board[1, 2].state = FieldState.O
        self.board[2, 0].state = FieldState.X
        self.board[2, 1].state = FieldState.O
        self.board[2, 2].state = FieldState.X

        self.board.print_board()

        self.board.get_field_by_flat_index(target_field).location = test_point

        self.assert_best_move_for_board(target_field, test_point)

        # Simulate another partial board state
        target_field = 3
        self.board[0, 0].state = FieldState.X

        self.board.print_board()

        self.board.get_field_by_flat_index(target_field).location = test_point

        self.assert_best_move_for_board(target_field, test_point)

        # Simulate another partial board state
        self.board[1, 0].state = FieldState.O
        target_field = 4

        self.board.print_board()

        self.board.get_field_by_flat_index(target_field).location = test_point

        self.assert_best_move_for_board(target_field, test_point)

    def assert_best_move_for_board(self, target_field, test_point=Point(100, 100)):
        """
        Helper function to assert the best move for a given board state.
        Args:
            board (Board): The board instance to test.
            target_field (int): The expected best move field index.
            :param target_field:
            :param test_point:
        """
        best_move = self.agent.get_best_move(self.board)
        self.assertEqual(
            best_move, target_field, f"Best move should be {target_field}."
        )
        self.assertEqual(
            self.board.get_field_by_flat_index(best_move).location,
            test_point,
            "Field must have a specific location.",
        )

    def _generate_board(self, full_board=False, winner=FieldState.EMPTY):
        """
        Helper function to generate a board state.
        Args:
            full_board (bool): If True, fill the board completely.
            winner (FieldState): If provided, set a winning condition for this player.
        Returns:
            Board: A board instance with the specified state.
        """
        for row in range(self.board.BOARD_SIZE):
            for col in range(self.board.BOARD_SIZE):
                if full_board:
                    self.board[row, col].state = (
                        FieldState.X if (row + col) % 2 == 0 else FieldState.O
                    )
                else:
                    self.board[row, col].state = FieldState.EMPTY

        if winner == FieldState.X:
            self.board[0, 0].state = FieldState.X
            self.board[0, 1].state = FieldState.X
            self.board[0, 2].state = FieldState.X
        elif winner == FieldState.O:
            self.board[0, 0].state = FieldState.O
            self.board[0, 1].state = FieldState.O
            self.board[0, 2].state = FieldState.O

        return self.board
