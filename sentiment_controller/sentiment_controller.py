import re
import json
import string
import datetime
import sqlalchemy as db
import snscrape.modules.twitter as sntwitter
from datetime import datetime

from custom_logger import Logger
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from colony_client import bot, core_controller, god_mode_controller, visualiser

class SentimentController:

    def __init__(self):
        self.engine = None
        self.logger = Logger()
        self.logTitle = "sentiment"
        self.sia = SentimentIntensityAnalyzer()
    
    def connectToDatabase(self):
        try:
            self.engine = db.create_engine("mysql+pymysql://softwareuser:$B4s3dcrypt0$@localhost/project")
        except Exception as e:
            self.logger.errorLog(self.logTitle, str(e))

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

    # Adds a new entry of Sentiment analysis to the JSON file coins.json.
    def coinAnalysisToJson(self, coins):
        timeOfEvaluation = "Sentiment analysis of currencies for %s" % datetime.datetime.now()
        newFileData = {timeOfEvaluation: {}}

        for coin in coins:
            coinData = {coin: SentimentController().analyzeCurrency(coin)}
            newFileData[timeOfEvaluation].update(coinData)

        with open("../coins.json", "r", encoding='utf-8') as file:
            fileData = json.load(file)

        fileData.update(newFileData)

        with open("../coins.json", "w", encoding='utf-8') as file:
            self.logger.debugLog(self.logTitle, "Transferred analysis to JSON")
            json.dump(fileData, file, ensure_ascii=False, indent=4)

