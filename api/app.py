from flask import Flask, jsonify, send_file
import mysql.connector as db
from sentimentcontroller import SentimentController
import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return '<a href="coinsJSON"> JSON of coin analysis <a/>'

@app.route("/coinsJSON", methods=["GET", "POST"])
def returnJson():
    # Sends JSON file of Coin Sentiment Analysis
    
    coins = ["BTC", "ETH", "UDST", "BNB", "USDC", "XRP", "BUSD", "DOGE", "ADA", "SOL", "MATIC", "DOT",
             "STETH", "SHIB", "SHIB", "DAI", "TRX", "OKB", "AVAX", "UNI", "WBTC", "LTC", "ATOM", "LINK",
             "LEO", "ETC", "ALGO", "CRO", "FTT", "XMR", "XLM", "NEAR", "TON", "BHC", "QNT", "VET", "FIL",
             "FLOW", "LUNC", "CHZ", "HBAR", "APE", "ICP", "EGLD", "SAND", "AAVE", "XTZ", "FRAX", "MANA",
             "LDO", "THETA"]

    SentimentController.coinAnalysis2Json(coins)
    
    return send_file("../coins.json", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)