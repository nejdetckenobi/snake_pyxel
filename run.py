import pyxel

from src.game import Game
from src.constants import CELL_SIZE


if __name__ == '__main__':
    pyxel.init(8 * CELL_SIZE, 8 * CELL_SIZE)
    pyxel.load("resources.pyxres")
    pyxel.mouse(True)
    game = Game()
    game.run()
