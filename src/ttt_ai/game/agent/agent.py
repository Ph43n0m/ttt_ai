from abc import ABC
from collections import deque

from ttt_ai.game.field import FieldState

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent(ABC):
    def __init__(
            self, field_state_type: FieldState = FieldState.X, randomness: float = 0.2
    ):
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

    def update(
            self,
            game_won: bool = False,
            game_lost: bool = False,
            game_draw: bool = False,
    ) -> None:
        if game_draw:
            self.reward += 1
            self.games_draw += 1
            return
        if game_won:
            self.reward += 2
            self.games_won += 1
        elif game_lost:
            self.reward -= 1
            self.games_lost += 1

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

    def get_best_move(self, board) -> int | None:
        pass
