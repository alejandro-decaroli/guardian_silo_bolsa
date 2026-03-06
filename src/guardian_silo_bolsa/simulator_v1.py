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

            if self.temp is None:
                self.temp = round(20 + random.uniform(-0.1, 0.1), 2)
            if self.hum is None:
                self.hum = round(10 + random.uniform(-0.05, 0.05), 2)
            if self.co2 is None:
                self.co2 = round(350 + random.uniform(-5, 5), 2)

            if random.random() < 0.01:
                self.modo = random.choice(["CALENTAMIENTO", "FALLA_SENSOR"])
            
        elif self.modo == "CALENTAMIENTO":
            incremento_hum = random.uniform(0.05, 0.1)
            self.hum = round(self.hum + incremento_hum, 2)

            incremento_co2 = (self.hum * 2.5) + random.randint(10, 30)
            self.co2 = round(self.co2 + incremento_co2, 2)

            incremento_temp = (incremento_co2 / 100) + random.uniform(0.1, 0.3)
            self.temp = round(self.temp + incremento_temp, 2)

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
    Sensor("sensor_01", "soja", "Silo-Norte-Rosario"), 
    Sensor("sensor_02", "soja", "Silo-Sur-Casilda"), 
    Sensor("sensor_03", "maiz", "Silo-Este-Victoria"), 
    Sensor("sensor_04", "trigo", "Silo-Oeste-Roldan"),
    Sensor("sensor_05", "trigo", "Silo-este-Roldan"),
    Sensor("sensor_06", "maiz", "Silo-oeste-Victoria")
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
    

