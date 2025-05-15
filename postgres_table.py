import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432")
)


cursor = conn.cursor()


create_order_summary = """
DROP TABLE IF EXISTS realtime_order_summary;

CREATE TABLE realtime_order_summary (
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    category TEXT,
    payment_method TEXT,
    total_revenue DOUBLE PRECISION,
    order_count BIGINT
);
"""


create_user_activity_summary = """
DROP TABLE IF EXISTS user_activity_summary;

CREATE TABLE user_activity_summary (
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    user_id TEXT,
    device TEXT,
    location TEXT,
    event_count BIGINT,
    session_start TIMESTAMP,
    session_end TIMESTAMP,
    session_duration_seconds BIGINT
);

"""


cursor.execute(create_order_summary)
cursor.execute(create_user_activity_summary)

conn.commit()
cursor.close()
conn.close()

print("✅ Tables created if they didn't already exist.")
