import pyxel
from src.events import SceneChange
from src.scene.base import BaseScene


class MarketScene(BaseScene):
    def draw(self):
        pyxel.rect(0, 0, pyxel.width, pyxel.height, col=0)

    def update(self):
        return

    def handle_key(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.event_bus.emit(SceneChange(screen_name="playground"))
