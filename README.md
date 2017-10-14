# agentbot
The project "agentbot" is a chatbot on LINE IM platform to provide users identify URL is malicious or not.

## How to use it?
1. Add **@ygm2447v** as your friend through LINE app
2. Send a message include a link start with a http or https
3. The chatbot will parse every single mesage in the chatroom, and return scan result if found http or https string

## How dose it work?
1. When chatbot got a message, it will check if it include string star with http or https
2. Send the link to Virus total to get scan result
3. Return the scan result to you through LINE API callback

## Work with Heroku
You have to set following environment variable in your heroku server console for the LINE API token.
```
CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET       = os.environ['CHANNEL_SECRET']
```

You have to set following environment variable in your heroku server console for the VirusTotal API token.
```
LOCAL_STRING         = os.environ['LOCAL_STRING']
```

## Reference
- ![line/line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)
- ![VirusTotal Public API v2.0](https://www.virustotal.com/zh-tw/documentation/public-api/)
