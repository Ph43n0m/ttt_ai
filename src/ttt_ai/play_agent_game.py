from pathlib import Path

from ttt_ai.game.agent.minimax_agent import MiniMaxAgent
from ttt_ai.game.agent.nn_agent import NNAgent
from ttt_ai.game.board import Board
from ttt_ai.game.field import FieldState


class PlayAgentGame:
    def __init__(self, agents, maximum_games: int = 10):
        project_root = Path(__file__).parent.parent.parent
        resources_models_dir = project_root / "assets" / "resources" / "models"
        resources_models_dir.mkdir(parents=True, exist_ok=True)
        self.resource_model_file = resources_models_dir / "nn_agent_weights.pth"
        self.maximum_games = maximum_games
        self.agents = agents
        self.board = Board()

        for agent in self.agents:
            if isinstance(agent, NNAgent):
                if not self.resource_model_file.exists():
                    agent.save_weights(str(self.resource_model_file))
                agent.load_weights(str(self.resource_model_file))

    def start(self):

        n_turn = 0
        """Run the game loop for the specified number of games."""
        for game_number in range(self.maximum_games):
            self.board.reset()
            current_agent = None
            print(f"Starting game {game_number + 1} of {self.maximum_games}.")
            # self.board.print_board()

            while (
                    not self.board.is_board_full()
                    and not self.board.is_winner(FieldState.X)
                    and not self.board.is_winner(FieldState.O)
            ):
                current_agent = self.agents[n_turn % len(self.agents)]
                best_move = current_agent.get_best_move(self.board)
                # print(f"Turn {n_turn + 1} with agent {current_agent.FIELD_STATE_TYPE}.")

                if best_move is not None:
                    field = self.board.get_field_by_flat_index(best_move)
                    if field is not None:
                        field.state = current_agent.FIELD_STATE_TYPE

                        # print(f"Agent {current_agent.FIELD_STATE_TYPE} played at {best_move}."  )
                    else:
                        print(
                            f"Invalid move by agent {current_agent.FIELD_STATE_TYPE}."
                        )
                        break

                n_turn += 1

            print(f"Game {game_number + 1}/{self.maximum_games} completed.")
            print(
                f"Winner is {FieldState.X if self.board.is_winner(FieldState.X) else FieldState.O}. "
            )
            self.board.print_board()

            for agent in self.agents:
                agent.update(game_won=self.board.is_winner(agent.FIELD_STATE_TYPE),
                             game_lost=not self.board.is_winner(agent.FIELD_STATE_TYPE), game_draw=(
                            not self.board.is_winner(FieldState.X) and not self.board.is_winner(FieldState.O)))
                print(
                    f"Game stats: {agent.FIELD_STATE_TYPE} won: {agent.games_won}, lost: {agent.games_lost}, draw: {agent.games_draw}, reward: {agent.reward}, wl_ratio: {agent.get_wl_ratio():.2f}, win_rate: {agent.get_win_rate():.2f}")

            if isinstance(current_agent, NNAgent):
                current_agent.save_weights(str(self.resource_model_file))


def main():
    """Main entry point for the application."""
    agent_x = MiniMaxAgent(FieldState.X, 0.3)
    agent_o = NNAgent(FieldState.O, 0)

    play_loop = PlayAgentGame([agent_x, agent_o], 1000)
    play_loop.start()


if __name__ == "__main__":
    main()
