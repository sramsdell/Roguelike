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
        self._pos = [self._x * self.scale, self._y * self.scale]
        self._type = "none"
        self._obstacle = False

    def get_coordinates(self):
        if self._obstacle:
            return [self._x * self.scale, self._y * self.scale]
        else:
            pass

    def get_type(self):
        return self._type

    def get_pos(self):
        return self._pos


class Floor(Tile):
    def __init__(self, pos, scale):
        Tile.__init__(self, pos, scale)

    def render(self, screen, camera, grid):
            pygame.draw.rect(screen, BLUE,
                             [[(self._x * self.scale) + camera.get_x(),
                               (self._y * self.scale) + camera.get_y()],
                              [self.scale, self.scale]])

    def sub_render(self, screen, camera, grid):
            pygame.draw.rect(screen, BLUE,
                             [[(self._x * self.scale) + camera.get_x(),
                               (self._y * self.scale) + camera.get_y()],
                              [self.scale, self.scale]])


class Fog(Tile):
    def __init__(self, pos, scale):
        Tile.__init__(self, pos, scale)
        self.ren = pygame.Surface((self.scale, self.scale))
        self.ren.set_alpha(128)
        self.ren.fill(BLACK)
        self.ren.convert_alpha()

    def render(self, screen, camera):
        screen.blit(self.ren,[(self._x * self.scale) + camera.get_x(),
                           (self._y * self.scale) + camera.get_y()])


class Wall(Tile):
    def __init__(self, pos, scale):
        Tile.__init__(self, pos, scale)
        self._obstacle = True

    def render(self, screen, camera, grid):
        pygame.draw.rect(screen, BLACK,
                         [[(self._x * self.scale) + camera.get_x(),
                           (self._y * self.scale) + camera.get_y()],
                          [self.scale, self.scale]])


class Door(Floor):
    def __init__(self, pos, scale):
        Tile.__init__(self, pos, scale)
        self._type = "Door"

    def render(self, screen, camera, grid):
        fog_lis = []
        for fog in grid.get_fog_set():
            fog_lis.append(fog.get_pos())

        if self._pos not in fog_lis:
            pygame.draw.rect(screen, PINK,
                             [[(self._x * self.scale) + camera.get_x(),
                               (self._y * self.scale) + camera.get_y()],
                              [self.scale, self.scale]])
        else:
            self.sub_render(screen, camera, grid)


class Door_up(Tile):
    def __init__(self, pos, scale):
        Tile.__init__(self, pos, scale)
        self._type = "Door_up"

    def render(self, screen, camera, grid):
        pygame.draw.rect(screen, YELLOW,
                         [[(self._x * self.scale) + camera.get_x(),
                           (self._y * self.scale) + camera.get_y()],
                          [self.scale, self.scale]])
