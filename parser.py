import re
from agentbot import DATA_TYPE

class Parser(object):
	def __init__(self):
		self.dataType  = DATA_TYPE.TYPE_UNDEFINE
		self.strOutput = False
	def classify(self, strInput):
		if self.parseURL(strInput):
			print 'URL found : %s'%self.strOutput
		else:
			print 'Found Nothing'

		if self.dataType == DATA_TYPE.TYPE_UNDEFINE:
			return False, False

		if self.dataType == DATA_TYPE.TYPE_URL:
			return self.dataType, self.strOutput

	def parseURL(self, strInput):
		reURL = re.compile('([Hh][Tt][Tt][Pp][Ss]?\:\S+)')
		lstMatch = reURL.findall(strInput)
		if(len(lstMatch)>0):
			self.strOutput = lstMatch[0]
			self.dataType = DATA_TYPE.TYPE_URL
			return True
		return False

if __name__ == '__main__':
	parser = Parser()
	print parser.classify('test message http://www.googlde.com')