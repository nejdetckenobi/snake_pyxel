import pyxel
from src.events import SceneChange
from src.scene.base import BaseScene


class PauseScene(BaseScene):
    def draw(self):
        pass

    def update(self):
        pass

    def handle_key(self):
        if pyxel.btnp(key=pyxel.KEY_P):
            self.event_bus.emit(SceneChange(screen_name="playground"))
