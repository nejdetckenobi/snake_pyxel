import pyxel
from src.scene.base import BaseScene
from sys import argv


class MainScene(BaseScene):
    def draw(self):
        super(MainScene, self).draw()
        pyxel.text(0, 0, "Press R to start", 2)
