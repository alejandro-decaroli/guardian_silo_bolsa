from influxdb_client_3 import (
  InfluxDBClient3, 
  InfluxDBError, 
  Point, 
  WritePrecision,
  WriteOptions,
  write_client_options
  )
from dotenv import load_dotenv
import os
from ...domain.repository.database import ISensorDatabase


load_dotenv()

host = os.getenv('INFLUX_HOST', "http://influxdb3-core:8181")
token = os.getenv('INFLUX_TOKEN')
database = os.getenv('INFLUX_DATABASE', "guardian_db")

client = InfluxDBClient3(host=host,
                        database=database,
                        token=token) 

class InfluxDB3Database(ISensorDatabase):
    """Implementacion de la interfaz de base de datos para InfluxDB3."""
    def __init__(self, client=client):
        self.client = client
    
    def write(self, data: dict) -> bool:
        """Escribe datos en el TSDB."""
        try:
            self.client.write(record=data)
            return True
        except Exception as e:
            print(f"Error writing to InfluxDB: {e}")
            return False
    
    def read(self, query: str) -> bool:
        """Lee datos del TSDB."""
        try:
            self.client.query(query)
            return True
        except Exception as e:
            print(f"Error reading from InfluxDB: {e}")
            return False
    
    def get_data(self, query: str) -> bool:
        """Obtiene datos del TSDB."""
        try:
            self.client.query(query)
            return True
        except Exception as e:
            print(f"Error getting data from InfluxDB: {e}")
            return False

    def create_db_and_tables(self):
        """Crea la base de datos y las tablas."""
        raise NotImplementedError

    def connect(self):
        """Conecta a la base de datos."""
        raise NotImplementedError

    def close(self):
        """Cierra la conexión a la base de datos."""
        raise NotImplementedError

    def get_status(self):
        """Obtiene el estado de la base de datos."""
        raise NotImplementedError