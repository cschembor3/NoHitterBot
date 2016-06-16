from twython import Twython

def init():
	with open("secret.txt") as f:
    	 secret = f.readlines()
	APP_KEY = secret[0].rstrip()
	APP_SECRET = secret[1].rstrip()
	OAUTH_TOKEN = secret[2].rstrip()
	OAUTH_TOKEN_SECRET = secret[3]
	return [APP_KEY,APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET]

def post():
	secretData = init()
	twitter = Twython(secretData[0], secretData[1],secretData[2], secretData[3])
	twitter.update_status(status='This works')





