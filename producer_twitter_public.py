# https://towardsdatascience.com/using-kafka-to-optimize-data-flow-of-your-twitter-stream-90523d25f3e8
"""API ACCESS KEYS"""

access_token = "929886734-cDN321qqWfQPAROumjI6IIwLBf4pSpexMOl9opHs"
access_token_secret = "rvjfwEn9MRAiWkH3XSHMi0ZV3JLLFtNhJjaElFTzKfwr0"
consumer_key = "tXskNrFeWAEqiqGauybTLdHOP"
consumer_secret = "YJS9pd99pMFkY3khU9eu0Mz47cfePNNGwNlcXPEeHTtgzzf94a"


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from confluent_kafka import Producer


conf = {'bootstrap.servers': "localhost:9092",
        'client.id': socket.gethostname()}
producer = Producer(conf)

topic_name = "twitterPublic"


class twitterAuth():
    """SET UP TWITTER AUTHENTICATION"""

    def authenticateTwitterApp(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        return auth



class TwitterStreamer():

    """SET UP STREAMER"""
    def __init__(self):
        self.twitterAuth = twitterAuth()

    def stream_tweets(self):
        while True:
            listener = ListenerTS() 
            auth = self.twitterAuth.authenticateTwitterApp()
            stream = Stream(auth, listener)
            stream.filter(track=["Apple"], stall_warnings=True, languages= ["en"])


class ListenerTS(StreamListener):

    def on_data(self, raw_data):
            producer.produce(topic_name, str.encode(raw_data))
            return True


if __name__ == "__main__":
    TS = TwitterStreamer()
    TS.stream_tweets()