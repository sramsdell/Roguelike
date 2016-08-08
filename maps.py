import sys
sys.dont_write_bytecode = True
import pygame
import random
from rogue import *
from map_generator import generate_map
from helper import *
from mob import *

class Map:

    def __init__(self, grid, game, n, m, door_up=True, num_mobs=5, no_fog=False, items_on=True):
        self.no_fog = no_fog
        self.door_up = door_up
        self.n = n
        self.m = m
        self.tile_set = set()
        self.mob_set = set()
        self.fog_set = set()
        self.scale = game.get_scale()
        self.screen_size = game.get_size()
        self.view = list(self.screen_size)
        self.init_mobs = num_mobs
        self.grid = grid
        self.items_on = items_on
        self.item_set = set()
        self.init()

    def init(self):
        mapp = [[None for col in range(self.n)] for row in range(self.m)]
        for i, v in enumerate(mapp):
            for j, w in enumerate(v):
                mapp[i][j] = self.grid[i][j]
        self.map = mapp

        if not self.no_fog:
            self.fog = [[0 for col in range(self.n)] for row in range(self.m)]
            for i, v in enumerate(self.fog):
                for j, w in enumerate(v):
                    if self.map[i][j] == "x" or self.map[i][j] == " ":
                        self.fog[i][j] = 1
        else:
            self.fog = [[1 for col in range(self.n)] for row in range(self.m)]

        pos = spawn_pos(self, game)
        self.map[pos[1] / self.scale][pos[0] / self.scale] = "d"
        if self.door_up:
            pos = spawn_pos(self, game)
            self.map[pos[1] / self.scale][pos[0] / self.scale] = "D"

        ##init mob spawn
        for i in range(int(self.init_mobs)):
            pos = spawn_pos(self, game)
            mob = Mob(pos, game)
            self.mob_set.add(mob)

        if self.items_on:
            for i in range(random.randrange(1, 4)):
                pos = spawn_pos(self, game)
                item = Blue_Potion(pos, game)
                self.item_set.add(item)
    
    def get_fog_set(self):
        return self.fog_set

    def add_fog_to_set(self, fog_tile):
        self.fog_set.add(fog_tile)

    def del_fog_from_set(self, fog_tile):
        self.fog_set.discard(fog_tile)

    def alt_fog_grid(self, pos, alt):
        self.fog[pos[1]][pos[0]] = alt

    def get_fog_grid(self):
        return self.fog

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

##    def update(self):
##        pass
##
##    def render(self, screen):
##        pygame.draw.rect(screen, BLACK,
##                         [[self._x * self.scale, self._y * self.scale],
##                          [self.scale, self.scale]])

    def get_map(self):
        return self.map

    def change_map(self, grid):
        self.map = grid

    def fog_update(self, coordinate):

        for i, v in enumerate(self.fog):
            for j, w in enumerate(v):

                if coordinate == [i, j]:
                    self.fog[i][j] = 1
                

    def map_update(self, coordinate, value):
        lis = [[None for col in range(self.n)] for row in range(self.m)]
        for i, v in enumerate(self.map):
            for j, w in enumerate(v):

                if coordinate == [i, j]:
                    lis[i][j] = value
                else:
                    lis[i][j] = w
        self.map = lis

    def map_reset(self):
        self.tile_set = set()
        self.mob_set = set()
        self.fog_set = set()
        self.item_set = set()
        self.init()

##
##grid = Map(["xxxxxxxxxxxx",
##            "xxxxxxxxxxxx",
##            "xx........xx",
##            "xx........xx",
##            "xx........xx",
##            "xx........xx",
##            "xx........xx",
##            "xx........xx",
##            "xx........xx",
##            "xx........xx",
##            "xxxxxxxxxxxx",
##            "xxxxxxxxxxxx"], game, 12, 12, door_up=False, num_mobs=1, no_fog=True)
##

class Grids:

    def __init__(self, game):
        grid_post = [Map(generate_map(30, 30), game, 30, 30, False) for i in range(10)]
        grid = Map(["xxxxxxxxxxxx",
            "xxxxxxxxxxxx",
            "xx........xx",
            "xx........xx",
            "xx........xx",
            "xx........xx",
            "xx........xx",
            "xx........xx",
            "xx........xx",
            "xx........xx",
            "xxxxxxxxxxxx",
            "xxxxxxxxxxxx"], game, 12, 12, door_up=False, num_mobs=1, no_fog=True, items_on=False)
        grid_pre = ["maybe a warp?", grid]
        grids = grid_pre + grid_post
        self.grids = grids

    def reset(self):
        grid_post = [Map(generate_map(30, 30), game, 30, 30, False) for i in range(10)]
        grid = Map(["xxxxxxxxxxxx",
            "xxxxxxxxxxxx",
            "xx........xx",
            "xx........xx",
            "xx........xx",
            "xx........xx",
            "xx........xx",
            "xx........xx",
            "xx........xx",
            "xx........xx",
            "xxxxxxxxxxxx",
            "xxxxxxxxxxxx"], game, 12, 12, door_up=False, num_mobs=1, no_fog=True, items_on=False)
        grid_pre = ["maybe a warp?", grid]
        grids = grid_pre + grid_post
        self.grids = grids

    def get_grids(self):
        return self.grids

game_grids = Grids(game)

def change_level(game):
    level = game.get_level()
    return game_grids.get_grids()[level]
