import requests
import time
import random
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://guardian_api:8000/ingest")

silos = [
    {"id": "sensor_01", "name": "Silo-Norte-Rosario", "grano": "soja_premium"},
    {"id": "sensor_02", "name": "Silo-Sur-Casilda", "grano": "soja_base"},
    {"id": "sensor_03", "name": "Silo-Este-Victoria", "grano": "maiz_2024"},
    {"id": "sensor_04", "name": "Silo-Oeste-Roldan", "grano": "soja_premium"}
]

def generate_data(silo_info):
    return {
        "grano": silo_info["grano"],
        "sensor_id": silo_info["id"],
        "silo": silo_info["name"],
        "timestamp": datetime.now().isoformat(),
        "measurements": {
            "temp": round(random.uniform(20.0, 28.0), 2),
            "co2": random.randint(350, 600),
            "hum": round(random.uniform(11.0, 14.0), 2)
        }
    }

print("🚀 Iniciando simulador de 4 sensores... (Ctrl+C para detener)")

try:
    while True:
        for silo in silos:
            payload = generate_data(silo)
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    print(f"✅ Enviado: {payload['silo']} | CO2: {payload['measurements']['co2']}")
                else:
                    print(f"⚠️ Error {response.status_code} en {payload['silo']}")
            except requests.exceptions.ConnectionError:
                print("❌ No se pudo conectar con el servidor. ¿Está prendido?")
        
        print("-" * 30)
        time.sleep(5)  
except KeyboardInterrupt:
    print("\n👋 Simulador detenido.")