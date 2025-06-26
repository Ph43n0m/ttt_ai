import sys
import threading
from pathlib import Path
from time import sleep

from pynput import keyboard

from ttt_ai.agent import Agent, MiniMaxAgent

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from game_info import GameInfo
import matplotlib.pyplot as plt
import numpy as np


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
                    self.agent.update(True)

                if self.game_info.is_lose_shown():
                    print("You lost.")
                    self.agent.update(False, True)

                if self.game_info.is_draw_shown():
                    print("Draw.")
                    self.agent.update(False, False, True)

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
            print("Win/Loss ratio: {:.2f}".format(self.agent.get_wl_ratio()))
            print("Win rate: {:.2f}".format(self.agent.get_win_rate()))
            print("Agent Reward: ", self.agent.reward)


def main():
    """Main entry point for the application."""
    play_loop = PlayRealGame(MiniMaxAgent(), 100)
    play_loop.start()
    # play_loop.stop()
    try:
        while not play_loop.stop_event.is_set():
            sleep(play_loop.check_speed)

    except KeyboardInterrupt:
        print("Interrupted by user. Exiting...")
        play_loop.stop()

    filenametosaveplot = str(
        play_loop.game_info.screenshotter.screens_dir
        / f"{play_loop.game_info.screenshotter.window_title}_result.png".replace(
            " ", "_"
        ).replace(":", "_")
    )
    # X axis parameter:
    # xaxis = np.array([1, 2, 4, 16, 32])
    # Y axis parameter:
    # yaxis = np.array([1, 2, 3, 4, 5])
    # plt.plot(xaxis, yaxis)
    # plt.show()

    t = np.array(
        [
            [0, 0, 0, 0],
            [1, 1, 0, 0],
            [2, 2, 0, 0],
            [3, 2, 1, 0],
            [4, 2, 1, 1],
            [5, 2, 2, 1],
            [6, 2, 2, 2],
            [7, 2, 3, 2],
            [8, 3, 3, 2],
            [9, 3, 4, 2],
            [10, 3, 4, 2],
        ]
    )

    plt.style.use("dark_background")
    plt.plot(t[:, 0], t[:, 1], ls="dashed", color="chartreuse", label="Games won")
    plt.plot(t[:, 0], t[:, 2], ls="dashed", color="OrangeRed", label="Games lost")
    plt.plot(t[:, 0], t[:, 3], ls="dotted", color="silver", label="Games draw")

    plt.legend()
    # plt.show()
    # plt.savefig(filenametosaveplot)


if __name__ == "__main__":
    main()
