from abc import ABC, abstractmethod


class BaseScene(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def draw(self):
        pass
