import time
import json
from kafka import KafkaProducer
from data_generator import generate_order

producer = KafkaProducer(
  bootstrap_servers='kafka:9092',
  value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = "orders"

def produce_orders():
  while True:
     order_data = generate_order()
     producer.send(TOPIC_NAME, value=order_data)
     print(f'produced to {TOPIC_NAME}: {order_data}')
     time.sleep(1)

if __name__ == "__main__":
   produce_orders()