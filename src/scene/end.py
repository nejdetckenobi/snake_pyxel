import pyxel
from src.events import EventBus, GameOver, Reset, ScoreChange
from src.scene.base import BaseScene


class EndScene(BaseScene):
    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus)
        self._score = 0
        self.event_bus.register(ScoreChange, self.on_score_change)

    def on_score_change(self, event: ScoreChange):
        self._score = event.new_score

    def handle_key(self):
        if pyxel.btnr(pyxel.KEY_R):
            self.event_bus.emit(Reset())

    def draw(self):
        pyxel.cls(0)
        texts = [
            f"Game Over",
            f"You scored {self._score}",
            f"Press R to restart",
        ]
        for index, text in enumerate(texts):
            pyxel.text(
                x=pyxel.width // 2 - len(text) * 2,
                y=pyxel.height // 2 - 6 * len(texts) // 2 + index * 6,
                s=text,
                col=1,
            )
