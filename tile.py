import sys
sys.dont_write_bytecode = True
import pygame
import random
from helper import *
from colors import *

class Tile:

    def __init__(self, pos, scale):
        self._x = pos[0]
        self._y = pos[1]
        self.scale = scale
        self._type = "none"
##    def get_coordinates(self):
##        return [self._x * self.scale, self._y * self.scale]
    def get_type(self):
        return self._type

    def get_pos(self):
        return [self._x * self.scale, self._y * self.scale]


class Wall(Tile):
    def __init__(self, pos, scale):
        Tile.__init__(self, pos, scale)

    def render(self, screen, camera):
        pygame.draw.rect(screen, BLACK,
                         [[(self._x * self.scale) + camera.get_x(),
                           (self._y * self.scale) + camera.get_y()],
                          [self.scale, self.scale]])

    def get_coordinates(self):
        return [self._x * self.scale, self._y * self.scale]


class Door(Tile):
    def __init__(self, pos, scale):
        Tile.__init__(self, pos, scale)
        self._type = "Door"

    def render(self, screen, camera):
        pygame.draw.rect(screen, PINK,
                         [[(self._x * self.scale) + camera.get_x(),
                           (self._y * self.scale) + camera.get_y()],
                          [self.scale, self.scale]])

    def get_coordinates(self):
        pass


class Door_up(Tile):
    def __init__(self, pos, scale):
        Tile.__init__(self, pos, scale)
        self._type = "Door_up"

    def render(self, screen, camera):
        pygame.draw.rect(screen, YELLOW,
                         [[(self._x * self.scale) + camera.get_x(),
                           (self._y * self.scale) + camera.get_y()],
                          [self.scale, self.scale]])

    def get_coordinates(self):
        pass


class Floor(Tile):
    def __init__(self, pos, scale):
        Tile.__init__(self, pos, scale)

    def render(self, screen, camera):
        pygame.draw.rect(screen, BLUE,
                         [[(self._x * self.scale) + camera.get_x(),
                           (self._y * self.scale) + camera.get_y()],
                          [self.scale, self.scale]])

    def get_coordinates(self):
        pass
