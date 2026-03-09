from dotenv import load_dotenv
import csv
from pathlib import Path
import os
from ...domain.repository.backup import IBackup
from ...domain.models.models import TelemetrySchema

load_dotenv()
# Definimos la ruta del archivo 
CSV_FILE = Path(os.getenv("CSV_PATH", "backups/data_backup.csv"))

class CSVBackup(IBackup):
    """
    Implementación de backup usando CSV
    """
    def __init__(self, path: str = None):
        if path is None:
            path = CSV_FILE
        self.path = path

    def create_backup(self, datos: TelemetrySchema, silobolsa_id: int, sensor_id: int) -> dict:

        try:
            # Verifico si el archivo existe para escribir la cabecera la primera vez
            file_exists = Path(self.path).exists()
            
            with open(self.path, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                
                # Cabecera (solo si el archivo es nuevo)
                if not file_exists:
                    writer.writerow(["timestamp", "silo_id", "sensor_id", "temp", "hum", "co2"])
                
                # Fila de datos
                writer.writerow([
                    datos.timestamp,
                    silobolsa_id,
                    sensor_id,
                    datos.temp,
                    datos.hum,
                    datos.co2
                ])

                f.flush()
            
        except Exception as e:
            print(f"Error al crear backup: {e}")
            return {"status_code": 500, "message": "Error al crear backup, causa:" + str(e)}
        
        return {"status_code": 201, "message": "Backup creado con éxito"}

    def restore_backup(self) -> dict:
        try:
            # TODO: Implementar restauración desde CSV
            pass
        except Exception as e:
            print(f"Error al restaurar backup: {e}")
            return {"status_code": 500, "message": "Error al restaurar backup, causa:" + str(e)}
        
        return {"status_code": 200, "message": "Backup restaurado con éxito"}
