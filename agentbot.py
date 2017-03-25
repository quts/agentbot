# global.py
from linebot.models import (
    TemplateSendMessage, ButtonsTemplate, URITemplateAction, MessageTemplateAction, ConfirmTemplate
)

class RATE_RESULT:
    NOT_FOUND  = 0
    FOUND      = 1
    GOOD       = 1000
    SUSPICIOUS = 1010
    DANGER     = 1020

class DATA_TYPE:
    TYPE_UNDEFINE = 2000
    TYPE_URL      = 2010

class REPLY_MESSAGE:
    DANGER_URL  = '%s might not a safe website'
    NORMAL_URL  = '%s is a safe website'
    UNKNOWN_URL = 'Nobody consider %s is danger'

    TEMPLATE_BUTTON_GOTO = 'Go To'
    TEMPLATE_BUTTON_HELP = 'What Can I do?'

    GROUP_JOINED = 'Hi All, thanks for the invitation! I am agent Monkey, who want to make your chat room more safety.'
    FRIEND_ADDED = 'Hi There, thanks for adding me as friend! I am agent Monkey, who want to make your chat room more safety.'

    HELP_MESSAGE = 'I can scan URLs be mentioned in your chat room, and tell you if it is safe or not!'

class REPLY_TEMPLATE(object):
    def __init__(self):
        print 'Object Created'

    def ButtonsTemplate_URL(self, strURL, strRplyMsg):
        return TemplateSendMessage( alt_text=strRplyMsg,
                                    template=ButtonsTemplate(
                                        text=strRplyMsg,
                                        actions=[ URITemplateAction( label=REPLY_MESSAGE.TEMPLATE_BUTTON_GOTO, 
                                                                     uri=strURL )]))

    def ButtonsTemplate_JoinMessage(self):
        return TemplateSendMessage( alt_text=REPLY_MESSAGE.FRIEND_ADDED,
                                    template=ButtonsTemplate( text=REPLY_MESSAGE.FRIEND_ADDED,
                                                              actions=[ MessageTemplateAction( label=REPLY_MESSAGE.TEMPLATE_BUTTON_HELP, 
                                                                                               text=REPLY_MESSAGE.HELP_MESSAGE ) ] ) )

    def ButtonsTemplate_GroupJoinMessage(self):
        '''
        return TemplateSendMessage( alt_text=REPLY_MESSAGE.GROUP_JOINED,
                                    template=ButtonsTemplate( text=REPLY_MESSAGE.GROUP_JOINED,
                                                              actions=[ MessageTemplateAction( label=REPLY_MESSAGE.TEMPLATE_BUTTON_HELP, 
                                                                                               text=REPLY_MESSAGE.HELP_MESSAGE ) ] ) )
        '''
        return TemplateSendMessage( alt_text=REPLY_MESSAGE.GROUP_JOINED,
                                    template=ConfirmTemplate( text=REPLY_MESSAGE.GROUP_JOINED, 
                                                              actions=[ PostbackTemplateAction( label=REPLY_MESSAGE.TEMPLATE_BUTTON_HELP,
                                                                                                data='EVENT_HELP_MESSAGE' ) ] ) )
