import re
import os
import string
import datetime
import pymysql
from datetime import datetime
import snscrape.modules.twitter as sntwitter

from custom_logger import Logger
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from colony_client import bot, core_controller, god_mode_controller, visualiser


class SentimentController:

    def __init__(self):
        self.colonies = {}
        self.logger = Logger()
        self.logTitle = "sentiment"
        self.sia = SentimentIntensityAnalyzer()

    def connectToDatabase(self):
        sql_user = os.environ.get("SQL_USER")
        sql_pass = os.environ.get("SQL_PASS")
        try:
            connection = pymysql.connect(host='localhost',
                                         user=sql_user,
                                         password=sql_pass,
                                         database='project',
                                         cursorclass=pymysql.cursors.DictCursor)
            return connection
        except Exception as e:
            self.logger.errorLog(self.logTitle, str(e))
            return None

    def createColony(self, colony: str) -> str:
        if re.match("^[A-Za-z0-9]*$", colony):
            if colony not in self.colonies:
                self.colonies[colony] = {"bots": []}
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

    def createBot(self, colony: str, botId: str, botCoin: str) -> str:
        if re.match("^[A-Za-z0-9]*$", botId):
            try:
                for botData in self.colonies[colony]["bots"]:
                    if botData["id"] == botId:
                        return "failure"

                self.colonies[colony]["bots"].append({"id": botId, "coinAmount": 0, "coinName": botCoin})
                return "success"

            except Exception as e:
                return str(e)
        else:
            return "failure"

    def getBot(self, colony: str, botId: str) -> dict:
        if colony in self.colonies:
            if botId in self.colonies[colony]["bots"]:
                return {
                    "id": str(botId),
                    "details": {
                        "balance": self.colonies[colony]["bots"][botId]["coinAmount"],
                        "coinName": self.colonies[colony]["bots"][botId]["coinName"]
                    }
                }
        else:
            return {"Error": "Bot not found!"}

    def updateBot(self, colony: str, botId: str, currentBalance: float) -> str:
        if re.match("^[A-Za-z0-9]*$", botId):
            try:
                if botId in self.colonies[colony]["bots"]:
                    self.colonies[colony]["bots"][botId]["coinAmount"] = currentBalance
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

    # Assumes that the coin already exists in the database.
    def updateSentimentAnalysis(self, coin: str):

        analysis = self.analyzeCurrency(coin)
        connection = self.connectToDatabase()

        if connection:
            with connection:
                with connection.cursor() as cursor:
                    query = "UPDATE coins_current SET sentiment = %s WHERE coin == %s"
                    try:
                        cursor.execute(query, (coin, analysis))
                        connection.commit()
                    except Exception as e:
                        message = str(e)
                        self.logger.errorLog(message)

    def getCoinSentiment(self, coin):

        connection = self.connectToDatabase()

        if connection:
            with connection:
                with connection.cursor() as cursor:
                    query = "SELECT coin FROM coins_current WHERE coin == %s"
                    try:
                        result = cursor.execute(query, (coin,))
                        return result
                    except Exception as e:
                        message = str(e)
                        self.logger.errorLog(message)
