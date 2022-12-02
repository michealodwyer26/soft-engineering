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
        self.coin = ""

        self._buyInAmount = 0
        self._strategy = strategy
        self._initialPrice = 0

        self.xpos = 0
        self.ypos = 0
        self.logger = Logger()
        self.logTitle = "bot"
        self.engine = None

    def getCoinList(self):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
        parameters = {
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
        leverage = self.getLeverage()

        if self._balance / price > 1:
            change = (self._balance / price) - (self._balance // price)
            coinAmount = self._balance // price
            self._coinBalance += coinAmount * leverage
            self._balance -= self._balance + change

    def checkTrade(self):
        current_price = self.getCoinPriceEur(1)
        leverage = self.getLeverage()

        valueOfTrade = current_price * self._coinBalance
        initialValueOfTrade = self._initialPrice * self._coinBalance

        investedAmount = initialValueOfTrade / leverage 
        change = valueOfTrade - initialValueOfTrade

        if change <= -investedAmount:
            self.sellCoin() # Bot has lost all money
        elif change >= initialValueOfTrade * 0.10:
            self.sellCoin() # Take 10% profit for long-term trade 
        elif change >= initialValueOfTrade * 0.05 and self._strategy == "Medium":
            self.sellCoin() # Take 5% profit for medium risk trade 
        elif change >= initialValueOfTrade * 0.02 and self._strategy == "High":
            self.sellCoin() # Take 2% profit for medium risk trade 
        elif change >= initialValueOfTrade * 0.01 and self._strategy == "Scalp":
            self.sellCoin() # Take 1% profit for scalp

    def sellCoin(self):
        if self._coinBalance != 0:
            self._balance += self.getCoinPriceEur(self._coinBalance)
            self._coinBalance = 0

    async def run(self):
        coinList = self.getCoinList()

        for coin in coinList:
            sentiment = self.getCoinSentiment(coin)

            if sentiment < 0 and self.getLeverage() == 1:
                self.coin = coin
            if sentiment > 0 and self.getLeverage() == 1:
                self.coin = coin
            if sentiment > 5 and self.getLeverage() == 2:
                self.coin = coin
            if sentiment > 10 and self.getLeverage() == 5:
                self.coin = coin
            if sentiment > 15 and self.getLeverage() == 10:
                self.coin = coin
        while True:
            await asyncio.gather(self.main())

    async def main(self):
        await asyncio.sleep(10)

        if self._balance > 0:
            self.investInCoin()
        else:
            self.checkTrade()

    def getBalance(self):
        return self._balance

    def setBalance(self, balance):
        self._balance = balance
        return

    def getCoinBalance(self):
        return self._coinBalance

    def feedback(self):
        earnings = ""
        dataJSON = "{'id': '{}', 'strategy': '{}', 'balance': '{}', 'coin_balance': '{}', 'earnings': '{}', 'x': '{}', " \
                   "'y': '{}'}".format(
            self.identifier, self._strategy, self._balance, self._coinBalance, earnings, self.xpos, self.ypos)

        return dataJSON

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
