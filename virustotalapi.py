import ConfigParser, os, requests, time
from agentbot import RATE_RESULT

class VirusTotalAPI(object):
	def __init__(self, configPath = 'config.cfg'):
			self.publickey = os.environ['VirusTotal_PublicKey']

	def busyWaiting(self, intSeconds):
		now = time.time()
		while (time.time()-now < intSeconds) :
			time.sleep(1)
			print 'busy waiting...'
			continue

	def scanURL(self, strURL, recurssive=0):
		# Retrieve scanned report from Virus Total	
		headers = {
		  "Accept-Encoding": "gzip, deflate",
		  "User-Agent" : "gzip,  Python"
		  }
		params = {'apikey': self.publickey, 'resource':strURL}
		response = requests.post('https://www.virustotal.com/vtapi/v2/url/report',
		  params=params, headers=headers)
		json_response = response.json()

		print json_response

		# If data found in VirusTotal or not
		if json_response['response_code'] == RATE_RESULT.FOUND:
			return RATE_RESULT.FOUND, json_response['total'], json_response['positives']
		else:
			# Send scan request to Virus Total
			params = {'apikey': self.publickey, 'url': strURL}
			response = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=params)
			json_response = response.json()

			print json_response

			# Return NOT_FOUND this time
			return RATE_RESULT.NOT_FOUND, 0, 0

if __name__ == '__main__':
	virustotal = VirusTotalAPI()
	print virustotal.scanURL('http://www.google.com')