from fastapi import APIRouter, Depends, status # type: ignore
from ...application.user_cases.silo import (
    CreateSilo, 
    GetSilo, 
    GetSilos, 
    UpdateSilo, 
    DeleteSilo,
    SetearSensor,
)
from ...application.user_cases.telemetry import GetSiloTelemetry
from ..database.deps import postgres_db, influxdb3_db
from ...domain.models.models import (
    Silobolsa, 
    SilobolsaBase, 
    Usuario,
    SensorSilo
)
from typing import List, Optional, Dict, Any
from ..security.deps import get_current_user

def get_user_case(case_type: str):
    def _get_case():
        if case_type == "get": return GetSilo(postgres_db)
        if case_type == "get_all": return GetSilos(postgres_db)
        if case_type == "create": return CreateSilo(postgres_db)
        if case_type == "update": return UpdateSilo(postgres_db)
        if case_type == "delete": return DeleteSilo(postgres_db)
        if case_type == "setear_sensor": return SetearSensor(postgres_db)
        if case_type == "telemetry": return GetSiloTelemetry(postgres_db, influxdb3_db)
    return _get_case

silo_router = APIRouter(prefix="/silos", tags=["silos"], dependencies=[Depends(get_current_user)])

@silo_router.get("/{silo_id}", response_model=Silobolsa)
def get_silo(silo_id: int, case: GetSilo = Depends(get_user_case("get")), current_user: Usuario = Depends(get_current_user)) -> Silobolsa:
    return case.execute(silo_id, current_user.id)

@silo_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Silobolsa])
def get_silos(case: GetSilos = Depends(get_user_case("get_all")), current_user: Usuario = Depends(get_current_user)) -> Optional[List[Silobolsa]]:
    return case.execute(current_user.id)

@silo_router.post("/create/{campo_id}", status_code=status.HTTP_201_CREATED, response_model=Silobolsa)
def create_silo(campo_id: int, silo: SilobolsaBase, case: CreateSilo = Depends(get_user_case("create")), current_user: Usuario = Depends(get_current_user)) -> Silobolsa:
    return case.execute(campo_id, silo, current_user.id)

@silo_router.put("/update/{silo_id}", status_code=status.HTTP_200_OK)
def update_silo(silo_id: int, silo: SilobolsaBase, case: UpdateSilo = Depends(get_user_case("update")), current_user: Usuario = Depends(get_current_user)) -> Silobolsa:
    return case.execute(silo_id, silo, current_user.id)

@silo_router.delete("/delete/{silo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_silo(silo_id: int, case: DeleteSilo = Depends(get_user_case("delete")), current_user: Usuario = Depends(get_current_user)) -> None:
    case.execute(silo_id, current_user.id)

@silo_router.post("/setear-sensor", status_code=status.HTTP_201_CREATED, response_model=str)
def setear_sensor(data: SensorSilo, case: SetearSensor = Depends(get_user_case("setear_sensor")), current_user: Usuario = Depends(get_current_user)) -> str:
    case.execute(data, current_user.id)
    return "Sensor vinculado con éxito"

@silo_router.get(
    "/{silo_id}/telemetry",
    status_code=status.HTTP_200_OK,
    response_model=List[Dict[str, Any]]
)
def get_silo_telemetry(
    silo_id: int,
    case: GetSiloTelemetry = Depends(get_user_case("telemetry")),
    current_user: Usuario = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Devuelve las lecturas de humedad, temperatura y CO2 de las últimas 24 horas
    del sensor vinculado al silobolsa. Usado para renderizar los gráficos en el
    frontend.

    Formato de cada elemento de la lista:
    {
        "time": <datetime>,
        "temp": <float | null>,
        "hum":  <float | null>,
        "co2":  <float | null>
    }
    """
    return case.execute(silo_id, current_user.id)


