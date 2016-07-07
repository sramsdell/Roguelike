import sys
sys.dont_write_bytecode = True
import pygame
import math
import random

def spawn_pos(grid, game):
    lis = []
    for i, v in enumerate(grid.get_map()):
        for j, w in enumerate(v):

            if grid.get_map()[j][i] == ".":
                    lis += [[i * game.get_scale(), j * game.get_scale()]]
    pos = random.choice(lis)
    return pos


def distance(x, y):
    """ takes lists """
    return math.sqrt(((x[0] - y[0])**2) + ((x[1] - y[1])**2))