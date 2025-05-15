import os
import shutil
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, sum, count
from pyspark.sql.types import StructType, StringType, FloatType, TimestampType, DoubleType
from dotenv import load_dotenv

load_dotenv()


order_schema = StructType() \
    .add("order_id", StringType()) \
    .add("user_id", StringType()) \
    .add("product_id", StringType()) \
    .add("category", StringType()) \
    .add("amount", DoubleType()) \
    .add("payment_method", StringType()) \
    .add("timestamp", TimestampType())


spark = SparkSession.builder \
  .appName("LiveOrderAggregator") \
  .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

spark.conf.set("spark.sql.streaming.stateStore.maintenanceInterval", "300s")
spark.conf.set("spark.sql.streaming.statefulOperator.checkpointLocation.numRetainedCheckpoints", "3")


raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "orders") \
    .option("startingOffsets", "latest") \
    .load()


parsed_df = raw_df.selectExpr("CAST(value AS STRING)") \
  .select(from_json(col("value"), order_schema).alias("orders_data")) \
  .select("orders_data.*")


aggregated_order_df = parsed_df \
  .withWatermark("timestamp", "10 minutes") \
  .groupBy(
    window(col("timestamp"), "5 minutes"),
    col("category"),
    col("payment_method")
  ) \
  .agg(
    sum("amount").alias("total_revenue"),
    count("*").alias("order_count")
  )


def write_postgresql_orders(batch_df, batch_id):
  try:
    print(f"Processing batch: {batch_id}")
    batch_df.show(5, truncate=False)
    
    if batch_df.count() > 0:
      batch_df \
      .withColumn("window_start", col("window.start")) \
      .withColumn("window_end", col("window.end")) \
      .drop("window") \
      .write \
      .format("jdbc") \
      .option("url", f"jdbc:postgresql://{os.getenv('POSTGRES_HOST')}:5432/{os.getenv('POSTGRES_DB')}") \
      .option("dbtable", "realtime_order_summary") \
      .option("user", os.getenv("POSTGRES_USER")) \
      .option("password", os.getenv("POSTGRES_PASSWORD")) \
      .option("driver", "org.postgresql.Driver") \
      .option("numPartitions", "1") \
      .option("createTableColumnTypes", 
              "window VARCHAR(255), " \
              "category VARCHAR(50), " \
              "payment_method VARCHAR(50), " \
              "total_revenue DECIMAL(10,2), " \
              "order_count INT") \
      .mode("append") \
      .save()
      print(f"Successfully wrote batch {batch_id} to PostgreSQL")
    else:
      print(f"Batch {batch_id} was empty, skipping write")
  except Exception as e:
    print(f'Error writing to PostgreSQL: {e}')


checkpoint_dir = "/tmp/spark-checkpoints/orders-agg-fresh"
# if os.path.exists(checkpoint_dir):
#     print(f"Removing existing checkpoint directory: {checkpoint_dir}")
#     shutil.rmtree(checkpoint_dir)
# print(f"Creating fresh checkpoint directory: {checkpoint_dir}")
# os.makedirs(checkpoint_dir, exist_ok=True)


print("Starting streaming query...")


query = aggregated_order_df.writeStream \
  .outputMode("update") \
  .foreachBatch(write_postgresql_orders) \
  .option("checkpointLocation", checkpoint_dir) \
  .start()


print("Query started. Awaiting termination...")
query.awaitTermination()