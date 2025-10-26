# Dockerized ETL Pipeline

This project is now fully dockerized and can run autonomously without manual intervention.

## Quick Start

1. **Start the entire pipeline:**
   ```bash
  docker-compose up -d kafka postgres db-init data_producers superset
   ```

2. **Monitor the pipeline:**
   ```bash
  docker-compose logs -f
   ```

3. **Stop the pipeline:**
   ```bash
   docker-compose down
   ```

## What's Included

The dockerized pipeline includes:

- **Kafka** - Message broker for data streaming
- **PostgreSQL** - Data warehouse for processed data
- **Data Producers** - Generate and stream sample data
- **Spark** - Process and aggregate streaming data
- **Superset** - Data visualization dashboard

## Service Dependencies & Startup Sequence

The pipeline starts in the following order:

1. **Kafka** - Message broker starts first
2. **PostgreSQL** - Database starts in parallel
3. **Database Initialization** - Creates tables and schema
4. **Data Producers** - Start generating data after Kafka and DB are ready
5. **Spark Jobs** - Start processing after producers begin
6. **Superset** - Dashboard starts after database is ready

## Access Points

- **Kafka**: `localhost:9092`
- **PostgreSQL**: `localhost:5432`
- **Spark Master**: `localhost:7077`
- **Spark UI**: `http://localhost:8080`
- **Superset**: `http://localhost:8088`

## Environment Configuration

All configuration is in `docker.env`:

```bash
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=salesdb
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
# ... other settings
```

## Monitoring & Troubleshooting

### Check Service Status
```bash
docker-compose ps
```

### View Logs for Specific Service
```bash
docker-compose logs -f [service_name]
```

### Restart a Service
```bash
docker-compose restart [service_name]
```

### Access Container Shell
```bash
docker-compose exec [service_name] bash
```

## Data Flow

1. **Data Generation**: Producers create sample sales data
2. **Streaming**: Data flows through Kafka topics
3. **Processing**: Spark jobs aggregate and transform data
4. **Storage**: Processed data stored in PostgreSQL
5. **Visualization**: Superset provides dashboard views

## Scaling

To scale specific services:

```bash
docker-compose up -d --scale data_producers=3
```

## Cleanup

To completely remove all containers and volumes:

```bash
docker-compose down -v
```

## Development

For development, you can override settings using `docker-compose.override.yml` or modify `docker.env`.