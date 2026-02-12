from fastapi import APIRouter, Depends, status
from ...application.user_cases.sensor import (
    CreateSensor, 
    GetSensor, 
    GetSensors, 
    UpdateSensor, 
    DeleteSensor
)
from ..database.deps import postgres_db
from ...domain.models.models import Sensor, SensorBase
from typing import List, Dict

def get_user_case(case_type: str):
    def _get_case():
        if case_type == "get": return GetSensor(postgres_db)
        if case_type == "get_all": return GetSensors(postgres_db)
        if case_type == "create": return CreateSensor(postgres_db)
        if case_type == "update": return UpdateSensor(postgres_db)
        if case_type == "delete": return DeleteSensor(postgres_db)
    return _get_case

sensor_router = APIRouter(prefix="/sensors", tags=["sensors"])

@sensor_router.get("/{sensor_id}", response_model=Sensor)
def get_sensor(sensor_id: int, service: GetSensor = Depends(get_user_case("get"))) -> Sensor:
    return service.execute(sensor_id)

@sensor_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Sensor])
def get_sensors(service: GetSensors = Depends(get_user_case("get_all"))) -> List[Sensor]:
    return service.execute()

@sensor_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Sensor)
def create_sensor(sensor: SensorBase, service: CreateSensor = Depends(get_user_case("create"))) -> Sensor:
    db_sensor = Sensor.model_validate(sensor)
    return service.execute(db_sensor)

@sensor_router.put("/{sensor_id}", status_code=status.HTTP_200_OK)
def update_sensor(sensor_id: int, sensor: SensorBase, service: UpdateSensor = Depends(get_user_case("update"))) -> Sensor:
    db_sensor = Sensor.model_validate(sensor)
    return service.execute(sensor_id, db_sensor)

@sensor_router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(sensor_id: int, service: DeleteSensor = Depends(get_user_case("delete"))) -> None:
    service.execute(sensor_id)

