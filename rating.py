from parser import Parser, DATA_TYPE
from virustotalapi import VirusTotalAPI

class RATE_RESULT:
	NORMAL     = 0
	DANGER     = 1
	SUSPICIOUS = 2

class rating(object):
	def __init__(self):
		self.ratingResult = RATE_RESULT.NORMAL

	def ratingInput(self, strInput):
		dataParser = Parser()
		dataType, strReturn = dataParser.classify(strInput)

		if dataType == DATA_TYPE.TYPE_URL:
			virustotal = VirusTotalAPI()
			returnCode, totalscaned, positive = virustotal.scanURL(strReturn)
			return True, '%s be considered as SAFE in %s scanners(total %s)'%(strReturn, totalscaned-positive, totalscaned)

		return False, 'No Threat Found'

if __name__ == '__main__':
	objRating = rating()
	print objRating.ratingInput('string https://www.google.com')