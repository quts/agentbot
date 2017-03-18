import os
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from rating import rating

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

@handler.add(MessageEvent, message=TextMessage)
def TextMessageHandler(event):
    print event
    if event.type == 'message':
        if event.message.type == 'text':
            objRating = rating()
            bResult, replyMsg = objRating.ratingInput(event.message.text)
            if bResult:
                line_bot_api.reply_message( event.reply_token, 
                                            TextSendMessage( text=replyMsg ) )

@handler.add(MessageEvent, message=StickerMessage)
def StickerMessageHandler(event):
    print event
     if event.type == 'message':
        if event.message.type == 'sticker':   
            line_bot_api.reply_message( event.reply_token, 
                                        StickerSendMessage( package_id=event.message.packageId, 
                                                            sticker_id=event.message.stickerId ) )

@handler.default()
def default(event):
    print event
    replyMsg = '%s'%event
    line_bot_api.reply_message( event.reply_token, TextSendMessage(text=replyMsg) )

if __name__ == '__main__':
    app.run(debug=True)
