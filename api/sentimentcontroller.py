# Dependencies
# 
# pandas, sqlalchemy, snscrape, vaderSentiment, json

import pandas as pd
import sqlalchemy as db
import snscrape.modules.twitter as sntwitter
import json

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re, string, datetime

class sentimentController:

    def __init__(self):
        self.engine = None
        self.sia = SentimentIntensityAnalyzer()
    
    def connectToDatabase(self):
        try:
            self.engine = db.create_engine("mysql+pymysql://softwareuser:$B4s3dcrypt0$@localhost/project")
        except Exception as e:
            print(e)

    # Handles data processing and database transfer
    def scraping(self, query: str, limit: int):
        
        count = 0
        tweets = []
        
        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            if len(tweets) == limit:
                break
            else:
                count += 1
                text = re.sub(f'[^{re.escape(string.printable)}]', '', tweet.content)
                tweets.append(text)

        #df = pd.DataFrame(tweets, columns=["Date", "Tweet"])
        #print("Dataframe transfer complete!") # Replace with logging to Grafana
        #df.to_sql("Tweets", self.engine, if_exists="replace", index=False)

        return tweets

    def requestListener(self):
        pass
        # API request --> API response
        # Sentiment request --> Sentiment response
    
    def analyzeCurrency(self, currency):
        # Returns current sentiment of a coin.

        self.connectToDatabase()
        tweets = self.scraping("#" + currency, 100)
        
        final_sentiment = 0

        for tweet in tweets:         
            tweet_sentiment = float(str(self.sia.polarity_scores(tweet)).strip("}").split()[-1])
            final_sentiment += tweet_sentiment

        return final_sentiment

    def coinAnalysis2Json(coins):
        # Adds a new entry of Sentiment analysis to the JSON file coins.json.

        timeOfEvaluation = "Sentiment analysis of currencies for " + str(datetime.datetime.now())
        newFileData = {timeOfEvaluation: {}}

        for coin in coins:
            coinData = {coin: sentimentController().analyzeCurrency(coin)}
            newFileData[timeOfEvaluation].update(coinData)

        with open("coins.json", "r", encoding='utf-8') as file:

            fileData = json.load(file)  
        
        file.close()

        fileData.update(newFileData)
            
        with open("coins.json", "w", encoding='utf-8') as file:

            json.dump(fileData, file, ensure_ascii=False, indent=4)

        file.close()




