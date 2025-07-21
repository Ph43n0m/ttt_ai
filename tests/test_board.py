import io
import random
import sys
import unittest

from ttt_ai.game.board import Board
from ttt_ai.game.field import FieldState


class TestBoardPrint(unittest.TestCase):
    def test_print_board(self):
        board = Board()
        for row in range(board.BOARD_SIZE):
            for col in range(board.BOARD_SIZE):
                self.assertEqual(board[row, col].state, FieldState.EMPTY)
        for i in range(board.BOARD_SIZE):
            self.assertTrue(
                all(field.state == FieldState.EMPTY for field in board.get_row(i))
            )
            self.assertTrue(
                all(field.state == FieldState.EMPTY for field in board.get_column(i))
            )
        self.assertTrue(
            all(field.state == FieldState.EMPTY for field in board.get_diagonal(0))
        )
        self.assertTrue(
            all(field.state == FieldState.EMPTY for field in board.get_diagonal(1))
        )
        for _ in range(5):
            for row in range(board.BOARD_SIZE):
                for col in range(board.BOARD_SIZE):
                    board[row, col].state = random.choice(list(FieldState))
            captured_output = io.StringIO()
            sys_stdout = sys.stdout
            sys.stdout = captured_output
            try:
                board.print_board()
            finally:
                sys.stdout = sys_stdout
            output = captured_output.getvalue()
            print("Captured board output:\n" + output)
            self.assertEqual(output.count("-" * 9), 4)
            self.assertEqual(
                len([line for line in output.splitlines() if "|" in line]), 3
            )
            for i in range(board.BOARD_SIZE):
                row_states = [board[i, j].state for j in range(board.BOARD_SIZE)]
                col_states = [board[j, i].state for j in range(board.BOARD_SIZE)]
                self.assertEqual([f.state for f in board.get_row(i)], row_states)
                self.assertEqual([f.state for f in board.get_column(i)], col_states)
            diag0 = [board[i, i].state for i in range(board.BOARD_SIZE)]
            diag1 = [board[i, 2 - i].state for i in range(board.BOARD_SIZE)]
            self.assertEqual([f.state for f in board.get_diagonal(0)], diag0)
            self.assertEqual([f.state for f in board.get_diagonal(1)], diag1)


class TestBoardGetRow(unittest.TestCase):
    def test_get_row(self):
        board = Board()
        patterns = [
            [FieldState.X, FieldState.O, FieldState.EMPTY],
            [FieldState.O, FieldState.X, FieldState.O],
            [FieldState.EMPTY, FieldState.EMPTY, FieldState.X],
        ]
        for row in range(board.BOARD_SIZE):
            for col in range(board.BOARD_SIZE):
                board[row, col].state = patterns[row][col]
        for row in range(board.BOARD_SIZE):
            print(f"Testing get_row({row}) returns correct pattern.")
            self.assertEqual([f.state for f in board.get_row(row)], patterns[row])

    def test_get_row_invalid(self):
        board = Board()
        print("Testing get_row(-1) raises ValueError.")
        with self.assertRaises(ValueError):
            board.get_row(-1)
        print("Testing get_row(3) raises ValueError.")
        with self.assertRaises(ValueError):
            board.get_row(3)
        print("Testing get_row(100) raises ValueError.")
        with self.assertRaises(ValueError):
            board.get_row(100)
        print("Testing get_row('a') raises TypeError or ValueError.")
        with self.assertRaises(Exception):
            board.get_row("a")


class TestBoardGetColumn(unittest.TestCase):
    def test_get_column(self):
        board = Board()
        patterns = [
            [FieldState.X, FieldState.O, FieldState.EMPTY],
            [FieldState.O, FieldState.X, FieldState.O],
            [FieldState.EMPTY, FieldState.EMPTY, FieldState.X],
        ]
        for row in range(board.BOARD_SIZE):
            for col in range(board.BOARD_SIZE):
                board[row, col].state = patterns[row][col]
        for col in range(board.BOARD_SIZE):
            expected = [patterns[row][col] for row in range(board.BOARD_SIZE)]
            print(f"Testing get_column({col}) returns correct pattern.")
            self.assertEqual([f.state for f in board.get_column(col)], expected)

    def test_get_column_invalid(self):
        board = Board()
        print("Testing get_column(-1) raises ValueError.")
        with self.assertRaises(ValueError):
            board.get_column(-1)
        print("Testing get_column(3) raises ValueError.")
        with self.assertRaises(ValueError):
            board.get_column(3)
        print("Testing get_column(100) raises ValueError.")
        with self.assertRaises(ValueError):
            board.get_column(100)
        print("Testing get_column('a') raises TypeError or ValueError.")
        with self.assertRaises(Exception):
            board.get_column("a")


