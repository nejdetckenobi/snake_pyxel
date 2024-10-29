import pyxel
from src.scene.base import BaseScene


class MainScene(BaseScene):
    def draw(self):
        pyxel.text(0, "Press any arrow key to start", 2)
