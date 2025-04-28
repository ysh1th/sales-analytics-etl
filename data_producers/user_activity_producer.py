import time
import json
from kafka import KafkaProducer
from data_generator import generate_user_activity

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = "userActivity"

def produce_user_activities():
    while True:
        activity_data = generate_user_activity()
        if activity_data:
            producer.send(TOPIC_NAME, value=activity_data)
            print(f"Produced to {TOPIC_NAME}: {activity_data}")
        time.sleep(0.5) 

if __name__ == "__main__":
    produce_user_activities()
