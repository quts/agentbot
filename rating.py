from parser import Parser, DATA_TYPE
from virustotalapi import VirusTotalAPI
from agentbot import RATE_RESULT, REPLY_MESSAGE

class rating(object):
	def __init__(self):
		self.ratingResult = RATE_RESULT.NOT_FOUND

	def ratingInput(self, strInput):
		dataParser = Parser()
		dataType, strStringToScan = dataParser.classify(strInput)

		if dataType == DATA_TYPE.TYPE_URL:
			virustotal = VirusTotalAPI()
			returnCode, totalscaned, positive = virustotal.scanURL(strStringToScan)

			if RATE_RESULT.NOT_FOUND == returnCode:
				return True, REPLY_MESSAGE.UNKNOWN_URL%strStringToScan, dataType
			elif RATE_RESULT.FOUND == returnCode:
				if positive > 5 :
					return True, REPLY_MESSAGE.DANGER_URL%strStringToScan, dataType
				else:
					return True, REPLY_MESSAGE.NORMAL_URL%strStringToScan, dataType
			return True, '%s be considered as SAFE in %s scanners(total %s)'%(strStringToScan, totalscaned-positive, totalscaned), dataType

		return False, 'No Threat Found', DATA_TYPE.TYPE_UNDEFINE

if __name__ == '__main__':
	objRating = rating()
	print objRating.ratingInput('string https://www.google.com')