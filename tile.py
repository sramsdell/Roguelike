import sys
sys.dont_write_bytecode = True
import pygame
import random
from helper import *
from colors import *
from image import *

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
        self._scale = scale

        num = random.randrange(1,16)
        if num <= 5:
            self._image = floor_1
        elif num >= 6 and num <= 10:
            self._image = floor_2
        else:
            self._image = floor_3
        self._image = pygame.transform.scale(self._image,[self._scale, self._scale])
        self._image.convert_alpha()


    def render(self, screen, camera, grid):
        pos_camera = [self._pos[0] + camera.get_x(),
        self._pos[1] + camera.get_y()]

        screen.blit(self._image, pos_camera)
##            pygame.draw.rect(screen, GREY,
##                             [[(self._x * self.scale) + camera.get_x(),
##                               (self._y * self.scale) + camera.get_y()],
##                              [self.scale, self.scale]])

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
        self._scale = scale
        self._obstacle = True
        self.num = random.randrange(1,13)

        if self.num <= 5:
            self._image = brick_0
        elif self.num == 6:
            self._image = brick_2
##        elif self.num == 7:
##            self._image = brick_3
        else:
            self._image = brick_1
        self._image = pygame.transform.scale(self._image,[self._scale, self._scale])
        self._image.convert_alpha()

    def render(self, screen, camera, grid):
        pos_camera = [self._pos[0] + camera.get_x(),
                self._pos[1] + camera.get_y()]

        screen.blit(self._image, pos_camera)
##        pygame.draw.rect(screen, BLACK,
##                         [[(self._x * self.scale) + camera.get_x(),
##                           (self._y * self.scale) + camera.get_y()],
##                          [self.scale, self.scale]])
        


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
