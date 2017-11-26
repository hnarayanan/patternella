import tweepy
import urllib2
from PIL import Image

import tensorflow as tf
from style_transfer_tester import StyleTransferTester

from credentials import (consumer_key,
                         consumer_secret,
                         access_token,
                         access_token_secret)


class PatternellaStreamListener(tweepy.StreamListener):

    def __init__(self, api, sess):
        self.sess = sess
        self.api = api

    def on_status(self, status):
        sender = status.author.screen_name
        try:
            photo_id = status.extended_entities['media'][0]['id_str']
            photo_url = status.extended_entities['media'][0]['media_url']
            photo = Image.open(urllib2.urlopen(photo_url))
            photo.save('input/{photo_id}.png'.format(photo_id=photo_id))

            # TODO: We need to grab the style from the style hashtag if it exists
            # style = status.entities['hashtags'][0]
            style = 'la_muse'

            transformer = StyleTransferTester(
                session=self.sess,
                model_path='style_models/{style}.ckpt'.format(style=style),
                content_image=photo,
            )
            transformed_photo = transformer.test()
            photo.save('output/{photo_id}.png'.format(photo_id=photo_id))

            tweet = "@{sender} Here you go!".format(sender=sender)
            self.api.update_with_media('output/{photo_id}.png'.format(photo_id=photo_id), status=tweet)
        except:
            tweet = "@{sender} Please tweet me with the image you'd like cutened!".format(sender=sender)
            try:
                self.api.update_status(status=tweet)
            except tweepy.error.TweepError:
                # TODO: This exception should be better logged, e.g.
                # print("Error: ({code}): {message}".format(code=error['code'], message=error['message']))
                pass
        print tweet


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

soft_config = tf.ConfigProto(allow_soft_placement=True)
soft_config.gpu_options.allow_growth = True
sess = tf.Session(config=soft_config)

listener = PatternellaStreamListener(sess=sess, api=api)
stream = tweepy.Stream(auth=api.auth, listener=listener)

stream.filter(track=['@patternella'])
