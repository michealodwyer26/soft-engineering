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

if __name__ == '__main__':
    app.run(debug=True)