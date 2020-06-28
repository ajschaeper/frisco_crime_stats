import logging
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as psf

KAFKA_BROKER_URL = "localhost:9092"
KAFKA_TOPIC_NAME = "com.udacity.streams.sf_crime_stats.from_json"
SPARK_CHECKPOINT_DIR = "/tmp/spark-checkpoints"

schemaCall = StructType([
    StructField("crime_id", StringType(), True),
    StructField("original_crime_type_name", StringType(), True),
    StructField("report_date", StringType(), True),
    StructField("call_date", StringType(), True),
    StructField("offense_date", StringType(), True),
    StructField("call_time", StringType(), True),
    StructField("call_date_time", TimestampType(), True),
    StructField("disposition", StringType(), True),
    StructField("address", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("agency_id", StringType(), True),
    StructField("address_type", StringType(), True),
    StructField("common_location", StringType(), True),
])

def run_spark_job(spark):

    # Spark Stream configuration
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER_URL) \
        .option("subscribe", KAFKA_TOPIC_NAME) \
        .option('startingOffsets', 'earliest') \
        .option('maxOffsetsPerTrigger', 32) \
        .option('maxRatePerPartition', 32) \
        .option('stopGracefullyOnShutdown', "true") \
        .load()

    # Show schema for the incoming resources for checks
    df.printSchema()

    # Extract the correct column from the kafka input resources
    kafka_df = df.selectExpr("CAST(value AS STRING)")

    service_table = kafka_df \
        .select(psf.from_json(psf.col("value"), schemaCall).alias("DF")) \
        .select("DF.*")

    # Select original_crime_type_name and disposition
    distinct_table = service_table \
        .select("original_crime_type_name", "call_date_time") \
        .dropna() \
        .distinct() \
        .withWatermark("call_date_time", "5 minutes")

    # Count the number of original crime type
    agg_df = distinct_table \
        .groupBy("original_crime_type_name") \
        .agg({"call_date_time": "count"}) \
        .orderBy(psf.desc("count(call_date_time)"))

    # Write stream
    query = agg_df.writeStream \
            .outputMode("complete") \
            .format("console") \
            .queryName("sf_crime_stats") \
            .start()

    # Attach a ProgressReporter
    query.awaitTermination()

    # Get radio code table
    radio_code_json_filepath = "./radio_code.json"
    radio_code_df = spark.read.json(radio_code_json_filepath)

    # Rename disposition_code column to disposition
    radio_code_df = radio_code_df.withColumnRenamed("disposition_code", "disposition")

    # Join on disposition column
    join_query = agg_df.join(radio_code_df, "disposition", "left_outer")

    # Attach a ProgressReporter
    join_query.awaitTermination()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    # Create Spark in, with Spark UI on port 3000
    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("KafkaSparkStructuredStreaming") \
        .config("spark.ui.port", 3000) \
        .getOrCreate()

    logger.info("Spark started")

    run_spark_job(spark)

    spark.stop()
