import random
import time

import pyxel
from src.entity.wall import Wall
from src.entity.food import Food
from src.constants import CELL_SIZE, FOOD_EFFECT_AMOUNT, HEIGHT_IN_CELL_COUNT, MAX_HUNGER_LIMIT, TICK_PERIOD, TRANSPARENT_COLOR, MARGIN, WIDTH_IN_CELL_COUNT, Direction
from src.entity.snakepart import SnakePart
from src.scene.base import BaseScene


class PlaygroundScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.snake_parts = []
        self.foods = []
        self.walls = []
        self.turns = []
        self.last_tick = time.time()
        self.hunger_limit = MAX_HUNGER_LIMIT
        start_x = WIDTH_IN_CELL_COUNT // 2
        start_y = HEIGHT_IN_CELL_COUNT // 2 
        self.snake_parts = [SnakePart(start_x, start_y, Direction.UP),
                            SnakePart(start_x, start_y + 1, Direction.UP)]
        self.put_random_food()

    # TODO: Fix calculations to accept block (cell) system
    def _get_random_coords(self):
        x = random.randrange(0, WIDTH_IN_CELL_COUNT)
        y = random.randrange(0, HEIGHT_IN_CELL_COUNT)

        return x, y

    # TODO: Fix calculations to accept block (cell) system
    def _get_empty_coords(self):
        is_valid = False
        while not is_valid:
            x, y = self._get_random_coords()
            is_valid = True
            for part in self.snake_parts + self.foods + self.walls:
                if part.x == x and part.y == y:
                    is_valid = False
        return x, y


    # TODO: Fix calculations to accept block (cell) system
    def _get_next_head_grid(self, x: int, y: int, direction: Direction):
        if direction == Direction.UP:
            result_x = x
            result_y = (y - 1) % HEIGHT_IN_CELL_COUNT
        elif direction == Direction.DOWN:
            result_x = x
            result_y = (y + 1) % HEIGHT_IN_CELL_COUNT
        elif direction == Direction.LEFT:
            result_x = (x - 1) % WIDTH_IN_CELL_COUNT
            result_y = y
        elif direction == Direction.RIGHT:
            result_x = (x + 1) % WIDTH_IN_CELL_COUNT
            result_y = y
        return result_x, result_y, direction

    def put_food(self, x, y):
        self.foods.append(Food(x, y))

    def put_random_food(self):
        food_coords = self._get_empty_coords()
        self.put_food(*food_coords)

    def draw_foods(self):
        for food in self.foods:
            pyxel.blt(food.real_x, food.real_y, 
                      0,
                      0, CELL_SIZE,
                      CELL_SIZE, CELL_SIZE,
                      TRANSPARENT_COLOR)

    def draw_snake(self):
        for part in self.snake_parts:
            pyxel.blt(part.real_x, part.real_y, 
                      0, 
                      0, 0,
                      CELL_SIZE, CELL_SIZE,
                      TRANSPARENT_COLOR)


    def draw_walls(self):
        for wall in self.walls:
            pyxel.blt(wall.real_x, wall.real_y,
                      0,
                      0, 2 * CELL_SIZE,
                      CELL_SIZE, CELL_SIZE,
                      TRANSPARENT_COLOR)

    def draw(self):
        super(PlaygroundScene, self).draw()
        self.draw_foods()
        self.draw_snake()
        self.draw_walls()
        if self.hunger_limit != 0:
            pyxel.text(0, 0, f"{self.game.score} ({self.hunger_limit})", 2)
        else:
            pyxel.text(0, 0, f"You scored {self.game.score}", 2)

    def update(self):
        now = time.time()
        if now - self.last_tick > TICK_PERIOD:
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
        if self.hunger_limit == 0:
            return
        head = self.snake_parts[0]
        # Take snake programming into account
        try:
            next_direction = self.turns.pop(0)
        except IndexError:
            next_direction = head.direction

        # TODO: Fix calculations to accept block (cell) system
        next_x, next_y, next_direction = self._get_next_head_grid(head.x, head.y, next_direction)
        new_part = SnakePart(next_x, next_y, next_direction)
        print(new_part)
        print(self.foods)
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
        is_stopped = False
        for wall in self.walls:
            if wall.x == new_part.x and wall.y == new_part.y:
                is_stopped = True
        
        if is_stopped:
            self.hunger_limit = max(0, self.hunger_limit - 1)
            return

        self.snake_parts.insert(0, new_part)
        if is_eating:
            self.put_random_food()
            self.foods.remove(food)
            self.game.score += 1
            self.hunger_limit = min(self.hunger_limit + FOOD_EFFECT_AMOUNT, MAX_HUNGER_LIMIT)
        else:
            self.snake_parts.pop()
            # self.hunger_limit = max(0, self.hunger_limit - 1)
