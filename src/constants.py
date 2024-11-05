from enum import IntEnum


TICK_PERIOD = 0.05
MARGIN = 8
CELL_SIZE = 16
WIDTH_IN_CELL_COUNT = 16
HEIGHT_IN_CELL_COUNT = 16
TRANSPARENT_COLOR = 0

MAX_HUNGER_LIMIT = 100
FOOD_EFFECT_AMOUNT = 20


class GameState(IntEnum):
    START = 0
    PAUSED = 1
    PLAYING = 2
    OVER = 3
    RESTARTED = 4


class Direction(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3
