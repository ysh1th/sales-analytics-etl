# spark_jobs/Dockerfile

FROM bitnami/spark:3.4.1-debian-11-r10

WORKDIR /app

COPY ./order_aggregator.py .
COPY ./user_trend.py .

# Download PostgreSQL JDBC driver
RUN mkdir -p /opt/spark/jars && \
    curl -L -o /opt/spark/jars/postgresql.jar https://jdbc.postgresql.org/download/postgresql-42.7.3.jar

CMD [ "sleep", "infinity" ]
