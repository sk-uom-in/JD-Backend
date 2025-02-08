import asyncio
import json
from aiokafka import AIOKafkaConsumer
from ..config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPICS, KAFKA_GROUPS

async def consume_sensor_data():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPICS["sensor_data"],
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUPS["atkins"],
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received sensor data: {msg.value}")
            # Process the sensor data here
    finally:
        await consumer.stop()
