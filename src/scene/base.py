from abc import ABC, abstractmethod


class BaseScene(ABC):
    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def handle_key(self):
        pass

    @abstractmethod
    def draw(self):
        pass
