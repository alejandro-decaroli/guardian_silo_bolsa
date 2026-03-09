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

INGEST_API_URL = os.getenv("INGEST_API_URL", "http://guardian_api:8000/api/v1/ingest")
HANDSHAKE_API_URL = os.getenv("HANDSHAKE_API_URL", "http://guardian_api:8000/api/v1/sensors/handshake")

MAC_ADDRESS = [
    "00:11:22:33:44:55",
    "00:11:22:33:44:56",
    "00:11:22:33:44:57",
    "00:11:22:33:44:58",
    "00:11:22:33:44:59",
    "00:11:22:33:44:60"
]
  
class Sensor:
    def __init__(self, mac_address: str):
        self.mac_address = mac_address
        self.api_key = None
        self.modo = "NORMAL"
        self.temp = 20
        self.hum = 10
        self.co2 = 350
        self.handshake = False

    def do_handshake(self) -> None:
        """Método para realizar el handshake con la API"""

        try:
            response: JSONResponse = requests.get(HANDSHAKE_API_URL, json={"mac_address": self.mac_address})
            if response.status_code == 200:
                self.handshake = True
                self.api_key = response.json().get("api_key")
        except requests.exceptions.ConnectionError:
            time.sleep(5)
        except Exception as e:
            time.sleep(5)

    def simular(self) -> None:
        """Método para simular los valores de los sensores"""

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
            "api_key": self.api_key,
            "timestamp": datetime.now().isoformat(),
            "temp": self.temp,
            "co2": self.co2,
            "hum": self.hum
        }

        response: JSONResponse = requests.post(INGEST_API_URL, json=payload)

        return response

sensores = [
    Sensor(mac_address) for mac_address in MAC_ADDRESS
]

try:
    while True:
        for sensor in sensores:
            try:
                if not sensor.handshake:
                    sensor.do_handshake()
                else:
                    sensor.simular()
                    response: JSONResponse = sensor.publicar()
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        time.sleep(2)  
except KeyboardInterrupt:
    print("\n👋 Simulador detenido.")
    

