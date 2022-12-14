from cryptocolony.custom_logger import Logger
from flask import Flask, request
from cryptocolony.sentiment_controller import SentimentController

app = Flask(__name__)
mainController = SentimentController()
flaskLogger = Logger()
flaskLogTitle = "API"


@app.route("/api/v1/", methods=["GET"])
def index():
    return 'Sentiment Controller API'


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
    # Fetch the JSON data from the POST request
    requestJSON = request.get_json()
    colonyName = requestJSON["colony"]
    botId = requestJSON["id"]
    botCoin = requestJSON["coin"]

    try:
        response = mainController.createBot(colonyName, botId, botCoin)  # Tells the sentiment controller to update
        # itself.

        if response == "success":
            logMessage = 'Created bot: %s' % colonyName
            flaskLogger.debugLog(flaskLogTitle, logMessage)
            return "Success"
        else:
            logMessage = 'Bot failed: %s' % botId
            flaskLogger.errorLog(flaskLogTitle, logMessage)
            flaskLogger.errorLog(flaskLogTitle, response)
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
    botId = str(botId)
    result = mainController.getBot(colony, botId)

    try:
        botCoin = mainController.getBot(colony, botId)["details"]["coinName"]
    except Exception as e:
        print("getBot error")
        return str(e)

    try:
        coinState = mainController.getCoinState(botCoin)
        result["details"]["coinState"] = coinState
    except Exception as e:
        print("getCurrentCoinState error")
        return str(e)

    if not result:
        return "Bot not found"
    else:
        return result


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


@app.route("/api/v1/coin/update", methods=["POST"])
def updateCoin():
    requestJSON = request.get_json()
    coin = requestJSON["name"]

    try:
        SentimentController().updateSentimentAnalysis(coin)
        response = "Success"
    except Exception as e:
        response = e

    return response


@app.route("/api/v1/coin/sentiment", methods=["POST"])
def getSentiment():
    requestJSON = request.get_json()
    coin = requestJSON["name"]
    response = {"coinSentiment": SentimentController().getCoinSentiment(coin)}

    return response


if __name__ == '__main__':
    app.run(debug=True)
