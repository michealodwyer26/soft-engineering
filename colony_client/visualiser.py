from .bot import Bot
from .core_controller import CoreController
import pygame 
from pygame.locals import *
from sys import exit
from random import *

screen = pygame.display.set_mode((500, 500), 0,32)
pygame.display.set_caption("Crypto Bot Colony")

class Bot:
    def __init__(self, pos, color, size):
        self.pos = pos
        self.color = color
        self.size = size
    def draw(self):
        pygame.draw.rect(screen, self.color, Rect(self.pos, self.size))

class CoreController:
    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (250, 250), 30)

class Visualiser:
    def __init__(self):
        pygame.init()
        bots = []     

        for i in range(10):
            randomColor = (randint(0,255), randint(0,255), randint(0,255))
            randomPos = (randint(20,480), randint(20,480))
            size = ((20, 20))
            bots.append(Bot(randomPos, randomColor, size))

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            screen.lock()
            CoreController().draw()
            for bot in bots:
                bot.draw()
            screen.unlock()
            pygame.display.update()


vis = Visualiser()

# class Visualiser:
#     def __init__(self):
#         self.mainDisplay = None
#         self.logTitle = "visualiser"

#     def initialise(self):
#         screen = (800, 600)
#         pg.init()
#         pg.display.set_caption('Crypto Bot Colony')
#         self.mainDisplay = pg.display.set_mode(screen)
#         displayer = pg.Surface(screen)

#     def drawBot(self, bot):
#         self.mainDisplay.set_at((bot.xpos, bot.ypos), (255, 255, 255))

#     def eraseBot(self, bot):
#         self.mainDisplay.set_at((bot.xpos, bot.ypos), (0, 0, 0))

# class Visualiser:
#     def __init__(self):
#         self.WIDTH, self.HEIGHT = 500, 500
#         self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
#         pygame.display.set_caption("Visualization")  # window name
#         self.WHITE = (255, 255, 255)
#         self.FPS = 10
#         self.main()

#     def draw_window(self):
#         self.WIN.fill(self.WHITE)
#         pygame.draw.circle(self.WIN, (0, 255, 0), (250, 250), 30)
#         self.draw_bot()
#         pygame.display.update()

#     # def draw_bot(self):
#     #     bot_coordinate = (100, 100)
#     #     surf = pygame.Surface((50, 50))
#     #     surf.fill((0, 0, 0))
#     #     rect = surf.get_rect()
#     #     self.WIN.blit(surf, (self.WIDTH/2, self.HEIGHT/2))
#     #     pygame.display.flip()

#     def draw_bot(self):
#         bot_coordinate = (random.randint(0, 500), random.randint(0, 500))
#         # bot = pygame.draw.circle(self.WIN, (0, 0, 0), bot_coordinate, 10)
#         bot = pygame.Surface((10, 10))
#         bot.fill((0, 0, 0))
#         rect = bot.get_rect()
#         self.WIN.blit(bot, bot_coordinate)
#         pygame.display.flip()

#     def main(self):
#         clock = pygame.time.Clock()
#         run = True
#         while run:
#             clock.tick(self.FPS)  # Never go over 60 fps
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     run = False
#             self.draw_window()
#         pygame.quit()


# vis = Visualiser()