from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LecturaSilo(BaseModel):
    grano: str
    sensor_id: str
    silo: str
    timestamp: datetime
    temp: Optional[float]
    hum: Optional[float]
    co2: Optional[float]

