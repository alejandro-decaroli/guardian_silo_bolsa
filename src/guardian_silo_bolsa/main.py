from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import requests

app = FastAPI(title="Guardián de Silobolsas API")

# Modelo anidado para las mediciones
class Measurements(BaseModel):
    temp: float
    co2: int
    hum: float

# Modelo principal
class LecturaSensor(BaseModel):
    tag: str
    sensor_id: str
    silo: str
    timestamp: str
    measurements: Measurements

@app.post("/ingest")
async def recibir_datos(datos: LecturaSensor):
    return {"status code": 200}

@app.get("/")
async def root():
    return {"message": "Hello world!"}
