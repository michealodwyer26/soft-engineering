from flask import Flask, send_file
from sentiment_controller import SentimentController

app = Flask(__name__)

@app.route("/api/v1/", methods=["GET"])
def index():
    return ''

@app.route("/api/v1/updateCoin/<coin>", methods=["GET"])
def updateCoin(coin):
    print(coin)

    SentimentController().updateSentimentAnalysis(coin)

    return "Success"

if __name__ == '__main__':
    app.run(debug=True)