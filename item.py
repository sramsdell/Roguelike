import sys
sys.dont_write_bytecode = True
import pygame
import random
from helper import *
from colors import *

class Item:

	def __init__(self, pos, game):
            self._pos = pos
            self._scale = game.get_scale()
            self.type = random.choice(["apple", "banana", "cheese"])
	def update(self):
            pass

	def render(self, screen, camera):
	    pygame.draw.rect(screen, YELLOW,
                             [[self._pos[0] + camera.get_x(),
                               self._pos[1] + camera.get_y()],
                              [self._scale, self._scale]])

	def get_pos(self):
		return self._pos

	def __str__(self):
            return self.type


