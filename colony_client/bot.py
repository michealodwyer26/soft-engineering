import json
import asyncio
import requests
from custom_logger import Logger
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class Bot:
    def __init__(self, identifier, coin):
        self.identifier = identifier
        self._coinBalance = 0
        self._balance = 0
        self.xpos = 0
        self.ypos = 0
        self.logger = Logger()
        self.logTitle = "bot"
        self.coin = coin
        self.engine = None

    # A request to the server is made to perform sentiment analysis on self.coin
    def updateCoinRequest(self):
        dataJSON = '{"name":"%s"}' % self.coin
        try:
            requests.post(
                "http://65.108.214.180/api/v1/coin/sentiment",
                data=dataJSON,
                headers={"Content-Type": "application/json"}
            )
        except Exception as e:
            message = str(e)
            self.logger.errorLog("bot", message)

    def getCoinSentiment(self):
        self.updateCoinRequest(self.coin)

        dataJSON = '{"name":"%s"}' % self.coin

        coinSentiment = requests.post(
            "http://65.108.214.180/api/v1/coin/update",
            data=dataJSON,
            headers={"Content-Type": "application/json"}
        )
        return coinSentiment["coinSentiment"]

    def investInCoin(self):
        sentiment = self.investingState()

        match sentiment:
            case "Excellent":
                amount = self._balance / 0.90
            case "Great":
                amount = self._balance / 0.75
            case "Good":
                amount = self._balance / 0.5
            case "Ok":
                amount = 0
            case "Bad":
                self.sellCoin()

        price = self.getCoinPriceEur(1)

        if amount / price > 1:
            change = (amount / price) - (amount // price)
            coinAmount = amount // price
            self._coinBalance += coinAmount
            self._balance -= amount + change

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

    def getCoinPriceEur(self, amount):
        url = 'https://pro-api.coinmarketcap.com/v2/tools/price-conversion'
        parameters = {
            'symbol': '{}'.format(self.coin),
            'amount': '{}'.format(amount),
            'convert': 'EUR'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '76bff3ac-5544-4a06-9814-8326c089a8ac',
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            print("Worth of balance in EUR: {}".format(data["data"][0]["quote"]["EUR"]["price"]))
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        return data["data"][0]["quote"]["EUR"]["price"]

    def getBalance(self):
        return self._balance

    def setBalance(self, balance):
        self._balance = balance
        return

    def getCoinBalance(self):
        return self._coinBalance

    def listenForGodMode(self):
        pass

    def feedback(self):
        earnings = self._balance - self._initialBalance
        dataJSON = "{'id': '{}', 'coin': '{}', 'balance': '{}', 'coin_balance': '{}', 'earnings': '{}', 'x': '{}', 'y': '{}'}".format(
            self.identifier, self.coin, self._balance, self._coinBalance, earnings, self.xpos, self.ypos)

        return dataJSON

    def die(self):
        pass

    async def run(self):
        while True:
            await asyncio.gather(self.main())

    async def main(self):
        await asyncio.sleep(10)
        self.investInCoin()
