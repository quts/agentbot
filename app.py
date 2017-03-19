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
    StickerMessage, StickerSendMessage,
    TemplateSendMessage, ButtonsTemplate,
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
            if int(event.message.package_id) > 4:
                print "unable to handle stickers out of list"
            else:
                package_id=event.message.package_id
                sticker_id=event.message.sticker_id
                line_bot_api.reply_message( event.reply_token, 
                                            StickerSendMessage( package_id=package_id, 
                                                                sticker_id=sticker_id ) )

def LeaveEventHandler(event):
    #{"source": {"groupId": "C3fc91cd1bae9c8988d05d24b4dfa04a6", "type": "group"}, "timestamp": 1489908217481, "type": "leave"}
def JoinEventHandler(event):
    #{"replyToken": "2c110ba76aaf4961832c2cc53cc86da2", "source": {"groupId": "C3fc91cd1bae9c8988d05d24b4dfa04a6", "type": "group"}, "timestamp": 1489908317510, "type": "join"}
    objTemplate = {
                      "type": "template",
                      "altText": "this is a buttons template",
                      "template": {
                          "type": "buttons",
                          "thumbnailImageUrl": "https://example.com/bot/images/image.jpg",
                          "title": "Menu",
                          "text": "Please select",
                          "actions": [
                              {
                                "type": "postback",
                                "label": "Buy",
                                "data": "action=buy&itemid=123"
                              },
                              {
                                "type": "postback",
                                "label": "Add to cart",
                                "data": "action=add&itemid=123"
                              },
                              {
                                "type": "uri",
                                "label": "View detail",
                                "uri": "http://example.com/page/123"
                              }
                          ]
                      }
                    }
    line_bot_api.reply_message( event.reply_token, TemplateSendMessage(objTemplate) )


@handler.default()
def default(event):
    print event
    replyMsg = '%s'%event
    line_bot_api.reply_message( event.reply_token, TextSendMessage(text=replyMsg) )

if __name__ == '__main__':
    app.run(debug=True)
