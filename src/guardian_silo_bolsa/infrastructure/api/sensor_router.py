from fastapi import APIRouter, Depends, status
from ...application.user_cases.sensor import (
    CreateSensor, 
    GetSensor, 
    GetSensors, 
    UpdateSensor, 
    DeleteSensor
)
from ..database.deps import postgres_db
from ...domain.models.models import Sensor, SensorBase, Usuario
from typing import List, Dict, Any
from ..security.deps import get_current_user
from ..security.auth_handler import auth_service_instance

def get_user_case(case_type: str):
    def _get_case():
        if case_type == "get": return GetSensor(postgres_db)
        if case_type == "get_all": return GetSensors(postgres_db)
        if case_type == "create": return CreateSensor(postgres_db, auth_service_instance)
        if case_type == "update": return UpdateSensor(postgres_db)
        if case_type == "delete": return DeleteSensor(postgres_db)
    return _get_case

sensor_router = APIRouter(prefix="/sensors", tags=["sensors"], dependencies=[Depends(get_current_user)])

@sensor_router.get("/handshake", status_code=status.HTTP_200_OK, response_model=Sensor)
def handshake(mac_address: Any, case: GetSensor = Depends(get_user_case("get"))) -> Sensor:
    return case.get_by_handshake(mac_address)

@sensor_router.get("/{sensor_id}", response_model=Sensor)
def get_sensor(sensor_id: int, case: GetSensor = Depends(get_user_case("get")), current_user: Usuario = Depends(get_current_user)) -> Sensor:
    return case.execute(sensor_id, current_user.id)

@sensor_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Sensor])
def get_sensors(case: GetSensors = Depends(get_user_case("get_all")), current_user: Usuario = Depends(get_current_user)) -> List[Sensor]:
    return case.execute(current_user.id)

@sensor_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=Sensor)
def create_sensor(sensor: SensorBase, case: CreateSensor = Depends(get_user_case("create")), current_user: Usuario = Depends(get_current_user)) -> Sensor:
    return case.execute(sensor, current_user.id)

@sensor_router.put("/update/{sensor_id}", status_code=status.HTTP_200_OK, response_model=Sensor)
def update_sensor(sensor_id: int, sensor: SensorBase, case: UpdateSensor = Depends(get_user_case("update")), current_user: Usuario = Depends(get_current_user)) -> Sensor:
    return case.execute(sensor_id, sensor, current_user.id)

@sensor_router.delete("/delete/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_sensor(sensor_id: int, case: DeleteSensor = Depends(get_user_case("delete")), current_user: Usuario = Depends(get_current_user)) -> None:
    case.execute(sensor_id, current_user.id)

