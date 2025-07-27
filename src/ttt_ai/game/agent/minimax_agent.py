import random

from ttt_ai.game.agent.agent import Agent
from ttt_ai.game.field import FieldState


class MiniMaxAgent(Agent):
    """
    An agent that uses the minimax algorithm to play Tic Tac Toe.
    """

    def __init__(
            self, field_state_type: FieldState = FieldState.X, randomness: float = 0.2
    ):
        super().__init__(field_state_type, randomness)
        if self.epsilon <= 0:
            self.exploration_mode = False

    def _get_best_move(self, board) -> int | None:
        """
        Get the best move for the current board state using the minimax algorithm.
        Args:
            board: The current state of the Tic Tac Toe board.
        Returns:
            The best move for the current player.
            :param board:
        """
        # Implement the minimax algorithm to find the best move

        if board.is_game_over():
            return None

        if (
                self.exploration_mode
                and random.uniform(0, 1) < self._get_epsilon_by_game_count()
        ):
            self.n_invalid_move += 1
            return (
                board.get_flat_index_of_radom_free_field()
            )  # Random move if randomness condition is met
        else:
            # If randomness condition is not met, use minimax algorithm
            self.n_best_move += 1

            if board.is_empty():
                return random.choice(
                    [0, 2, 8]
                )  # pick a random corner as the first move except 6

            best_score = float("-inf")
            best_move = None
            for row in range(board.BOARD_SIZE):
                for col in range(board.BOARD_SIZE):
                    if board[row, col].state == FieldState.EMPTY:
                        # Make the move
                        board[row, col].state = self.FIELD_STATE_TYPE
                        score = self._minimax(
                            board,
                            0,
                            False if self.FIELD_STATE_TYPE == FieldState.X else True,
                        )
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
        elif board.is_winner(
                FieldState.O if not self.FIELD_STATE_TYPE == FieldState.X else FieldState.X
        ):
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
                        board[row, col].state = (
                            FieldState.O
                            if not self.FIELD_STATE_TYPE == FieldState.X
                            else FieldState.X
                        )
                        score = self._minimax(board, depth + 1, True)
                        board[row, col].state = FieldState.EMPTY
                        best_score = min(score, best_score)
            return best_score
