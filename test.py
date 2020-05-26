import os
import sys


os.environ['SPARK_HOME'] = "/home/kirito/Documents/project/python"


sys.path.append("/home/kirito/Documents/project/python/pyspark")
# sys.path.append("D:\python\spark-1.4.1-bin-hadoop2.4\python\lib\py4j-0.8.2.1-src.zip")

try:
    from pyspark import SparkContext
    from pyspark import SparkConf

    print ("success")

except ImportError as e:
    print ("error importing spark modules", e)
    sys.exit(1)