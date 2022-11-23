# from .bot import Bot
# from .core_controller import CoreController
import pygame
from pygame.locals import *
from sys import exit
from random import *


class VisualBot:
    def __init__(self, screen, index, font, botId, balance, coin):
        self.botId = botId
        self.balance = balance
        self.coin = coin
        self.index = index  # Identifier with the visualiser
        self.y = 30
        self.x = (20 + (40 * self.index))
        self.pos = (self.y, self.x)
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.size = (20, 20)
        self.renderer = screen
        self.font = font

    def draw(self):
        pygame.draw.rect(self.renderer, self.color, Rect(self.pos, self.size))
        self.renderer.blit(self.font.render(
            f'{self.botId} {self.balance} {self.coin}', True, (255, 255, 255)), (self.y-7, self.x-20))
        pygame.display.update()

    def updateData(self):
        pass


class VisualCoreController:
    def __init__(self, screen):
        self.renderer = screen

    def draw(self):
        pygame.draw.circle(self.renderer, (255, 255, 255), (250, 250), 30)


class Visualiser:
    def __init__(self, coreController):
        pygame.init()
        self.coreController = coreController
        self.bots = []
        self.currentIndex = 0
        self.screen = pygame.display.set_mode((500, 500), 0, 32)
        self.font = pygame.font.SysFont('Times', 20)

    def addBot(self, botId, balance, coin):
        self.bots.append(
            VisualBot(self.screen, self.currentIndex, self.font, botId, balance, coin))
        self.currentIndex += 1

    def run(self):

        pygame.init()
        elapsedTime = 0
        clock = pygame.time.Clock()

        while True:

            currentTime = clock.tick()
            elapsedTime += currentTime

            if elapsedTime > 5000:
                # Triggers every 5 seconds. Update the view with new information.
                pass

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            # self.screen.lock()

            VisualCoreController(self.screen).draw()

            for bot in self.bots:
                bot.draw()

            self.screen.unlock()
            pygame.display.update()


cs = VisualCoreController  # create corecontroller
vis = Visualiser(cs)  # add it to the visualizer

bots = {"bot1": {"coinAmount": 10, "coinName": "BTC"},
        "bot2": {"coinAmount": 20, "coinName": "DOGE"},
        "bot3": {"coinAmount": 40, "coinName": "NAPH"},
        "bot4": {"coinAmount": 60, "coinName": "MONKE"}}


for key, value in bots.items():
    values = list(value.values())
    vis.addBot(key, values[0], values[1])  # add bots to visualixer bot list
vis.run()  # run visulaizer
