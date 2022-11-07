import pygame as pg

class Bot:
    def __init__(self, identifier, balance):
        self.identifier = identifier
        self._balance = balance
        self.xpos = 0
        self.ypos = 0
        self.botId = 0

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


class coreController:
    def __init__(self):
        self.bots = []
    
    def listenForGodMode(self):
        pass

    def visualise(self):
        pass

    def createBot(self, startingBalance: int):
        self.botId += 1
        bot = Bot(self.botId, startingBalance)
        self.bots.append(bot)

    def deleteBot(self, bot):
        for selectedBot in self.bots:
            if selectedBot.identifier == bot.identifier:
                self.bots.remove(bot)
                break
            else:
                continue

class godModeController:
    def __init__(self):
        pass

class Visualiser:
    def __init__(self):
        self.mainDisplay = None

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


