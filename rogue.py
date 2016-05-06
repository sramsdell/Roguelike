import pygame,sys,random,stdarray
sys.dont_write_bytecode = True
from objects import *
from maps import *

SIZE = (500,500)
screen = pygame.display.set_mode(SIZE)

# inits
game = Game()       
hero = Hero()
hero1 = Hero()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True
    manager = TransManager(screen)

    while running:
        running = manager.state.event_handler(pygame.event.get())

        manager.update()
        manager.render(screen)
        clock.tick(60)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


class TransManager:

    def __init__(self, screen):
        self.change(IntroState(screen))

    def change(self, state):
        self.state = state
        self.state.currentstate = self

    def update(self):
        self.state.update()

    def render(self,screen):
        self.state.render(screen)


class MasterState:
    def __init__(self, screen):
        self.screen = screen

    def quit(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            return False


class PlayState_1(MasterState):
    def __init__(self, screen):
        MasterState.__init__(self,screen)
        self.myfont = pygame.font.SysFont("fixedsys", 20)
    def update(self):
        hero1.hunt(grid1)
        mob_spawn(grid1,game)
        hero_mob_collide(hero1,game,grid1)
        for i in game.get_mob_set():
            i.map_update(grid1)
    def render(self,screen):
        screen.fill(YELLOW)
        grid1.render(screen)
        hero1.render(screen)
        for i in game.get_mob_set():
            i.render(screen)
    def event_handler(self,events):

        for event in events:
            self.quit(event)
            if event.type == pygame.KEYDOWN:
                hero1.move(event.key,grid1)
                if event.key == pygame.K_SPACE:
                    pass
                elif event.key == pygame.K_p:
                    self.currentstate.change(IntroState(screen))
        return True


class IntroState(MasterState):
    def __init__(self, screen):
        MasterState.__init__(self,screen)
        self.myfont = pygame.font.SysFont("fixedsys", 20)
    def update(self):
        hero.hunt(grid)
    def render(self,screen):
        screen.fill(BLUE)
        logic(hero,game,grid,screen)
    def event_handler(self,events):

        for event in events:
            self.quit(event)
            if event.type == pygame.KEYDOWN:
                hero.move(event.key,grid)
                if event.key == pygame.K_p:
                    self.currentstate.change(PlayState_1(screen))
        return True
        

if __name__ == '__main__':
    main()
