from flask import Flask, send_file
from sentiment_controller import SentimentController

app = Flask(__name__)

@app.route("/api/v1/", methods=["GET"])
def index():
    return ''

@app.route("/api/v1/coins", methods=["GET"])
def returnJson():
    # Sends JSON file of Coin Sentiment Analysis
    coins = ["BTC", "ETH", "UDST", "BNB", "USDC", "XRP", "BUSD", "DOGE", "ADA", "SOL", "MATIC", "DOT",
        "STETH", "SHIB", "SHIB", "DAI", "TRX", "OKB", "AVAX", "UNI", "WBTC", "LTC", "ATOM", "LINK",
        "LEO", "ETC", "ALGO", "CRO", "FTT", "XMR", "XLM", "NEAR", "TON", "BHC", "QNT", "VET", "FIL",
        "FLOW", "LUNC", "CHZ", "HBAR", "APE", "ICP", "EGLD", "SAND", "AAVE", "XTZ", "FRAX", "MANA",
        "LDO", "THETA"]

    coinsJSON = {coins.index(i): i for i in coins}
    #SentimentController.coinAnalysisToJson(coins)

    return coinsJSON

if __name__ == '__main__':
    app.run(debug=True)