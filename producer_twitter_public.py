from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from confluent_kafka import Producer
import socket
import argparse
import json

# Twitter credentials steffen
access_token = "929886734-bnhLGa6cLzn9RKRZN1ydy50So6KVx8Bonwh2ynMH"
access_token_secret = "1L4KdxrDYbKmGViLo1zsLl3qeeSYIIGQm7LSqGEdB1xCd"
consumer_key = "KTLTyI9eQL1R3nv5ko8PJ4wrn"
consumer_secret = "l6zjKXJfiIkWUhhinZoEHyodhK2v6Jk6ng6X96rLhRYVwaB2pH"

# Used to select different modes
# normal: send to kafka topic
# debug: only print in terminal
parser = argparse.ArgumentParser()
parser.add_argument("action", choices=['normal', 'debug'])
args = parser.parse_args()

# Configure and create kafka producer
conf = {'bootstrap.servers': "localhost:9092",
        'client.id': socket.gethostname()}
producer = Producer(conf)

# topic to write to
topic_name = "twitterPublic"

# Twitter authentication
class twitterAuth():
    """SET UP TWITTER AUTHENTICATION"""

    def authenticateTwitterApp(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        return auth


# Twitter streaming handler
class TwitterStreamer():

    """SET UP STREAMER"""
    def __init__(self):
        self.twitterAuth = twitterAuth()

    def stream_tweets(self):
        while True:
            listener = ListenerTS() 
            auth = self.twitterAuth.authenticateTwitterApp()
            stream = Stream(auth, listener)
            stream.sample(stall_warnings=True, languages= ["en"])


class ListenerTS(StreamListener):

    def on_data(self, raw_data):
        tweet_raw = json.loads(raw_data)
        tweet = {
            "full_text": tweet_raw["extended_tweet"]["full_text"],
        }
        tweet_str = json.dumps(tweet)

        if args.action == "normal":
            producer.produce(topic_name, str.encode(tweet_str))
            return True
        if args.action == "debug":
            print("raw_data",raw_data)
            print("tweet_str",tweet_str)


if __name__ == "__main__":
    TS = TwitterStreamer()
    TS.stream_tweets()