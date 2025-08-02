import unittest

from pyautogui import Point

from ttt_ai.game.agent.minimax_agent import MiniMaxAgent
from ttt_ai.game.board import Board
from ttt_ai.game.field import FieldState


class TestMiniMaxAgent(unittest.TestCase):
    def setUp(self):
        self.agent = MiniMaxAgent(FieldState.X, 0)
        self.board = Board()
        self.test_point = Point(100, 100)

    def test_get_best_move_empty_board(self):
        self._generate_board(full_board=False)
        self.board.get_field_by_flat_index(0).location = self.test_point
        best_move = self.agent.get_best_move(self.board)
        self.assertIsNotNone(
            best_move, "Best move should be not None on an empty board."
        )
        self.assert_best_move_for_board(0)

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

        self.board.print_board()
        self.board.get_field_by_flat_index(target_field).location = self.test_point
        self.assert_best_move_for_board(target_field)

        # Simulate another partial board state
        self._generate_board(full_board=False)
        target_field = 6
        self.board[0, 0].state = FieldState.X
        self.board[0, 1].state = FieldState.O
        self.board[1, 0].state = FieldState.X
        self.board[1, 1].state = FieldState.O

        self.board.print_board()
        self.board.get_field_by_flat_index(target_field).location = self.test_point
        self.assert_best_move_for_board(target_field)

        # Simulate another partial board state
        self._generate_board(full_board=False)
        target_field = 7
        self.board[0, 0].state = FieldState.X
        self.board[0, 1].state = FieldState.O
        self.board[0, 2].state = FieldState.X
        self.board[1, 1].state = FieldState.O

        self.board.print_board()
        self.board.get_field_by_flat_index(target_field).location = self.test_point
        self.assert_best_move_for_board(target_field)

        # Simulate a partial board state
        self._generate_board(full_board=False)
        target_field = 2
        self.board[0, 0].state = FieldState.X
        self.board[0, 1].state = FieldState.X
        self.board[1, 1].state = FieldState.O

        self.board.print_board()
        self.board.get_field_by_flat_index(target_field).location = self.test_point

        self.assert_best_move_for_board(target_field)

        # Simulate another partial board state
        self._generate_board(full_board=False)
        target_field = 0
        self.board[1, 2].state = FieldState.O
        self.board[2, 0].state = FieldState.X
        self.board[2, 1].state = FieldState.O
        self.board[2, 2].state = FieldState.X

        self.board.print_board()
        self.board.get_field_by_flat_index(target_field).location = self.test_point
        self.assert_best_move_for_board(target_field)

        # Simulate another partial board state
        target_field = 1
        self.board[0, 0].state = FieldState.X

        self.board.print_board()
        self.board.get_field_by_flat_index(target_field).location = self.test_point
        self.assert_best_move_for_board(target_field)

        # Simulate another partial board state
        self.board[1, 0].state = FieldState.O
        target_field = 4

        self.board.print_board()
        self.board.get_field_by_flat_index(target_field).location = self.test_point
        self.assert_best_move_for_board(target_field)

    def assert_best_move_for_board(self, target_field):
        """
        Helper function to assert the best move for a given board state.
        Args:
            board (Board): The board instance to test.
            target_field (int): The expected best move field index.
            :param target_field:
        """
        best_move = self.agent.get_best_move(self.board)
        self.assertEqual(
            best_move, target_field, f"Best move should be {target_field}."
        )
        self.assertEqual(
            self.board.get_field_by_flat_index(best_move).location,
            self.test_point,
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


class TestAgentWinRate(unittest.TestCase):
    def setUp(self):
        self.agent = MiniMaxAgent(FieldState.X, 0)

    def test_get_win_rate(self):
        print("Testing win rate with no games played.")
        self.assertEqual(
            self.agent.get_win_rate(),
            0.0,
            "Win rate should be 0.0 when no games are played.",
        )
        for draws in range(1, 5):
            for losts in range(0, 5):
                for wins in range(0, 5):
                    self.agent.games_won = wins
                    self.agent.games_lost = losts
                    self.agent.games_draw = draws
                    expected_rate = wins / (draws + losts + wins)
                    print(
                        f"Testing win rate for {wins} wins out of {(draws + losts + wins)} games: {expected_rate:.2f}"
                    )
                    self.assertEqual(self.agent.get_win_rate(), expected_rate)
        self.agent.games_won = 0
        self.agent.games_lost = 0
        self.agent.games_draw = 1
        print("Testing win rate with no game won.")
        self.assertEqual(self.agent.get_win_rate(), 0.0)
        self.agent.games_won = -1
        self.agent.games_lost = 0
        self.agent.games_draw = 1
        print("Testing win rate with negative games_won.")
        self.assertEqual(self.agent.get_win_rate(), 0.0)
        self.agent.games_won = 0
        self.agent.games_lost = -1
        self.agent.games_draw = 0
        print("Testing win rate with negative games_lost.")
        self.assertEqual(self.agent.get_win_rate(), 0.0)
        self.agent.games_won = 0
        self.agent.games_lost = 0
        self.agent.games_draw = -1
        print("Testing win rate with negative games_draw.")
        self.assertEqual(self.agent.get_win_rate(), 0.0)
        self.agent.games_won = -1
        self.agent.games_lost = -1
        self.agent.games_draw = -1
        print(
            "Testing win rate with all negative games_won, game_count and games_draw."
        )
        self.assertEqual(self.agent.get_win_rate(), 0.0)


class TestPlayWinLossRatio(unittest.TestCase):
    def setUp(self):
        self.agent = MiniMaxAgent(FieldState.X, 0)

    def test_get_wl_ratio(self):
        self.agent.games_draw = 5  # draws will not affect the win/loss ratio! So we set it to 5 to make sure it does not affect the tests.

        print("Testing win/loss ratio with no games played.")
        self.assertEqual(self.agent.get_wl_ratio(), 0.0)
        self.agent.games_won = 5
        self.agent.games_lost = 0
        print("Testing win/loss ratio with 5 wins and 0 losses.")
        self.assertEqual(self.agent.get_wl_ratio(), 5.0)
        self.agent.games_won = 0
        self.agent.games_lost = 3
        print("Testing win/loss ratio with 0 wins and 3 losses.")
        self.assertEqual(self.agent.get_wl_ratio(), 0.0)
        for loses in range(0, 11):
            for wins in range(0, loses * 2 + 1):
                self.agent.games_won = wins
                self.agent.games_lost = loses
                expected_ratio = wins / loses if loses > 0 else float(wins)
                print(
                    f"Testing win/loss ratio for {wins} wins and {loses} losses: {expected_ratio:.2f}"
                )
                self.assertEqual(self.agent.get_wl_ratio(), expected_ratio)
        self.agent.games_won = -2
        self.agent.games_lost = 4
        print("Testing win/loss ratio with -2 wins and 4 losses.")
        self.assertEqual(self.agent.get_wl_ratio(), 0.0)
        self.agent.games_won = 4
        self.agent.games_lost = -2
        print("Testing win/loss ratio with 4 wins and -2 losses.")
        self.assertEqual(self.agent.get_wl_ratio(), 0.0)
        self.agent.games_won = -2
        self.agent.games_lost = -2
        print("Testing win/loss ratio with -2 wins and -2 losses.")
        self.assertEqual(self.agent.get_wl_ratio(), 0.0)
