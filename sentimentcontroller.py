import pandas as pd
import sqlalchemy as db
import snscrape.modules.twitter as sntwitter

class sentimentController:

    def __init__(self):
        self.engine = None
    
    def connectToDatabase(self):
        try:
            self.engine = db.create_engine("mysql+pymysql://softwareuser:$B4s3dcrypt0$@localhost/project")
            print("Connection successful")
        except Exception as e:
            print(e)

    # Handles data processing and database transfer
    def scraping(self, query: str, limit: int):
        
        count = 0
        tweets = []
        
        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            if len(tweets) == limit:
                print("Done!")
                break
            else:
                count += 1
                print(count)
                tweets.append([tweet.date, tweet.content])

        df = pd.DataFrame(tweets, columns=["Date", "Tweet"])
        print("Dataframe transfer complete!") # Replace with logging to Grafana
        df.to_sql("Tweets", self.engine, if_exists="replace", index=False)

    def requestListener(self):
        pass
        # API request --> API response
        # Sentiment request --> Sentiment response
        


#sentiment = sentimentController()
#sentiment.connectToDatabase()
#sentiment.scraping("#crypto", 100)
