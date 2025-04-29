import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, min, max, count
from pyspark.sql.types import StructType, StringType, TimestampType
from dotenv import load_dotenv

load_dotenv()

user_activity_schema = StructType() \
    .add("event_id", StringType()) \
    .add("user_id", StringType()) \
    .add("session_id", StringType()) \
    .add("event_type", StringType()) \
    .add("device", StringType()) \
    .add("location", StringType()) \
    .add("timestamp", TimestampType())


spark = SparkSession.builder \
    .appName("UserTrendTracker") \
    .getOrCreate()


spark.sparkContext.setLogLevel("ERROR")


raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "userActivity") \
    .option("startingOffsets", "latest") \
    .load()


parsed_df = raw_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), user_activity_schema).alias("activity_data")) \
    .select("activity_data.*")


# Event count per device/location/user_id per window
activity_summary_df = parsed_df \
    .withWatermark("timestamp", "2 minutes") \
    .groupBy(
        window(col("timestamp"), "5 minutes"),
        col("device"),
        col("location"),
        col("user_id")
    ) \
    .agg(
        count("*").alias("event_count"),
        min("timestamp").alias("session_start"),
        max("timestamp").alias("session_end")
    ) \
    .withColumn("session_duration_seconds",
                (col("session_end").cast("long") - col("session_start").cast("long")))


def write_postgresql_activity(batch_df, batch_id):
    try:
        print(f'processing batch: {batch_id}')
        batch_df.show(truncate=False)


        if batch_df.count() > 0:
            df_to_write = batch_df \
                .withColumn("window_start", col("window.start")) \
                .withColumn("window_end", col("window.end")) \
                .drop("window")

            # for sanity check
            # df_to_write.printSchema()

            df_to_write.write \
                .format("jdbc") \
                .option("url", f"jdbc:postgresql://{os.getenv('POSTGRES_HOST', 'localhost')}:5432/{os.getenv('POSTGRES_DB')}") \
                .option("dbtable", "user_activity_summary") \
                .option("user", os.getenv("POSTGRES_USER")) \
                .option("password", os.getenv("POSTGRES_PASSWORD")) \
                .option("driver", "org.postgresql.Driver") \
                .option("numPartitions", "1") \
                .option("createTableColumnTypes",
                        "window_start TIMESTAMP, "
                        "window_end TIMESTAMP, "
                        "device VARCHAR(20), "
                        "location VARCHAR(100), "
                        "user_id INT, "
                        "event_count INT, "
                        "session_start TIMESTAMP, "
                        "session_end TIMESTAMP, "
                        "session_duration_seconds BIGINT") \
                .mode("append") \
                .save()

            
            print(f"✅ Successfully wrote batch {batch_id} to PostgreSQL")
        else:
            print(f"⚠️ Batch {batch_id} was empty, skipping write")
    except Exception as e:
        print(f'❌ Error writing to PostgreSQL: {e}')


checkpoint_dir = "/tmp/spark-checkpoints/userActivity"


query = activity_summary_df.writeStream \
    .outputMode("update") \
    .foreachBatch(write_postgresql_activity) \
    .option("checkpointLocation", checkpoint_dir) \
    .start()


print("Query started. Awaiting termination...")
query.awaitTermination()