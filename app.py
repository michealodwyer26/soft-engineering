from flask import Flask, request
from sentiment_controller import SentimentController

app = Flask(__name__)

@app.route("/api/v1/", methods=["GET"])
def index():
    return ''

@app.route("/api/v1/updateCoin", methods=["POST"])
def updateCoin(coin):
    requestJSON = request.get_json()
    coin = requestJSON["name"]

    SentimentController().updateSentimentAnalysis(coin)

    return "Success"

@app.route("/api/v1/getCoinSentiment", methods=["POST"])
def updateCoin(coin):
    requestJSON = request.get_json()
    coin = requestJSON["name"]

    coinSentiment = SentimentController().getCoinSentiment(coin)

    return coinSentiment

if __name__ == '__main__':
    #app.run(debug=True)

    coins = ["BTC", "ETH", "UDST", "BNB", "USDC", "XRP", "BUSD", "DOGE", "ADA", "SOL", "MATIC", "DOT",
        "STETH", "SHIB", "SHIB", "DAI", "TRX", "OKB", "AVAX", "UNI", "WBTC", "LTC", "ATOM", "LINK",
        "LEO", "ETC", "ALGO", "CRO", "FTT", "XMR", "XLM", "NEAR", "TON", "BHC", "QNT", "VET", "FIL", 
        "FLOW", "LUNC", "CHZ", "HBAR", "APE", "ICP", "EGLD", "SAND", "AAVE", "XTZ", "FRAX", "MANA", 
        "LDO", "THETA"]

    for coin in coins:
        print( "{}: {}".format(coin, SentimentController().analyzeCurrency(coin)))