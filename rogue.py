import sys
sys.dont_write_bytecode = True
import pygame
from logics import *
from maps import *

SIZE = (600, 600)
SCALE = 30
screen = pygame.display.set_mode(SIZE)
game = Game(SIZE, SCALE)

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

    def render(self, screen):
        self.state.render(screen)


class MasterState:
    def __init__(self, screen):
        self.screen = screen

    def quit(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            return False


class IntroState(MasterState):
    def __init__(self, screen):
        MasterState.__init__(self, screen)
        self.font1 = pygame.font.SysFont("fixedsys",24)
        self.font2 = pygame.font.SysFont("fixedsys",16)
        self.text1 = self.font1.render("A Roguelike Concept; SPACE to start",1,BLACK)
        self.text2 = self.font2.render("Arrows to move, SPACE to attack",1,BLACK)

    def update(self):
        pass

    def render(self, screen):
        screen.fill(YELLOW)
        screen.blit(self.text1,(SIZE[0]/2-100,SIZE[1]/2))
        screen.blit(self.text2,(SIZE[0]/2-75,SIZE[1]/2 + 100))

    def event_handler(self, events):

        for event in events:
            self.quit(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.currentstate.change(PlayState_1(screen))
                elif event.key == pygame.K_p:
                    self.currentstate.change(PlayState_1(screen))
        return True


class PlayState_1(MasterState):
    def __init__(self, screen):
        MasterState.__init__(self, screen)
        self.myfont = pygame.font.SysFont("fixedsys", 20)
        self.grid = change_level(game)
        
    def update(self):
        pass

    def render(self, screen):
        screen.fill(GREY)
        level = logic(game, self.grid, screen)
        self.grid = change_level(game)
        logic_2(game, self.grid, screen, level)

    def event_handler(self, events):

        for event in events:
            self.quit(event)
            if event.type == pygame.KEYDOWN:
                for i in game.get_hero_set():
                    i.move(event.key, self.grid, game)
                if event.key == pygame.K_p:
                    self.currentstate.change(IntroState(screen))
        return True


if __name__ == '__main__':
    main()
