import pyxel
from src.events import EventBus, FoodEat, GameOver, Reset, SceneChange, ScoreChange
from src.scene.pause import PauseScene
from src.scene.market import MarketScene
from src.scene.base import BaseScene
from src.scene.end import EndScene
from src.scene.main import MainScene
from src.scene.playground import PlaygroundScene


class Game(object):
    def __init__(self):
        super(Game, self).__init__()
        self.event_bus = EventBus()
        self.scenes = {
            "playground": PlaygroundScene(event_bus=self.event_bus),
            "market": MarketScene(event_bus=self.event_bus),
            "main": MainScene(event_bus=self.event_bus),
            "end": EndScene(event_bus=self.event_bus),
            "pause": PauseScene(event_bus=self.event_bus),
        }
        self.score = 0
        self.current_scene_name = "playground"

        self.event_bus.register(SceneChange, self.on_scene_change)
        self.event_bus.register(FoodEat, self.on_food_eat)
        self.event_bus.register(GameOver, self.on_game_over)
        self.event_bus.register(Reset, self.on_reset)
        self.event_bus.emit(Reset())

    def on_scene_change(self, event: SceneChange):
        self.current_scene_name = event.screen_name

    def on_food_eat(self, event: FoodEat):
        print("cagrildim!!!")
        self.score += event.value
        self.event_bus.emit(ScoreChange(new_score=self.score))

    def on_game_over(self, event: GameOver):
        self.event_bus.emit(SceneChange(screen_name="end"))

    def on_reset(self, event: Reset):
        self.score = 0
        self.event_bus.emit(ScoreChange(new_score=0))
        self.event_bus.emit(SceneChange(screen_name="playground"))

    @property
    def current_scene(self) -> BaseScene:
        return self.scenes[self.current_scene_name]

    def draw(self):
        self.current_scene.draw()

    def update(self):
        if pyxel.btn(pyxel.KEY_ESCAPE):
            pass
        self.current_scene.handle_key()
        self.current_scene.update()

    def run(self):
        pyxel.run(self.update, self.draw)
