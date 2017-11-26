import tweepy
import urllib2
from PIL import Image

from credentials import (consumer_key,
                         consumer_secret,
                         access_token,
                         access_token_secret)


class PatternellaStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        sender = status.author.screen_name
        try:
            photo_id = status.extended_entities['media'][0]['id_str']
            photo_url = status.extended_entities['media'][0]['media_url']
            photo = Image.open(urllib2.urlopen(photo_url))
            photo.save('input/{photo_id}.png'.format(photo_id=photo_id))

            # TODO: We need to grab the style from the style hashtag if it exists
            # style = status.entities['hashtags'][0]

            tweet = "@{sender} Here you go!".format(sender=sender)
            api.update_with_media('input/{photo_id}.png'.format(photo_id=photo_id), status=tweet)
        except:
            tweet = "@{sender} Please tweet me with the image you'd like cutened!".format(sender=sender)
            try:
                api.update_status(status=tweet)
            except tweepy.error.TweepError:
                # TODO: This exception should be better logged, e.g.
                # print("Error: ({code}): {message}".format(code=error['code'], message=error['message']))
                pass
        print tweet


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

listener = PatternellaStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=listener)

stream.filter(track=['@patternella'])
