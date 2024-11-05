import pyxel
from src.scene.base import BaseScene
from sys import argv


class MainScene(BaseScene):
    def draw(self):
        pyxel.cls(8)
        super(MainScene, self).draw()

    def handle_key(self):
        if any(pyxel.btnp(key) for key in range(16)):
            self.game.current_scene_name = 'playground'
