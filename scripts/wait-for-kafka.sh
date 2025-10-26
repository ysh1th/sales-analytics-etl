#!/bin/bash

echo "Waiting for Kafka to be ready..."
while ! nc -z kafka 9092; do
  sleep 2
done

echo "Kafka is ready." 