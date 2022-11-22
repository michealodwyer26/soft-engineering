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
    colonyName = str(requestJSON["name"])
    try:
        response = mainController.createColony(colonyName)
        if response == "success":
            logMessage = 'Created colony: %s' % colonyName
            flaskLogger.debugLog(flaskLogTitle, logMessage)
            returnMessage = "Created colony '%s'" % colonyName
            return returnMessage
        else:
            logMessage = 'Colony failed: %s' % colonyName
            flaskLogger.errorLog(flaskLogTitle, logMessage)
            returnMessage = "Invalid colony name '%s'" % colonyName
            return returnMessage
    except Exception as e:
        print(e)
        exceptionMessage = "Unhandled error: %s" % str(e)
        return exceptionMessage


@app.route('/api/v1/bot/create', methods=['POST'])
def createBot():
    requestJSON = request.get_json()
    colonyName = requestJSON["colony"]
    botId = requestJSON["id"]
    try:
        response = mainController.createBot(colonyName, botId, 0.0)
        if response == "success":
            logMessage = 'Created bot: %s' % colonyName
            flaskLogger.debugLog(flaskLogTitle, logMessage)
            return "Success"
        else:
            logMessage = 'Bot failed: %s' % botId
            flaskLogger.errorLog(flaskLogTitle, logMessage)
            return response
    except Exception as e:
        return str(e)


@app.route('/api/v1/bot/update', methods=['POST'])
def updateBot():
    requestJSON = request.get_json()
    colonyName = requestJSON["colony"]
    botId = requestJSON["id"]
    newBalance = requestJSON["balance"]
    try:
        response = mainController.updateBot(colonyName, botId, newBalance)
        if response == "success":
            logMessage = 'Updated bot: %s' % colonyName
            flaskLogger.debugLog(flaskLogTitle, logMessage)
            returnMessage = "Updated balance to %s" % newBalance
            return returnMessage
        else:
            logMessage = 'Update failed: %s' % botId
            flaskLogger.errorLog(flaskLogTitle, logMessage)
            return response
    except Exception as e:
        return str(e)


@app.route('/api/v1/colony/<colony>/<botId>')
def getBot(colony: str, botId: int):
    try:
        botId = str(botId)
        result = mainController.getBot(colony, botId)
        if not result:
            return "Bot not found"
        else:
            return result
    except Exception as e:
        return e


@app.route('/api/v1/colony/<colony>')
def getColony(colony: str):
    try:
        result = mainController.getColony(colony)
        if not result:
            return "Colony not found"
        else:
            return result
    except Exception as e:
        return e


if __name__ == '__main__':
    app.run(debug=True)
