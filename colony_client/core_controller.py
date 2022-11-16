from colony_client.bot import Bot
from custom_logger import Logger


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

    def deleteBot(self, bot: Bot):
        for selectedBot in self.bots:
            if selectedBot.identifier == bot.identifier:
                self.bots.remove(bot)
                loggingMessage = "Deleted Bot %s" % selectedBot.identifier
                self.logger.debugLog(self.logTitle, loggingMessage)
                break
            else:
                continue

