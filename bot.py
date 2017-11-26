import tweepy

from credentials import *


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweet = 'Hello, from the patternella bot!'
api.update_status(status=tweet)
