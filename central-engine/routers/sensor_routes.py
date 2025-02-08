from fastapi import APIRouter, Depends
from ..models.sensorModel import SensorData
from ..producer import kafka_producer
from ..config import KAFKA_TOPICS

sensor_router = APIRouter()

@sensor_router.post("/sensor-data")
async def receive_sensor_data(data: SensorData):
    """Receive and forward sensor data to Kafka"""
    await kafka_producer.send(KAFKA_TOPICS["sensor_data"], data.dict())
    return {"message": "Sensor data sent to Kafka"}
