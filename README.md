# spra_group_project

This document describes how to set up and execute our spra group assignment. Please check the `presentation.pdf` to get more information.






## Setup

### 0. Get/ update files
The following command is only required once. Execute the following command in a terminal to connect to the repository. It will create a new folder with all the needed files.
```shell
git clone https://github.com/stffnwhlrs/spra_group_project.git
```

### 1. Set up Kafka
Run the bash script `setup_kafka_env.sh` to start the Kafka environment and create the needed topics if they don't exist.
```shell
sudo bash setup_kafka_env.sh
```
## Exeute the pubplic opinion data process

### 2. Run producer: Twitter public
The twitter public producer fetches tweets from Twitter that belong to Apple, Bayer, Bitcoin, Google, Tesla, and publish them into the *twitterPublic* topic. The producer only inserts the *text* field (the text message) of the whole tweet object to reduce the payload of the event. The producer can be run in two different modes which can be specified when executing the python script:
- `normal`: Publish data to the topic
- `debug`: Print data to the terminal

```shell
python3 producer_twitter_public.py normal
```

### 3. Run Spark: Public opinion
This Spark appliaction filters, adds a sentiment, and aggregates the tweets per company

Parameters:
-`console`: Prints results to the console
-`topic`: Sends data to the specific topic

```shell
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 spark_public_opinion.py topic
```

### 4. Run consumer: PowerBI 
This application consumes the data from the specific topic and sends it via REST request to PowerBI

```shell
python3 consumer_powerbi_public_opinion.py
```

## Exeute the pubplic opnion data process

### 5. Run producer: Influencer
We created threee producer that fetch Twitter data from influencers. it fetches tweets, RT and direct responses. The producer only inserts the *text* field (the text message) of the whole tweet object to reduce the payload of the event. The producer can be run in two different modes which can be specified when executing the python script:
- `normal`: Publish data to the topic
- `debug`: Print data to the 

```shell
python3 producer_twitter_elon.py normal
```

### 6. Run Spark: Influencers
This Spark appliaction filters, adds a sentiment, and aggregates the tweets per influencers and company

Parameters:
-`console`: Prints results to the console
-`topic`: Sends data to the specific topic

```shell
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 spark_influencers.py topic
```

### 7. Run consumer: PowerBI 
This application consumes the data from the specific topic and sends it via REST request to PowerBI

```shell
python3 python3 consumer_powerbi_influencers.py
```

### 8. Check the results in PowerBI
We created several PowerBI Dashboards to visualize our results. You can check them out here (IE account needed):
- https://app.powerbi.com/links/6Gl-PiJ4Un?ctid=73458443-1627-4091-8b39-2222134907c5&pbi_source=linkShare
- https://app.powerbi.com/links/qqnEkp1qVw?ctid=73458443-1627-4091-8b39-2222134907c5&pbi_source=linkShare

![Public opinion](https://github.com/stffnwhlrs/spra_group_project/blob/main/public_opinion.png)

![Influencers](https://github.com/stffnwhlrs/spra_group_project/blob/main/influencers.png)
