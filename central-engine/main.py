import asyncio
import json
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from .tDatabase import Base, engine, get_db
from .producer import kafka_producer
from .routers import sensor_routes
from sqlalchemy import text
from .consumers.sensor_consumer import consume_sensor_data
from sqlalchemy.ext.asyncio import AsyncSession
from .config import KAFKA_BOOTSTRAP_SERVERS  # Import Kafka settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan event handling Kafka startup and shutdown."""
    global consumer_tasks

    
    await init_db()

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


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
# Include API routes
app.include_router(sensor_routes.sensor_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test-db/")
async def test_db_connection(db: AsyncSession = Depends(get_db)):  # ✅ Async function
    try:
        result = await db.execute(text("SELECT 1"))  # ✅ Await the DB query
        return {"message": "Database connected successfully"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0000", port=8000)