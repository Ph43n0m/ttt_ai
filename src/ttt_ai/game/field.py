from dataclasses import dataclass
from enum import StrEnum

from pyautogui import Point


class FieldState(StrEnum):
    EMPTY = "-"
    X = "X"
    O = "O"


@dataclass
class Field:
    location: Point = None
    state: FieldState = FieldState.EMPTY
