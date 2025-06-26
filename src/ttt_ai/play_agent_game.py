from ttt_ai.agent import MiniMaxAgent
from ttt_ai.board import Board
from ttt_ai.field import FieldState


class PlayAgentGame:
    def __init__(self, agents, maximum_games: int = 10):
        self.maximum_games = maximum_games
        self.agents = agents
        self.board = Board()

    def start(self):
        n_turn = 0
        """Run the game loop for the specified number of games."""
        for game_number in range(self.maximum_games):
            self.board.reset()

            print(f"Starting game {game_number + 1} of {self.maximum_games}.")
            # self.board.print_board()

            while not self.board.is_board_full() and not self.board.is_winner(
                    FieldState.X) and not self.board.is_winner(FieldState.O):
                current_agent = self.agents[n_turn % len(self.agents)]
                best_move = current_agent.get_best_move(self.board)
                # print(f"Turn {n_turn + 1} with agent {current_agent.FIELD_STATE_TYPE}.")

                if best_move is not None:
                    field = self.board.get_field_by_flat_index(best_move)
                    if field is not None:
                        field.state = current_agent.FIELD_STATE_TYPE

                        print(f"Agent {current_agent.FIELD_STATE_TYPE} played at {best_move}.")
                    else:
                        print(f"Invalid move by agent {current_agent.FIELD_STATE_TYPE}.")
                        break

                n_turn += 1

            print(f"Game {game_number + 1} completed.")
            print(f"Winner is {FieldState.X if self.board.is_winner(FieldState.X) else FieldState.O}. ")
            self.board.print_board()


def main():
    """Main entry point for the application."""
    agent_x = MiniMaxAgent(FieldState.X, 0.3)
    agent_o = MiniMaxAgent(FieldState.O, 0.3)

    play_loop = PlayAgentGame([agent_x, agent_o], 100)
    play_loop.start()


if __name__ == "__main__":
    main()
