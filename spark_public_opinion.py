from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import split
from pyspark.sql.functions import udf
from time import sleep
import re
from pyspark.streaming.kafka import KafkaUtils
import pyspark.sql.functions as f
from pyspark.sql.functions import lit


spark = SparkSession.builder\
                    .appName('Tweet Sentiment Analysis')\
                    .getOrCreate()


location = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "twitterPublic") \
  .option("startingOffsets", "latest") \
  .option("failOnDataLoss", "false") \
  .load()

location = location.selectExpr("CAST(value AS STRING)")

print("Are we streaming? " + str(location.isStreaming))


if __name__ == "__main__":
    print("lol")