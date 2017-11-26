import tweepy

from credentials import *


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class PatternellaStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status)
        # api.update_with_media('/data/projects/tensorflow-fast-style-transfer/model/result_15000.jpg', status='Amazing!')
        print(status.text)


listener = PatternellaStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=listener)

stream.filter(track=['@patternella'])
