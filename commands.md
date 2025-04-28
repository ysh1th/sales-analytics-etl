
# start PostgreSQL
```
pg_ctl -D /opt/homebrew/var/postgres -l logfile start
(or)
brew services start postgresql
```

- to stop postgresql services:
`brew services stop postgresql`

# start kafka server
```
cd kafka_2.13-4.0.0/ 
bin/kafka-server-start.sh config/server.properties
```

# start kafka consumers
```
~/kafka_2.13-4.0.0/bin/kafka-console-consumer.sh --topic orders --bootstrap-server localhost:9092
~/kafka_2.13-4.0.0/bin/kafka-console-consumer.sh --topic userActivity --bootstrap-server localhost:9092
~/kafka_2.13-4.0.0/bin/kafka-console-consumer.sh --topic productViews --bootstrap-server localhost:9092
```

# run all producers at once
`python run_producers.py`


# run spark job with JDBC JAR (while in project root dir)
```
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 \
  --jars ~/jars/postgresql-42.7.3.jar \
  --conf "spark.driver.extraJavaOptions=-XX:+UseG1GC" \
  --conf "spark.executor.extraJavaOptions=-XX:+UseG1GC" \
  spark_jobs/order_aggregator.py
```

```
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 \
  --jars ~/jars/postgresql-42.7.3.jar \
  --conf "spark.driver.extraJavaOptions=-XX:+UseG1GC" \
  --conf "spark.executor.extraJavaOptions=-XX:+UseG1GC" \
  spark_jobs/user_trend.py
```

# setting up superset
## first time:
### step 1:
```
git clone https://github.com/apache/superset
cd superset
git checkout tags/4.1.2
docker compose -f docker-compose-image-tag.yml up
```

### Step 2: Log in to Superset
Visit http://localhost:8088

Username: admin
Password: admin

### step 3:
In Superset:
- Settings > Data > Databases > + Database

SQLAlchemy URI:
your postgresql credentials in the command:
`postgresql://<user>:<password>@<host>:<port>/<database>`

---

# post dockerizing

docker ps   # (to find spark container name)

docker exec -it <your-spark-container-name> bash

## Now inside container:
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 \
  --jars /opt/spark/jars/postgresql.jar \
  --conf "spark.driver.extraJavaOptions=-XX:+UseG1GC" \
  --conf "spark.executor.extraJavaOptions=-XX:+UseG1GC" \
  order_aggregator.py

## superset
docker-compose exec superset superset fab create-admin \
   --username admin --firstname Superset --lastname Admin --email admin@superset.com --

docker-compose build

docker-compose up -d

docker exec -it spark bash

spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 \
  --jars /app/postgresql-42.7.3.jar \
  /app/order_aggregator.py
