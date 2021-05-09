from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import requests as re
import statistics as stats
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=['console', 'topic'])
args = parser.parse_args()


# ------ HELPER FUNCTIONS -------


def get_content(tweet):
  """
  Extract the company out of the tweet
  """

  tesla = ["Tesla", "tesla", "tsla", "TSLA", "#tsla", "#TSLA"]
  apple = ["Apple", "apple", "aapl", "AAPL", "#aapl", "#AAPL"]
  google = ["Google", "google", "googl", "GOOGL", "#googl", "#GOOGL"]
  bayer = ["Bayer", "bayer", "bayn", "BAYN", "#bayn", "#BAYN"]
  bitcoin = ["Bitcoin", "bitcoin"]
  
  if any(map(tweet.__contains__, tesla)):
    return "tesla"
  elif any(map(tweet.__contains__, apple)):
    return "apple"
  elif any(map(tweet.__contains__, google)):
    return "google"
  elif any(map(tweet.__contains__, bayer)):
    return "bayer"
  elif any(map(tweet.__contains__, bitcoin)):
    return "bitcoin"
  else:
    return "-"
    

# Create UDF
get_content_udf = udf(get_content, StringType())


def get_sentiment(tweet):
  """
  Helper function that extracts the sentiment of each tweet
  1 = positive
  0 = negative 
  """

  # Do the API request (Stanford Sentiment)
  r = re.post(
      "https://api.deepai.org/api/sentiment-analysis",
      data={
          'text': tweet,
      },
      headers={'api-key': 'ca26882d-52af-4903-b0f7-571801ebd67a'}
  )

  # Get only the output array. Each sentence has its own sentiments
  result = r.json()["output"]

  # Map strings to integers helper function
  def classify(sentiment):
    sentiment = sentiment.lower()
    if sentiment == "verynegative":
      return -2
    elif sentiment == "negative":
      return -1
    elif sentiment == "positive":
      return 1
    elif sentiment == "verypositive":
      return 2
    else:
      return 0

  # Map strings to integers helper function
  result = list( map(classify, result))

  # Calculate the entire
  result = stats.mean(result)
    
  return 1 if result >= 0 else 0

# Create UDF
get_sentiment_udf = udf(get_sentiment, StringType())


# ------ SPARK PROCESS -------

spark = SparkSession.builder\
                    .appName('Tweet Sentiment Analysis')\
                    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Create the schema for input data
schema = StructType([ \
  StructField("text", StringType(), True),
  StructField("created_at", StringType(), True) \
    ])

# Get the stream
raw_input = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "twitterPublic") \
  .option("startingOffsets", "latest") \
  .option("failOnDataLoss", "false") \
  .load()

# Transform byte code to string
raw_input = raw_input.selectExpr("CAST(value AS STRING)")

# Check if the stream is running
print("Are we streaming? " + str(raw_input.isStreaming))

# print schema of the raw input
print("Data Schema: raw_input")
raw_input.printSchema()

# Transform value information to a column
tweets = raw_input.select(from_json(raw_input.value, schema).alias("tweet"))

#Select only the text and insert process time
tweets = tweets.select(col("tweet.text").alias("tweet"),).withColumn("process_time", current_timestamp())

# print schema of the new structured stream
print("Data Schema tweets:")
tweets.printSchema()

# Extract the content of the tweet
tweets = tweets.withColumn("company", get_content_udf(col("tweet")))

# Filter not interesting tweets
tweets = tweets.filter(~(tweets.company == "-"))

# ADD SENTIMENT
# Positive
tweets = tweets.withColumn("sentiment_positive",get_sentiment_udf(col("tweet")))
# Add additional negative for easier count
tweets = tweets.withColumn("sentiment_negative", 1 - col("sentiment_positive"))


# Specify windowing
window_length = "10 seconds"
# sliding_interval = "0 seconds"

# Aggreagte tweets
tweets_aggregated = tweets \
  .withWatermark("process_time", window_length).groupBy(
    window(tweets.process_time, window_length),
    tweets.user, tweets.company
  ).agg( \
    sum("sentiment_positive").alias("sentiment_positive"),
    sum("sentiment_negative").alias("sentiment_negative"),
    count(lit(1)).alias("tweet_count")
    )

# Create fraction for sentiments and add timestamp
tweets_aggregated = tweets_aggregated.withColumn("sentiment_positive", col("sentiment_positive") / col("tweet_count")) \
  .withColumn("sentiment_negative", col("sentiment_negative") / col("tweet_count")) \
    .withColumn("time", current_timestamp())


# Define output
tweets_aggregated = tweets_aggregated.select( \
  col("company"),
  col("sentiment_positive"),
  col("sentiment_negative"),
  col("tweet_count"),
  col("time")
)




  


# Start running the query that prints the running counts to the console
# use append for non aggregated data
# use complete for aggregation
# used update for only last aggregate

if args.action == "console":
  output = tweets_aggregated \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .start()

elif args.action == "topic":  
  output = tweets_aggregated \
    .selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .outputMode("update") \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "twitterPublicOutput") \
    .option("checkpointLocation", "/tmp/steffen/checkpoint") \
    .start()



output.awaitTermination()


if __name__ == "__main__":
  print("lol")



# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 spark_public_opinion.py console