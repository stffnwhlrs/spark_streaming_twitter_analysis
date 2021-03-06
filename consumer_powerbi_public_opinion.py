#!/usr/bin/python3

from confluent_kafka import Consumer, KafkaError, KafkaException
import json
import pandas as pd
import requests

conf = {'bootstrap.servers': "localhost:9092",
        'auto.offset.reset': 'latest',
        'group.id': "IE"}

consumer = Consumer(conf)
consumer.subscribe(["twitterPublicOutput"])
    

def send_rest(message):
  message = json.loads(message.value())
  data = [message]

  url = "https://api.powerbi.com/beta/73458443-1627-4091-8b39-2222134907c5/datasets/20792726-b470-438e-a12c-6c99b9bba033/rows?key=p9e7FOz8G%2FkXhiHCGQ1rzm1MydzL8r26XyMdMcFcRMFWY4h6sUv4uatSqNQeR36ZC0%2FFDNwTbxsFJzboM57bZg%3D%3D"

  response = requests.post(url,json=data)
  print(data)
  print(response)



while True:
    message = consumer.poll(timeout=1.0)
    if message is None: continue

    if message.error():
      if message.error().code() == KafkaError._PARTITION_EOF:
        # End of partition event
        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                         (message.topic(), message.partition(), 
                          message.offset()))
      elif message.error():
        raise KafkaException(message.error())
    else:
      send_rest(message)


# python3 consumer_powerbi_public_opinion.py