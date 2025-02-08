import asyncio
import json
from fastapi import FastAPI
from aiokafka import AIOKafkaProducer
from contextlib import asynccontextmanager

from .producer import kafka_producer
from .routers import sensor_routes
from .consumers.sensor_consumer import consume_sensor_data
from .config import KAFKA_BOOTSTRAP_SERVERS  # Import Kafka settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan event handling Kafka startup and shutdown."""
    global consumer_tasks
    
    # Initialize Kafka producer
    await kafka_producer.start()
    print("Kafka Producer Started.")

    # Start Kafka consumers
    consumer_tasks = [
        asyncio.create_task(consume_sensor_data())
    ]
    print("Kafka Consumers Started.")

    yield  # Run the FastAPI application

    # Cleanup on shutdown
    print("Shutting down Kafka Producer and Consumers...")
    await kafka_producer.stop()

    for task in consumer_tasks:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

app = FastAPI(lifespan=lifespan)

# Include API routes
app.include_router(sensor_routes.sensor_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0000", port=8000)