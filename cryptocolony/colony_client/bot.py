import json
import asyncio
import requests
from cryptocolony.custom_logger import Logger
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class Bot:
    def __init__(self, identifier, strategy):
        self.identifier = identifier
        self._coinBalance = 0
        self._balance = 0
        self._buyInAmount = 0
        self._strategy = strategy

        self.xpos = 0
        self.ypos = 0
        self.logger = Logger()
        self.logTitle = "bot"
        self.engine = None

    def getCoinList(self):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
        parameters = {
            'symbol': '{}'.format(self.coin),
            'sort': 'rank', 
		'limit': '100'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '76bff3ac-5544-4a06-9814-8326c089a8ac',
        }

        session = Session()
        session.headers.update(headers)

        coinList = []

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            for coin in data["data"]:
                coinName = coin["symbol"]
                coinList += coinName
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        return data["data"][0]["quote"]["EUR"]["price"]

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
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        return data["data"][0]["quote"]["EUR"]["price"]


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

    def getCoinSentiment(self, coin):
        self.updateCoinRequest(coin)

        dataJSON = '{"name":"%s"}' % coin

        coinSentiment = requests.post(
            "http://65.108.214.180/api/v1/coin/update",
            data=dataJSON,
            headers={"Content-Type": "application/json"}
        )
        return coinSentiment["coinSentiment"]

    def investInCoin(self):

        coinList = self.getCoinList()

        for coin in coinList:    
            sentiment = self.getCoinSentiment(coin)

            if sentiment < 0 and self.getLeverage() == 1:
                self.buyCoin(coin)
            if sentiment > 0 and self.getLeverage() == 1:
                self.buyCoin(coin)
            if sentiment > 5 and self.getLeverage() == 2:
                self.buyCoin(coin)
            if sentiment > 10 and self.getLeverage() == 5:
                self.buyCoin(coin)
            if sentiment > 15 and self.getLeverage() == 10:
                self.buyCoin(coin)

    def buyCoin(self):
        pass

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
            case self._strategy if self._strategy == "Short" or self._strategy == "Long-term":
                return 1
            case self._strategy if self._strategy == "Medium":
                return 2 
            case self._strategy if self._strategy == "High leverage":
                return 5 
            case self._strategy if self._strategy == "Scalp":
                return 10

    def sellCoin(self):
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

    def feedback(self):
        earnings = ""
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