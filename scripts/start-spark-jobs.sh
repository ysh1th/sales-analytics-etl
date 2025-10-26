#!/bin/bash

echo "Waiting for Spark master to be ready..."
while ! nc -z spark 7077; do
  sleep 5
done

echo "Spark master is ready. Starting Spark jobs..."

cd /app

echo "Starting order aggregator job..."
spark-submit \
  --master spark://spark:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 \
  --jars /opt/spark/jars/postgresql.jar \
  --conf "spark.driver.extraJavaOptions=-XX:+UseG1GC" \
  --conf "spark.executor.extraJavaOptions=-XX:+UseG1GC" \
  order_aggregator.py &

echo "Starting user trend job..."
spark-submit \
  --master spark://spark:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 \
  --jars /opt/spark/jars/postgresql.jar \
  --conf "spark.driver.extraJavaOptions=-XX:+UseG1GC" \
  --conf "spark.executor.extraJavaOptions=-XX:+UseG1GC" \
  user_trend.py &

wait 