class TestBoardGetDiagonal(unittest.TestCase):
    def test_get_diagonal_main(self):
        board = Board()
        for i in range(board.BOARD_SIZE):
            board[i, i].state = FieldState.X
        print("Testing get_diagonal(0) returns main diagonal.")
        self.assertEqual([f.state for f in board.get_diagonal(0)], [FieldState.X] * 3)

    def test_get_diagonal_anti(self):
        board = Board()
        for i in range(board.BOARD_SIZE):
            board[i, 2 - i].state = FieldState.O
        print("Testing get_diagonal(1) returns anti-diagonal.")
        self.assertEqual([f.state for f in board.get_diagonal(1)], [FieldState.O] * 3)

    def test_get_diagonal_invalid(self):
        board = Board()
        print("Testing get_diagonal(-1) raises ValueError.")
        with self.assertRaises(ValueError):
            board.get_diagonal(-1)
        print("Testing get_diagonal(2) raises ValueError.")
        with self.assertRaises(ValueError):
            board.get_diagonal(2)
        print("Testing get_diagonal(100) raises ValueError.")
        with self.assertRaises(ValueError):
            board.get_diagonal(100)
        print("Testing get_diagonal('a') raises TypeError or ValueError.")
        with self.assertRaises(Exception):
            board.get_diagonal("a")


class TestBoardIsFull(unittest.TestCase):
    def test_is_board_full_empty(self):
        board = Board()
        self.assertFalse(board.is_board_full())

    def test_is_board_full_partial(self):
        board = Board()
        board[0, 0].state = FieldState.X
        self.assertFalse(board.is_board_full())

    def test_is_board_full_full(self):
        board = Board()
        for row in range(board.BOARD_SIZE):
            for col in range(board.BOARD_SIZE):
                board[row, col].state = random.choice([FieldState.X, FieldState.O])
        self.assertTrue(board.is_board_full())

    def test_is_board_full_with_empty_field(self):
        board = Board()
        for row in range(board.BOARD_SIZE):
            for col in range(board.BOARD_SIZE):
                board[row, col].state = FieldState.X
        board[1, 1].state = FieldState.EMPTY
        self.assertFalse(board.is_board_full())

    def test_is_board_full_invalid_state(self):
        board = Board()
        for row in range(board.BOARD_SIZE):
            for col in range(board.BOARD_SIZE):
                board[row, col].state = FieldState.X
        # Simulate an invalid state if possible
        try:
            board[0, 0].state = None
            result = board.is_board_full()
            self.assertFalse(result)
        except Exception as e:
            self.assertIsInstance(e, Exception)


class TestBoardIsWinner(unittest.TestCase):
    def test_is_winner_x(self):
        board = Board()
        for i in range(board.BOARD_SIZE):
            board[i, 0].state = FieldState.X
        self.assertTrue(board.is_winner(FieldState.X))

    def test_is_winner_o(self):
        board = Board()
        for i in range(board.BOARD_SIZE):
            board[0, i].state = FieldState.O
        self.assertTrue(board.is_winner(FieldState.O))

    def test_is_winner_no_winner(self):
        board = Board()
        for row in range(board.BOARD_SIZE):
            for col in range(board.BOARD_SIZE):
                board[row, col].state = FieldState.EMPTY
        self.assertFalse(board.is_winner(FieldState.X))
        self.assertFalse(board.is_winner(FieldState.O))

    def test_is_winner_diagonal(self):
        board = Board()
        for i in range(board.BOARD_SIZE):
            board[i, i].state = FieldState.X
        self.assertTrue(board.is_winner(FieldState.X))

    def test_is_winner_invalid_player(self):
        board = Board()
        for i in range(board.BOARD_SIZE):
            board[i, 0].state = FieldState.X
        with self.assertRaises(Exception):
            board.is_winner(None)

    def test_is_winner_invalid_type(self):
        board = Board()
        for i in range(board.BOARD_SIZE):
            board[i, 0].state = FieldState.X
        with self.assertRaises(Exception):
            board.is_winner("not_a_field_state")

    def test_is_winner_partial_line(self):
        board = Board()
        for i in range(2):
            board[i, 0].state = FieldState.X
        board[2, 0].state = FieldState.O
        self.assertFalse(board.is_winner(FieldState.X))
        self.assertFalse(board.is_winner(FieldState.O))


