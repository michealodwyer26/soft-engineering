from custom_logger import Logger

class Bot:
    def __init__(self, identifier, balance):
        self.identifier = identifier
        self._balance = balance
        self.xpos = 0
        self.ypos = 0
        self.logger = Logger()
        self.logTitle = "bot"

    def getBalance(self):
        return self._balance
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