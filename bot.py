import tweepy
import urllib2

from credentials import (consumer_key,
                         consumer_secret,
                         access_token,
                         access_token_secret)


class PatternellaStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        sender = status.user.screen_name
        try:
            print "I got an image"
            photo_url = status.extended_entities['media'][0]['media_url']
            photo = Image.open(urllib2.urlopen(photo_url))
            photo.save('random.jpg')
            # style = status.entities['hashtags'][0]
            tweet = "@{sender} Here you go!".format(sender=sender)
            api.update_with_media('/data/projects/tensorflow-fast-style-transfer/model/result_15000.jpg', status=tweet)
        except:
            print "I didn't get an image"
            tweet = "@{sender} Please tweet me with the image you'd like cutened!".format(sender=sender)
            api.update_status(status=tweet)


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)        

listener = PatternellaStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=listener)

stream.filter(track=['@patternella'])
