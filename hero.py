import sys
sys.dont_write_bytecode = True
import pygame
import random
from helper import *
from colors import *

class Attack:
    def __init__(self, pos, game):
        self.scale = game.get_scale()
        self.pos = pos
        self.lifespan = 50

    def render(self, screen, camera):
        pygame.draw.rect(screen, RED,
                         [[self.pos[0] + camera.get_x(),
                           self.pos[1] + camera.get_y()],
                          [self.scale, self.scale]])

    def get_pos(self):
        return self.pos

    def get_lifespan(self):
        return self.lifespan

    def sub_lifespan(self):
        self.lifespan -= 1


class Hero:
    def __init__(self, pos, game, bot=False):
        self.pos = pos
        self.scale = game.get_scale()
        self.bot = bot
        self.color = RED
        self.held_item_set = set()
        self.value = "H"
        self.orientation = "s"

        partial = int(.75 * self.scale)
        self.orientations = {"s" : [0, partial, 0, -partial],
                             "e" : [partial, 0, -partial, 0],
                             "n" : [0, 0, 0, -self.scale + (self.scale - partial)],
                             "w" : [0, 0, -self.scale + (self.scale - partial), 0]}

        self.attack_orientations = {"s" : [self.pos[0], self.pos[1] + self.scale],
                                    "e" : [self.pos[0], self.pos[1]],
                                    "n" : [self.pos[0], self.pos[1] - self.scale],
                                    "w" : [self.pos[0], self.pos[1]]}

    def attack(self):
        pass

    def map_update(self, grid, value="."):
        grid.map_update([self.pos[1] / self.scale, self.pos[0] / self.scale],
                        value)

    def get_value(self):
        return self.value

	def get_held_item_set(self):
		return self.held_item_set

    def add_held_item_to_set(self, item):
		self.held_item_set.add(item)

    def del_held_item_from_set(self, item):
        self.held_item_set.discard(item)

    def get_pos(self):
        return self.pos

    def alt_pos(self, lis):
        self.pos[0] += lis[0]
        self.pos[1] += lis[1]

    def tele_pos(self, lis):
        self.pos[0] = lis[0]
        self.pos[1] = lis[1]

    def is_bot(self):
        return self.bot

    def update(self, grid):
        pass

    def render(self, screen, camera):
        pygame.draw.rect(screen, self.color,
                         [[self.pos[0] + camera.get_x(),
                           self.pos[1] + camera.get_y()],
                          [self.scale, self.scale]])

        self.orientations[self.orientation]

        for i in self.orientations:
            
            if i == self.orientation:
                pygame.draw.rect(screen, BLACK,
                             [[self.pos[0] + camera.get_x() + self.orientations[i][0],
                               self.pos[1] + camera.get_y() + self.orientations[i][1]],
                              [self.scale + self.orientations[i][2],
                               self.scale + self.orientations[i][3]]])

    def move(self, key, grid, game):
        for mob in grid.get_mob_set():
            if distance(mob.get_pos(), self.pos) / game.get_scale() < mob.get_sight():
                mob.add_turn(1)


        no_move = []
        for tile in grid.get_tile_set():
            no_move += [tile.get_coordinates()]

        if not self.bot:
            if key == pygame.K_SPACE:
                for i in self.held_item_set:
                    print "test"
                hero_teleport(grid, game)

            if key == pygame.K_UP:
                if [self.pos[0], self.pos[1] - self.scale] not in no_move:
                    self.map_update(grid)
                    self.orientation = "n"
                    self.pos[1] -= self.scale

            if key == pygame.K_DOWN:
                if [self.pos[0], self.pos[1] + self.scale] not in no_move:
                    self.map_update(grid)
                    self.orientation = "s"
                    self.pos[1] += self.scale

            if key == pygame.K_LEFT:
                if [self.pos[0] - self.scale, self.pos[1]] not in no_move:
                    self.map_update(grid)
                    self.orientation = "w"
                    self.pos[0] -= self.scale

            if key == pygame.K_RIGHT:
                if [self.pos[0] + self.scale, self.pos[1]] not in no_move:
                    self.map_update(grid)
                    self.orientation = "e"
                    self.pos[0] += self.scale
