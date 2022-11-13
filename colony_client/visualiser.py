from .bot import Bot
from .core_controller import CoreController

class Visualiser:
    def __init__(self):
        self.mainDisplay = None
        self.logTitle = "visualiser"

    def initialise(self):
        screen = (800, 600)
        pg.init()
        pg.display.set_caption('Crypto Bot Colony')
        self.mainDisplay = pg.display.set_mode(screen)
        displayer = pg.Surface(screen)

    def drawBot(self, bot):
        self.mainDisplay.set_at((bot.xpos, bot.ypos), (255, 255, 255))

    def eraseBot(self, bot):
        self.mainDisplay.set_at((bot.xpos, bot.ypos), (0, 0, 0))