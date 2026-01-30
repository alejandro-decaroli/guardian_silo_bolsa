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

load_dotenv()

host = os.getenv('INFLUX_HOST', "http://influxdb3-core:8181")
token = os.getenv('INFLUX_TOKEN')
database = os.getenv('INFLUX_DATABASE', "guardian_db")

client = InfluxDBClient3(host=host,
                        database=database,
                        token=token) 