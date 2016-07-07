import sys
sys.dont_write_bytecode = True
import pygame
import random
from helper import *
from colors import *

class Game:

    def __init__(self, size, scale=50):
        self.turn = 0
        self.hero_set = set()
        self.camera_set = set()
        self.scale = scale
        self.size = size
        self._level = 1

    def get_level(self):
        return self._level

    def add_level(self):
        self._level += 1

    def sub_level(self):
        self._level += -1

    def get_turn(self):
        return self.turn

    def add_turn(self, num):
        self.turn += num

    def sub_turn(self, num):
        self.turn -= num

    def get_hero_set(self):
        return self.hero_set

    def add_hero_to_set(self, hero):
        self.hero_set.add(hero)

    def del_hero_from_set(self, hero):
        self.hero_set.discard(hero)

    def get_camera_set(self):
        return self.camera_set

    def add_camera_to_set(self, camera):
        self.camera_set.add(camera)

    def del_camera_from_set(self, camera):
        self.camera_set.discard(camera)

    def get_scale(self):
        return self.scale

    def get_size(self):
        return self.size

class Camera:

    def __init__(self, game, hero):
        self.size = game.get_size()
        self.hero = hero
        self.scale = game.get_scale()
        self._x = 0
        self._y = 0
        self.inner_box = self.scale * 4

    def in_view(self):

        if self.hero.get_pos()[0] + self._x > self.size[0] - self.inner_box:
            self._x -= self.scale
        if self.hero.get_pos()[0] + self._x < self.inner_box - self.scale:
            self._x += self.scale
        if self.hero.get_pos()[1] + self._y > self.size[1] - self.inner_box:
            self._y -= self.scale
        if self.hero.get_pos()[1] + self._y < self.inner_box - self.scale:
            self._y += self.scale

    def spawn(self, pos):
        self._x = pos[1]
        self._y = pos[0]

    def get_y(self):
        return self._y

    def get_x(self):
        return self._x
