__author__ = "David Antonucci"
__version__ = "1.0.0"

from enum import Enum


class Color(Enum):
    BLACK = 0
    WHITE = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    YELLOW = 5


class MoveError(Enum):
    OKAY = 0
    OUT_OF_RANGE = 1
    TAKEN = 2
    GAME_WON = 3
