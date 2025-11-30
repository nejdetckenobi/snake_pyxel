import pyxel
from src.scene.base import BaseScene


class MarketScene(BaseScene):
    def draw(self):
        pyxel.rect(0, 0, pyxel.width, pyxel.height, col=0)

    def update(self):
        return

    def handle_key(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.game.current_scene_name = "playground"
