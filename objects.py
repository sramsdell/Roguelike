import pygame, sys, random

BLACK = (0, 0, 0)
RED = (255, 0, 0)
PINK = (250, 30, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (0,255,255)

class Game:

    def __init__(self,size, scale = 50):
        self.mob_set = set()
        self.hero_set = set()
        self.scale = scale
        self.size = size
    def get_mob_set(self):
        return self.mob_set
    def add_mob_to_set(self,mob):
        self.mob_set.add(mob)
    def del_mob_from_set(self,mob):
        self.mob_set.discard(mob)
    def get_hero_set(self):
        return self.hero_set
    def add_hero_to_set(self, hero):
        self.hero_set.add(hero)
    def del_hero_from_set(self, hero):
        self.hero_set.discard(hero)
    def get_scale(self):
        return self.scale
    def get_size(self):
        return self.size
    
class Map:

    def __init__(self,grid, game,n = 10,m = 10):
        self.n = n
        self.m = m
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
    def update(self):
        pass
    def get_map(self):
        return self.map
    def change_map(self,grid):
        self.map = grid

    def map_update(self, coordinate, value):
        #lis = stdarray.create2D(self.n,self.m)
        lis = [[None for col in range(self.n)] for row in range(self.m)]
        for i, v in  enumerate(self.map):
            
            for j, w in enumerate(v):
                
                if coordinate == [i,j]:
                    
                    lis[i][j] = value
                    
                else:
                    
                    lis[i][j] = w
        self.map = lis
                
    def render(self,screen, camera):
        for i, v in enumerate(self.map):
            for j, w in enumerate(v):
                if w == "x":
                    pygame.draw.rect(screen, BLACK,[[j * self.scale + (self.scale * camera.get_horizontal()),
                                                     i * self.scale + (self.scale * camera.get_vertical())],
                                                    [self.scale,self.scale]])
                if w == "c":
                    pygame.draw.rect(screen, GREEN,[[j * self.scale,
                                                     i * self.scale],
                                                    [self.scale,self.scale]])

class Camera:
    
    def __init__(self, game, hero):
        self.all_objects = game.get_mob_set().union(game.get_hero_set())
        self.vertical = 0
        self.horizontal = 0

        self.hero = hero
        
        self.scale = game.get_scale()
        self.screen_size = game.get_size()

        #screen
        self.view = list(self.screen_size)
        
    def get_vertical(self):
        return self.vertical
    def get_horizontal(self):
        return self.horizontal
    def in_view(self, grid):
        hero = self.hero    
        if not hero.is_bot():
            if hero.get_pos()[1] + (self.scale * self.vertical) > self.view[1] - self.scale:
                self.vertical -= 1
                self.view[1] -= self.scale
                self.shift_vertical()
##                temp = grid.get_map()
##                new = [["-"] * 10]
##                grid.change_map(temp + new)
##                print grid.get_map()
                
    def shift_vertical(self):
        for i in self.all_objects:
            i.alt_pos([0,-self.scale])
            
            
    

class Mob:

    def __init__(self,pos, game):
        self.pos = pos[:]
        self.scale = game.get_scale()
        self.move_lis = ["."]
        self.value = "c"
    def dead(self,grid):
        self.value = "."
        self.map_update(grid)
    def get_pos(self):
        return self.pos
    def alt_pos(self,lis):
        self.pos[0] += lis[0]
        self.pos[1] += lis[1]
    def update(self):
        pass
    def render(self, screen):
        pygame.draw.rect(screen, GREEN, [self.pos, [self.scale,self.scale]])
    def map_update(self, grid):
        grid.map_update([self.pos[1] / self.scale, self.pos[0] / self.scale], self.value)

class Hero:
    def __init__(self,game, bot = False, spawn = [100,100]):
        self.pos = spawn
        self.scale = game.get_scale()
        self.move_lis = [".","c"]
        self.bot = bot
        self.color = RED
    def get_pos(self):
        return self.pos
    def alt_pos(self,lis):
        self.pos[0] += lis[0]
        self.pos[1] += lis[1]
    def is_bot(self):
        return self.bot
    def update(self, grid):
        pass
    def render(self, screen):
        pygame.draw.rect(screen, self.color,[self.pos,[self.scale,self.scale]])
    def ind_move(self, grid):

        move_trace_store = []
        for j in range(200):
            pos = self.pos[:]
            move_trace = []
            count = 0
            while grid.get_map()[pos[1]/self.scale][pos[0]/self.scale] != "c" and count < 100:
                count += 1
                pre_up = [grid.get_map()[(pos[1]/self.scale)-1][(pos[0]/self.scale)] ,pos[0], pos[1] - self.scale]
                pre_down = [grid.get_map()[(pos[1]/self.scale)+1][(pos[0]/self.scale)] ,pos[0], pos[1] + self.scale]
                pre_left = [grid.get_map()[(pos[1]/self.scale)][(pos[0]/self.scale)-1],pos[0]- self.scale, pos[1]]
                pre_right = [grid.get_map()[(pos[1]/self.scale)][(pos[0]/self.scale)+1],pos[0]+ self.scale, pos[1]]
                pre_move = [pre_up,pre_down,pre_left,pre_right]
                
                pot_move =[]
                
                for i in pre_move:
                    
                    if i[0] in self.move_lis:
                        pot_move += [i]
                the_move = random.choice(pot_move)
                pos[0] = the_move[1]
                pos[1] = the_move[2]
                move_trace += [[the_move[1],the_move[2]]]
            move_trace_store += [[len(move_trace),move_trace]]
        trace = min(move_trace_store)
        return trace[1]
    
    def hunt(self,grid):
        if grid.get_map()[self.pos[1]/self.scale][self.pos[0]/self.scale] != "c":
            if pygame.time.get_ticks() % 200 <= 30:
                self.pos = self.ind_move(grid)[0]

    
    def move(self,key,grid,camera):
        move_lis = [".","c"]
        #print grid.get_map()[self.pos[1]/self.scale][self.pos[0]/self.scale]
        if not self.bot:
            if key == pygame.K_UP:
                
                #print "next",grid.get_map()[(self.pos[1]/self.scale)-1][(self.pos[0]/self.scale)]
                if grid.get_map()[(self.pos[1]/self.scale)-1][(self.pos[0]/self.scale)] in self.move_lis:
                    self.pos[1] -= self.scale
                
            if key == pygame.K_DOWN:
                
                #print "next",grid.get_map()[(self.pos[1]/self.scale)+1][(self.pos[0]/self.scale)]
                if grid.get_map()[(self.pos[1]/self.scale)+1][(self.pos[0]/self.scale)] in self.move_lis:
                    self.pos[1] += self.scale
                
            if key == pygame.K_LEFT:
                #print "next",grid.get_map()[(self.pos[1]/self.scale)][(self.pos[0]/self.scale)-1]
                if grid.get_map()[(self.pos[1]/self.scale)][(self.pos[0]/self.scale)-1] in self.move_lis:
                    self.pos[0] -= self.scale
            if key == pygame.K_RIGHT:
                #print "next",grid.get_map()[(self.pos[1]/self.scale)][(self.pos[0]/self.scale)+1]
                if grid.get_map()[(self.pos[1]/self.scale)][(self.pos[0]/self.scale)+1] in self.move_lis:
                    self.pos[0] += self.scale
##        if key == pygame.K_SPACE:
##            self.pos = [50,50]
##        if key == pygame.K_b:
##            self.pos = [300,100]

def mob_spawn(grid,game):
    pass
    lis = []
    for i, v in enumerate(grid.get_map()):
        for j, w in enumerate(v):
            
            if grid.get_map()[j][i] == ".":
                    lis += [[i * game.get_scale(), j * game.get_scale()]]
    pos = random.choice(lis)
    if len(game.get_mob_set()) < 2:
        mob = Mob(pos,game)
        game.add_mob_to_set(mob)

def heros_mob_collide(hero,game,grid):
    mob_set2 = game.get_mob_set().copy()
    heros = game.get_hero_set()
    for mob in mob_set2:
        for hero in heros:
            if mob.get_pos() == hero.get_pos():
                mob.dead(grid)
                game.del_mob_from_set(mob)

def logic(game, grid, screen, camera):
    mob_spawn(grid, game)
    grid.render(screen, camera)
    for hero in game.get_hero_set():
        camera.in_view(grid)
        heros_mob_collide(hero, game, grid)
        hero.render(screen)
    for i in game.get_mob_set():
            i.render(screen)
            i.map_update(grid)
