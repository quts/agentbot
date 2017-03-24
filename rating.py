from parser import Parser, DATA_TYPE
from virustotalapi import VirusTotalAPI
from agentbot import RATE_RESULT, REPLY_MESSAGE

class rating(object):
    def __init__(self):
        self.ratingResult = RATE_RESULT.NOT_FOUND

    def ratingInput(self, strInput):
        dataParser = Parser()
        dataType, strStringToScan = dataParser.classify(strInput)
        dictReturn = {}
        dictReturn['Enable'] = False
        dictReturn['Message'] = 'No Threat Found'
        dictReturn['type'] = DATA_TYPE.TYPE_UNDEFINE

        if dataType == DATA_TYPE.TYPE_URL:
            virustotal = VirusTotalAPI()
            returnCode, totalscaned, positive = virustotal.scanURL(strStringToScan)
            dictReturn['Enable'] = True
            dictReturn['type'] = dataType
            dictReturn['data'] = strStringToScan


            dictReturn['Message'] = '%s be considered as SAFE in %s scanners(total %s)'%(strStringToScan, totalscaned-positive, totalscaned)
            if RATE_RESULT.NOT_FOUND == returnCode:
                dictReturn['Message'] = REPLY_MESSAGE.UNKNOWN_URL%strStringToScan
            elif RATE_RESULT.FOUND == returnCode:
                if positive > 5 :
                    dictReturn['Message'] = REPLY_MESSAGE.DANGER_URL%strStringToScan
                else:
                    dictReturn['Message'] = REPLY_MESSAGE.NORMAL_URL%strStringToScan

        return dictReturn

if __name__ == '__main__':
    objRating = rating()
    print objRating.ratingInput('string https://www.google.com')