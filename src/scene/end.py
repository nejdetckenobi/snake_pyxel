import pyxel
from src.scene.base import BaseScene


class EndScene(BaseScene):
    def draw(self):
        pyxel.text(0, f"You scored {self.game.score}. Press R to restart.", 2)
