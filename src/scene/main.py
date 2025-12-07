import pyxel
from src.constants import Direction
from src.events import GameStart
from src.scene.base import BaseScene
from sys import argv


class MainScene(BaseScene):
    def draw(self):
        pyxel.cls(0)
        super(MainScene, self).draw()

    def handle_key(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.event_bus.emit(GameStart(initial_direction=Direction.UP))
        elif pyxel.btnp(pyxel.KEY_LEFT):
            self.event_bus.emit(GameStart(initial_direction=Direction.LEFT))
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.event_bus.emit(GameStart(initial_direction=Direction.RIGHT))
