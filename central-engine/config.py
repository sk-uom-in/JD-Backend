import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

# Define multiple topics
KAFKA_TOPICS = {
    "sensor_data": "sensor_topic",
    "accident_data": "accident_topic"
}

KAFKA_GROUPS = {
    "atkins": "atkins_group",
}