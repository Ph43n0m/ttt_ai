from dataclasses import dataclass

from ttt_ai.field import Field


@dataclass
class Board:
    def __init__(self):
        # Assuming a 3x3 board with empty fields initialized
        self.fields = [[Field() for _ in range(3)] for _ in range(3)]

    def __setitem__(self, key, value):
        row, col = key
        self.fields[row][col] = value

    def __getitem__(self, key):
        row, col = key
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
        if not (0 <= col < 3):
            raise ValueError("Column index must be between 0 and 2.")
        return [self.fields[row][col] for row in range(3)]

    def get_diagonal(self, diagonal: int):
        """
        Get a specific diagonal from the board.
        Args:
            diagonal (int): The diagonal index (0 for main diagonal, 1 for anti-diagonal).
        Returns:
            list[Field]: The specified diagonal of fields.
        """
        if diagonal == 0:
            return [self.fields[i][i] for i in range(3)]
        elif diagonal == 1:
            return [self.fields[i][2 - i] for i in range(3)]
        else:
            raise ValueError(
                "Diagonal index must be 0 (main diagonal) or 1 (anti-diagonal)."
            )

    def print_board(self):
        """
        Print the board in a readable format.
        """
        print("-" * 9)
        for row in self.fields:
            print(" | ".join(field.state.value for field in row))
            print("-" * 9)
