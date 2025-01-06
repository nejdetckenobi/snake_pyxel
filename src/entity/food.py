from dataclasses import dataclass
from src.entity.base import Entity


def get_all_food_types():
    return (
        ShortenerFood, 
        WallDestroyerFood,
        TailCutter,
    )


@dataclass
class BaseFood(Entity):
    pass


@dataclass
class RegularFood(BaseFood):
    pass


@dataclass
class ShortenerFood(BaseFood):
    pass


@dataclass
class WallDestroyerFood(BaseFood):
    pass


@dataclass
class TailCutter(BaseFood):
    pass
