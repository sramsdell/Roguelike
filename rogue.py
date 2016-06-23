import sys
sys.dont_write_bytecode = True
import pygame
import random
from objects import *
from maps import *


SIZE = (500, 500)
SCALE = 25
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


class PlayState_1(MasterState):
    def __init__(self, screen):
        MasterState.__init__(self, screen)
        self.myfont = pygame.font.SysFont("fixedsys", 20)

    def update(self):
        pass

    def render(self, screen):
        screen.fill(YELLOW)

    def event_handler(self, events):

        for event in events:
            self.quit(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
                elif event.key == pygame.K_p:
                    self.currentstate.change(IntroState(screen))
        return True


class IntroState(MasterState):
    def __init__(self, screen):
        MasterState.__init__(self, screen)
        self.myfont = pygame.font.SysFont("fixedsys", 20)

    def update(self):
        pass

    def render(self, screen):
        screen.fill(BLUE)
        logic(game, grid, screen)

    def event_handler(self, events):

        for event in events:
            self.quit(event)
            if event.type == pygame.KEYDOWN:
                for i in game.get_hero_set():
                    i.move(event.key, grid, game)
                if event.key == pygame.K_p:
                    self.currentstate.change(PlayState_1(screen))
        return True


if __name__ == '__main__':
    main()
