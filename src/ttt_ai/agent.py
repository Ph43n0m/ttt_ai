import random
from abc import ABC
from collections import deque

from ttt_ai.field import FieldState

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent(ABC):
    def __init__(self, field_state_type: FieldState = FieldState.X, randomness: float = 0.2):
        self.FIELD_STATE_TYPE = field_state_type
        self.games_won = 0
        self.games_lost = 0
        self.games_draw = 0
        self.reward = 0
        self.epsilon = randomness  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()

    def get_game_count(self) -> int:
        """Get the number of games played."""
        return self.games_won + self.games_lost + self.games_draw

    def update(self, game_won: bool = False, game_lost: bool = False, game_draw: bool = False, ) -> None:
        if game_won:
            self.reward += 2
            self.games_won += 1
        elif game_lost:
            self.reward -= 1
            self.games_lost += 1
        elif game_draw:
            self.reward += 1
            self.games_draw += 1

    def get_wl_ratio(self) -> float:
        """Calculate the win/loss ration."""
        if self.games_won < 0 or self.games_lost < 0:
            print("Invalid game count or games lost. Returning 0.0 for win/loss ratio.")
            return float(0)

        return (
            self.games_won / self.games_lost
            if self.games_lost > 0
            else float(self.games_won)
        )

    def get_win_rate(self) -> float:
        """Calculate the win rate."""

        if self.games_won < 0 or self.get_game_count() < 0:
            print("Invalid game count or games won. Returning 0.0 for win rate.")
            return float(0)

        return self.games_won / self.get_game_count() if self.get_game_count() > 0 else float(0)

    def get_best_move(self, board) -> int | None:
        pass


class MiniMaxAgent(Agent):
    """
    An agent that uses the minimax algorithm to play Tic Tac Toe.
    """

    def __init__(self, field_state_type: FieldState = FieldState.X, randomness: float = 0.2):
        super().__init__(field_state_type, randomness)

    def get_best_move(self, board) -> int | None:
        """
        Get the best move for the current board state using the minimax algorithm.
        Args:
            board: The current state of the Tic Tac Toe board.
        Returns:
            The best move for the current player.
            :param board:
        """
        # Implement the minimax algorithm to find the best move

        if (
                board.is_board_full()
                or board.is_winner(FieldState.X)
                or board.is_winner(FieldState.O)
        ):
            return None

        if random.uniform(0, 1) < self.epsilon:
            return board.get_flat_index_of_radom_free_field()  # Random move if randomness condition is met
        else:
            # If randomness condition is not met, use minimax algorithm

            if board.is_empty():
                return random.choice([0, 2, 6, 8])  # pick a random corner as the first move

            best_score = float("-inf")
            best_move = None
            for row in range(board.BOARD_SIZE):
                for col in range(board.BOARD_SIZE):
                    if board[row, col].state == FieldState.EMPTY:
                        # Make the move
                        board[row, col].state = self.FIELD_STATE_TYPE
                        score = self._minimax(board, 0, False if self.FIELD_STATE_TYPE == FieldState.X else True)
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
        if board.is_board_full():
            return 0
        elif board.is_winner(self.FIELD_STATE_TYPE):
            return float("inf")
        elif board.is_winner(FieldState.O if not self.FIELD_STATE_TYPE == FieldState.X else FieldState.X):
            return float("-inf")

        if depth >= 7:  # Limit the depth to prevent excessive recursion
            print(f"Critical depth of {depth} reached, returning 0")
            return 0

        # Recursive case: explore all possible moves
        if is_maximizing:
            best_score = -1000
            for row in range(board.BOARD_SIZE):
                for col in range(board.BOARD_SIZE):
                    if board[row, col].state == FieldState.EMPTY:
                        board[row, col].state = self.FIELD_STATE_TYPE
                        score = self._minimax(board, depth + 1, False)
                        board[row, col].state = FieldState.EMPTY
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = 1000
            for row in range(board.BOARD_SIZE):
                for col in range(board.BOARD_SIZE):
                    if board[row, col].state == FieldState.EMPTY:
                        board[
                            row, col].state = FieldState.O if not self.FIELD_STATE_TYPE == FieldState.X else FieldState.X
                        score = self._minimax(board, depth + 1, True)
                        board[row, col].state = FieldState.EMPTY
                        best_score = min(score, best_score)
            return best_score
