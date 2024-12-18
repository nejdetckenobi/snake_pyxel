import pyxel
from src.scene.base import BaseScene
from src.scene.end import EndScene
from src.scene.main import MainScene
from src.scene.playground import PlaygroundScene


class Game(object):
    def __init__(self):
        super(Game, self).__init__()
        self.scenes = {
            "playground": PlaygroundScene(game=self),
            "main": MainScene(game=self),
            "end": EndScene(game=self),
        }
        self.score = 0
        self.current_scene_name = "playground"
        self.reset()

    @property
    def current_scene(self) -> BaseScene:
        return self.scenes[self.current_scene_name]

    def reset(self):
        self.scenes["playground"] = PlaygroundScene(game=self)
        self.current_scene_name = "playground"
        self.score = 0

    def draw(self):
        self.current_scene.draw()

    def update(self):
        if pyxel.btn(pyxel.KEY_ESCAPE):
            pass
        elif pyxel.btnr(pyxel.KEY_R):
            self.reset()
        self.current_scene.handle_key()
        self.current_scene.update()

    def run(self):
        pyxel.run(self.update, self.draw)
