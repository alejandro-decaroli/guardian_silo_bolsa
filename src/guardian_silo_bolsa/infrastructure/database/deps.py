from .postgres import PostgresDatabase
from .influxdb3 import InfluxDB3Database

postgres_db: PostgresDatabase = PostgresDatabase()
influxdb3_db: InfluxDB3Database = InfluxDB3Database()


def get_db() -> PostgresDatabase:
    return postgres_db

def get_influxdb3_db() -> InfluxDB3Database:
    return influxdb3_db