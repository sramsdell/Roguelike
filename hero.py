import sys
sys.dont_write_bytecode = True
import pygame
import random
from helper import *
from colors import *
from item import *


class Attack:
    def __init__(self, pos, game):
        self.scale = game.get_scale()
        self.pos = pos
        self.lifespan = 10
        self.attack_power = 10

    def render(self, screen, camera):
        self.lifespan -= 1
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

    def get_attack_power(self):
        return self.attack_power

    def attack(self):
        if self.attack_power == 0:
            return 0
        else:
            temp = self.attack_power
            self.attack_power = 0
            return temp


class Hero:
    def __init__(self, pos, game, bot=False):
        self.pos = pos
        self.scale = game.get_scale()
        self.screen_size = game.get_size()
        self.bot = bot
        self.color = RED
        self.held_item = [Orange_Potion((0,0),game),
                          Blue_Potion((0,0),game),
                          Yellow_Potion((0,0),game)]
        self.value = "H"
        self.orientation = "s"
        self.max_hp = 1000
        self.hp = self.max_hp
        self.sight = 3
        partial = int(.75 * self.scale)
        self.orientations = {"s" : [0, partial, 0, -partial],
                             "e" : [partial, 0, -partial, 0],
                             "n" : [0, 0, 0, -self.scale + (self.scale - partial)],
                             "w" : [0, 0, -self.scale + (self.scale - partial), 0]}
        #menu
        self.font2 = pygame.font.SysFont("fixedsys",self.scale)
        self.menu = pygame.Surface((self.scale * 5.5, self.scale * 2))
        self.menu.set_alpha(64)
        self.menu.fill(BLUE)
        self.menu1 = self.font2.render("HP: " + str(self.max_hp) + " / " + str(self.hp),
                                       1,(255,255,255))
        self.menu2 = self.font2.render("MP: " + str("0000") + " / " + str("0000"),
                                       1,(255,255,255))

    def get_sight(self):
        return self.sight

    def get_hp(self):
        return self.hp

    def sub_hp(self, val):
        self.hp -= val

    def add_hp(self, val):
        self.hp += val

    def attack(self, game):
        attack_orientations = {"s" : [self.pos[0], self.pos[1] + self.scale],
                               "e" : [self.pos[0] + self.scale, self.pos[1]],
                               "n" : [self.pos[0], self.pos[1] - self.scale],
                               "w" : [self.pos[0] - self.scale, self.pos[1]]}
        for i in attack_orientations:
            if self.orientation == i:
                attack = Attack(attack_orientations[i], game)
                game.add_attack_to_set(attack)

    def map_update(self, grid, value="."):
        grid.map_update([self.pos[1] / self.scale, self.pos[0] / self.scale],
                        value)

    def fog_update(self, grid):
        grid.fog_update([self.pos[1] / self.scale, self.pos[0] / self.scale])

    def get_value(self):
        return self.value

    def get_held_item(self):
	return self.held_item

    def add_held_item(self, item):
    	self.held_item.append(item)

    def del_held_item(self, item):
        self.held_item.discard(item)

    def get_scale(self):
        return self.scale

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
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        self.menu1 = self.font2.render("HP: " + str(self.max_hp) + " / " + str(self.hp),
                                       1,(255,255,255))

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

        # menu
        screen.blit(self.menu1,(self.scale,
                                self.scale))
        screen.blit(self.menu2,(self.scale,
                                self.scale * 1.75))
        screen.blit(self.menu, (self.scale * .75, self.scale * .75))

    def move(self, key, grid, game):

        no_move = []
        for tile in grid.get_tile_set():
            no_move += [tile.get_coordinates()]
        for mob in grid.get_mob_set():
            no_move += [mob.get_pos()]

        if not self.bot:
            if key == pygame.K_m:
                for i in self.held_item:
                    pass
                print "asdf"
                mob_turn(self, grid)
                
            if key == pygame.K_SPACE:
                self.attack(game)
                mob_turn(self, grid)

            if key == pygame.K_UP:
                self.orientation = "n"
                mob_turn(self, grid)
                if [self.pos[0], self.pos[1] - self.scale] not in no_move:
                    self.map_update(grid)
                    self.pos[1] -= self.scale
                    game.alt_hero_ref([0,0])

            if key == pygame.K_DOWN:
                self.orientation = "s"
                mob_turn(self, grid)
                if [self.pos[0], self.pos[1] + self.scale] not in no_move:
                    self.map_update(grid)
                    self.pos[1] += self.scale
                    game.alt_hero_ref([0,0])

            if key == pygame.K_LEFT:
                self.orientation = "w"
                mob_turn(self, grid)
                if [self.pos[0] - self.scale, self.pos[1]] not in no_move:
                    self.map_update(grid)
                    self.pos[0] -= self.scale
                    game.alt_hero_ref([0,0])

            if key == pygame.K_RIGHT:
                self.orientation = "e"
                mob_turn(self, grid)
                if [self.pos[0] + self.scale, self.pos[1]] not in no_move:
                    self.map_update(grid)
                    self.pos[0] += self.scale
                    game.alt_hero_ref([0,0])
