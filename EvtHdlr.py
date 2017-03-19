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
    TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction
)

from rating import rating
from agentbot import RATE_RESULT, REPLY_MESSAGE


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
        elif event.type == 'join':
            if event.source.type == 'group':
                return self.GroupJoinEventHandler(event)
        elif event.type == 'follow':
                return self.FollowEventHandler(event)
        elif event.type == 'unfollow':
                return self.FollowEventHandler(event)
        
        # default handler
        try:
            print event
            replyMsg = '%s'%event
            line_bot_api.reply_message( event.reply_token, TextSendMessage(text=replyMsg) )
        except Exception,e:
            print e

    def TextMessageHandler(self, event):
        if event.message.text == 'give_me_a_test':
            return self.testFunction(event)
        objRating = rating()
        bResult, replyMsg = objRating.ratingInput(event.message.text)
        if bResult:
            line_bot_api.reply_message( event.reply_token, 
                                        TextSendMessage( text=replyMsg ) )

    def StickerMessageHandler(self, event):
        if int(event.message.package_id) > 4:
            print "unable to handle stickers out of list"
        else:
            line_bot_api.reply_message( event.reply_token, 
                                        StickerSendMessage( package_id=event.message.package_id, 
                                                            sticker_id=event.message.sticker_id ) )
    def GroupJoinEventHandler(self, event):
            line_bot_api.reply_message( event.reply_token, 
                                        TextSendMessage( text=REPLY_MESSAGE.GROUP_JOINED ) )

    def UnfollowEventHandler(self, event):
        return 0

    def FollowEventHandler(self, event):
            line_bot_api.reply_message( event.reply_token, 
                                        TextSendMessage( text=REPLY_MESSAGE.FRIEND_ADDED ) )

    def testFunction(self, event):
            line_bot_api.reply_message( event.reply_token, 
                                        TemplateSendMessage( type="template",
                                                             altText="this is a buttons template",
                                                             template=ButtonsTemplate(type                = 'buttons',
                                                                                      text                = 'Please select',
                                                                                      title               = 'Menu',
                                                                                      thumbnail_image_url = 'https://example.com/bot/images/image.jpg',
                                                                                      actions             = PostbackTemplateAction(type  = 'postback',
                                                                                                                                   label = 'View detail',
                                                                                                                                   text  = 'text'))))
