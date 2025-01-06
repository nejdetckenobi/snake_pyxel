import random
import time

import pyxel
from src.entity.wall import Wall
from src.entity.food import RegularFood
from src.constants import (CELL_SIZE, 
                           INITIAL_FOOD_SATIETY_AMOUNT, INITIAL_FOOD_TAIL_AMOUNT, 
                           HEIGHT_IN_CELL_COUNT, 
                           MAX_HUNGER_LIMIT, PANE_HEIGHT, 
                           PANE_PADDING, 
                           TICK_PERIOD, 
                           WIDTH_IN_CELL_COUNT, 
                           Direction)
from src.entity.snakepart import SnakePart
from src.scene.base import BaseScene


HEAD_ROTATION_MAP = {
    # head only
    Direction.RIGHT: (0,   0),
    Direction.LEFT : (0, 180),
    Direction.UP   : (0,  90),
    Direction.DOWN : (0, 270),
}

MID_ROTATION_MAP = {
    # prev + curr only
    (Direction.RIGHT, Direction.RIGHT): (3,   0),
    (Direction.LEFT,  Direction.LEFT ): (3, 180),
    (Direction.UP,    Direction.UP   ): (3,  90),
    (Direction.DOWN,  Direction.DOWN ): (3, 270),
    (Direction.RIGHT, Direction.UP   ): (4,   0),
    (Direction.RIGHT, Direction.DOWN ): (5, 180),
    (Direction.UP,    Direction.RIGHT): (5, 270),
    (Direction.UP,    Direction.LEFT ): (4,  90),
    (Direction.LEFT,  Direction.UP   ): (5,   0),
    (Direction.LEFT,  Direction.DOWN ): (4, 180),
    (Direction.DOWN,  Direction.RIGHT): (4, 270),
    (Direction.DOWN,  Direction.LEFT ): (5,  90),
}

TAIL_ROTATION_MAP = {
    (Direction.RIGHT, Direction.RIGHT): (6,   0),
    (Direction.LEFT,  Direction.LEFT ): (6, 180),
    (Direction.UP,    Direction.UP   ): (6,  90),
    (Direction.DOWN,  Direction.DOWN ): (6, 270),
    (Direction.RIGHT, Direction.UP   ): (7,   0),
    (Direction.RIGHT, Direction.DOWN ): (8, 180),
    (Direction.UP,    Direction.RIGHT): (8, 270),
    (Direction.UP,    Direction.LEFT ): (7,  90),
    (Direction.LEFT,  Direction.UP   ): (8,   0),
    (Direction.LEFT,  Direction.DOWN ): (7, 180),
    (Direction.DOWN,  Direction.RIGHT): (7, 270),
    (Direction.DOWN,  Direction.LEFT ): (8,  90),    
}


class PlaygroundScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.snake_parts = []
        self.foods = []
        self.walls = []
        self.turns = []
        self.last_tick = time.time()
        self._tail_debt = 0
        self.hunger_limit = MAX_HUNGER_LIMIT
        self.food_tail_amount = INITIAL_FOOD_TAIL_AMOUNT
        self.food_satiety_amount = INITIAL_FOOD_SATIETY_AMOUNT
        start_x = WIDTH_IN_CELL_COUNT // 2
        start_y = HEIGHT_IN_CELL_COUNT // 2 
        self.snake_parts = [SnakePart(start_x, start_y, Direction.UP),
                            SnakePart(start_x, start_y + 1, Direction.UP),
                            SnakePart(start_x, start_y + 2, Direction.UP)]
        self.put_random_food()

    def _get_random_coords(self):
        x = random.randrange(0, WIDTH_IN_CELL_COUNT)
        y = random.randrange(0, HEIGHT_IN_CELL_COUNT)

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
        self.foods.append(RegularFood(x, y))

    def put_random_food(self):
        food_coords = self._get_empty_coords()
        self.put_food(*food_coords)

    def draw_foods(self):
        for food in self.foods:
            pyxel.blt(food.real_x, PANE_HEIGHT + food.real_y, 
                      0,
                      0, CELL_SIZE,
                      CELL_SIZE, CELL_SIZE)

    def draw_snake(self):
        head = self.snake_parts[0]
        head_sprite_data = HEAD_ROTATION_MAP[head.direction]
        pyxel.blt(head.real_x, PANE_HEIGHT + head.real_y,
                  0, 
                  head_sprite_data[0], 0,
                  CELL_SIZE, CELL_SIZE, 
                  rotate=head_sprite_data[1])

        tail = self.snake_parts[-1]
        prev_tail = self.snake_parts[-2]
        tail_sprite_data = TAIL_ROTATION_MAP[(prev_tail.direction, tail.direction)]
        pyxel.blt(tail.real_x, PANE_HEIGHT + tail.real_y,
                  0, 
                  tail_sprite_data[0] * CELL_SIZE, 0,
                  CELL_SIZE, CELL_SIZE, 
                  rotate=tail_sprite_data[1])
        
        if len(self.snake_parts) > 2:
            for index, curr_part in enumerate(self.snake_parts[1:-1], start=1):
                prev_part = self.snake_parts[index - 1]
                sprite_data = MID_ROTATION_MAP[(prev_part.direction, curr_part.direction)]
                pyxel.blt(curr_part.real_x, PANE_HEIGHT + curr_part.real_y, 
                          0, 
                          (sprite_data[0] - (1 if curr_part.is_eating and sprite_data[0] == 3 else 0)) * CELL_SIZE, 0,
                          CELL_SIZE, CELL_SIZE,
                          rotate=sprite_data[1])


    def draw_walls(self):
        for wall in self.walls:
            pyxel.blt(wall.real_x, PANE_HEIGHT + wall.real_y,
                      0,
                      0, 2 * CELL_SIZE,
                      CELL_SIZE, CELL_SIZE)

    def draw_game_over(self):
        texts = [
            f"Game Over",
            f"You scored {self.game.score}",
            f"Press R to restart",
        ]
        rect_width = max(map(len, texts)) * 4 + 4
        rect_height = len(texts) * 6 + 4

        pyxel.rect((pyxel.width - rect_width) // 2, (pyxel.height - rect_height) // 2,
                   rect_width, rect_height,
                   col=0)

        for index, text in enumerate(texts):
            pyxel.text(pyxel.width // 2 - 2 * len(text),
                       pyxel.height // 2 + 2 - 6 * (len(texts) - index - 1), text, 7)

    def draw_pane(self):
        hunger_percentage = self.hunger_limit / MAX_HUNGER_LIMIT

        pyxel.rectb(0, 0, pyxel.width, 10, col=1)
        pyxel.text(PANE_PADDING, PANE_PADDING, f"Score: {self.game.score}", 1)
        pyxel.text(pyxel.width // 2 + PANE_PADDING, PANE_PADDING, "Satiety:{:>3}%".format(int(hunger_percentage * 100)), 1)

    def draw(self):
        super(PlaygroundScene, self).draw()
        pyxel.cls(0)
        self.draw_foods()
        self.draw_snake()
        self.draw_walls()
        self.draw_pane()
        if self.hunger_limit == 0:
            self.draw_game_over()

    def update(self):
        now = time.time()
        if now - self.last_tick > TICK_PERIOD:
            self.last_tick = now
            self.tick()

    def handle_key(self):
        if pyxel.btnp(key=pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            if self.snake_parts[0].direction != Direction.DOWN:
                self.turns.append(Direction.UP)
        elif pyxel.btnp(key=pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            if self.snake_parts[0].direction != Direction.UP:
                self.turns.append(Direction.DOWN)
        elif pyxel.btnp(key=pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            if self.snake_parts[0].direction != Direction.RIGHT:
                self.turns.append(Direction.LEFT)
        elif pyxel.btnp(key=pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            if self.snake_parts[0].direction != Direction.LEFT:
                self.turns.append(Direction.RIGHT)

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

        next_x, next_y, next_direction = self._get_next_head_grid(head.x, head.y, next_direction)
        new_part = SnakePart(next_x, next_y, next_direction)
        new_part.is_eating = False

        # Check if there is a food on the way
        for food in self.foods:
            if food.x == new_part.x and food.y == new_part.y:
                new_part.is_eating = True
                break

        if new_part.is_eating:
            self.put_random_food()
            self.foods.remove(food)
            self.game.score += 1
            self.hunger_limit = min(self.hunger_limit + self.food_satiety_amount, MAX_HUNGER_LIMIT)
            self._tail_debt += self.food_tail_amount
            pyxel.play(0, 0)

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
        if self._tail_debt == 0:
            self.snake_parts.pop()
            self.hunger_limit = max(0, self.hunger_limit - 1)
        else:
            self._tail_debt -= 1
