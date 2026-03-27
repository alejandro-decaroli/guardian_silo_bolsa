from dotenv import load_dotenv # type: ignore
import csv
from pathlib import Path
import os
from ...domain.repository.backup import IBackup
from ...domain.models.models import TelemetrySchema
from ...domain.exceptions.exceptions import AppError
from typing import Dict, Any

load_dotenv()
# Definimos la ruta del archivo 
CSV_FILE = Path(os.getenv("CSV_PATH", "backups/data_backup.csv"))

class CSVBackup(IBackup):
    """
    Implementación de backup usando CSV
    """
    def __init__(self, path: str | None = None):
        if path is None:
            path = str(CSV_FILE)
        self.path = path

    def create_backup(self, datos: TelemetrySchema, sensor_id: int) -> Dict[str,Any]:

        try:
            # Verifico si el archivo existe para escribir la cabecera la primera vez
            file_exists = Path(self.path).exists()
            
            with open(self.path, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                
                # Cabecera (solo si el archivo es nuevo)
                if not file_exists:
                    writer.writerow(["timestamp", "sensor_id", "temp", "hum", "co2"])
                
                # Fila de datos
                writer.writerow([
                    datos.timestamp,
                    sensor_id,
                    datos.temp,
                    datos.hum,
                    datos.co2
                ])

                f.flush()
            return {"status_code": 201, "message": "Backup creado con éxito"}
        except Exception as e:
            raise AppError("Error al crear backup", 500)
        

    def restore_backup(self) -> Dict[str,Any]:
        try:
            # TODO: Implementar restauración desde CSV
            pass
        except Exception as e:
            raise AppError("Error al restaurar backup", 500)
        
        return {"status_code": 200, "message": "Backup restaurado con éxito"}
