import pygame, sys, random

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (0,255,255)

class Game:

    def __init__(self):
        self.mob_set = set()
    def get_mob_set(self):
        return self.mob_set
    def add_mob_to_set(self,mob):
        self.mob_set.add(mob)
    def del_mob_from_set(self,mob):
        self.mob_set.discard(mob)


class Map:

    def __init__(self, grid,n = 10,m = 10):
        self.n = n
        self.m = m
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
        
    def render(self,screen):
        for i, v in enumerate(self.map):
            for j, w in enumerate(v):
                if w == "x":
                    pygame.draw.rect(screen, BLACK,[[j * 50,i * 50],[50,50]])
                if w == "c":
                    pygame.draw.rect(screen, GREEN,[[j * 50,i * 50],[50,50]])

class Mob:

    def __init__(self,pos):
        self.pos = pos[:]
        self.scale = 50
        self.move_lis = ["."]
        self.value = "c"
    def dead(self,grid):
        self.value = "."
        self.map_update(grid)
    def get_pos(self):
        return self.pos
    def update(self):
        pass
    def render(self, screen):
        pygame.draw.rect(screen, GREEN, [self.pos, [self.scale,self.scale]])
    def map_update(self, grid):
        grid.map_update([self.pos[1] / self.scale, self.pos[0] / self.scale], self.value)

class Hero:
    def __init__(self):
        self.pos = [100,100]
        self.scale = 50
        self.move_lis = [".","c"]
    def get_pos(self):
        return self.pos
    def update(self, grid):
        pass
    def render(self, screen):
        pygame.draw.rect(screen, RED,[self.pos,[50,50]])
        
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
            if pygame.time.get_ticks() % 500 <= 30:
                self.pos = self.ind_move(grid)[0]

    
    def move(self,key,grid):
        move_lis = [".","c"]
        print grid.get_map()[self.pos[1]/self.scale][self.pos[0]/self.scale]
        if key == pygame.K_UP:
            
            print "next",grid.get_map()[(self.pos[1]/self.scale)-1][(self.pos[0]/self.scale)]
            if grid.get_map()[(self.pos[1]/self.scale)-1][(self.pos[0]/self.scale)] in self.move_lis:
                self.pos[1] -= self.scale
            
        if key == pygame.K_DOWN:
            
            print "next",grid.get_map()[(self.pos[1]/self.scale)+1][(self.pos[0]/self.scale)]
            if grid.get_map()[(self.pos[1]/self.scale)+1][(self.pos[0]/self.scale)] in self.move_lis:
                self.pos[1] += self.scale
            
        if key == pygame.K_LEFT:
            print "next",grid.get_map()[(self.pos[1]/self.scale)][(self.pos[0]/self.scale)-1]
            if grid.get_map()[(self.pos[1]/self.scale)][(self.pos[0]/self.scale)-1] in self.move_lis:
                self.pos[0] -= self.scale
        if key == pygame.K_RIGHT:
            print "next",grid.get_map()[(self.pos[1]/self.scale)][(self.pos[0]/self.scale)+1]
            if grid.get_map()[(self.pos[1]/self.scale)][(self.pos[0]/self.scale)+1] in self.move_lis:
                self.pos[0] += self.scale
        if key == pygame.K_SPACE:
            self.pos = [50,50]
        if key == pygame.K_b:
            self.pos = [300,100]

def mob_spawn(grid,game):
    lis = []
    for i, v in enumerate(grid.get_map()):
        for j, w in enumerate(v):
            
            if grid.get_map()[j][i] == ".":
                    lis += [[i * 50, j * 50]]
    pos = random.choice(lis)
    if len(game.get_mob_set()) < 2:
        mob = Mob(pos)
        game.add_mob_to_set(mob)

def hero_mob_collide(hero,game,grid):
    mob_set2 = game.get_mob_set().copy()   
    for mob in mob_set2:
        if mob.get_pos() == hero.get_pos():
            mob.dead(grid)
            game.del_mob_from_set(mob)

def logic(hero, game, grid, screen):
    mob_spawn(grid, game)
    hero_mob_collide(hero, game, grid)
    grid.render(screen)
    hero.render(screen)
    for i in game.get_mob_set():
            i.render(screen)
            i.map_update(grid)
