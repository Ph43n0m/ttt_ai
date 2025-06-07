import sys
import threading
from pathlib import Path
from time import sleep

from pynput import keyboard

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from game_info import GameInfo


class Play:
    def __init__(self, maximum_games: int = 10):
        self.thread = None
        self.listener = None
        self.check_speed = 0.2
        self.game_info = GameInfo(0.1)
        self.stop_event = threading.Event()
        self.game_count = 0
        self.maximum_games = maximum_games

    def start(self):
        """Start the hotkey listener and the screenshot loop."""
        # Register global hotkey for Ctrl+X
        self.listener = keyboard.GlobalHotKeys({"<ctrl>+x": self._on_hotkey})
        self.listener.start()

        # Start the main loop in a separate thread
        self.thread = threading.Thread(target=self._loop)
        self.thread.daemon = True
        self.thread.start()

    def _on_hotkey(self):
        """Callback when Ctrl+X is pressed."""
        print("Ctrl+X detected. Stopping loop.")
        self.stop_event.set()

    def stop(self):
        """Stop the loop and the hotkey listener."""
        self.stop_event.set()
        if self.listener is not None:
            self.listener.stop()
        if self.thread is not None and self.thread.is_alive():
            self.thread.join()

    def _loop(self):
        print("Starting Game. Press Ctrl+X to stop.")
        try:
            while not self.stop_event.is_set():

                if self.game_info.start_next_game():
                    self.game_count += 1
                    if self.game_count > self.maximum_games:
                        self.stop_event.set()  # Stop the loop if maximum games reached.
                        break

                    print(
                        f"Game {self.game_count} of {self.maximum_games} has been started."
                    )

                if self.game_info.is_click_square_shown():
                    print("Click any square to start the next round.")

                if self.game_info.is_your_turn_shown():
                    print("Your turn.")

                if self.game_info.is_win_shown():
                    print("You won!")

                if self.game_info.is_lose_shown():
                    print("You lost.")

                if self.game_info.is_draw_shown():
                    print("Draw.")

                sleep(self.check_speed)

        except Exception as e:
            print(f"Unexpected error in loop: {e}")
        finally:
            print("Game stopped.")
            self.game_info.is_go_back_clicked()


def main():
    """Main entry point for the application."""
    play_loop = Play(2)
    play_loop.start()
    try:
        while not play_loop.stop_event.is_set():
            sleep(0.5)
    except KeyboardInterrupt:
        print("Interrupted by user. Exiting...")
        play_loop.stop()


if __name__ == "__main__":
    main()
