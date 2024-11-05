import pyxel

from src.game import Game
from src.constants import CELL_SIZE, HEIGHT_IN_CELL_COUNT, PANE_HEIGHT, WIDTH_IN_CELL_COUNT


if __name__ == '__main__':
    pyxel.init(WIDTH_IN_CELL_COUNT * CELL_SIZE, 
               HEIGHT_IN_CELL_COUNT * CELL_SIZE + PANE_HEIGHT)
    pyxel.load("resources.pyxres")
    # pyxel.mouse(True)
    game = Game()
    game.run()
