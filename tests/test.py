import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ttt_ai.window_screenshotter import WindowScreenshotter


class Test:
    def __init__(self):
        self.window_title = "Fluent Tic-Tac-Toe"
        cwd = Path.cwd()
        self.indicate_play_file_path = str(cwd / "resources" / "indicate_StartPlay.png")
        print(self.indicate_play_file_path)

    def start(self):
        print(self.window_title)
        screenshotter = WindowScreenshotter(self.window_title)

        location = screenshotter.get_image_in_screen_location(
            self.indicate_play_file_path
        )
        print(location)

        # if screenshotter.find_window():

        # screenshotter.activate_window()

        # try:
        # location = pyautogui.locateCenterOnScreen(self.indicate_play_file_path, confidence=0.99, region=screenshotter.window_region)
        # print(location)
        # except:
        # print("Indicator not found")

        # pyautogui.moveTo(location)

        return


# Usage example:
if __name__ == "__main__":
    test = Test()
    test.start()
