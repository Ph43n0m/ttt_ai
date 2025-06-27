import sys
import threading
import time
from datetime import datetime
from pathlib import Path

from pynput import keyboard

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from ttt_ai.tools.window_screenshotter import WindowScreenshotter


class GameScreenLogger:
    def __init__(self, window_title: str):
        self.thread = None
        self.listener = None
        self.window_title = window_title
        self.screenshotter = WindowScreenshotter(self.window_title)
        self.stop_flag = False
        project_root = Path(__file__).parent.parent.parent
        self.screens_dir = project_root / "screens"
        self.screens_dir.mkdir(parents=True, exist_ok=True)

    def start(self):
        """Start the hotkey listener and the screenshot loop."""
        # Register global hotkey for Ctrl+Q
        self.listener = keyboard.GlobalHotKeys({"<ctrl>+q": self._on_hotkey})
        self.listener.start()

        # Start the main loop in a separate thread
        self.thread = threading.Thread(target=self._loop)
        self.thread.daemon = True
        self.thread.start()

    def _on_hotkey(self):
        """Callback when Ctrl+Q is pressed."""
        print("Ctrl+Q detected. Stopping loop.")
        self.stop_flag = True

    def stop(self):
        """Stop the loop and the hotkey listener."""
        self.stop_flag = True
        self.listener.stop()
        if self.thread.is_alive():
            self.thread.join()

    def _loop(self):
        """Main loop: take a screenshot every 300ms until stopped."""
        print("Starting GameScreenLogger. Press Ctrl+C to stop.")
        while not self.stop_flag:
            if self.screenshotter.find_window():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = str(
                    self.screens_dir
                    / f"{self.window_title}_{timestamp}.png".replace(" ", "_").replace(
                        ":", "_"
                    )
                )
                self.screenshotter.take_screenshot(filename)
            time.sleep(0.3)
        print("GameScreenLogger stopped.")


# Usage example:
if __name__ == "__main__":
    window_title = "Fluent Tic-Tac-Toe"
    logger = GameScreenLogger(window_title)
    logger.start()
    try:
        while not logger.stop_flag:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Interrupted by user. Exiting...")
        logger.stop()
