# https://towardsdatascience.com/using-kafka-to-optimize-data-flow-of-your-twitter-stream-90523d25f3e8
"""API ACCESS KEYS"""

access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from confluent_kafka import Producer