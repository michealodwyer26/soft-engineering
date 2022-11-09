from flask import Flask, jsonify
import mysql.connector as db
from sentimentcontroller import sentimentController
import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    print("Sentiment analysis of currencies for " + str(datetime.datetime.now()))

    coins = ["BTC", "ETH", "UDST", "BNB", "USDC", "XRP", "BUSD", "DOGE", "ADA", "SOL", "MATIC", "DOT",
             "STETH", "SHIB", "SHIB", "DAI", "TRX", "OKB", "AVAX", "UNI", "WBTC", "LTC", "ATOM", "LINK",
             "LEO", "ETC", "ALGO", "CRO", "FTT", "XMR", "XLM", "NEAR", "TON", "BHC", "QNT", "VET", "FIL",
             "FLOW", "LUNC", "CHZ", "HBAR", "APE", "ICP", "EGLD", "SAND", "AAVE", "XTZ", "FRAX", "MANA",
             "LDO", "THETA"]

    for coin in coins:  
        print("{}: {}".format(coin, sentimentController().analyzeCurrency(coin)))
    
    return "Hello"

if __name__ == '__main__':
    app.run(debug=True)