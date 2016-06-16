from twython import Twython

APP_KEY = 

APP_SECRET =

OAUTH_TOKEN = 

OAUTH_TOKEN_SECRET =

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)



twitter.update_status(status='I am a beast') 
