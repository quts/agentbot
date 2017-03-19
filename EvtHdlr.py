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
)

from rating import rating

app = Flask(__name__)
CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET       = os.environ['CHANNEL_SECRET']
LOCAL_STRING         = os.environ['LOCAL_STRING']
line_bot_api         = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler              = WebhookHandler(CHANNEL_SECRET)

class EventHandler(object):
    def __init__(self, event):
        if event.type == 'message':
            if event.message.type == 'text':
                return self.TextMessageHandler(event)
            if event.message.type == 'sticker': 
                return self.StickerMessageHandler(event)
        
        # default handler
        try:
            print event
            replyMsg = '%s'%event
            line_bot_api.reply_message( event.reply_token, TextSendMessage(text=replyMsg) )
        except Exception,e:
            print e

    def TextMessageHandler(self, event):
        objRating = rating()
        bResult, replyMsg = objRating.ratingInput(event.message.text)
        if bResult:
            line_bot_api.reply_message( event.reply_token, 
                                        TextSendMessage( text=replyMsg ) )

    def StickerMessageHandler(self, event):
        if int(event.message.package_id) > 4:
            print "unable to handle stickers out of list"
        else:
            package_id=event.message.package_id
            sticker_id=event.message.sticker_id
            line_bot_api.reply_message( event.reply_token, 
                                        StickerSendMessage( package_id=package_id, 
                                                            sticker_id=sticker_id ) )