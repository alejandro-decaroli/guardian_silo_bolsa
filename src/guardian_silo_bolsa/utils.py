from dotenv import load_dotenv
import csv
from pathlib import Path
import os
from .models import LecturaSilo

load_dotenv()
# Definimos la ruta del archivo 
CSV_FILE = Path(os.getenv("CSV_PATH", "backups/data_backup.csv"))

def guardar_en_csv(datos: LecturaSilo) -> None:

    # Verifico si el archivo existe para escribir la cabecera la primera vez
    file_exists = CSV_FILE.exists()
    
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        # Cabecera (solo si el archivo es nuevo)
        if not file_exists:
            writer.writerow(["timestamp", "silo", "grano", "sensor_id", "temp", "hum", "co2"])
        
        # Fila de datos
        writer.writerow([
            datos.timestamp,
            datos.silo,
            datos.grano,
            datos.sensor_id,
            datos.temp,
            datos.hum,
            datos.co2
        ])

        f.flush()