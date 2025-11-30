import pyxel
from src.scene.base import BaseScene


class PauseScene(BaseScene):
    def draw(self):
        pass

    def update(self):
        pass

    def handle_key(self):
        if pyxel.btnp(key=pyxel.KEY_P):
            self.game.current_scene_name = "playground"
