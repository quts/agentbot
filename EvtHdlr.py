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
    TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction, ConfirmTemplate
)

from rating import rating
from agentbot import RATE_RESULT, REPLY_MESSAGE, DATA_TYPE, REPLY_TEMPLATE


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
            elif event.message.type == 'sticker': 
                return self.StickerMessageHandler(event)
            elif event.message.type == 'location': 
                return self.LocationMessageHandler(event)
        elif event.type == 'join':
            if event.source.type == 'group':
                return self.GroupJoinEventHandler(event)
        elif event.type == 'follow':
            return self.FollowEventHandler(event)
        elif event.type == 'unfollow':
            return self.FollowEventHandler(event)
        elif event.type == 'postback':
            return self.PostBackEventHandler(event)

    def TextMessageHandler(self, event):
        objRating  = rating()
        dictReturn = objRating.ratingInput(event.message.text)
        print dictReturn
        if dictReturn['Enable']:
            if DATA_TYPE.TYPE_URL == dictReturn['type']:
                objTemplate = REPLY_TEMPLATE()
                buttons_template_message = objTemplate.ButtonsTemplate_URL(dictReturn['data'], dictReturn['Message'])
                line_bot_api.reply_message( event.reply_token, 
                                            buttons_template_message )           
            else:
                line_bot_api.reply_message( event.reply_token, 
                                            TextSendMessage( text=dictReturn['Message'] ) )

    def StickerMessageHandler(self, event):
        if int(event.message.package_id) > 4:
            print "unable to handle stickers out of list"
        else:
            line_bot_api.reply_message( event.reply_token, 
                                        StickerSendMessage( package_id=event.message.package_id, 
                                                            sticker_id=event.message.sticker_id ) )
    def LocationMessageHandler(self, event):
        objTemplate = REPLY_TEMPLATE()
        buttons_template_message = objTemplate.ButtonsTemplate_Location(event.message.address, event.message.latitude, event.message.longitude)
        line_bot_api.reply_message( event.reply_token, 
                                    buttons_template_message )

    def GroupJoinEventHandler(self, event):
        objTemplate = REPLY_TEMPLATE()
        buttons_template_message = objTemplate.ButtonsTemplate_GroupJoinMessage()
        line_bot_api.reply_message( event.reply_token, 
                                    buttons_template_message )

    def UnfollowEventHandler(self, event):
        print event

    def FollowEventHandler(self, event):
        objTemplate = REPLY_TEMPLATE()
        buttons_template_message = objTemplate.ButtonsTemplate_JoinMessage()
        line_bot_api.reply_message( event.reply_token, 
                                    buttons_template_message )

    def PostBackEventHandler(self, event):
        if event.postback.data == 'EVENT_HELP_MESSAGE':
            line_bot_api.reply_message( event.reply_token, 
                                        TextSendMessage( text=REPLY_MESSAGE.HELP_MESSAGE ) )           
