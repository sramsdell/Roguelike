import sys
sys.dont_write_bytecode = True
import pygame
import random
from helper import *
from colors import *
from hero import Attack
from image import *

class Mob:

    def __init__(self, pos, game):
        self.pos = pos[:]
        self.scale = game.get_scale()
        self.move_lis = ["."]
        self.value = "m"
        self.sight = 6
        self.turn = 0
        self.hp_max = 25
        self.hp = self.hp_max
        self.speed = 0
        self.age = 0

    def sub_hp(self, val):
        self.hp -= val

    def get_hp(self):
        return self.hp

    def get_value(self):
        return self.value

    def dead(self, grid, value):
        self.map_update(grid, value)

    def add_turn(self, num):
        self.turn += num + self.speed

    def get_sight(self):
        return self.sight

    def get_pos(self):
        return self.pos

    def alt_pos(self, lis):
        self.pos[0] += lis[0]
        self.pos[1] += lis[1]

    def update(self):
        pass

    def health_render(self, screen, camera, grid):

        pygame.draw.rect(screen, RED,
                         [[self.pos[0] + camera.get_x() - 5,
                           self.pos[1] + camera.get_y() - 5],
                          [self.scale, 3]])

        pygame.draw.rect(screen, GREEN,
                         [[self.pos[0] + camera.get_x() - 5,
                           self.pos[1] + camera.get_y() - 5],
                          [(self.hp * self.scale) // self.hp_max, 3]])

    def render(self, screen, camera, grid):
        fog_lis = []
        for fog in grid.get_fog_set():
            fog_lis.append(fog.get_pos())
        
        if self.pos not in fog_lis:

            self.health_render(screen, camera, grid)
            
            pygame.draw.rect(screen, RED,
                             [[self.pos[0] + camera.get_x(),
                               self.pos[1] + camera.get_y()],
                              [self.scale, self.scale]])
##            self.age += 0.05
##            current_index = int((self.age % 4) // 1)
##
##        ##rec= left,top,width,height
##            self._image = pygame.transform.scale(spider_1, (self.scale, self.scale * 4))
##            self._image.convert_alpha()
##                                                 
##            scroll = [0, self.scale * current_index, self.scale, self.scale]
##            screen.blit(self._image,
##                        [self.pos[0] + camera.get_x(),
##                         self.pos[1] + camera.get_y()],
##                        area=scroll)
            


    def map_update(self, grid, value):
        grid.map_update([self.pos[1] / self.scale, self.pos[0] / self.scale],
                        value)

    def pre_move(self):
        pos = self.pos[:]

        pre_up = [pos[0], pos[1] - self.scale]
        pre_down = [pos[0], pos[1] + self.scale]
        pre_left = [pos[0] - self.scale, pos[1]]
        pre_right = [pos[0] + self.scale, pos[1]]

        return [pre_up, pre_down, pre_left, pre_right]
        
    def no_move(self, grid, game):
        no_move = []
        for tile in grid.get_tile_set():
            no_move += [tile.get_coordinates()]

        for hero in game.get_hero_set():
            no_move += [hero.get_pos()]

        for mob in grid.get_mob_set():
            no_move += [mob.get_pos()]
        return no_move

    def goals(self, game):
        goals = []
        for hero in game.get_hero_set():
            goals += [[hero.get_pos()[0], hero.get_pos()[1] - self.scale],
                      [hero.get_pos()[0] - self.scale,hero.get_pos()[1]],
                      [hero.get_pos()[0] + self.scale,hero.get_pos()[1]],
                      [hero.get_pos()[0], hero.get_pos()[1] + self.scale]
                      ]
        return goals

    def closest_move(self, grid, game):
        goals = self.goals(game)
        no_move = self.no_move(grid, game)
        pos = self.pos[:]

##        pre_up = [pos[0], pos[1] - self.scale]
##        pre_down = [pos[0], pos[1] + self.scale]
##        pre_left = [pos[0] - self.scale, pos[1]]
##        pre_right = [pos[0] + self.scale, pos[1]]

        pre_move = self.pre_move()#[pre_up, pre_down, pre_left, pre_right]

        closest = [float("INF"), pos]

        for i in pre_move:

            if i not in no_move:
                for hero in game.get_hero_set():
                    if distance(hero.get_pos(), i) < closest[0]:
                        closest = [distance(hero.get_pos(), i), i]
        return closest[1]
                        
                        
                

        
    def ind_move(self, grid, game):
        # Brute Force Random walk
        smart = 100
        no_move = self.no_move(grid, game)

        goals = self.goals(game)

        move_trace_store = []
        final = [None] * (smart + 1)
        for j in range(smart):
            pos = self.pos[:]
            move_trace = []
            count = 0

            while (pos not in goals) and count < self.sight:

                count += 1

                pre_up = [pos[0], pos[1] - self.scale]
                pre_down = [pos[0], pos[1] + self.scale]
                pre_left = [pos[0] - self.scale, pos[1]]
                pre_right = [pos[0] + self.scale, pos[1]]

                pre_move = [pre_up, pre_down, pre_left, pre_right]
                #pre_move = self.pre_move()
                pot_move = []

                for i in pre_move:

                    if i not in no_move:
                        pot_move += [i]

                the_move = random.choice(pot_move)
                pos[0] = the_move[0]
                pos[1] = the_move[1]
                move_trace += [[the_move[0], the_move[1]]]

            if len(move_trace) < len(final):
                final = move_trace

        return final[0]

    def hunt(self, grid, game):
        if self.turn >= 1:
            self.turn -= 1
            goals = self.goals(game)

            if self.pos not in goals:

                for hero in game.get_hero_set():
                    if distance(hero.get_pos(), self.pos) / game.get_scale() < self.sight:

                        self.map_update(grid, ".")
                        try:
                            #self.pos = self.ind_move(grid, game)
                            self.pos = self.closest_move(grid, game)
                        except:
                            pass
            else:
                """must edit if plan to add multiple players"""
                for hero in game.get_hero_set():
                    attack = Attack(hero.get_pos(), game)
                    game.add_mob_attack_to_set(attack)


class Spider_1(Mob):
    def __init__(self, pos, game):
        Mob.__init__(self, pos, game)
        self._image = pygame.transform.scale(spider_1, (self.scale, self.scale * 4))
        self._image.convert_alpha()

        self.sight = 7
        self.hp_max = 12
        self.hp = self.hp_max
        self.speed = .7

    def render(self, screen, camera, grid):
        fog_lis = []
        for fog in grid.get_fog_set():
            fog_lis.append(fog.get_pos())
        
        if self.pos not in fog_lis:

            self.health_render(screen, camera, grid)

            self.age += 0.08
            current_index = int((self.age % 4) // 1)
        
            scroll = [0, self.scale * current_index, self.scale, self.scale]
            screen.blit(self._image,
                        [self.pos[0] + camera.get_x(),
                         self.pos[1] + camera.get_y()],
                        area=scroll)

class Eye_1(Mob):
    def __init__(self, pos, game):
        Mob.__init__(self, pos, game)
        self._image = pygame.transform.scale(eye_1, (self.scale, self.scale * 4))
        self._image.convert_alpha()

        self.sight = 12
        self.hp_max = 21
        self.hp = self.hp_max
        self.speed = 0

    def render(self, screen, camera, grid):
        fog_lis = []
        for fog in grid.get_fog_set():
            fog_lis.append(fog.get_pos())
        
        if self.pos not in fog_lis:

            self.health_render(screen, camera, grid)

            self.age += 0.08
            current_index = int((self.age % 4) // 1)
        
            scroll = [0, self.scale * current_index, self.scale, self.scale]
            screen.blit(self._image,
                        [self.pos[0] + camera.get_x(),
                         self.pos[1] + camera.get_y()],
                        area=scroll)

class Squid_1(Mob):
    def __init__(self, pos, game):
        Mob.__init__(self, pos, game)
        self._image = pygame.transform.scale(squid_1, (self.scale, self.scale * 6))
        self._image.convert_alpha()

        self.sight = 5
        self.hp_max = 51
        self.hp = self.hp_max
        self.speed = 0

    def render(self, screen, camera, grid):
        fog_lis = []
        for fog in grid.get_fog_set():
            fog_lis.append(fog.get_pos())
        
        if self.pos not in fog_lis:

            self.health_render(screen, camera, grid)

            self.age += 0.08
            current_index = int((self.age % 6) // 1)
        
            scroll = [0, self.scale * current_index, self.scale, self.scale]
            screen.blit(self._image,
                        [self.pos[0] + camera.get_x(),
                         self.pos[1] + camera.get_y()],
                        area=scroll)

class Black_spirit_1(Mob):
    def __init__(self, pos, game):
        Mob.__init__(self, pos, game)
        self._image = pygame.transform.scale(black_spirit_1, (self.scale, self.scale * 7))
        self._image.convert_alpha()

        self.sight = 5
        self.hp_max = 10
        self.hp = self.hp_max
        self.speed = 2

    def render(self, screen, camera, grid):
        fog_lis = []
        for fog in grid.get_fog_set():
            fog_lis.append(fog.get_pos())
        
        if self.pos not in fog_lis:

            self.health_render(screen, camera, grid)

            self.age += 0.18
            current_index = int((self.age % 7) // 1)
        
            scroll = [0, self.scale * current_index, self.scale, self.scale]
            screen.blit(self._image,
                        [self.pos[0] + camera.get_x(),
                         self.pos[1] + camera.get_y()],
                        area=scroll)
