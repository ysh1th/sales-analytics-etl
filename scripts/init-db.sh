#!/bin/bash

echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h postgres -p 5432 -U admin; do
  sleep 2
done

echo "PostgreSQL is ready. Initializing database..."
python /app/postgres_table.py

echo "Database initialization complete." 