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

def mob_turn(hero, grid):
#def hero_action_helper(static, no_move, hero, grid):
    for mob in grid.get_mob_set():
        if distance(mob.get_pos(), hero.get_pos()) / hero.get_scale() < mob.get_sight():
            mob.add_turn(1)

##    hero.map_update(grid)
##    return ([hero.get_pos()[0], hero.get_pos()[1] - hero.get_scale()] not in no_move)

def distance(x, y):
    """ takes lists """
    return math.sqrt(((x[0] - y[0])**2) + ((x[1] - y[1])**2))
