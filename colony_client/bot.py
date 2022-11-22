from custom_logger import Logger
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class Bot:
    def __init__(self, identifier, coinBalance, balance, coin):
        self.identifier = identifier
        self._coinBalance = coinBalance
        self._balance = balance
        self._initialBalance = balance
        self.xpos = 0
        self.ypos = 0
        self.logger = Logger()
        self.logTitle = "bot"
        self.coin = coin
        self.engine = None

    def investingState(self):
        sentiment = self.getCoinSentiment()

        match sentiment:
            case sentiment if sentiment < 0:
                return "Bad"
            case sentiment if sentiment > 0:
                return "Ok"
            case sentiment if sentiment > 5:
                return "Good"
            case sentiment if sentiment > 10:
                return "Great"
            case sentiment if sentiment > 20:
                return "Excellent"

    def sellAllCoin(self):
        if self._coinBalance != 0:
            self._balance += self.getCoinPriceEur(self._coinBalance)
            self._coinBalance = 0

    def getBalance(self):
        return self._balance

    def setBalance(self, balance):
        self._balance = balance
        return

    def getCoinBalance(self):
        return self._coinBalance

    def listenForGodMode(self):
        pass

    def investingState(self):
        pass

    def feedback(self):
        pass

    def die(self):
        pass