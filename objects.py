import pygame
import sys
import random
from map_generator import distance

BLACK = (0, 0, 0)
RED = (255, 0, 0)
PINK = (250, 30, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (0, 255, 255)


class Game:

    def __init__(self, size, scale=50):
        self.turn = 0
        self.hero_set = set()
        self.camera_set = set()
        self.scale = scale
        self.size = size

    def get_turn(self):
        return self.turn

    def add_turn(self, num):
        self.turn += num

    def sub_turn(self, num):
        self.turn -= num

    def get_hero_set(self):
        return self.hero_set

    def add_hero_to_set(self, hero):
        self.hero_set.add(hero)

    def del_hero_from_set(self, hero):
        self.hero_set.discard(hero)

    def get_camera_set(self):
        return self.camera_set

    def add_camera_to_set(self, camera):
        self.camera_set.add(camera)

    def del_camera_from_set(self, camera):
        self.camera_set.discard(camera)

    def get_scale(self):
        return self.scale

    def get_size(self):
        return self.size


class Map:

    def __init__(self, grid, game, n=10, m=10):
        self.n = n
        self.m = m
        self.tile_set = set()
        self.mob_set = set()
        self.scale = game.get_scale()
        self.screen_size = game.get_size()
        self.view = list(self.screen_size)
        self.a = 0
        self.b = 0

        #mapp = stdarray.create2D(n,m)
        mapp = [[None for col in range(self.n)] for row in range(self.m)]
        for i, v in enumerate(mapp):
            for j, w in enumerate(v):
                mapp[i][j] = grid[i][j]
        self.map = mapp

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


class Tile:

    def __init__(self, pos, scale):
        self._x = pos[0]
        self._y = pos[1]
        self.scale = scale

    def get_coordinates(self):
        return [self._x * self.scale, self._y * self.scale]


class Wall(Tile):
    def __init__(self, pos, scale):
        Tile.__init__(self, pos, scale)

    def render(self, screen, camera):
        pygame.draw.rect(screen, BLACK,
                         [[(self._x * self.scale) + camera.get_x(),
                           (self._y * self.scale) + camera.get_y()],
                          [self.scale, self.scale]])


class Camera:

    def __init__(self, game, hero):
        self.size = game.get_size()
        self.hero = hero
        self.scale = game.get_scale()
        self._x = 0
        self._y = 0
        self.inner_box = self.scale * 4

    def in_view(self):

        if self.hero.get_pos()[0] + self._x > self.size[0] - self.inner_box:
            self._x -= self.scale
        if self.hero.get_pos()[0] + self._x < self.inner_box - self.scale:
            self._x += self.scale
        if self.hero.get_pos()[1] + self._y > self.size[1] - self.inner_box:
            self._y -= self.scale
        if self.hero.get_pos()[1] + self._y < self.inner_box - self.scale:
            self._y += self.scale

    def spawn(self, pos):
        self._x = pos[1]
        self._y = pos[0]

    def get_y(self):
        return self._y

    def get_x(self):
        return self._x


class Mob:

    def __init__(self, pos, game):
        self.pos = pos[:]
        self.scale = game.get_scale()
        self.move_lis = ["."]
        self.value = "c"
        self.sight = 7
        self.turn = 0

    def dead(self, grid):
        self.value = "."
        self.map_update(grid)
    def add_turn(self, num):
        self.turn += num
        print self.turn

    def get_sight(self):
        return self.sight

    def get_pos(self):
        return self.pos

    def alt_pos(self, lis):
        self.pos[0] += lis[0]
        self.pos[1] += lis[1]

    def update(self):
        pass

    def render(self, screen, camera):
        pygame.draw.rect(screen, GREEN,
                         [[self.pos[0] + camera.get_x(),
                           self.pos[1] + camera.get_y()],
                          [self.scale, self.scale]])

    def map_update(self, grid):
        grid.map_update([self.pos[1] / self.scale, self.pos[0] / self.scale],
                        self.value)

    def ind_move(self, grid, game):
        smart = 100
        
        no_move = []
        for tile in grid.get_tile_set():
            no_move += [tile.get_coordinates()]
        goals = []
        for i in game.get_hero_set():
            goals += [i.get_pos()]

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

        return final

    def hunt(self, grid, game):
        if self.turn >= 1:
            self.turn -= 1
            goals = []
            for i in game.get_hero_set():
                goals += [i.get_pos()]
            if self.pos not in goals:
                if True:#if pygame.time.get_ticks() % 200 <= 40:
                    for i in game.get_hero_set():
                        if distance(i.get_pos(), self.pos) / game.get_scale() < self.sight:
                            self.pos = self.ind_move(grid, game)[0]


class Hero:
    def __init__(self, pos, game, bot=False):
        self.pos = pos
        self.scale = game.get_scale()
        self.bot = bot
        self.color = RED

    def get_pos(self):
        return self.pos

    def alt_pos(self, lis):
        self.pos[0] += lis[0]
        self.pos[1] += lis[1]

    def is_bot(self):
        return self.bot

    def update(self, grid):
        pass

    def render(self, screen, camera):
        pygame.draw.rect(screen, self.color,
                         [[self.pos[0] + camera.get_x(),
                           self.pos[1] + camera.get_y()],
                          [self.scale, self.scale]])

    def move(self, key, grid, game):
        for mob in grid.get_mob_set():
            if distance(mob.get_pos(), self.pos) / game.get_scale() < mob.get_sight():
                mob.add_turn(1)

            
        no_move = []
        for tile in grid.get_tile_set():
            no_move += [tile.get_coordinates()]

        if not self.bot:
            if key == pygame.K_UP:
                if [self.pos[0], self.pos[1] - self.scale] not in no_move:
                    self.pos[1] -= self.scale

            if key == pygame.K_DOWN:
                if [self.pos[0], self.pos[1] + self.scale] not in no_move:
                    self.pos[1] += self.scale

            if key == pygame.K_LEFT:
                if [self.pos[0] - self.scale, self.pos[1]] not in no_move:
                    self.pos[0] -= self.scale

            if key == pygame.K_RIGHT:
                if [self.pos[0] + self.scale, self.pos[1]] not in no_move:
                    self.pos[0] += self.scale


def mob_spawn(grid, game):
    lis = []
    for i, v in enumerate(grid.get_map()):
        for j, w in enumerate(v):

            if grid.get_map()[j][i] == ".":
                    lis += [[i * game.get_scale(), j * game.get_scale()]]
    pos = random.choice(lis)

    if len(grid.get_mob_set()) < 10:
        mob = Mob(pos, game)
        grid.add_mob_to_set(mob)


def hero_spawn(grid, game):
    lis = []
    for i, v in enumerate(grid.get_map()):
        for j, w in enumerate(v):

            if grid.get_map()[j][i] == ".":
                    lis += [[i * game.get_scale(), j * game.get_scale()]]
    pos = random.choice(lis)

    if len(game.get_hero_set()) < 1:
        print "hero"
        hero = Hero(pos, game, bot=False)
        camera = Camera(game, hero)
        game.add_hero_to_set(hero)
        game.add_camera_to_set(camera)
        camera.spawn(hero.get_pos())


def heros_mob_collide(hero, game, grid):
    mob_set = grid.get_mob_set().copy()
    heros = game.get_hero_set()
    for mob in mob_set:
        for hero in heros:
            if mob.get_pos() == hero.get_pos():
                mob.dead(grid)
                grid.del_mob_from_set(mob)


def tile_generate(game, grid, camera=None):
    scale = game.get_scale()
    x = 0
    for i, v in enumerate(grid.get_map()):
            for j, w in enumerate(v):
                if w == "x" or w == " ":
                    x += 1
                    if len(grid.get_tile_set()) < x:
                        tile = Wall([j, i], scale)
                        grid.add_tile_to_set(tile)

                if w == "c":
                    pass


def logic(game, grid, screen):
    mob_spawn(grid, game)
    tile_generate(game, grid)
    hero_spawn(grid, game)
    for camera in game.get_camera_set():
        camera.in_view()
        for tile in grid.get_tile_set():
            tile.render(screen, camera)

        for i in grid.get_mob_set():
            i.hunt(grid, game)
            i.render(screen, camera)
            i.map_update(grid)

        for hero in game.get_hero_set():
            heros_mob_collide(hero, game, grid)
            hero.render(screen, camera)
