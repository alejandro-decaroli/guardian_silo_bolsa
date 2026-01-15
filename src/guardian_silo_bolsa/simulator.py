import requests
import time
import random
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import Any
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status

load_dotenv()

API_URL = os.getenv("API_URL", "http://guardian_api:8000/ingest")

class Sensor:
    def __init__(self, sensor_id: str, grano: str, silo: str):
        self.sensor_id = sensor_id
        self.grano = grano
        self.silo = silo
        self.modo = "NORMAL"
        self.temp = 20
        self.hum = 10
        self.co2 = 350

    def simular(self) -> None:
        
        if self.modo == "NORMAL":

            if self.temp == None:
                self.temp = round(20 + random.uniform(-0.1, 0.1), 2)
            if self.hum == None:
                self.hum = round(10 + random.uniform(-0.05, 0.05), 2)
            if self.co2 == None:
                self.co2 = round(350 + random.uniform(-0.05, 0.05), 2)

            if random.random() < 0.01:
                self.modo = random.choice(["CALENTAMIENTO", "FALLA_SENSOR"])
            
        elif self.modo == "CALENTAMIENTO":
            self.temp = round(self.temp + random.uniform(0.2, 0.5), 2)
            self.co2 = round(self.hum + random.randint(20, 50), 2)
            self.hum = round(self.co2 + random.uniform(0.1, 0.2), 2)

            if self.temp > 45: 
                 self.modo = "FALLA_SENSOR"

        elif self.modo == "FALLA_SENSOR":
            self.temp = None
            self.co2 = None
            self.hum = None
            
            if random.random() < 0.1: 
                self.modo = "NORMAL"
        

    def publicar(self) -> JSONResponse:

        payload = {
            "grano": self.grano,
            "sensor_id": self.sensor_id,
            "silo": self.silo,
            "timestamp": datetime.now().isoformat(),
            "temp": self.temp,
            "co2": self.co2,
            "hum": self.hum
        }

        response: JSONResponse = requests.post(API_URL, json=payload)

        return response

sensores = [
    Sensor("sensor_01", "Silo-Norte-Rosario", "soja_premium"), 
    Sensor("sensor_02", "Silo-Sur-Casilda", "soja_base"), 
    Sensor("sensor_03", "Silo-Este-Victoria", "maiz_2024"), 
    Sensor("sensor_04", "Silo-Oeste-Roldan", "soja_premium")
    ]


print("🚀 Iniciando simulador de 4 sensores... (Ctrl+C para detener)")

try:
    while True:
        for sensor in sensores:
            try:
                sensor.simular()
                response: JSONResponse = sensor.publicar()
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        time.sleep(2)  
except KeyboardInterrupt:
    print("\n👋 Simulador detenido.")
    

