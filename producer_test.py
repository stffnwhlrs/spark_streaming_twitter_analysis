#!/usr/bin/python3

import argparse
import json
import time
import socket
from confluent_kafka import Producer

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=['manually', 'file'])
parser.add_argument("-t", "--topic", help="topic to publish to")
parser.add_argument("-f", "--file", help="filepath")
args = parser.parse_args()


# Configure and create kafka producer
conf = {
    'bootstrap.servers': "localhost:9092",
    'client.id': socket.gethostname()
}
producer = Producer(conf)


def send_message(topic):
    while True:
        message = input("Which message should be sent?")
        print("Send:", message, "to:",topic)
        producer.produce(topic, value=message)


def send_file(file_path, topic):
    messages = []
    with open(file_path) as json_file:
        for row in json_file:
            messages.append(row.replace("\n","").replace("\r",""))
    
    for message in messages:
        print("Send:", message, "to:",topic)
        producer.produce(topic, value=message)
        # add a delay between messages
        time.sleep(3)



# Action dispatching
if args.action == "manually":
    if args.topic = None:
        print("Specify topic")
        return

    send_message(args.topic)

elif args.action == "file":
    if args.topic == None:
        print("Specify topic")
        return
    if args.file == None:
        print("Specify file")
        return

    send_file(args.file, args.topic)

else:
    print("Specify action")