from twython import Twython

with open("secret.txt") as f:
    secret = f.readlines()

APP_KEY = secret[0].rstrip()

APP_SECRET = secret[1].rstrip()

OAUTH_TOKEN = secret[2].rstrip()

OAUTH_TOKEN_SECRET = secret[3]

twitter = Twython(APP_KEY, APP_SECRET,
                 OAUTH_TOKEN, OAUTH_TOKEN_SECRET)



twitter.update_status(status='This works')
