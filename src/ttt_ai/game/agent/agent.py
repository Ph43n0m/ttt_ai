from abc import ABC

from ttt_ai.game.field import FieldState


class Agent(ABC):
    def __init__(
        self, field_state_type: FieldState = FieldState.X, randomness: float = 0.1
    ):
        self.FIELD_STATE_TYPE = field_state_type
        self.games_won = 0
        self.games_lost = 0
        self.games_draw = 0
        self.total_reward = 0
        self.epsilon = randomness  # randomness
        self.record = 0
        self.n_best_move = 0
        self.n_invalid_move = 0

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

        return (
            self.games_won / self.get_game_count()
            if self.get_game_count() > 0
            else float(0)
        )

    def get_game_count(self) -> int:
        """Get the number of games played."""
        return self.games_won + self.games_lost + self.games_draw

    def update_stats(self, board) -> None:
        if board.is_game_over():
            if not board.is_winner(FieldState.X) and not board.is_winner(FieldState.O):
                self.games_draw += 1
            elif board.is_winner(self.FIELD_STATE_TYPE):
                self.games_won += 1
            elif not board.is_winner(self.FIELD_STATE_TYPE):
                self.games_lost += 1

            self.total_reward += self._calculate_reward(board)

    # Decrease epsilon over time to reduce exploration
    def _get_epsilon_by_game_count(self) -> float:
        value = (min(0.1, self.epsilon) ** 0.01) * (0.99 ** (self.get_game_count() + 1))
        return value if value > 0.0001 else 0

    def _calculate_reward(self, board) -> float:
        """Calculate the reward based on the board."""
        ret = 0
        if board.is_game_over():
            if not board.is_winner(FieldState.X) and not board.is_winner(FieldState.O):
                ret += 1
            elif board.is_winner(self.FIELD_STATE_TYPE):
                ret += 2
            elif not board.is_winner(self.FIELD_STATE_TYPE):
                ret -= 1
        return ret

    def perform_action(self, board) -> int:
        """Perform an action on the board and return the chosen field index."""
        ret = -1

        best_move = self.get_best_move(board)
        if best_move is not None:
            field = board.get_field_by_flat_index(best_move)
            if field is not None:
                ret = best_move
                field.state = self.FIELD_STATE_TYPE
            else:
                print(f"Invalid move by agent {self.FIELD_STATE_TYPE}.")
        else:
            print(f"No valid move found for agent {self.FIELD_STATE_TYPE}.")

        return ret

    def get_best_move(self, board) -> int | None:
        pass
