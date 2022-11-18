from custom_logger import Logger
import sqlalchemy as db
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class Bot:
    def __init__(self, identifier, balance, coin):
        self.identifier = identifier
        self._balance = balance
        self.xpos = 0
        self.ypos = 0
        self.logger = Logger()
        self.logTitle = "bot"
        self.coin = coin
        self.engine = None

    def connectToDatabase(self):
        try:
            self.engine = db.create_engine("mysql+pymysql://softwareuser:$B4s3dcrypt0$@localhost/project")
        except Exception as e:
            self.logger.errorLog(self.logTitle, str(e))

    def updateCoinRequest(self):
        dataJSON = '{"name":"%s"}' % self.coin
        
        requests.post(
            "http://65.108.214.180/api/v1/updateCoin",
            data=dataJSON,
            headers={"Content-Type": "application/json"}
        )

    def getCoinSentiment(self):
        self.updateCoinRequest()

        self.connectToDatabase()
        metaData = db.MetaData(bind=self.engine)
        db.MetaData.reflect(metaData)
        
        coinAnalysis = metaData.tables["coins_current"]

        query = self.engine.select([coinAnalysis.columns.sentiment]).where(coinAnalysis.columns.coin == self.coin)
        sentimentOfCoin = self.engine.execute(query).fetchall()

        self.engine.close()

        return sentimentOfCoin

    def getCoinPriceEur(self):
        url = 'https://pro-api.coinmarketcap.com/v2/tools/price-conversion'
        parameters = {
        'symbol':'{}'.format(self.coin),
        'amount':'{}'.format(self.getBalance()),
        'convert':'EUR'
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