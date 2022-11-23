# from .bot import Bot
# from .core_controller import CoreController
import pygame
from pygame.locals import *
from sys import exit
from random import *


class VisualBot:
    def __init__(self, screen):
        self.pos = (randint(20, 480), randint(20, 480))
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.size = (20, 20)
        self.renderer = screen

    def draw(self):
        pygame.draw.rect(self.renderer, self.color, Rect(self.pos, self.size))


class VisualCoreController:
    def __init__(self, screen):
        self.renderer = screen

    def draw(self):
        pygame.draw.circle(self.renderer, (255, 255, 255), (250, 250), 30)


class Visualiser:
    def __init__(self, coreController):
        self.coreController = coreController
        self.bots = []
        self.screen = pygame.display.set_mode((500, 500), 0, 32)
        pygame.init()

    def addBot(self):
        self.bots.append(VisualBot(self.screen))

    def run(self):

        pygame.init()
        elapsedTime = 0
        clock = pygame.time.Clock()

        while True:

            currentTime = clock.tick()
            elapsedTime += currentTime

            if elapsedTime > 5000:
                pass  # Triggers every 5 seconds. Update the view with new information.

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            self.screen.lock()

            VisualCoreController(self.screen).draw()

            for bot in self.bots:
                bot.draw()

            self.screen.unlock()
            pygame.display.update()
