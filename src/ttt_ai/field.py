from dataclasses import dataclass
from enum import Enum

from pyautogui import Point


class FieldState(Enum):
    EMPTY = "-"
    X = "X"
    O = "O"


@dataclass
class Field:
    location: Point = None
    state: FieldState = FieldState.EMPTY
