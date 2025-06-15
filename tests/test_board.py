import io
import sys
import unittest
import random

from ttt_ai.board import Board
from ttt_ai.field import FieldState


class TestBoardPrint(unittest.TestCase):
    def test_print_board(self):
        board = Board()
        for row in range(3):
            for col in range(3):
                self.assertEqual(board[row, col].state, FieldState.EMPTY)
        for i in range(3):
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
            for row in range(3):
                for col in range(3):
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
            for i in range(3):
                row_states = [board[i, j].state for j in range(3)]
                col_states = [board[j, i].state for j in range(3)]
                self.assertEqual([f.state for f in board.get_row(i)], row_states)
                self.assertEqual([f.state for f in board.get_column(i)], col_states)
            diag0 = [board[i, i].state for i in range(3)]
            diag1 = [board[i, 2 - i].state for i in range(3)]
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
        for row in range(3):
            for col in range(3):
                board[row, col].state = patterns[row][col]
        for row in range(3):
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
        for row in range(3):
            for col in range(3):
                board[row, col].state = patterns[row][col]
        for col in range(3):
            expected = [patterns[row][col] for row in range(3)]
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
        for i in range(3):
            board[i, i].state = FieldState.X
        print("Testing get_diagonal(0) returns main diagonal.")
        self.assertEqual([f.state for f in board.get_diagonal(0)], [FieldState.X] * 3)

    def test_get_diagonal_anti(self):
        board = Board()
        for i in range(3):
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


if __name__ == "__main__":
    unittest.main()
