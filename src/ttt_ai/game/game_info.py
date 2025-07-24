import sys
import threading
from pathlib import Path
from time import sleep
from typing import Optional

import pyautogui
from numpy import random

from ttt_ai.game.board import Board
from ttt_ai.game.field import Field, FieldState

# Add the current directory to a path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from ttt_ai.tools.window_screenshotter import WindowScreenshotter

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
        self.start_next_game_sleep = 0.2
        project_root = Path(__file__).parent.parent.parent
        self.resources_dir = project_root / "assets" / "resources"
        self.resources_dir.mkdir(parents=True, exist_ok=True)
        self.resources_images_dir = self.resources_dir / "images"
        self.resources_images_dir.mkdir(parents=True, exist_ok=True)
        self.screenshotter = WindowScreenshotter("Fluent Tic-Tac-Toe")
        # self.field_locations = []
        self._previous_game_state = GameState.INIT
        self.actual_game_state = GameState.INIT
        self.board = Board()

        self._state_lock = threading.Lock()
        # Initialize image paths for next game indicators
        indicate_next_game_image_files: list[str] = [
            "indicate_StartPlay.png",
            "indicate_PlayAgain.png",
            "indicate_TryAgain.png",
        ]

        self.check_next_game_button_paths: list[str] = [
            str(self.resources_images_dir / filename)
            for filename in indicate_next_game_image_files
        ]

        self.check_block_o_path = str(
            self.resources_images_dir / "indicate_Block_O.png"
        )
        self.check_block_o_win_path = str(
            self.resources_images_dir / "indicate_Block_O_Win.png"
        )
        self.check_block_x_path = str(
            self.resources_images_dir / "indicate_Block_X.png"
        )
        self.check_block_x_win_path = str(
            self.resources_images_dir / "indicate_Block_X_Win.png"
        )

        self.check_click_square_path = str(
            self.resources_images_dir / "indicate_ClickSquareToStart.png"
        )
        self.check_your_turn_path = str(
            self.resources_images_dir / "indicate_YourTurn.png"
        )
        self.check_go_back_path = str(self.resources_images_dir / "indicate_GoBack.png")
        self.check_win_path = str(self.resources_images_dir / "indicate_Win.png")
        self.check_lose_path = str(self.resources_images_dir / "indicate_Lost.png")
        self.check_draw_path = str(self.resources_images_dir / "indicate_Draw.png")
        self.check_block_clear_path = str(
            self.resources_images_dir / "indicate_Block_Clear.png"
        )

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
            location = self.screenshotter.get_image_in_screen_location(
                self.check_draw_path
            )
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
            location = self.screenshotter.get_image_in_screen_location(
                self.check_lose_path
            )
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
            location = self.screenshotter.get_image_in_screen_location(
                self.check_win_path
            )
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
            self._switch_game_state(
                GameState.YOUR_TURN
            )  # be carefully to not use it "strict" as return value because this state will be able to be Your Turn before
            return self.update_board_information()
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
                return self.click_random_clear_block()
        except Exception as e:
            print(e)
        return False

    def click_random_clear_block(self) -> bool:
        """
        Clicks a random clear block if available.
        Returns:
            bool: True if the indicator is visible, False otherwise.
        """
        list_of_field_locations = self.get_clear_block_locations()

        if len(list_of_field_locations) > 0:
            location = list_of_field_locations[
                random.randint(0, len(list_of_field_locations))
            ]

            if location is not None:
                return self._click_at_location(location)

        return False

    def get_clear_block_locations(self) -> list[pyautogui.Point]:
        """Retrieves the locations of all clear blocks on the board."""
        return self.screenshotter.get_locations_of_image(self.check_block_clear_path)

    def get_o_block_locations(self) -> list[pyautogui.Point]:
        """Retrieves the locations of all 'O' blocks on the board."""
        return self.screenshotter.get_locations_of_image(
            self.check_block_o_path
        ) + self.screenshotter.get_locations_of_image(self.check_block_o_win_path)

    def get_x_block_locations(self) -> list[pyautogui.Point]:
        """Retrieves the locations of all 'X' blocks on the board."""
        return self.screenshotter.get_locations_of_image(
            self.check_block_x_path
        ) + self.screenshotter.get_locations_of_image(self.check_block_x_win_path)

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
                sleep(self.start_next_game_sleep)  # Wait for the game to reset
            return True
        return False

    def move_mouse_to_save_location(self) -> bool:
        """
        Moves the mouse to a random location within the window area.
        Returns:
            bool: True if the move was successful, False otherwise.
        """
        try:
            return self._click_at_location(
                pyautogui.Point(
                    random.randint(
                        self.screenshotter.window.right - 100,
                        self.screenshotter.window.right - 50,
                    ),
                    random.randint(
                        self.screenshotter.window.bottom - 100,
                        self.screenshotter.window.bottom - 50,
                    ),
                ),
                0.1,  # TODO: check... if 0.2 might be better
            )
        except Exception as e:
            print(f"Error moving mouse to save location: {e}")
        return False

    def _switch_game_state(self, new_state: GameState) -> bool:
        with self._state_lock:
            if new_state != self._previous_game_state:
                print(
                    f"PRE Game state changed p: {self._previous_game_state} a: {self.actual_game_state.name}"
                )
                self._previous_game_state = self.actual_game_state
                self.actual_game_state = new_state
                print(
                    f"Game state changed from {self._previous_game_state} to: {self.actual_game_state.name}"
                )
                return True
            print(
                f"Game state NOT changed from {self._previous_game_state} to: {self.actual_game_state.name}"
            )
        return False

    def update_board_information(self) -> bool:
        try:
            max_loop = 10
            update_loop = 0

            while update_loop < max_loop:
                update_loop += 1
                print(f"Updating board information {update_loop}/{max_loop}...")
                list_of_field_positions_clear = self.get_clear_block_locations()
                list_of_field_positions_o = self.get_o_block_locations()
                list_of_field_positions_x = self.get_x_block_locations()

                if (
                        len(list_of_field_positions_clear)
                        + len(list_of_field_positions_o)
                        + len(list_of_field_positions_x)
                ) == 9:
                    print(f"Clear Blocks found: {len(list_of_field_positions_clear)}")
                    print(f"O Blocks found: {len(list_of_field_positions_o)}")
                    print(f"X Blocks found: {len(list_of_field_positions_x)}")

                    # Update the board with the current field locations
                    for row in range(self.board.BOARD_SIZE):
                        for col in range(self.board.BOARD_SIZE):
                            field_location = self.board.fields[row][col].location
                            if field_location in list_of_field_positions_clear:
                                self.board.fields[row][col].state = FieldState.EMPTY
                            elif field_location in list_of_field_positions_o:
                                self.board.fields[row][col].state = FieldState.O
                            elif field_location in list_of_field_positions_x:
                                self.board.fields[row][col].state = FieldState.X
                            else:
                                print(f"Field {field_location} not found")
                    return True

            self.move_mouse_to_save_location()
            return False
        except Exception as e:
            print(f"Error updating board information: {e}")
            return False

    def _reset_field_locations(self) -> bool:
        try:
            max_loop = 10
            update_loop = 0
            list_of_field_locations = []

            while update_loop < max_loop and len(list_of_field_locations) != 9:
                update_loop += 1
                print("Resetting field locations...")

                self.move_mouse_to_save_location()

                list_of_field_locations = self.screenshotter.get_locations_of_image(
                    self.check_block_clear_path
                )

                if len(list_of_field_locations) == 9:
                    row = 0

                    for idx, location in enumerate(list_of_field_locations):
                        if idx > 0 and idx % 3 == 0:
                            row += 1
                        self.board.fields[row][idx % 3] = Field(location)

                    print("Field locations reset successfully.")
                    return True
                else:
                    print("Not all field locations found.")
                    return False

            print("Failed to reset field locations after maximum attempts.")
            return False

        except Exception as e:
            print(f"Error resetting field locations: {e}")
        return False

    def click_at_field(self, location: Field, sleep_time: float = 0, uuu=0) -> bool:
        return self._click_at_location(location.location, sleep_time)

    def _click_at_location(
            self, location: pyautogui.Point, sleep_time: float = 0
    ) -> bool:  # TODO: needs refactoring to an controller class
        """
        Moves the mouse to specified location and performs a click.

        Args:
            location: The point coordinates to click at.

        Returns:
            bool: True if click was successful, False otherwise.
            :param location: The point coordinates to click at.
            :param sleep_time: time to wait after clicking, default is 0 seconds.
        """
        ret = False
        try:
            ret = self._move_to_location(location)
            if ret:
                pyautogui.click()
                if sleep_time > 0:
                    sleep(sleep_time)
                    ret = self._move_to_location(location)
            return ret
        except Exception as e:
            print(f"Error moving mouse or clicking: {e}")
        return ret

    def _move_to_location(
            self, location: pyautogui.Point, random_distortion=10, sleep_time: float = 0
    ) -> bool:
        """
        Moves mouse to specified location

        Args:
            location: The point coordinates to click at.

        Returns:
            bool: True if click was successful, False otherwise.
        """
        try:
            pyautogui.moveTo(
                random.randint(
                    location.x - random_distortion, location.x + random_distortion
                ),
                random.randint(
                    location.y - random_distortion, location.y + random_distortion
                ),
                self.mouse_speed,
            )
            sleep(sleep_time)
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
