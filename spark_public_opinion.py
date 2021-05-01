
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json

# create spark configuration
sc = SparkContext("local[2]", "TwitterWordCount")
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 5)

kafkaStream = KafkaUtils.createStream(ssc, 'localhost:2181', 'spark-streaming', {'publicOpinion':1})





if __name__ == "__main__":
    print("lol")