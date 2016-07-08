import sys
sys.dont_write_bytecode = True
import pygame
from rogue import game
from map_generator import generate_map
from helper import *

class Map:

    def __init__(self, grid, game, n=10, m=10, door_up = True):
        self.door_up = door_up
        self.n = n
        self.m = m
        self.tile_set = set()
        self.mob_set = set()
        self.scale = game.get_scale()
        self.screen_size = game.get_size()
        self.view = list(self.screen_size)
        self.a = 0
        self.b = 0
        self.item_set = set()
        mapp = [[None for col in range(self.n)] for row in range(self.m)]
        for i, v in enumerate(mapp):
            for j, w in enumerate(v):
                mapp[i][j] = grid[i][j]
        self.map = mapp

        pos = spawn_pos(self, game)
        self.map[pos[1] / self.scale][pos[0] / self.scale] = "d"
        if self.door_up:
            pos = spawn_pos(self, game)
            self.map[pos[1] / self.scale][pos[0] / self.scale] = "D"
##        for i in self.map:
##            print " ".join(i)

    def get_item_set(self):
        return self.item_set

    def add_item_to_set(self, item):
        self.item_set.add(item)

    def del_item_from_set(self, item):
        self.item_set.discard(item)

    def get_mob_set(self):
        return self.mob_set

    def add_mob_to_set(self, mob):
        self.mob_set.add(mob)

    def del_mob_from_set(self, mob):
        self.mob_set.discard(mob)

    def get_tile_set(self):
        return self.tile_set

    def add_tile_to_set(self, tile):
        self.tile_set.add(tile)

    def del_tile_from_set(self, tile):
        self.tile_set.discard(tile)

    def update(self):
        pass

    def render(self, screen):
        pygame.draw.rect(screen, BLACK,
                         [[self._x * self.scale, self._y * self.scale],
                          [self.scale, self.scale]])

    def get_map(self):
        return self.map

    def change_map(self, grid):
        self.map = grid

    def map_update(self, coordinate, value):
        lis = [[None for col in range(self.n)] for row in range(self.m)]
        for i, v in enumerate(self.map):
            for j, w in enumerate(v):

                if coordinate == [i, j]:
                    lis[i][j] = value
                else:
                    lis[i][j] = w
        self.map = lis



grid = Map(["xxxxxxxxxx",
            "x........x",
            "x........x",
            "x........x",
            "x........x",
            "x........x",
            "x........x",
            "x........x",
            "x........x",
            "xxxxxxxxxx"], game, door_up=False)

grid_post = [Map(generate_map(30, 30), game, 30, 30, False) for i in range(10)]
grid_pre = ["maybe a warp?", grid]
grids = grid_pre + grid_post


def change_level(game):
    level = game.get_level()
    return grids[level]
