# from .bot import Bot
# from .core_controller import CoreController
import pygame
import requests
from pygame.locals import *
from sys import exit
from random import *


class VisualBot:
    def __init__(self, screen, index):
        self.index = index  # Identifier with the visualiser
        self.xpos = 30
        self.ypos = (20 + (40 * self.index))
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.size = (20, 20)
        self.renderer = screen

    def draw(self):
        pygame.draw.rect(self.renderer, self.color, Rect((self.xpos, self.ypos), self.size))


class VisualCoreController:
    def __init__(self, screen):
        self.renderer = screen
        self.xpos = 250
        self.ypos = 250

    def draw(self):
        pygame.draw.circle(self.renderer, (255, 255, 255), (self.xpos, self.ypos), 30)


class Visualiser:
    def __init__(self, coreController):
        pygame.init()

        self.coreController = coreController
        self.bots = []
        self.currentIndex = 0
        self.screen = pygame.display.set_mode((500, 500), 0, 32)
        self.font = pygame.font.SysFont('Times', 16)

    def renderText(self, message: str, posX, posY):
        text = self.font.render(message, True, (255, 255, 255))
        try:
            self.screen.blit(text, (posX, posY))
            print("S: Tried rendering text: " + message)
        except Exception as e:
            print(e)
            print("F: Tried rendering text: " + message)

    def updateBotData(self, colonyName: str):
        url = "http://65.108.214.180/api/v1/colony/%s" % colonyName
        try:
            response = requests.get(url)
        except Exception as e:
            print(e)

        json = response.json()

        if len(json["bots"]) > len(self.bots):
            print("JSON Bots:", len(json["bots"]))
            print("Local Bots:", len(self.bots))
            self.bots.append(self.addBot())
            print("Added a VisualBot")

        for bot in self.bots:
            if bot:
                try:
                    textToRender = str(json["bots"])
                    self.renderText(textToRender, bot.xpos + 30, bot.ypos)
                except Exception as e:
                    print(e)

    def addBot(self):
        self.bots.append(VisualBot(self.screen, self.currentIndex))
        self.currentIndex += 1

    def run(self):

        pygame.init()
        elapsedTime = 0
        clock = pygame.time.Clock()
        vCore = VisualCoreController(self.screen)
        firstIteration = False

        while True:

            currentTime = clock.tick()
            elapsedTime += currentTime

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

            if firstIteration:
                vCore.draw()
                for bot in self.bots:
                    bot.draw()
                pygame.display.update()

            if not firstIteration:
                self.updateBotData(self.coreController.identifier)
                self.renderText(self.coreController.identifier, vCore.xpos - 20, vCore.ypos + 40)

                vCore.draw()
                for bot in self.bots:
                    bot.draw()

                firstIteration = True
                pygame.display.update()

            if elapsedTime > 5000:
                self.updateBotData(self.coreController.identifier)
                self.renderText(self.coreController.identifier, vCore.xpos - 20, vCore.ypos + 40)
                self.bots = list(filter(lambda iterBot: iterBot is not None, self.bots))
                vCore.draw()
                for bot in self.bots:
                    bot.draw()
                pygame.display.update()
                elapsedTime = 0
