from pydantic import BaseModel

class Medidas(BaseModel):
    temp: float
    hum: float
    co2: float


class LecturaSilo(BaseModel):
    grano: str
    sensor_id: str
    silo: str
    timestamp: str
    measurements: Medidas