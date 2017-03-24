# global.py
from linebot.models import (
    TemplateSendMessage, ButtonsTemplate, URITemplateAction, 
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

    GROUP_JOINED = 'Hi All, thanks for the invitation! I am agent Monkey, who want to make your chat room more safety.'
    FRIEND_ADDED = 'Hi There, thanks for adding me as friend! I am agent Monkey, who want to make your chat room more safety.'

class REPLY_TEMPLATE(object):
    def __init__(self):
        print 'Object Created'

    def ButtonsTemplate_URL(self, strURL, strRplyMsg):
        return TemplateSendMessage( alt_text=strRplyMsg,
                                    template=ButtonsTemplate(
                                    text=strURL,
                                    actions=[ URITemplateAction( label=REPLY_MESSAGE.TEMPLATE_BUTTON_GOTO, uri=strURL )]))