
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

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