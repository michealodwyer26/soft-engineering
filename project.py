import pygame as pg
from customlogger import Logger

class Bot:
    def __init__(self, identifier, balance):
        self.identifier = identifier
        self._balance = balance
        self.xpos = 0
        self.ypos = 0
        self.logger = Logger()
        self.logTitle = "bot"

    def setBalance(self, balance):
        self._balance = balance
        return

    def listenForGodMode(self):
        pass

    def listenForResponse(self):
        pass

    def investingState(self):
        pass

    # Taking Earnings & Sending Feedback
    def feedback(self):
        pass

    def die(self):
        pass


class CoreController:
    def __init__(self):
        self.bots = []
        self.currentBotId = 0
        self.logTitle = "core"
        self.logger = Logger()

    def listenForGodMode(self):
        pass

    def createBot(self, startingBalance: int):
        self.currentBotId += 1
        bot = Bot(self.currentBotId, startingBalance)
        self.bots.append(bot)
        loggingMessage = "Created Bot %s" % self.currentBotId
        self.logger.debugLog("core", loggingMessage)

    def deleteBot(self, bot):
        for selectedBot in self.bots:
            if selectedBot.identifier == bot.identifier:
                self.bots.remove(bot)
                loggingMessage = "Deleted Bot %s" % selectedBot.identifier
                self.logger.debugLog(self.logTitle, loggingMessage)
                break
            else:
                continue

class GodModeController:
    def __init__(self):
        self.logTitle = "god"
        pass

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
       self.mainDisplay.set_at((bot.xpos, bot.ypos), (255,255,255))
    
    def eraseBot(self, bot):
        self.mainDisplay.set_at((bot.xpos, bot.ypos), (0, 0, 0))

#myCore = CoreController()
#myCore.createBot(100)
