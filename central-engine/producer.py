from aiokafka import AIOKafkaProducer
import json
from .config import KAFKA_BOOTSTRAP_SERVERS

class KafkaProducer:
    def __init__(self):
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.producer.start()

    async def send(self, topic: str, message: dict):
        if self.producer is None:
            raise Exception("Producer not started")
        await self.producer.send(topic, value=message)

    async def stop(self):
        if self.producer:
            await self.producer.stop()

# Singleton instance of producer
kafka_producer = KafkaProducer()
