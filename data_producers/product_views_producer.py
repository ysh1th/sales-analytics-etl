import time
import json
from kafka import KafkaProducer
from data_generator import generate_product_view

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = "productViews"

def produce_product_views():
    while True:
        view_data = generate_product_view()
        producer.send(TOPIC_NAME, value=view_data)
        print(f"Produced to {TOPIC_NAME}: {view_data}")
        time.sleep(0.7)  # simulate user browsing pace

if __name__ == "__main__":
    produce_product_views()
