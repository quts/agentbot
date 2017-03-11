import ConfigParser, os, requests

class VirusTotalAPI(object):
	def __init__(self, configPath = 'config.cfg'):
			self.publickey = os.environ['VirusTotal_PublicKey']

	def scanURL(self, strURL):
		# Send scan request to Virus Total
		params = {'apikey': self.publickey, 'url': strURL}
		response = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=params)
		json_response = response.json()

		print json_response

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

		return json_response['response_code'], json_response['total'], json_response['positives']

if __name__ == '__main__':
	virustotal = VirusTotalAPI()
	print virustotal.scanURL('http://www.google.com')
