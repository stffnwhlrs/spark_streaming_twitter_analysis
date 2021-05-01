
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


# create spark configuration
sc = SparkContext("local[2]", "TwitterWordCount")
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 5)

print("succes!!!!!!!!!!!")

df = ssc \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "twitterPublic") \
  .load()

print(df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)"))







if __name__ == "__main__":
    print("lol")