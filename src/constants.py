from enum import IntEnum


CELL_SIZE = 16


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
