import requests
from bot import Bot
from cryptocolony.custom_logger import Logger


class CoreController:
    def __init__(self, name):
        self.bots = []
        self.identifier = name
        self.currentBotId = 0
        self.logTitle = "core"
        self.logger = Logger()
        self.notifySentimentController()

    def listenForGodMode(self):
        pass

    def notifySentimentController(self):
        dataJSON = '{"name":"%s"}' % self.identifier
        try:
            requests.post(
                "http://65.108.214.180/api/v1/colony/create",
                data=dataJSON,
                headers={"Content-Type": "application/json"}
            )
        except Exception as e:
            print(e)

    def createBot(self, botCoin: str):
        self.currentBotId += 1  # Increases the botId
        bot = Bot(self.currentBotId, botCoin)  # Creates a bot with a botId and a coin
        self.bots.append(bot)

        loggingMessage = "Created Bot %s" % self.currentBotId
        self.logger.debugLog("core", loggingMessage)

        try:
            dataJSON = '{"colony":"%s", "id":"%s", "coin":"%s"}' % (self.identifier, self.currentBotId, botCoin)
            requests.post(
                "http://65.108.214.180/api/v1/bot/create",
                data=dataJSON,
                headers={"Content-Type": "application/json"}
            )
        except Exception as e:
            print(e)
        return

    def deleteBot(self, bot: Bot):
        for selectedBot in self.bots:
            if selectedBot.identifier == bot.identifier:
                self.bots.remove(bot)
                loggingMessage = "Deleted Bot %s" % selectedBot.identifier
                self.logger.debugLog(self.logTitle, loggingMessage)
                break
            else:
                continue
