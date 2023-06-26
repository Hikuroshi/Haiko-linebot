from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
import logging
from handlers import *
import os

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

if __name__ == '__main__':
    app.run(debug=False, port=os.getenv("PORT", default=5000))
