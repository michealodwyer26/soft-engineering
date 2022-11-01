import snscrape.modules.twitter as sntwitter
import pandas as pd


class godModeController:
    def __init__(self):
        pass

    def visualiserInputListener(self):
        pass

    def action(self):
        pass


class Agent:
    def __init__(self):
        pass

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
        query = "crypto"
        tweets = []
        limit = 200

        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            if len(tweets) == limit:
                break
            else:
                tweets.append([tweet.date, tweet.user.username, tweet.content])

        df = pd.DataFrame(tweets, columns=["Date", "User", "Tweet"])
        print(df)

        # saves to csv file
        # df.to_csv('tweets.csv')

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
