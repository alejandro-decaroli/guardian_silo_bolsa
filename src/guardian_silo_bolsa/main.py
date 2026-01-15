from fastapi import FastAPI, HTTPException, status
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
from fastapi.responses import JSONResponse

load_dotenv()

app = FastAPI(title="Guardián de Silobolsas API")

@app.post("/ingest")
async def guardar_registro(datos: LecturaSilo) -> JSONResponse: 

    try:

        fields = {}

        if datos.co2 != None:
            fields["co2"] = datos.co2
        if datos.hum != None:
            fields["hum"] = datos.hum
        if datos.temp != None:
            fields["temp"] = datos.temp

        point = {
                    "measurement": "sensores_silo",
                    "tags": {
                        "grano": datos.grano, 
                        "sensor_id": datos.sensor_id, 
                        "silo": datos.silo
                    },
                    "fields": fields,
                    "timestamp": datos.timestamp
                }

        if not fields:

            guardar_en_csv(datos)

            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED, 
                content="Aceptado, pero hay valores nulos en todos los 'fields'. No se registra el punto en influxdb3, pero si en el archivo csv"
                )

        client.write(record=point) 
        
        guardar_en_csv(datos)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Registro creado con éxito en influxdb3 y archivo csv")
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK, content="Bienvenido a Guardián silo bolsa")
