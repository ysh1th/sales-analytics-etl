# common Faker logic
from datetime import datetime, timedelta
import threading
import uuid
from faker import Faker
import random
import time
from tzlocal import get_localzone


faker = Faker()

PRODUCTS = [
    {"product_id": 101, "category": "Electronics"},
    {"product_id": 102, "category": "Clothing"},
    {"product_id": 103, "category": "Groceries"},
    {"product_id": 104, "category": "Books"},
    {"product_id": 105, "category": "Beauty"},
]

DEVICES = ["mobile", "desktop", "tablet"]

EVENTS = ["login", "search", "add_to_cart", "checkout", "logout"]


def current_local_time():
    return datetime.now(get_localzone()).isoformat()

# --- Order generator ---
def generate_order():
    product = random.choice(PRODUCTS)
    return {
        "order_id": faker.uuid4(),
        "user_id": random.randint(1, 100),
        "product_id": product["product_id"],
        "category": product["category"],
        "amount": round(random.uniform(5, 500), 2),
        "payment_method": random.choice(["card", "wallet", "cod"]),
        "timestamp": current_local_time()
    }


active_sessions = {}


def generate_user_activity():
    if len(active_sessions) < 5 and random.random() < 0.5:
        user_id = random.randint(1, 100)
        if user_id not in active_sessions:
            session_id = str(uuid.uuid4())
            device = random.choice(DEVICES)
            location = faker.city()
            active_sessions[user_id] = {
                "session_id": session_id,
                "device": device,
                "location": location,
                "current_event_index": 0,
                "start_time": datetime.now()
            }

    # pick random active user
    if active_sessions:
        user_id = random.choice(list(active_sessions.keys()))
        session = active_sessions[user_id]

        event_type = EVENTS[session["current_event_index"]]
        event_time = session["start_time"] + timedelta(seconds=random.randint(0, 2))

        event = {
            "event_id": str(uuid.uuid4()),
            "user_id": user_id,
            "session_id": session["session_id"],
            "event_type": event_type,
            "device": session["device"],
            "location": session["location"],
            "timestamp": event_time.isoformat()
        }

        session["current_event_index"] += 1

        # end session if all events done
        if session["current_event_index"] >= len(EVENTS):
            del active_sessions[user_id]
        return event
    return None


# # --- product views generator ---
# def generate_product_view():
#     product = random.choice(PRODUCTS)
#     return {
#         "view_id": faker.uuid4(),
#         "user_id": random.randint(1, 100),
#         "product_id": product["product_id"],
#         "category": product["category"],
#         "device": random.choice(DEVICES),
#         "referrer": faker.uri(),
#         "timestamp": current_local_time()
#     }