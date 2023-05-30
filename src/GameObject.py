import pygame
from random import randint
import os

global dirname
dirname = os.path.dirname(__file__)


class GameObject:
    def __init__(self, name: str, screen_width: int, screen_height: int) -> None:
        self.image = pygame.image.load(os.path.join(dirname, "img/" + name + ".png"))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.max_x = screen_width - self.width
        self.max_y = screen_height - self.height
        self.x = randint(0, self.max_x)
        self.y = randint(0, self.max_y)
        self.center_x = self.x + (self.width / 2)
        self.center_y = self.y + (self.height / 2)


class Coin(GameObject):
    def __init__(self, screen_width: int, screen_height: int) -> None:
        super().__init__("kolikko", screen_width, screen_height)

    def random_coin_placement(self):
        self.x = randint(0, self.max_x)
        self.y = randint(0, self.max_y)
        self.center_x = self.x + (self.width / 2)
        self.center_y = self.y + (self.height / 2)


class Robot(GameObject):
    def __init__(self, screen_width: int, screen_height: int) -> None:
        super().__init__("robo", screen_width, screen_height)
        self.move_up = False
        self.move_down = False
        self.move_right = False
        self.move_left = False

    def set_direction(self, direction: str, move: bool):
        if direction == "right":
            self.move_right = move
        if direction == "left":
            self.move_left = move
        if direction == "up":
            self.move_up = move
        if direction == "down":
            self.move_down = move

    def robot_movement(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.set_direction("left", True)
            if event.key == pygame.K_RIGHT:
                self.set_direction("right", True)
            if event.key == pygame.K_UP:
                self.set_direction("up", True)
            if event.key == pygame.K_DOWN:
                self.set_direction("down", True)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.set_direction("up", False)
            if event.key == pygame.K_DOWN:
                self.set_direction("down", False)
            if event.key == pygame.K_RIGHT:
                self.set_direction("right", False)
            if event.key == pygame.K_LEFT:
                self.set_direction("left", False)

    def move_robot(self):
        if self.move_left and self.x > 0:
            self.x -= 3
        if self.move_right and self.x < self.max_x:
            self.x += 3
        if self.move_up and self.y > 0:
            self.y -= 3
        if self.move_down and self.y < self.max_y:
            self.y += 3

        self.center_x = self.x + (self.width / 2)
        self.center_y = self.y + (self.height / 2)


class Monster(GameObject):
    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        follow_robot: bool,
        horizontal: bool,
        vertical: bool,
    ) -> None:
        super().__init__("hirvio", screen_width, screen_height)
        self.follow_robot = follow_robot
        self.horizontal = horizontal
        self.vertical = vertical
        self.x_speed = 1 if self.horizontal else 0
        self.y_speed = 1 if self.vertical else 0

    def monster_movement(self, robot: Robot):
        if self.follow_robot:
            if self.x > robot.x:
                self.x_speed = -1
            if self.x < robot.x:
                self.x_speed = 1
            if self.x == robot.x:
                self.x_speed = 0
            if self.y > robot.y:
                self.y_speed = -1
            if self.y < robot.y:
                self.y_speed = 1
            if self.y == robot.y:
                self.y_speed = 0
        if self.horizontal:
            if self.x == 0:
                self.x_speed = 1
            if self.x == self.max_x:
                self.x_speed = -1
        if self.vertical:
            if self.y == 0:
                self.y_speed = 1
            if self.y == self.max_y:
                self.y_speed = -1

    def move_monster(self, robot: Robot):
        self.monster_movement(robot)
        self.x += self.x_speed
        self.y += self.y_speed

        self.center_x = self.x + (self.width / 2)
        self.center_y = self.y + (self.height / 2)

    def new_spot(self, robot_x, robot_y):
        while True:
            self.x = randint(0, self.max_x)
            self.y = randint(0, self.max_y)
            if abs(self.x - robot_x) > 40 and abs(self.y - robot_y) > 100:
                break

        self.center_x = self.x + (self.width / 2)
        self.center_y = self.y + (self.height / 2)
