from pydantic import BaseModel
from typing import Optional

class LecturaSilo(BaseModel):
    grano: str
    sensor_id: str
    silo: str
    timestamp: str
    temp: Optional[float]
    hum: Optional[float]
    co2: Optional[float]