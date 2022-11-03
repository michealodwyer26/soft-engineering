import snscrape.modules.twitter as sntwitter
import pandas as pd
import sqlalchemy as db

try:
  engine = db.create_engine("mysql+pymysql://softwareuser:$B4s3dcrypt0$@localhost/project")
  print("Connection successful")
except Exception as e:
  print(e)


class godModeController:
    def __init__(self):
        pass

    def visualiserInputListener(self):
        pass

    def action(self):
        pass


class Agent:
    def __init__(self, balance):
        self._balance = balance

    def setBalance(self, balance):
        self._balance = balance
        return

    def addBalance(self, balance):
        self._balance += balance
        return

    def subtractBalance(self, balance):
        self._balance -= balance
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


class coreController:
    def __init__(self):
        pass

    def listenForGodMode(self):
        pass

    def visualise(self):
        pass

    def createBot(self):
        pass

    def deleteBot(self):
        pass


class sentimentController:
    def __init__(self):
        pass

    # Handles data processing and databse Transfer
    def scraping(self):
        query = "#crypto"
        tweets = []
        limit = 200 # was 500,000
        count = 0

        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            if len(tweets) == limit:
                print("Done!")
                break
            else:
                count += 1
                print(count)
                tweets.append([tweet.date, tweet.content])

        df = pd.DataFrame(tweets, columns=["Date", "Tweet"])
        #print("Dataframe transfer complete!")
        #df.to_sql("Tweets", engine, if_exists="replace", index=False)

    def requestListener(self):
        #API request --> API response
        #Sentiment request --> Sentiment response
        pass

    def databaseTransfer(self):
        pass


class Visualiser:
    def __init__(self):
        pass

    def listener(self):
        pass

    def godeModeAction():
        pass

    def coreControllerFeedbackReceiver():
        pass

    def visualise(self):
        pass

sentiment = sentimentController()
sentiment.scraping()
