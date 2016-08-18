import sys
sys.dont_write_bytecode = True
import pygame
import random
import copy
from helper import *
from hero import *
from mob import *
from tile import *
from item import *
from colors import *
from image import *


def render(self, screen, game):
    SIZE = game.get_size()
    scale = game.get_scale()
    trans_scale = [scale, scale]
    screen.fill(RED)
    for hero in game.get_hero_set():

        for i, item in enumerate(hero.get_held_item()):

            screen.blit(item.get_image(), [(scale // 2), (scale // 2) + (scale * i)])
    
