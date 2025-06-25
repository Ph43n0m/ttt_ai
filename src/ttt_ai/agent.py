import random
from abc import ABC
from collections import deque

from ttt_ai.field import FieldState

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent(ABC):
    def __init__(self):
        self.reward = 0
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()


class MiniMaxAgent(Agent):
    """
    An agent that uses the minimax algorithm to play Tic Tac Toe.
    """

    def __init__(self):
        super().__init__()

    def get_best_move(self, board) -> int | None:
        """
        Get the best move for the current board state using the minimax algorithm.
        Args:
            board: The current state of the Tic Tac Toe board.
        Returns:
            The best move for the current player.
        """
        # Implement the minimax algorithm to find the best move

        if (
                board.is_board_full()
                or board.is_winner(FieldState.X)
                or board.is_winner(FieldState.O)
        ):
            return None

        if board.is_empty():
            return random.choice([0, 2, 6, 8])  # pick a random corner as the first move

        best_score = float("-inf")
        best_move = None
        for row in range(board.BOARD_SIZE):
            for col in range(board.BOARD_SIZE):
                if board[row, col].state == FieldState.EMPTY:
                    # Make the move
                    board[row, col].state = FieldState.X
                    score = self._minimax(board, 0, False)
                    # Undo the move
                    board[row, col].state = FieldState.EMPTY

                    if score > best_score:
                        best_score = score
                        best_move = board.get_flat_index(row, col)

        return best_move

    def _minimax(self, board, depth, is_maximizing):
        """
        The minimax algorithm to evaluate the best move.
        Args:
            board: The current state of the Tic Tac Toe board.
            depth: The current depth in the game tree.
            is_maximizing: Boolean indicating if the current player is maximizing or minimizing.
        Returns:
            The score of the board state.
        """
        # Base case: check for terminal states (win/loss/draw)
        if board.is_winner(FieldState.X):
            return float("inf")
        elif board.is_winner(FieldState.O):
            return float("-inf")
        elif board.is_board_full():
            return 0

        # Recursive case: explore all possible moves
        if is_maximizing:
            best_score = -1000
            for row in range(board.BOARD_SIZE):
                for col in range(board.BOARD_SIZE):
                    if board[row, col].state == FieldState.EMPTY:
                        board[row, col].state = FieldState.X
                        score = self._minimax(board, depth + 1, False)
                        board[row, col].state = FieldState.EMPTY
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = 1000
            for row in range(board.BOARD_SIZE):
                for col in range(board.BOARD_SIZE):
                    if board[row, col].state == FieldState.EMPTY:
                        board[row, col].state = FieldState.O
                        score = self._minimax(board, depth + 1, True)
                        board[row, col].state = FieldState.EMPTY
                        best_score = min(score, best_score)
            return best_score
