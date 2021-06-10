
import os
import datetime
if "HADOOP_CONF_DIR" in os.environ:
    del os.environ["HADOOP_CONF_DIR"] 

import socket
from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, length, when, col
from pyspark.sql.types import BooleanType, IntegerType, LongType, StringType, ArrayType, FloatType, StructType, StructField
import pyspark.sql.functions as F
from pyspark.sql.functions import pandas_udf
from pyspark.sql.functions import PandasUDFType
from jinja2 import Environment, FileSystemLoader
from pyspark.sql.functions import col, window, from_json
from pyspark.sql.types import *
import json
humans = {'time':[], 'number':[]}
def func(batch_df, batch_id): 
        global humans
        
        humans['time'].append(datetime.datetime.now().minute)
        count = [0]
        for data in batch_df.toJSON().collect():
            data = eval(data)
            count.append(int(data['value']))
        humans['number'].append(max(count))
        humans['number'] = humans['number'][-18:]
        humans['time'] =  humans['time'][-18:]
        
        with open('../json/camera_data.json', 'w') as f:
            json.dump(humans, f)
        print(humans)

if __name__ == "__main__":
    # setting constants
    APP_NAME = "jupsparkapp"
    NORMALIZED_APP_NAME = APP_NAME.replace('/', '_').replace(':', '_')

    APPS_TMP_DIR = os.path.join(os.getcwd(), "tmp")
    APPS_CONF_DIR = os.path.join(os.getcwd(), "conf")
    APPS_LOGS_DIR = os.path.join(os.getcwd(), "logs")
    LOG4J_PROP_FILE = os.path.join(APPS_CONF_DIR, "pyspark-log4j-{}.properties".format(NORMALIZED_APP_NAME))
    LOG_FILE = os.path.join(APPS_LOGS_DIR, 'pyspark-{}.log'.format(NORMALIZED_APP_NAME))
    EXTRA_JAVA_OPTIONS = "-Dlog4j.configuration=file://{} -Dspark.hadoop.dfs.replication=1 -Dhttps.protocols=TLSv1.0,TLSv1.1,TLSv1.2,TLSv1.3"\
        .format(LOG4J_PROP_FILE)

    LOCAL_IP = socket.gethostbyname(socket.gethostname())

    # preparing configuration files from templates
    for directory in [APPS_CONF_DIR, APPS_LOGS_DIR, APPS_TMP_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    env = Environment(loader=FileSystemLoader('/opt'))
    template = env.get_template("pyspark_log4j.properties.template")
    template\
        .stream(logfile=LOG_FILE)\
        .dump(LOG4J_PROP_FILE)

    # run spark
    spark = SparkSession\
        .builder\
        .appName(APP_NAME)\
        .master("k8s://https://10.32.7.103:6443")\
        .config("spark.driver.host", LOCAL_IP)\
        .config("spark.driver.bindAddress", "0.0.0.0")\
        .config("spark.executor.instances", "2")\
        .config("spark.executor.cores", '3')\
        .config("spark.memory.fraction", "0.8")\
        .config("spark.memory.storageFraction", "0.6")\
        .config("spark.executor.memory", '3g')\
        .config("spark.driver.memory", "3g")\
        .config("spark.driver.maxResultSize", "1g")\
        .config("spark.kubernetes.memoryOverheadFactor", "0.3")\
        .config("spark.driver.extraJavaOptions", EXTRA_JAVA_OPTIONS)\
        .config("spark.kubernetes.namespace", "zvolovikova-283281")\
        .config("spark.kubernetes.driver.label.appname", APP_NAME)\
        .config("spark.kubernetes.executor.label.appname", APP_NAME)\
        .config("spark.kubernetes.container.image", "node03.st:5000/spark-executor:zvolovikova-283281")\
        .config("spark.local.dir", "/tmp/spark")\
        .config("spark.driver.extraClassPath", "/home/jovyan/shared-data/my-project-name-jar-with-dependencies.jar")\
        .config("spark.executor.extraClassPath", "/home/jovyan/shared-data/my-project-name-jar-with-dependencies.jar")\
        .config("spark.kubernetes.executor.volumes.emptyDir.spark-local-dir-tmp-spark.mount.path", "/tmp/spark")\
        .config("spark.kubernetes.executor.volumes.emptyDir.spark-local-dir-tmp-spark.mount.readOnly", "false")\
        .config("spark.kubernetes.executor.volumes.hostPath.depdir.mount.path", "/home/jovyan/shared-data")\
        .config("spark.kubernetes.executor.volumes.hostPath.depdir.options.path", "/nfs/shared")\
        .config("spark.kubernetes.executor.volumes.hostPath.depdir.options.type", "Directory")\
        .config("spark.kubernetes.executor.volumes.hostPath.depdir.mount.readOnly", "true")\
        .getOrCreate()

    # printing important urls and pathes
    print("Web UI: {}".format(spark.sparkContext.uiWebUrl))
    print("\nlog4j file: {}".format(LOG4J_PROP_FILE))
    print("\ndriver log file: {}".format(LOG_FILE))


    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka-svc:9092") \
        .option("subscribePattern", "camera.*") \
        .load()


    universe = df.selectExpr("CAST(value AS STRING)","CAST(key AS STRING)")
    universe_query = universe.writeStream.trigger(processingTime="1 minutes")\
                                        .outputMode("update").foreachBatch(func).start()

    universe_query.awaitTermination()
