from dataclasses import dataclass

from src.constants import CELL_SIZE, MARGIN


@dataclass
class Entity:
    x: int
    y: int

    @property
    def real_x(self):
        return self.x * CELL_SIZE + MARGIN

    @property
    def real_y(self):
        return self.y * CELL_SIZE + MARGIN
