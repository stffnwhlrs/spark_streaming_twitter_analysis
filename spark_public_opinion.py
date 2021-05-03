from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from import pyspark.sql.functions pyspark.sql.functions import *


spark = SparkSession.builder\
                    .appName('Tweet Sentiment Analysis')\
                    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")


schema = StructType([ \
  StructField("text", StringType(), True) \
    ])


raw_input = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "twitterPublic") \
  .option("startingOffsets", "latest") \
  .option("failOnDataLoss", "false") \
  .load()

raw_input = raw_input.selectExpr("CAST(value AS STRING)")

print("Are we streaming? " + str(raw_input.isStreaming))

tweets = raw_input.select(from_json(raw_input.text, schema))


print("Data Schema:")
tweets.printSchema()


# Start running the query that prints the running counts to the console
query = raw_input \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()


query.awaitTermination()


if __name__ == "__main__":
    print("lol")


# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 spark_public_opinion.py