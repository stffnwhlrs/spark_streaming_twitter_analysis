from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

# ------ HELPER FUNCTIONS -------

def get_content(tweet):
  tesla = ["Tesla", "tesla"]
  
  if any(map(tweet.__contains__, tesla)):
    return "tesla"
  else: 
    return "-"

get_content_udf = udf(get_content, StringType())


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
tweets = tweets.select(col("tweet.text").alias("tweet")).withColumn("process_time", current_timestamp())

# print schema of the new structured stream
print("Data Schema tweets:")
tweets.printSchema()

# Extract the content of the tweet
tweets = tweets.withColumn("content", get_content_udf(col("tweet")))

tweets_aggregated = tweets
.withWatermark("process_time", "10 seconds")
.groupBy(
  window(tweets.process_time, "10 seconds"),
  tweets.content
  ).count()



  


# Start running the query that prints the running counts to the console
# use append for non aggregated data
# use complete for aggregation
query = tweets_aggregated \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()


query.awaitTermination()


if __name__ == "__main__":
    print("lol")


# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 spark_public_opinion.py