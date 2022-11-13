from flask import Flask, send_file
from sentiment_controller import SentimentController

app = Flask(__name__)

@app.route("/api/v1/", methods=["GET"])
def index():
    return ''

@app.route("/api/v1/coins", methods=["GET"])
def returnJson():
    # Sends JSON file of Coin Sentiment Analysis
    coins = {
                "coin": "BTC",
                "coin": "ETH",
                "coin": "UDST",
                "coin": "BNB",
                "coin": "USDC",
                "coin": "XRP",
                "coin": "BUSD",
                "coin": "DOGE",
                "coin": "ADA",
                "coin": "SOL",
                "coin": "MATIC",
                "coin": "DOT",
                "coin": "STETH",
                "coin": "SHIB",
                "coin": "SHIB",
                "coin": "DAI",
                "coin": "TRX",
                "coin": "OKB",
                "coin": "AVAX",
                "coin": "UNI",
                "coin": "WBTC",
                "coin": "LTC",
                "coin": "ATOM",
                "coin": "LINK",
                "coin": "LEO",
                "coin": "ETC",
                "coin": "ALGO",
                "coin": "CRO",
                "coin": "FTT",
                "coin": "XMR",
                "coin": "XLM",
                "coin": "NEAR",
                "coin": "TON",
                "coin": "BHC",
                "coin": "QNT",
                "coin": "VET",
                "coin": "FIL",
                "coin": "FLOW",
                "coin": "LUNC",
                "coin": "CHZ",
                "coin": "HBAR",
                "coin": "APE",
                "coin": "ICP",
                "coin": "EGLD",
                "coin": "SAND",
                "coin": "AAVE",
                "coin": "XTZ",
                "coin": "FRAX",
                "coin": "MANA",
                "coin": "LDO",
                "coin": "THETA"
    }
    coinsArray = list(coins.values())
    SentimentController.coinAnalysis2Json(coinsArray)

    return coins

if __name__ == '__main__':
    app.run(debug=True)