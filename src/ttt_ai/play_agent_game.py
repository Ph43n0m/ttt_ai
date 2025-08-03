from pathlib import Path

from ttt_ai.game.agent.minimax_agent import MiniMaxAgent
from ttt_ai.game.agent.model.NNModel_V1 import NNModel_V1
from ttt_ai.game.agent.model.NNModel_V2 import NNModel_V2
from ttt_ai.game.agent.nn_agent import NNAgent
from ttt_ai.game.board import Board
from ttt_ai.game.field import FieldState
from ttt_ai.tools.plotter import plot


class PlayAgentGame:
    def __init__(self, agents, maximum_games: int = 10):
        project_root = Path(__file__).parent.parent.parent
        resources_models_dir = project_root / "assets" / "resources" / "models"
        resources_models_dir.mkdir(parents=True, exist_ok=True)
        self.resource_model_file_v1 = resources_models_dir / "nn_agent_v1_weights.pt"
        self.resource_model_file_v2 = resources_models_dir / "nn_agent_v2_weights.pt"
        self.maximum_games = maximum_games
        self.agents = agents
        self.board = Board()

        for agent in self.agents:
            if isinstance(agent, NNAgent):
                if isinstance(agent.model, NNModel_V1):
                    if not self.resource_model_file_v1.exists():
                        agent.save_weights(str(self.resource_model_file_v1))
                    agent.load_weights(str(self.resource_model_file_v1))
                elif isinstance(agent.model, NNModel_V2):
                    if not self.resource_model_file_v2.exists():
                        agent.save_weights(str(self.resource_model_file_v2))
                    agent.load_weights(str(self.resource_model_file_v2))

    def start(self):
        plot_x_scores = []
        plot_o_scores = []

        n_turn = 0
        """Run the game loop for the specified number of games."""
        for game_number in range(self.maximum_games):
            self.board.reset()
            current_agent = None
            print(f"Starting game {game_number + 1} of {self.maximum_games}.")
            # self.board.print_board()

            while not self.board.is_game_over():
                current_agent = self.agents[n_turn % len(self.agents)]
                current_agent.perform_action(self.board)

                """best_move = current_agent.get_best_move(self.board)
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
                """
                n_turn += 1

            print(f"Game {game_number + 1}/{self.maximum_games} completed.")
            print(
                f"Winner is {FieldState.X if self.board.is_winner(FieldState.X) else FieldState.O if self.board.is_winner(FieldState.X) else 'None'}. "
            )
            self.board.print_board()

            for agent in self.agents:
                agent.update_stats(self.board)
                print(
                    f"Game stats: {agent.FIELD_STATE_TYPE} won: {agent.games_won}, lost: {agent.games_lost}, draw: {agent.games_draw}, reward: {agent.total_reward:.2f}, wl_ratio: {agent.get_wl_ratio():.2f}, win_rate: {agent.get_win_rate():.2f}, bm: {agent.n_best_move}, im: {agent.n_invalid_move}, bm/im: {(agent.n_best_move / agent.n_invalid_move) if agent.n_invalid_move > 0 else 1:.0%}"
                )

                if isinstance(agent, NNAgent):
                    if agent.total_reward > 0 and agent.total_reward > agent.record:
                        if isinstance(agent.model, NNModel_V1):
                            agent.save_weights(str(self.resource_model_file_v1))
                        elif isinstance(agent.model, NNModel_V2):
                            agent.save_weights(str(self.resource_model_file_v2))

            plot_x_scores.append(self.agents[0].total_reward)
            plot_o_scores.append(self.agents[1].total_reward)

            if game_number % 10 == 0:
                plot(plot_x_scores, plot_o_scores)

            """ weights seems always the same, so no need to save them every time
            if isinstance(current_agent, NNAgent_V1):
                current_agent.save_weights(str(self.resource_model_file_v1))
            elif isinstance(current_agent, NNAgent_V2):
                current_agent.save_weights(str(self.resource_model_file_v2))"""


def main():
    """Main entry point for the application."""
    randomness = 0  # Set the randomness for the agents

    # agent_x = MiniMaxAgent(FieldState.X, randomness)
    agent_x = NNAgent(NNModel_V1(), FieldState.X, randomness)
    # agent_x = NNAgent(NNModel_V2(), FieldState.X, randomness)

    # agent_o = MiniMaxAgent(FieldState.O, randomness)
    # agent_o = NNAgent(NNModel_V1(), FieldState.O, randomness)
    agent_o = NNAgent(NNModel_V2(), FieldState.O, randomness)

    play_loop = PlayAgentGame([agent_x, agent_o], 1000000)
    play_loop.start()


if __name__ == "__main__":
    main()
