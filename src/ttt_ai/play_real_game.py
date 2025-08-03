import sys
import threading
from pathlib import Path
from time import sleep

from pynput import keyboard

from ttt_ai.game.agent.agent import Agent
from ttt_ai.game.agent.model.NNModel_V1 import NNModel_V1
from ttt_ai.game.agent.model.NNModel_V2 import NNModel_V2
from ttt_ai.game.agent.nn_agent import NNAgent
from ttt_ai.game.field import FieldState

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from ttt_ai.game.game_info import GameInfo


class PlayRealGame:
    def __init__(self, agent: Agent, maximum_games: int = 10):
        self.thread = None
        self.listener = None
        self.check_speed = 0.1
        self.game_info = GameInfo(0.2)
        self.agent = agent
        self.stop_event = threading.Event()
        self.game_count = 0
        self.maximum_games = maximum_games
        project_root = Path(__file__).parent.parent.parent
        resources_models_dir = project_root / "assets" / "resources" / "models"
        self.resource_model_file_v1 = resources_models_dir / "nn_agent_v1_weights.pt"
        self.resource_model_file_v2 = resources_models_dir / "nn_agent_v2_weights.pt"

        if isinstance(agent, NNAgent):
            if isinstance(agent.model, NNModel_V1):
                if not self.resource_model_file_v1.exists():
                    agent.save_weights(str(self.resource_model_file_v1))
                agent.load_weights(str(self.resource_model_file_v1), False)
            elif isinstance(agent.model, NNModel_V2):
                if not self.resource_model_file_v2.exists():
                    agent.save_weights(str(self.resource_model_file_v2))
                agent.load_weights(str(self.resource_model_file_v2), False)

    def start(self):
        """Start the hotkey listener and the screenshot loop."""
        # Register global hotkey for Ctrl+Q
        self.listener = keyboard.GlobalHotKeys({"<ctrl>+q": self._on_hotkey})
        self.listener.start()

        # Start the main loop in a separate thread
        if self.game_info.screenshotter.find_window() is True:
            self.game_info.is_go_back_clicked()
            self.game_info.move_mouse_to_save_location()
            self.thread = threading.Thread(target=self._loop)
            self.thread.daemon = True
            self.thread.start()
        else:
            print("Window not found. Please ensure the game window is open.")
            self.stop()

    def _on_hotkey(self):
        """Callback when Ctrl+Q is pressed."""
        print("Ctrl+Q detected. Stopping loop.")
        self.stop()

    def stop(self):
        """Stop the loop and the hotkey listener."""
        self.stop_event.set()
        if self.listener is not None:
            self.listener.stop()
        if self.thread is not None and self.thread.is_alive():
            self.thread.join()

    def _loop(self):
        print("Starting Game. Press Ctrl+Q to stop.")

        try:
            while not self.stop_event.is_set():

                if self.game_info.is_click_square_shown():
                    print("Click any square to start the next round.")
                    self.game_info.move_mouse_to_save_location()

                if self.game_info.is_win_shown():
                    print("You won!")
                    self.agent.update_stats(self.game_info.board)

                if self.game_info.is_lose_shown():
                    print("You lost.")
                    self.agent.update_stats(self.game_info.board)

                if self.game_info.is_draw_shown():
                    print("Draw.")
                    self.agent.update_stats(self.game_info.board)

                if self.game_info.start_next_game():
                    if self.game_count >= self.maximum_games:
                        self.stop_event.set()  # Stop the loop if maximum games reached.
                        sleep(self.check_speed)
                        # self.game_count = self.maximum_games
                        continue

                    self.game_count += 1
                    print(
                        f"Game {self.game_count} of {self.maximum_games} has been started."
                    )

                if self.game_info.is_your_turn_shown():
                    print(f"Your turn. Game {self.game_count} of {self.maximum_games}")

                    print("Printing board state before click.")
                    self.game_info.board.print_board()

                    # Get the best move from the minimax agent
                    best_move = self.agent.get_best_move(self.game_info.board)
                    if best_move is not None:
                        field_to_click = self.game_info.board.get_field_by_flat_index(
                            best_move
                        )
                        if field_to_click is not None:
                            if self.game_info.click_at_field(field_to_click):
                                self.game_info.move_mouse_to_save_location()
                                self.game_info.update_board_information()
                                print("Printing board state after click.")
                                self.game_info.board.print_board()

                self._print_game_stats()

                sleep(self.check_speed)

        except Exception as e:
            print(f"Unexpected error in loop: {e}")
        finally:
            print("Game stopped.")
            self._print_game_stats()
            self.game_info.board.print_board()
            self.game_info.is_go_back_clicked()

    def _print_game_stats(self):
        """Print the game statistics."""
        print("Game statistics:")
        print(
            f"Game ({self.game_info.get_previous_game_state()} --> {self.game_info.actual_game_state}) - ({self.game_count}/{self.maximum_games})\nW: {self.agent.games_won} | L: {self.agent.games_lost} | D: {self.agent.games_draw}"
        )
        if self.game_count > 0:
            print(
                f"Game stats: {self.agent.FIELD_STATE_TYPE} won: {self.agent.games_won}, lost: {self.agent.games_lost}, draw: {self.agent.games_draw}, reward: {self.agent.total_reward}, wl_ratio: {self.agent.get_wl_ratio():.2f}, win_rate: {self.agent.get_win_rate():.2f}, bm: {self.agent.n_best_move}, im: {self.agent.n_invalid_move}, bm/im: {(self.agent.n_best_move / self.agent.n_invalid_move) if self.agent.n_invalid_move > 0 else 0:.0%}"
            )


def main():
    """Main entry point for the application."""

    # play_loop = PlayRealGame(MiniMaxAgent(FieldState.X, 0), 100)
    play_loop = PlayRealGame(NNAgent(NNModel_V2(), FieldState.X, 0), 100)
    play_loop.start()
    # play_loop.stop()
    try:
        while not play_loop.stop_event.is_set():
            sleep(play_loop.check_speed)

    except KeyboardInterrupt:
        print("Interrupted by user. Exiting...")
        play_loop.stop()


if __name__ == "__main__":
    main()
