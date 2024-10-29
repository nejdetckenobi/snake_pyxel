from enum import IntEnum
import random
import time
import pyxel
from dataclasses import dataclass, field


CELL_SIZE = 16

pyxel.init(20 * CELL_SIZE, 9 * CELL_SIZE)
pyxel.load("resources.pyxres")
pyxel.mouse(True)


class GameState(IntEnum):
    START = 0
    PAUSED = 1
    PLAYING = 2
    OVER = 3
    RESTARTED = 4


class Direction(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


@dataclass
class Entity:
    x: int
    y: int


@dataclass
class SnakePart(Entity):
    direction: Direction


@dataclass
class Food(Entity):
    pass


@dataclass
class Wall(Entity):
    pass


class BaseScene(object):
    def __init__(self, game):
        self.game = game

    def draw(self):
        pass


class PlaygroundScene(BaseScene):
    def draw(self):
        pass


class MainScene(BaseScene):
    def draw(self):
        pyxel.text(0, "Press any arrow key to start", 2)


class EndScene(BaseScene):
    def draw(self):
        pyxel.text(0, f"You scored {self.game.score}. Press R to restart.", 2)
        

class Game(object):
    def __init__(self):
        super(Game, self).__init__()
        self.scenes = {
            "playground": PlaygroundScene(game=self),
            "main": MainScene(game=self),
            "end": EndScene(game=self),
        }
        self.reset()

    def _get_next_head_coordinates(self, x: int, y: int, direction: Direction):
        if direction == Direction.UP:
            result_x = x
            result_y = (y - CELL_SIZE) % pyxel.height
        elif direction == Direction.DOWN:
            result_x = x
            result_y = (y + CELL_SIZE) % pyxel.height
        elif direction == Direction.LEFT:
            result_x = (x - CELL_SIZE) % pyxel.width
            result_y = y
        elif direction == Direction.RIGHT:
            result_x = (x + CELL_SIZE) % pyxel.width
            result_y = y
        
        return result_x, result_y, direction

    def _get_random_coords(self):
        x_limit = pyxel.width // CELL_SIZE
        y_limit = pyxel.height // CELL_SIZE

        x = random.randrange(0, x_limit) * CELL_SIZE
        y = random.randrange(0, y_limit) * CELL_SIZE

        return x, y

    def _get_non_snake_coords(self):
        while True:
            x, y = self._get_random_coords()
            for part in self.snake_parts:
                if part.x != x or part.y != y:
                    return x, y

    def draw_foods(self):
        for food in self.foods:
            pyxel.blt(food.x, food.y, 
                      0, 
                      16, 0,
                      16, 16,
                      0)

    def draw_snake(self):
        for part in self.snake_parts:
            pyxel.blt(part.x, part.y, 
                      0, 
                      0, 0,
                      16, 16,
                      0)

    def draw_walls(self):
        for wall in self.walls:
            pyxel.blt(wall.x, wall.y,
                      0,
                      32, 0,
                      16, 16,
                      0)

    def reset(self):
        self.current_scene_name = "main"
        self.state = GameState.START
        self.score = 0
        self.snake_parts = []
        self.foods = []
        self.walls = [Wall(64, 64)]
        self.snake_parts.append(SnakePart(0, 0, Direction.UP))
        self.put_random_food()
        self.turns = []
        self.last_tick = time.time()

    def put_food(self, x, y):
        self.foods.append(Food(x, y))

    def put_random_food(self):
        food_coords = self._get_non_snake_coords()
        self.put_food(*food_coords)

    def update(self):
        self.handle_keypress()
        if self.state == GameState.OVER:
            self.reset()

        if self.state == GameState.PLAYING:
            now = time.time()
            if now - self.last_tick > 0.05:
                self.last_tick = now
                self.tick()

    def draw(self):
        pyxel.cls(0)
        self.draw_foods()
        self.draw_snake()
        self.draw_walls()
        pyxel.text(0, 0, f"{self.score}", 2)

    def handle_keypress(self):
        if pyxel.btnp(key=pyxel.KEY_P):
            if self.state == GameState.PAUSED:
                self.state = GameState.PLAYING
                self.last_tick = time.time()
            elif self.state == GameState.PLAYING:
                self.state = GameState.PAUSED
                print(self.snake_parts)
                print(self.foods)
            elif self.state == GameState.OVER:
                self.state = GameState.START
        if pyxel.btnp(key=pyxel.KEY_UP):
            if self.state == GameState.START:
                self.state = GameState.PLAYING
            if self.snake_parts[0].direction != Direction.DOWN:
                self.turns.append(Direction.UP)
        elif pyxel.btnp(key=pyxel.KEY_DOWN):
            if self.state == GameState.START:
                self.state = GameState.PLAYING
            if self.snake_parts[0].direction != Direction.UP:
                self.turns.append(Direction.DOWN)
        elif pyxel.btnp(key=pyxel.KEY_LEFT):
            if self.state == GameState.START:
                self.state = GameState.PLAYING
            if self.snake_parts[0].direction != Direction.RIGHT:
                self.turns.append(Direction.LEFT)
        elif pyxel.btnp(key=pyxel.KEY_RIGHT):
            if self.state == GameState.START:
                self.state = GameState.PLAYING
            if self.snake_parts[0].direction != Direction.LEFT:
    
                self.turns.append(Direction.RIGHT)
    def run(self):
        pyxel.run(self.update, self.draw)

    def tick(self):
        head = self.snake_parts[0]
        try:
            next_direction = self.turns.pop(0)
        except IndexError:
            next_direction = head.direction
        next_x, next_y, next_direction = self._get_next_head_coordinates(head.x, head.y, next_direction)
        new_part = SnakePart(next_x, next_y, next_direction)
        is_eating = False
        for food in self.foods:
            if food.x == new_part.x and food.y == new_part.y:
                is_eating = True
                break
        self.snake_parts.insert(0, new_part)
        if is_eating:
            self.put_random_food()
            self.foods.remove(food)
            self.score += 1
        else:
            self.snake_parts.pop()

        for wall in self.walls:
            if wall.x == new_part.x and wall.y == new_part.y:
                self.state = GameState.OVER
            

if __name__ == '__main__':
    game = Game()
    game.run()
