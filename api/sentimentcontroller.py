# Dependencies
# 
# pandas, sqlalchemy, snscrape, vaderSentiment

import pandas as pd
import sqlalchemy as db
import snscrape.modules.twitter as sntwitter

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
        self.connectToDatabase()
        tweets = self.scraping("#" + currency, 100)
        
        
        final_sentiment = 0

        for tweet in tweets:         
            tweet_sentiment = float(str(self.sia.polarity_scores(tweet)).strip("}").split()[-1])
            final_sentiment += tweet_sentiment

        return final_sentiment

coins = ["BTC", "ETH", "UDST", "BNB", "USDC", "XRP", "BUSD", "DOGE", "ADA", "SOL", "MATIC", "DOT",
        "STETH", "SHIB", "SHIB", "DAI", "TRX", "OKB", "AVAX", "UNI", "WBTC", "LTC", "ATOM", "LINK",
        "LEO", "ETC", "ALGO", "CRO", "FTT", "XMR", "XLM", "NEAR", "TON", "BHC", "QNT", "VET", "FIL", 
        "FLOW", "LUNC", "CHZ", "HBAR", "APE", "ICP", "EGLD", "SAND", "AAVE", "XTZ", "FRAX", "MANA", 
        "LDO", "THETA"]

print("Sentiment analysis of currencies for " + str(datetime.datetime.now()))
for coin in coins:
    print( "{}: {}".format(coin, sentimentController().analyzeCurrency(coin)))
