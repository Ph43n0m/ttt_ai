import random
from dataclasses import dataclass
from typing import Any

from ttt_ai.field import Field, FieldState


@dataclass
class Board:
    def __init__(self):
        # Assuming a 3x3 board with empty fields initialized
        self.BOARD_SIZE = 3
        self.fields = [
            [Field() for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)
        ]

    def __setitem__(self, key, value):
        row, col = key
        self.fields[row][col] = value

    def __getitem__(self, key):
        row, col = key
        return self.fields[row][col]

    def reset(self):
        """
        Reset the board to its initial state with all fields empty.
        """
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                self.fields[row][col].state = FieldState.EMPTY

    def get_flat_index_of_radom_free_field(self) -> int | None:
        """
        Get the index of a random free field in the flattened board.
        Returns:
            int: The index of a random free field, or None if no free fields are available.
        """
        free_fields = [
            self.get_flat_index(row, col)
            for row in range(self.BOARD_SIZE)
            for col in range(self.BOARD_SIZE)
            if self.fields[row][col].state == FieldState.EMPTY
        ]
        if not free_fields:
            return None
        return random.choice(free_fields)

    def get_flat_index(self, row: int, col: int) -> int:
        """
        Get the index of a field if the board is flattened into a 1D array.
        Args:
            row (int): The row index (0, 1, or 2).
            col (int): The column index (0, 1, or 2).
        Returns:
            int: The index in the flattened array.
        """
        if not (0 <= row < self.BOARD_SIZE) or not (0 <= col < self.BOARD_SIZE):
            raise ValueError("Row and column indices must be between 0 and 2.")
        return row * self.BOARD_SIZE + col

    def get_field_by_flat_index(self, index: int) -> Field:
        """
        Get the field from the board using a flattened index (0-8).
        Args:
            index (int): The index in the flattened array.
        Returns:
            Field: The field at the specified index.
        """
        if not (0 <= index < self.BOARD_SIZE * self.BOARD_SIZE):
            raise ValueError("Index must be between 0 and 8.")
        row = index // self.BOARD_SIZE
        col = index % self.BOARD_SIZE
        return self.fields[row][col]

    def get_row(self, row: int):
        """
        Get a specific row from the board.
        Args:
            row (int): The row index (0, 1, or 2).
        Returns:
            list[Field]: The specified row of fields.
        """
        if not (0 <= row < 3):
            raise ValueError("Row index must be between 0 and 2.")
        return self.fields[row]

    def get_column(self, col: int):
        """
        Get a specific column from the board.
        Args:
            col (int): The column index (0, 1, or 2).
        Returns:
            list[Field]: The specified column of fields.
        """
        if not (0 <= col < self.BOARD_SIZE):
            raise ValueError("Column index must be between 0 and 2.")
        return [self.fields[row][col] for row in range(self.BOARD_SIZE)]

    def get_diagonal(self, diagonal: int):
        """
        Get a specific diagonal from the board.
        Args:
            diagonal (int): The diagonal index (0 for main diagonal, 1 for anti-diagonal).
        Returns:
            list[Field]: The specified diagonal of fields.
        """
        if diagonal == 0:
            return [self.fields[i][i] for i in range(self.BOARD_SIZE)]
        elif diagonal == 1:
            return [self.fields[i][2 - i] for i in range(self.BOARD_SIZE)]
        else:
            raise ValueError(
                "Diagonal index must be 0 (main diagonal) or 1 (anti-diagonal)."
            )

    def is_empty(self) -> bool:
        """
        Check if the board is empty (all fields are EMPTY).
        Returns:
            bool: True if the board is empty, False otherwise.
        """
        return all(
            field.state == FieldState.EMPTY for row in self.fields for field in row
        )

    def is_board_full(self) -> bool:
        """
        Check if the board is full (no empty fields).
        Returns:
            bool: True if the board is full, False otherwise.
        """
        return all(
            field.state != FieldState.EMPTY for row in self.fields for field in row
        )

    def is_winner(self, player: FieldState) -> bool:
        """
        Check if the specified player has won.
        Args:
            player (FieldState): The player to check for a win (X or O).
        Returns:
            bool: True if the player has won, False otherwise.
        """
        if not isinstance(player, FieldState):
            raise TypeError("player must be an instance of FieldState.")
        # Check rows, columns, and diagonals
        for i in range(self.BOARD_SIZE):
            row = self.get_row(i)
            col = self.get_column(i)
            for field in row + col:
                if not isinstance(field.state, FieldState):
                    raise TypeError("All field states must be instances of FieldState.")
            if all(field.state == player for field in row):
                return True
            if all(field.state == player for field in col):
                return True
        diag_main = self.get_diagonal(0)
        diag_anti = self.get_diagonal(1)
        for field in diag_main + diag_anti:
            if not isinstance(field.state, FieldState):
                raise TypeError("All field states must be instances of FieldState.")
        if all(field.state == player for field in diag_main):
            return True
        if all(field.state == player for field in diag_anti):
            return True
        return False

    def print_board(self):
        """
        Print the board in a readable format.
        """
        print("-" * 9)
        for row in self.fields:
            print(" | ".join(field.state.value for field in row))
            print("-" * 9)
