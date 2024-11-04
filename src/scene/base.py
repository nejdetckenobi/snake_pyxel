from abc import ABC, abstractmethod

import pyxel


class BaseScene(ABC):
    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def handle_key(self):
        pass

    @abstractmethod
    def draw(self):
        pyxel.cls(1)

