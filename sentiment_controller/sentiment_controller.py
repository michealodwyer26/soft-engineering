import re
import json
import string
import datetime
from datetime import datetime
import sqlalchemy as db
import snscrape.modules.twitter as sntwitter

from custom_logger import Logger
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from colony_client import bot, core_controller, god_mode_controller, visualiser


class SentimentController:

    def __init__(self):
        self.engine = None
        self.logger = Logger()
        self.logTitle = "sentiment"
        self.sia = SentimentIntensityAnalyzer()
        self.colonies = {}

    def connectToDatabase(self):
        try:
            self.engine = db.create_engine("mysql+pymysql://softwareuser:$B4s3dcrypt0$@localhost/project")
        except Exception as e:
            self.logger.errorLog(self.logTitle, str(e))

    def createColony(self, colony: str) -> str:
        if re.match("^[A-Za-z0-9]*$", colony):
            if colony not in self.colonies:
                self.colonies[colony] = {"bots": {}}
                return "success"
            else:
                return "failure"
        else:
            return "failure"

    def getColony(self, colony: str) -> dict:
        if colony in self.colonies:
            self.logger.debugLog(self.logTitle, "Tried to return colony %s" % colony)
            return self.colonies[colony]
        else:
            return {"Error": "Colony not found!"}

    def createBot(self, colony: str, botId: str, initialBalance: float) -> str:
        if re.match("^[A-Za-z0-9]*$", botId):
            try:
                if botId not in self.colonies[colony]["bots"]:
                    self.colonies[colony]["bots"][botId] = initialBalance
                    return "success"
                else:
                    return "failure"
            except Exception as e:
                return str(e)
        else:
            return "failure"

    def getBot(self, colony: str, botId: str) -> dict:
        if colony in self.colonies:
            if botId in self.colonies[colony]["bots"]:
                return {"id": str(botId), "balance": self.colonies[colony]["bots"][botId]}
        else:
            return {"Error": "Bot not found!"}

    def updateBot(self, colony: str, botId: str, currentBalance: float) -> str:
        if re.match("^[A-Za-z0-9]*$", botId):
            try:
                if botId in self.colonies[colony]["bots"]:
                    self.colonies[colony]["bots"][botId] = currentBalance
                    return "success"
                else:
                    return "failure"
            except Exception as e:
                return str(e)
        else:
            return "failure"

    # Handles data processing and database transfer
    def scraping(self, query: str, limit: int):
        count = 0
        tweets = []

        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            if len(tweets) == limit:
                self.logger.debugLog(self.logTitle, "Scraping complete")
                break
            else:
                count += 1
                text = re.sub(f'[^{re.escape(string.printable)}]', '', tweet.content)
                tweets.append(text)
        return tweets

    def requestListener(self):
        pass
        # API request --> API response
        # Sentiment request --> Sentiment response

    # Returns current sentiment of a coin.
    def analyzeCurrency(self, currency):
        finalSentiment = 0
        tweets = self.scraping("#" + currency, 100)
        self.connectToDatabase()

        for tweet in tweets:
            try:
                tweetSentiment = float(
                    str(self.sia.polarity_scores(tweet))
                    .strip("}")
                    .split()[-1]
                )
                finalSentiment += tweetSentiment
            except Exception as e:
                self.logger.errorLog(self.logTitle, str(e))
        logMessage = "Analysis of %s complete" % currency
        self.logger.debugLog(self.logTitle, logMessage)
        return finalSentiment


    def updateSentimentAnalysis(self, coin):
        self.connectToDatabase()
        metaData = db.MetaData(bind=self.engine)
        db.MetaData.reflect(metaData)
        
        coinAnalysis = metaData.tables["coins_current"]
        coinHistory = metaData.tables["coins_history"]

        analysis = self.analyzeCurrency(coin)

        if self.engine.execute(coinAnalysis.select().where(coinAnalysis.columns.coin == coin)).scalar() != None:
            query = coinAnalysis.update().where(coinAnalysis.columns.coin == coin).values(sentiment=analysis)
        else:
            query = coinAnalysis.insert().values(coin=coin, sentiment=analysis)
        
        self.engine.execute(query)

        query = coinHistory.insert().values(time=str(datetime.now())[0:19], coin=coin, sentiment=analysis)
        self.engine.execute(query)

        self.engine.commit()
        self.engine.close()

    def getCoinSentiment(self, coin):

        self.connectToDatabase()
        metaData = db.MetaData(bind=self.engine)
        db.MetaData.reflect(metaData)
        
        coinAnalysis = metaData.tables["coins_current"]

        query = self.engine.select([coinAnalysis.columns.sentiment]).where(coinAnalysis.columns.coin == coin)
        sentimentOfCoin = self.engine.execute(query).fetchall()

        self.engine.close()

        return sentimentOfCoin