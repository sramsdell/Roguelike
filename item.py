import sys
sys.dont_write_bytecode = True
import pygame
import random
from helper import *
from colors import *
from image import *

class Item:

	def __init__(self, pos, game):
            self._pos = pos
            self._scale = game.get_scale()
            self._type = None
            self._image = None

	def update(self):
            pass

	def render(self, screen, camera):
	    pygame.draw.rect(screen, YELLOW,
                             [[self._pos[0] + camera.get_x(),
                               self._pos[1] + camera.get_y()],
                              [self._scale, self._scale]])

        def get_type(self):
            return self._type

        def get_image(self):
            return self._image

	def get_pos(self):
	    return self._pos

	def __str__(self):
            return self._type


class Blue_Potion(Item):
        def __init__(self, pos, game):
                Item.__init__(self, pos, game)
                self._type = "blue_potion"
                self._image = pygame.transform.scale(blue_potion_image,[self._scale, self._scale])
                self._image.convert_alpha()

        def render(self, screen, camera, grid):
            fog_lis = []
            for fog in grid.get_fog_set():
                fog_lis.append(fog.get_pos())
            if self._pos not in fog_lis:
                pos_camera = [self._pos[0] + camera.get_x(),
                self._pos[1] + camera.get_y()]

                screen.blit(self._image,pos_camera)

        def effect(self, hero):
            hero.add_hp(20)
            #hero.add_held_item_to_set(item)


class Yellow_Potion(Item):
        def __init__(self, pos, game):
                Item.__init__(self, pos, game)
                self._type = "yellow_potion"
                self._image = pygame.transform.scale(yellow_potion_image,[self._scale, self._scale])
                self._image.convert_alpha()

        def render(self, screen, camera, grid):
            fog_lis = []
            for fog in grid.get_fog_set():
                fog_lis.append(fog.get_pos())
            if self._pos not in fog_lis:
                pos_camera = [self._pos[0] + camera.get_x(),
                self._pos[1] + camera.get_y()]

                screen.blit(self._image,pos_camera)

        def effect(self, hero):
            hero.add_hp(20)
            #hero.add_held_item_to_set(item)


class Orange_Potion(Item):
        def __init__(self, pos, game):
                Item.__init__(self, pos, game)
                self._type = "orange_potion"
                self._image = pygame.transform.scale(orange_potion_image,[self._scale, self._scale])
                self._image.convert_alpha()

        def render(self, screen, camera, grid):
            fog_lis = []
            for fog in grid.get_fog_set():
                fog_lis.append(fog.get_pos())
            if self._pos not in fog_lis:
                pos_camera = [self._pos[0] + camera.get_x(),
                self._pos[1] + camera.get_y()]

                screen.blit(self._image,pos_camera)

        def effect(self, hero):
            hero.add_hp(20)
            #hero.add_held_item_to_set(item)
