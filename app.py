import os
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, 
    TextMessage, TextSendMessage, 
)

from EvtHdlr import EventHandler

app = Flask(__name__)
CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET       = os.environ['CHANNEL_SECRET']
LOCAL_STRING         = os.environ['LOCAL_STRING']
line_bot_api         = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler              = WebhookHandler(CHANNEL_SECRET)

@app.route('/')
def home():
    return 'HTTP 200 : %s'%LOCAL_STRING

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.default()
def defaultHandler(event):
    objEvent = EventHandler(event)

if __name__ == '__main__':
    app.run(debug=True)
