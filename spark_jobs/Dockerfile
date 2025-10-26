# spark_jobs/Dockerfile

FROM bitnami/spark:3.4.1

RUN mkdir -p /var/lib/apt/lists/partial && apt-get update && apt-get install -y netcat-openbsd postgresql-client

WORKDIR /app

COPY ./order_aggregator.py .
COPY ./user_trend.py .
COPY ./start-spark-jobs.sh /scripts/

# Download PostgreSQL JDBC driver
RUN mkdir -p /opt/spark/jars && \
    curl -L -o /opt/spark/jars/postgresql.jar https://jdbc.postgresql.org/download/postgresql-42.7.3.jar

RUN chmod +x /scripts/start-spark-jobs.sh

CMD ["/scripts/start-spark-jobs.sh"]
