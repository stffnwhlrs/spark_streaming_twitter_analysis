#!/usr/bin/python3

from confluent_kafka import Consumer, KafkaError, KafkaException
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--topic",  help="topic to read from")
args = parser.parse_args()

def display_message(message):
  print("- '%s' %s %d %d" %
        (message.value(), message.topic(), message.offset(),
         message.timestamp()[1]))


conf = {'bootstrap.servers': "localhost:9092",
        'auto.offset.reset': 'latest',
        'group.id': "IE"}

consumer = Consumer(conf)
consumer.subscribe([args.topic])

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
      display_message(message)
