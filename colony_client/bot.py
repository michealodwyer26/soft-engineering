import json
import asyncio
import requests
from custom_logger import Logger
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class Bot:
    def __init__(self, identifier, strategy):
        self.identifier = identifier
        self._coinBalance = 0
        self._balance = 0
        self._initialPrice = 0
        self._strategy = strategy

        self.xpos = 0
        self.ypos = 0
        self.logger = Logger()
        self.logTitle = "bot"
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
                self._strategy = "Scalp"
            case "Great":
                self._strategy = "High leverage"
            case "Good":
                self._strategy = "Medium leverage"
            case "Ok":
                self._strategy = "Long-term"
            case "Bad":
                self._strategy = "Short"

        price = self.getCoinPriceEur(1)

        if amount / price > 1:
            change = (amount / price) - (amount // price)
            coinAmount = amount // price
            self._coinBalance += coinAmount
            self._balance -= amount + change

    def checkTrade(self):
        current_price = self.getCoinPriceEur(1)
        leverage = self.getLeverage()

        valueOfTrade = current_price * self._coinBalance
        initialValueOfTrade = self._initialPrice * self._coinBalance

        investedAmount = initialValueOfTrade / leverage 
        change = valueOfTrade - initialValueOfTrade

        if change <= -investedAmount:
            self.sellCoin()

    def getLeverage(self):
        match self._strategy:
            case self._strategy if self._strategy == "Short" or self._investment_strategy == "Long-term":
                return 1
            case self._strategy if self._strategy == "Medium":
                return 2 
            case self._strategy if self._strategy == "High leverage":
                return 5 
            case self._strategy if self._strategy == "High leverage":
                return 10


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

    def sellCoin(self):
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

    def feedback(self):
        dataJSON = "{'id': '{}', 'coin': '{}', 'balance': '{}', 'coin_balance': '{}', 'earnings': '{}', 'x': '{}', 'y': '{}'}".format(
            self.identifier, self.coin, self._balance, self._coinBalance, earnings, self.xpos, self.ypos)

        return dataJSON

    async def run(self):
        while True:
            await asyncio.gather(self.main())

    async def main(self):
        await asyncio.sleep(10)

        if self._balance > 0:
            self.investInCoin()
        else:
            self.checkTrade()

        # 1. Long-term ("Ok sentiment")
        # Balance < 100
        # Invest with no leverage

        # self.setBalance(100)
        # self.investInCoin()

        # 2. Medium leverage ("Good" sentiment)
        # Balance < 500
        # 2x leverage

        # self.setBalance(500)
        #

        # 3. Higher leverage ("Great")
        # Balance < 1000
        # 5x leverage

        # 4. Scalp ("Excellent")
        # Balance < 2000
        # 10x leverage