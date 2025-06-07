import time
from pathlib import Path
from typing import Optional

import pyautogui
import pygetwindow as gw
from pyautogui import Point


class WindowScreenshotter:
    """
    A utility class to capture screenshots of a specific window by title.
    Provides methods to find, activate, and capture screenshots of the window.
    """

    def __init__(self, window_title: str):
        """
        Initialize the WindowScreenshotter with the window title.
        Args:
            window_title (str): The title of the window to capture.
        """
        self.window_title: str = window_title
        self.window: Optional[gw.Window] = None
        self.window_region: Optional[tuple[int, int, int, int]] = None
        project_root = Path(__file__).parent.parent.parent
        self.screens_dir = project_root / "screens"
        self.screens_dir.mkdir(parents=True, exist_ok=True)

    def find_window(self) -> bool:
        """
        Attempt to find the window by its title.
        Returns:
            bool: True if the window is found, False otherwise.
        """
        windows = gw.getWindowsWithTitle(self.window_title)
        if windows:
            self.window = windows[0]
            self.window_region = (
                self.window.left,
                self.window.top,
                self.window.width,
                self.window.height,
            )
            return True
        return False

    def activate_window(self, sleeptime: float = 0.2) -> bool:
        """
        Restore and activate the window if needed, with a pause if restored.
        Args:
            sleeptime (float): Time to sleep after restoring a minimized window.
        Returns:
            bool: True if the window is activated, False otherwise.
        """
        if self.window:
            if self.window.isMinimized:
                self.window.restore()
                time.sleep(sleeptime)
                self.window_region = (
                    self.window.left,
                    self.window.top,
                    self.window.width,
                    self.window.height,
                )
            if not self.window.isActive:
                self.window.activate()
            return True
        return False

    def take_screenshot(self, filename: Optional[str] = None) -> None:
        """
        Main process: find, activate, pause if needed, then take a screenshot.
        Args:
            filename (Optional[str]): The filename to save the screenshot as. If None, uses default.
        """
        if filename is None:
            filename = self._get_default_filename()

        if not self.find_window():
            print(f"No window with the title '{self.window_title}' was found.")
            return

        if not self.activate_window():
            print(f"Failed to activate the window '{self.window_title}'.")
            return

        self._capture_screenshot(filename)

    def get_locations_of_image(self, search_image_path: str) -> list[Point]:
        """
        Locate all instances of an image within the window region on the screen.
        Args:
            search_image_path (str): Path to the image to search for.
        Returns:
            list[Point]: A list of center points of the located images.
        """
        try:
            if not self.find_window():
                return []
            if not self.activate_window():
                return []

            ret = []

            all_blank_locations = list(
                pyautogui.locateAllOnScreen(
                    search_image_path, confidence=0.95, region=self.window_region
                )
            )
            for item in all_blank_locations:
                ret.append(pyautogui.center(item))

            return ret
        except Exception:
            return []

    def get_image_in_screen_location(self, search_image_path: str) -> Optional[Point]:
        """
        Locate the center of an image within the window region on the screen.
        Args:
            search_image_path (str): Path to the image to search for.
        Returns:
            Optional[Point]: The center point if found, else None.
        """
        try:
            if not self.find_window():
                return None
            if not self.activate_window():
                return None
            return pyautogui.locateCenterOnScreen(
                search_image_path, confidence=0.95, region=self.window_region
            )
        except Exception:
            return None

    def _capture_screenshot(self, save_path: str) -> bool:
        """
        Capture a screenshot of the window using pyautogui.
        Args:
            save_path (str): The path to save the screenshot.
        Returns:
            bool: True if successful, False otherwise.
        """
        if self.window:
            screenshot = pyautogui.screenshot(region=self.window_region)
            screenshot.save(save_path)
            print(f"Screenshot saved as {save_path}")
            return True
        return False

    def _get_default_filename(self) -> str:
        """
        Generate a default filename for the screenshot based on the window title.
        Returns:
            str: The default filename path.
        """
        return str(
            self.screens_dir
            / f"{self.window_title}.png".replace(" ", "_").replace(":", "_")
        )


if __name__ == "__main__":
    window_title = "Fluent Tic-Tac-Toe"  # Replace with your actual window title
    screenshotter = WindowScreenshotter(window_title)
    screenshotter.take_screenshot()
