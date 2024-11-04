import pyxel

from src.game import Game
from src.constants import CELL_SIZE, HEIGHT_IN_CELL_COUNT, MARGIN, WIDTH_IN_CELL_COUNT


if __name__ == '__main__':
    pyxel.init(WIDTH_IN_CELL_COUNT * CELL_SIZE + 2 * MARGIN, HEIGHT_IN_CELL_COUNT * CELL_SIZE + 2 * MARGIN)
    pyxel.load("resources.pyxres")
    pyxel.mouse(True)
    game = Game()
    game.run()
