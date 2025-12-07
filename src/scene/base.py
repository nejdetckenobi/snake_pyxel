from abc import ABC, abstractmethod

from src.events import EventBus


class BaseScene(ABC):
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def update(self):
        pass

    def handle_key(self):
        pass

    @abstractmethod
    def draw(self):
        pass
