from pydantic import BaseModel
from typing import Dict

class SensorMeasurements(BaseModel):
    pressure: float
    average_temperature: float
    heat: Dict[str, float]
    water: Dict[str, float]
    volume: Dict[str, float]
    power: Dict[str, float]
    raw_data: Dict[str, float]

class SensorData(BaseModel):
    timestamp: str
    measurements: SensorMeasurements
