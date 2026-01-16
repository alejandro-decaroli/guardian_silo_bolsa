import requests
import os
from dotenv import load_dotenv
from datetime import timedelta
from .models import LecturaSilo
from typing import Dict

load_dotenv()

# Configuración de límites por tipo de grano
THRESHOLDS = {
    "soja": {"hum": 15.0, "temp": 35.0, "co2": 800},
    "maiz": {"hum": 16.0, "temp": 38.0, "co2": 900},
    "trigo": {"hum": 15.5, "temp": 34.0, "co2": 700}
}

def enviar_alarma_telegram(mensaje):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Error enviando Telegram: {e}")


ultimas_alertas: Dict = {}

def chequear_umbrales(datos: LecturaSilo) -> None:

    alertas = []

    limites = THRESHOLDS.get(datos.grano.lower(), {"hum": 15.0, "temp": 35.0, "co2": 800})

    if datos.temp is None:
        alertas.append("❌ *Falla*: Sensor de temperatura offline")
    elif datos.temp > limites["temp"]:
        alertas.append(f"⚠️ *Temperatura Crítica*: {datos.temp}°C")

    if datos.co2 is None:
        alertas.append("❌ *Falla*: Sensor de CO2 offline")
    elif datos.co2 > limites["co2"]:
        alertas.append(f"💨 *CO2 Elevado*: {datos.co2} ppm")

    if datos.hum is None:
        alertas.append("❌ *Falla*: Sensor de humedad offline")
    elif datos.hum > limites["hum"]:
        alertas.append(f"💧 *Humedad Elevada*: {datos.hum}%")

    if alertas:

        mensaje = f"🚨 *Alerta en silo:{datos.silo}*\nID: `{datos.sensor_id}` | Grano: {datos.grano.capitalize()}\n" + "\n".join(alertas)
  
        if datos.sensor_id not in ultimas_alertas:
            enviar_alarma_telegram(mensaje)
            ultimas_alertas[datos.sensor_id] = datos
        else:
            if datos.timestamp - ultimas_alertas[datos.sensor_id].timestamp > timedelta(minutes=1):
                enviar_alarma_telegram(mensaje)
                ultimas_alertas[datos.sensor_id] = datos
    else:

        if datos.sensor_id in ultimas_alertas:
            ultimas_alertas.pop(datos.sensor_id)