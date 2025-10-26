#!/bin/bash

echo "Waiting for Kafka to be ready..."
while ! nc -z kafka 9092; do
  sleep 2
done

echo "Kafka is ready. Starting data producers..."

cd /app

echo "Starting all data producers..."
python run_producers.py 