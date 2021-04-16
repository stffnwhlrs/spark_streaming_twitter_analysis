#!/bin/sh

echo "Start Kafka setup"

# Start Kafka
sudo service kafka start

# Wait until Kafka started
sleep 3
# Kafka status
systemctl is-active --quiet kafka && echo "Kafka is running."

# Create topic twitterPublic
#/opt/kafka/bin/kafka-topics.sh --create --topic twitterPublic --zookeeper localhost:2181 --partitions 1 --replication-factor 1 --if-not-exists &&
#echo "Kafka topic twitterPublic exists"


# Create topics if not existing
for topic in twitterPublic
do
  /opt/kafka/bin/kafka-topics.sh --create --topic $topic --zookeeper localhost:2181 --partitions 1 --replication-factor 1 --if-not-exists &&
  echo "Kafka topic ${topic} exists."
done

# List all existing topics
# /opt/kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181