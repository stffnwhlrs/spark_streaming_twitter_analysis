
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


# create spark configuration
sc = SparkContext("local[2]", "TwitterWordCount")
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 5)

print("succes!!!!!!!!!!!")









if __name__ == "__main__":