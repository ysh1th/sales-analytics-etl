#!/bin/bash

echo "Loading environment variables..."
export $(cat docker.env | xargs)

echo "Starting ETL pipeline..."
docker-compose up -d

echo "Pipeline started! Check status with: docker-compose ps"
echo "View logs with: docker-compose logs -f" 