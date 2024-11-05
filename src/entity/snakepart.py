from dataclasses import dataclass
from src.entity.base import Entity

from src.constants import Direction


@dataclass
class SnakePart(Entity):
    direction: Direction
    is_eating: bool = False
