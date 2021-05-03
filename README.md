# spra_group_project
This document describes how to set up and execute our spra group assignment. This project is developed on an iterative basis.

# 0. Get/ update files

The following command is only required once. Execute the following command in a terminal to connect to the repository. It will create a new folder with all the files.
```shell
git clone https://github.com/stffnwhlrs/spra_group_project.git
```

Before running the application you should make sure that the code is up to date and download all updated files. Use the following command to do it.
```shell 
git pull 
```

# 1. Set up Kafka
Run the bash script `setup_kafka_env.sh` to start the Kafka environment and create the needed topics if they don't exist.
```shell
sudo bash setup_kafka_env.sh
```

# 2. Run Producer: Twitter public
The twitter public producer fetches sample tweets from Twitter and publish them into the *twitterPublic* topic. The producer only inserts the *text* field (the text message) of the whole tweet object to reduce the payload of the event. The producer can be run in two different modes which can be specified when executing the python script:
- `normal`: Publish data to the topic
- `debug`: Print data to the terminal

```shell
python3 producer_twitter_public.py normal
```

# 3. Run the Consumer: Test consumer
The *consumer_test* consumer is a simple consumer to subscribe to a topic and check if data got inserted into the the topic. It prints the event to the terminal.
To subscribe to a topic, you need to specify the topic while executing the python script.
```shell 
python3 consumer_test.py -t twitterPublic
``` 

# 4. Run the producer: Test Producer
The *producer_test* producer is a simple consumer to write either manually or a file to a specified topic
- `manually`: write your own text
- `file`: write file
- `-t`: the topic to write to
- `-f`: the file path 

```shell
python3 producer_test.py manually -t twitterPublic
python3 producer_test.py file -t twitterPublic -f data_powerbi_test.json

```

# 5. Run public opinion

```shell
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 spark_public_opinion.py
```