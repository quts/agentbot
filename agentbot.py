# global.py
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