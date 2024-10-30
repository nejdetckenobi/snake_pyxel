import random
import time

import pyxel
from src.entity.wall import Wall
from src.entity.food import Food
from src.constants import CELL_SIZE, Direction
from src.entity.snakepart import SnakePart
from src.scene.base import BaseScene


class PlaygroundScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.snake_parts = []
        self.foods = []
        self.walls = []
        self.snake_parts.append(SnakePart(0, 0, Direction.UP))
        self.put_random_food()
        self.turns = []
        self.last_tick = time.time()

    def _get_random_coords(self):
        x_limit = pyxel.width // CELL_SIZE
        y_limit = pyxel.height // CELL_SIZE

        x = random.randrange(0, x_limit) * CELL_SIZE
        y = random.randrange(0, y_limit) * CELL_SIZE

        return x, y

    def _get_empty_coords(self):
        is_valid = False
        while not is_valid:
            x, y = self._get_random_coords()
            is_valid = True
            for part in self.snake_parts + self.foods + self.walls:
                if part.x == x and part.y == y:
                    is_valid = False
        return x, y


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

    def put_food(self, x, y):
        self.foods.append(Food(x, y))

    def put_random_food(self):
        food_coords = self._get_empty_coords()
        self.put_food(*food_coords)

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

    def draw(self):
        pyxel.cls(0)
        self.draw_foods()
        self.draw_snake()
        self.draw_walls()
        pyxel.text(0, 0, f"{self.game.score}", 2)

    def update(self):
        now = time.time()
        if now - self.last_tick > 0.05:
            self.last_tick = now
            self.tick()

    def handle_key(self):
        if pyxel.btnp(key=pyxel.KEY_UP):
            if self.snake_parts[0].direction != Direction.DOWN:
                self.turns.append(Direction.UP)
        elif pyxel.btnp(key=pyxel.KEY_DOWN):
            if self.snake_parts[0].direction != Direction.UP:
                self.turns.append(Direction.DOWN)
        elif pyxel.btnp(key=pyxel.KEY_LEFT):
            if self.snake_parts[0].direction != Direction.RIGHT:
                self.turns.append(Direction.LEFT)
        elif pyxel.btnp(key=pyxel.KEY_RIGHT):
            if self.snake_parts[0].direction != Direction.LEFT:
                self.turns.append(Direction.RIGHT)


    def tick(self):
        head = self.snake_parts[0]
        # Take snake programming into account
        try:
            next_direction = self.turns.pop(0)
        except IndexError:
            next_direction = head.direction

        next_x, next_y, next_direction = self._get_next_head_coordinates(head.x, head.y, next_direction)
        new_part = SnakePart(next_x, next_y, next_direction)
        is_eating = False

        # Check if there is a food on the way
        for food in self.foods:
            if food.x == new_part.x and food.y == new_part.y:
                is_eating = True
                break

        # Check if there is a snake part on the way
        is_self_bite = False
        for part in self.snake_parts:
            if part.x == new_part.x and part.y == new_part.y:
                is_self_bite = True
                break
        
        if is_self_bite:
            part_index = self.snake_parts.index(part)
            alive_parts, dead_parts = self.snake_parts[:part_index], self.snake_parts[part_index + 1:]
            self.snake_parts = alive_parts
            for dp in dead_parts:
                self.walls.append(Wall(dp.x, dp.y))

        # Check if there is a wall on the way
        is_dead = False
        for wall in self.walls:
            if wall.x == new_part.x and wall.y == new_part.y:
                is_dead = True
        
        if is_dead:
            return

        self.snake_parts.insert(0, new_part)
        if is_eating:
            self.put_random_food()
            self.foods.remove(food)
            self.game.score += 1
        else:
            self.snake_parts.pop()
            