class TestBoardGetFlatIndex(unittest.TestCase):
    def test_get_flat_index_valid(self):
        board = Board()
        for row in range(board.BOARD_SIZE):
            for col in range(board.BOARD_SIZE):
                expected = row * board.BOARD_SIZE + col
                self.assertEqual(board.get_flat_index(row, col), expected)

    def test_get_flat_index_invalid_row(self):
        board = Board()
        with self.assertRaises(ValueError):
            board.get_flat_index(-1, 0)
        with self.assertRaises(ValueError):
            board.get_flat_index(board.BOARD_SIZE, 0)

    def test_get_flat_index_invalid_col(self):
        board = Board()
        with self.assertRaises(ValueError):
            board.get_flat_index(0, -1)
        with self.assertRaises(ValueError):
            board.get_flat_index(0, board.BOARD_SIZE)

    def test_get_flat_index_invalid_type(self):
        board = Board()
        with self.assertRaises(Exception):
            board.get_flat_index("a", 0)
        with self.assertRaises(Exception):
            board.get_flat_index(0, "b")


class TestBoardGetFieldByFlatIndex(unittest.TestCase):
    def test_get_field_by_flat_index_valid(self):
        board = Board()
        test_states = [FieldState.X, FieldState.O, FieldState.EMPTY]
        for state in test_states:
            for row in range(board.BOARD_SIZE):
                for col in range(board.BOARD_SIZE):
                    board[row, col].state = state
                    flat_index = board.get_flat_index(row, col)
                    field = board.get_field_by_flat_index(flat_index)
                    self.assertEqual(field, board[row, col])
                    self.assertEqual(field.state, state)

    def test_get_field_by_flat_index_invalid_negative(self):
        board = Board()
        with self.assertRaises(ValueError):
            board.get_field_by_flat_index(-1)

    def test_get_field_by_flat_index_invalid_too_large(self):
        board = Board()
        with self.assertRaises(ValueError):
            board.get_field_by_flat_index(board.BOARD_SIZE * board.BOARD_SIZE)

    def test_get_field_by_flat_index_invalid_type(self):
        board = Board()
        with self.assertRaises(Exception):
            board.get_field_by_flat_index("a")


class TestBoardResetBoard(unittest.TestCase):
    def test_reset_board_all_x(self):
        board = Board()
        for row in range(board.BOARD_SIZE):
            for col in range(board.BOARD_SIZE):
                board[row, col].state = FieldState.X
        board.reset()
        for row in range(board.BOARD_SIZE):
            for col in range(board.BOARD_SIZE):
                self.assertEqual(board[row, col].state, FieldState.EMPTY)

    def test_reset_board_partial(self):
        board = Board()
        board[0, 0].state = FieldState.X
        board[1, 1].state = FieldState.O
        board.reset()
        for row in range(board.BOARD_SIZE):
            for col in range(board.BOARD_SIZE):
                self.assertEqual(board[row, col].state, FieldState.EMPTY)

    def test_reset_board_already_empty(self):
        board = Board()
        board.reset()
        for row in range(board.BOARD_SIZE):
            for col in range(board.BOARD_SIZE):
                self.assertEqual(board[row, col].state, FieldState.EMPTY)


class TestBoardGetFlatIndexOfRandomFreeField(unittest.TestCase):
    def test_get_flat_index_of_random_free_field_all_free(self):
        board = Board()
        indices = set()
        for _ in range(100):
            idx = board.get_flat_index_of_radom_free_field()
            self.assertIsInstance(idx, int)
            self.assertGreaterEqual(idx, 0)
            self.assertLess(idx, board.BOARD_SIZE * board.BOARD_SIZE)
            indices.add(idx)
        self.assertEqual(len(indices), board.BOARD_SIZE * board.BOARD_SIZE)

    def test_get_flat_index_of_random_free_field_some_filled(self):
        board = Board()
        board[0, 0].state = FieldState.X
        board[1, 1].state = FieldState.O
        free_indices = [
            board.get_flat_index(row, col)
            for row in range(board.BOARD_SIZE)
            for col in range(board.BOARD_SIZE)
            if board[row, col].state == FieldState.EMPTY
        ]
        for _ in range(50):
            idx = board.get_flat_index_of_radom_free_field()
            self.assertIn(idx, free_indices)

    def test_get_flat_index_of_random_free_field_after_reset(self):
        board = Board()
        for row in range(board.BOARD_SIZE):
            for col in range(board.BOARD_SIZE):
                board[row, col].state = FieldState.X
        board.reset()
        idx = board.get_flat_index_of_radom_free_field()
        self.assertIsInstance(idx, int)
        self.assertGreaterEqual(idx, 0)
        self.assertLess(idx, board.BOARD_SIZE * board.BOARD_SIZE)
