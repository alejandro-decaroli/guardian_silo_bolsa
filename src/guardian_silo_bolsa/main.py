from fastapi import FastAPI, HTTPException
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
from .models import LecturaSilo
from .utils import guardar_en_csv
from .db import client, database

load_dotenv()

app = FastAPI(title="Guardián de Silobolsas API")

@app.post("/ingest")
async def guardar_registro(datos: LecturaSilo): 

    try:

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
        
        guardar_en_csv(datos)

        return {"status code": 204}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Guardián silo bolsa"}
