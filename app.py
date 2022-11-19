from custom_logger import Logger
from flask import Flask, request
from sentiment_controller import SentimentController

app = Flask(__name__)
mainController = SentimentController()
flaskLogger = Logger()
flaskLogTitle = "API"


@app.route("/api/v1/", methods=["GET"])
def index():
    return 'Sentiment Controller API'


@app.route("/api/v1/coins", methods=["GET"])
def returnJson():
    # Sends JSON file of Coin Sentiment Analysis
    coins = ["BTC", "ETH", "UDST", "BNB", "USDC", "XRP", "BUSD", "DOGE", "ADA", "SOL", "MATIC", "DOT",
             "STETH", "SHIB", "SHIB", "DAI", "TRX", "OKB", "AVAX", "UNI", "WBTC", "LTC", "ATOM", "LINK",
             "LEO", "ETC", "ALGO", "CRO", "FTT", "XMR", "XLM", "NEAR", "TON", "BHC", "QNT", "VET", "FIL",
             "FLOW", "LUNC", "CHZ", "HBAR", "APE", "ICP", "EGLD", "SAND", "AAVE", "XTZ", "FRAX", "MANA",
             "LDO", "THETA"]

    coinsJSON = {coins.index(i): i for i in coins}
    # SentimentController.coinAnalysisToJson(coins)

    return coinsJSON


@app.route('/api/v1/colony/create', methods=['POST'])
def createColony():
    requestJSON = request.get_json()
    colonyName = requestJSON["name"]
    try:
        response = mainController.createColony(colonyName)
        if response == "success":
            logMessage = 'Created colony: %s' % colonyName
            flaskLogger.debugLog(flaskLogTitle, logMessage)
            return "Success"
        else:
            logMessage = 'Colony failed: %s' % colonyName
            flaskLogger.errorLog(flaskLogTitle, logMessage)
            return "Invalid colony name"
    except:
        return "Internal Server Error"

@app.route('/api/v1/colony/<colony>', methods=['GET'])
def getColony(colony):
    colonyName = request.view_args['colony']
    try:
        result = mainController.getColony(colonyName)
    except:
        pass
    if result == None:
        return "Colony not found"
    else:
        return result

if __name__ == '__main__':
    app.run(debug=True)
