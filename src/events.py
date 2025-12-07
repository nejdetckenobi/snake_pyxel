from collections import defaultdict
from dataclasses import dataclass, field

from src.entity.food import BaseFood


@dataclass
class BaseEvent:
    pass


class EventBus:
    def __init__(self):
        self.listeners = defaultdict(list)

    def register(self, event_type, listener):
        assert callable(listener)
        self.listeners[event_type.__name__].append(listener)

    def emit(self, event_instance):
        print(event_instance)
        for listener in list(self.listeners.get(event_instance.__class__.__name__, [])):
            try:
                listener(event_instance)
            except Exception:
                pass


@dataclass
class SceneChange(BaseEvent):
    screen_name: str
    extra: dict = field(default_factory=dict)


@dataclass
class ScoreChange(BaseEvent):
    new_score: int


@dataclass
class FoodEat(BaseEvent):
    food: BaseFood
    value: int


@dataclass
class SelfBite(BaseEvent):
    snake_part_index: int


@dataclass
class GameOver(BaseEvent):
    score: int = 0


@dataclass
class Reset(BaseEvent):
    pass
