import sys
from pathlib import Path
from time import sleep
from typing import Optional
import threading

import pyautogui
from numpy import random
from numpy.f2py.auxfuncs import throw_error

# Add the current directory to a path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from window_screenshotter import WindowScreenshotter

from enum import Enum


class GameState(Enum):
    INIT = 0
    PLAY_AGAIN = 1
    YOUR_TURN = 2
    WIN = 3
    LOSE = 4
    DRAW = 5


class GameInfo:

    def __init__(self, mouse_speed: float = 0.2) -> None:
        self.mouse_speed = mouse_speed
        project_root = Path(__file__).parent.parent.parent
        self.resources_dir = project_root / "assets" / "resources"
        # Ensure 'resources' directories exist
        self.resources_dir.mkdir(parents=True, exist_ok=True)
        self.screenshotter = WindowScreenshotter("Fluent Tic-Tac-Toe")
        self.field_locations = []
        self._previous_game_state = GameState.INIT
        self.actual_game_state = GameState.INIT
        self._state_lock = threading.Lock()
        # Initialize image paths for next game indicators
        indicate_next_game_image_files: list[str] = [
            "indicate_StartPlay.png",
            "indicate_PlayAgain.png",
            "indicate_TryAgain.png",
        ]

        self.check_next_game_button_paths = [
            str(self.resources_dir / filename)
            for filename in indicate_next_game_image_files
        ]
        self.check_click_square_path = str(
            self.resources_dir / "indicate_ClickSquareToStart.png"
        )
        self.check_your_turn_path = str(self.resources_dir / "indicate_YourTurn.png")
        self.check_go_back_path = str(self.resources_dir / "indicate_GoBack.png")
        self.check_win_path = str(self.resources_dir / "indicate_Win.png")
        self.check_lose_path = str(self.resources_dir / "indicate_Lost.png")
        self.check_draw_path = str(self.resources_dir / "indicate_Draw.png")
        self.check_block_clear_path = str(
            self.resources_dir / "indicate_Block_Clear.png"
        )
        self.check_block_o_path = str(self.resources_dir / "indicate_Block_O.png")
        self.check_block_x_path = str(self.resources_dir / "indicate_Block_X.png")

    def get_previous_game_state(self) -> GameState:
        """
        Returns the previous game state.
        Returns:
            GameState: The previous game state.
        """
        return self._previous_game_state

    def is_go_back_clicked(self) -> bool:
        """
        Checks if the go back button is clicked.
        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        location = self.screenshotter.get_image_in_screen_location(
            self.check_go_back_path
        )
        if location is not None:
            return self._click_at_location(location)
        return False

    def is_draw_shown(self) -> bool:
        """
        Checks for the visibility of the 'draw' indicator.
        Returns:
            bool: True if the indicator is visible, False otherwise.
        """
        if self._previous_game_state != GameState.LOSE:
            location = self.screenshotter.get_image_in_screen_location(self.check_draw_path)
            if location is not None:
                self._switch_game_state(GameState.DRAW)
                return True
        return False

    def is_lose_shown(self) -> bool:
        """
        Checks for the visibility of the 'lose' indicator.
        Returns:
            bool: True if the indicator is visible, False otherwise.
        """
        if self._previous_game_state != GameState.LOSE:
            location = self.screenshotter.get_image_in_screen_location(self.check_lose_path)
            if location is not None:
                self._switch_game_state(GameState.LOSE)
                return True
        return False

    def is_win_shown(self) -> bool:
        """
        Checks for the visibility of the 'win' indicator.
        Returns:
            bool: True if the indicator is visible, False otherwise.
        """
        if self._previous_game_state != GameState.WIN:
            location = self.screenshotter.get_image_in_screen_location(self.check_win_path)
            if location is not None:
                self._switch_game_state(GameState.WIN)
                return True
        return False

    def is_your_turn_shown(self) -> bool:
        """
        Checks for the visibility of the 'your turn' indicator.
        Returns:
            bool: True if the indicator is visible, False otherwise.
        """
        location = self.screenshotter.get_image_in_screen_location(
            self.check_your_turn_path
        )
        if location is not None:
            self._switch_game_state(GameState.YOUR_TURN)
            return True
        return False

    def is_click_square_shown(self) -> bool:
        """
        Checks if the 'Click Square to Start' indicator is shown and clicks a random field
        if all 9 field positions are known.

        Returns:
            bool: True if a click was performed, otherwise False.
        """
        try:
            location = self.screenshotter.get_image_in_screen_location(
                self.check_click_square_path
            )
            if location is not None:
                if len(self.field_locations) == 9:
                    self._click_at_location(
                        self.field_locations[
                            random.randint(0, len(self.field_locations))
                        ]
                    )
                    return True
            return False
        except Exception as e:
            print(e)
            return False

    def click_random_clear_block(self) -> bool:
        """
        Clicks a random clear block if available.
        Returns:
            bool: True if the indicator is visible, False otherwise.
        """
        list_of_field_locations = self.screenshotter.get_locations_of_image(
            self.check_block_clear_path
        )
        if len(list_of_field_locations) > 0:
            location = list_of_field_locations[random.randint(0, list_of_field_locations.__len__())]

            if location is not None:
                return self._click_at_location(location)

        return False

    def start_next_game(self) -> bool:
        """
        Clicks on the next game button if found.
        Returns:
            bool: True if click was successful, False otherwise.
        """
        location = self._get_one_of_the_next_game_button_locations()
        if location is not None:
            if self._click_at_location(location):
                self._reset_field_locations()
                self._switch_game_state(GameState.INIT)
                sleep(0.3)  # Wait for the game to reset
            return True
        return False

    def move_mouse_to_save_location(self) -> bool:
        """
        Moves the mouse to a random location within the window area.
        Returns:
            bool: True if the move was successful, False otherwise.
        """
        try:
            return self._move_to_location(
                pyautogui.Point(
                    random.randint(
                        self.screenshotter.window.right - 100,
                        self.screenshotter.window.right - 50,
                    ),
                    random.randint(
                        self.screenshotter.window.bottom - 100,
                        self.screenshotter.window.bottom - 50,
                    ),
                )
            )
        except Exception as e:
            print(f"Error moving mouse to save location: {e}")
            return False

    def _switch_game_state(self, new_state: GameState) -> bool:
        with self._state_lock:
            if new_state != self._previous_game_state:
                print(f"PRE Game state changed p: {self._previous_game_state} a: {self.actual_game_state.name}")
                self._previous_game_state = self.actual_game_state
                self.actual_game_state = new_state
                print(f"Game state changed from {self._previous_game_state} to: {self.actual_game_state.name}")
                return True
            print(f"Game state NOT changed from {self._previous_game_state} to: {self.actual_game_state.name}")
            return False

    def _reset_field_locations(self):
        try:
            if self.field_locations == [] and self.move_mouse_to_save_location():
                pyautogui.click()
                sleep(0.3)

                list_of_field_locations = self.screenshotter.get_locations_of_image(
                    self.check_block_clear_path
                )

                if list_of_field_locations.__len__() == 9:
                    self.field_locations = []
                    for location in list_of_field_locations:
                        self.field_locations.append(location)
                    print("Done resetting field locations." + str(self.field_locations))
                else:
                    throw_error("Not all field locations found.")

        except Exception as e:
            print(f"Error resetting field locations: {e}")

    def _click_at_location(self, location: pyautogui.Point) -> bool:
        """
        Moves the mouse to specified location and performs a click.

        Args:
            location: The point coordinates to click at.

        Returns:
            bool: True if click was successful, False otherwise.
        """
        try:
            self._move_to_location(location)
            pyautogui.click()
            return True
        except Exception as e:
            print(f"Error moving mouse or clicking: {e}")
            return False

    def _move_to_location(self, location: pyautogui.Point) -> bool:
        """
        Moves mouse to specified location

        Args:
            location: The point coordinates to click at.

        Returns:
            bool: True if click was successful, False otherwise.
        """
        try:
            pyautogui.moveTo(random.randint(location.x - 20, location.x + 20),
                             random.randint(location.y - 20, location.y + 20), self.mouse_speed)
            # sleep(0.2)
            return True
        except Exception as e:
            print(f"Error moving mouse: {e}")
            return False

    def _get_one_of_the_next_game_button_locations(self) -> Optional[pyautogui.Point]:
        """
        Searches for any of the next game button images on the screen.
        Returns:
            Optional[pyautogui.Point]: The location if found, else None.
        """
        for check_path in self.check_next_game_button_paths:
            location = self.screenshotter.get_image_in_screen_location(check_path)
            if location is not None:
                return location
        return None
