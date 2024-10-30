import pyxel
from src.scene.base import BaseScene
from sys import argv


class MainScene(BaseScene):
    def draw(self):
        pyxel.cls(0)
        for i, e in enumerate(argv):
            pyxel.text(0, i * 8, str(e), 2)
