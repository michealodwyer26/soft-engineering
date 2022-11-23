# from .bot import Bot
# from .core_controller import CoreController
import pygame 
from pygame.locals import *
from sys import exit
from random import *


class Bot:
    def __init__(self):
        self.screen = pygame.display.set_mode((500, 500), 0,32)
        self.pos = (randint(20,480), randint(20,480))
        self.color = (randint(0,255), randint(0,255), randint(0,255))
        self.size = ((20,20))

    def draw(self):
        pygame.draw.rect(self.screen, self.color, Rect(self.pos, self.size))


class CoreController:
    def draw(self):
        pygame.draw.circle(self.screen, (255, 255, 255), (250, 250), 30)


class Visualiser:
    def __init__(self, coreController):
        self.coreController = coreController
        self.bots = [] 
        pygame.init()
        # for i in range(10):
        #     self.bots.append(Bot())

    def addBot(self):
        self.bots.append(Bot())

    def run(self):
        pygame.init()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            self.screen.lock()
            CoreController().draw()
            for bot in self.bots:
                bot.draw()
            self.screen.unlock()
            pygame.display.update()


# cs = CoreController #create corecontroller
# vis = Visualiser(cs) #add it to the visualizer
# vis.addBot() #add bots to visualixer bot list
# vis.addBot()
# vis.addBot()
# vis.addBot()
# vis.run() # run visulaizer

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