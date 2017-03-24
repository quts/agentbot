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
    TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction,
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
        try:
            buttons_template_message = TemplateSendMessage(
                                                                alt_text='Buttons template',
                                                                template=ButtonsTemplate(
                                                                    thumbnail_image_url='https://example.com/image.jpg',
                                                                    title='Menu',
                                                                    text='Please select',
                                                                    actions=[
                                                                        PostbackTemplateAction(
                                                                            label='postback',
                                                                            text='postback text',
                                                                            data='action=buy&itemid=1'
                                                                        ),
                                                                        MessageTemplateAction(
                                                                            label='message',
                                                                            text='message text'
                                                                        ),
                                                                        URITemplateAction(
                                                                            label='uri',
                                                                            uri='http://example.com/'
                                                                        )
                                                                    ]
                                                                )
                                                            )
            line_bot_api.reply_message( event.reply_token, 
                                        buttons_template_message)
        except Exception,e:
            line_bot_api.reply_message( event.reply_token, 
                                        TextSendMessage( text='%s'%e ) )

