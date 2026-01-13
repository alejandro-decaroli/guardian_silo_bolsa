from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import requests
import os
from influxdb_client_3 import (
  InfluxDBClient3, 
  InfluxDBError, 
  Point, 
  WritePrecision,
  WriteOptions,
  write_client_options
  )
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('INFLUX_HOST', "http://influxdb3-core:8181")
token = os.getenv('INFLUX_TOKEN')
database = os.getenv('INFLUX_DATABASE', "guardian_db")

client = InfluxDBClient3(host=host,
                        database=database,
                        token=token)                       

app = FastAPI(title="Guardián de Silobolsas API")

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

@app.post("/ingest")
async def recibir_datos(datos: LecturaSilo): 
    try:
        
        print(f"Recibido: {datos.silo} - Grano: {datos.grano}")

        point = {
            "measurement": database, 
            "tags": {
                "grano": datos.grano, 
                "sensor_id": datos.sensor_id, 
                "silo": datos.silo
            },
            "fields": {
                "temp": datos.measurements.temp,
                "hum": datos.measurements.hum,
                "co2": datos.measurements.co2
            },
            "time": datos.timestamp
        }
        
        client.write(record=point) 
        
        return {"status code": 200, "msg": "Registro escrito con éxito"}
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error durante la escritura")

@app.get("/")
async def root():
    return {"message": "Guardián silo bolsa"}
