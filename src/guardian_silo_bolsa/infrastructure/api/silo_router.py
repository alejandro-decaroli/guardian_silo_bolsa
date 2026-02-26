from fastapi import APIRouter, Depends, status
from ...application.user_cases.silo import (
    CreateSilo, 
    GetSilo, 
    GetSilos, 
    UpdateSilo, 
    DeleteSilo
)
from ..database.deps import postgres_db
from ...domain.models.models import Silobolsa, SilobolsaBase
from typing import List
from ..security.deps import get_current_user
from ...domain.models.models import Usuario

def get_user_case(case_type: str):
    def _get_case():
        if case_type == "get": return GetSilo(postgres_db)
        if case_type == "get_all": return GetSilos(postgres_db)
        if case_type == "create": return CreateSilo(postgres_db)
        if case_type == "update": return UpdateSilo(postgres_db)
        if case_type == "delete": return DeleteSilo(postgres_db)
    return _get_case

silo_router = APIRouter(prefix="/silos", tags=["silos"], dependencies=[Depends(get_current_user)])

@silo_router.get("/{silo_id}", response_model=Silobolsa)
def get_silo(silo_id: int, case: GetSilo = Depends(get_user_case("get")), current_user: Usuario = Depends(get_current_user)) -> Silobolsa:
    return case.execute(silo_id, current_user.id)

@silo_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Silobolsa])
def get_silos(case: GetSilos = Depends(get_user_case("get_all")), current_user: Usuario = Depends(get_current_user)) -> List[Silobolsa]:
    return case.execute(current_user.id)

@silo_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Silobolsa)
def create_silo(silo: SilobolsaBase, case: CreateSilo = Depends(get_user_case("create")), current_user: Usuario = Depends(get_current_user)) -> Silobolsa:
    return case.execute(silo, current_user.id)

@silo_router.put("/{silo_id}", status_code=status.HTTP_200_OK)
def update_silo(silo_id: int, silo: SilobolsaBase, case: UpdateSilo = Depends(get_user_case("update")), current_user: Usuario = Depends(get_current_user)) -> Silobolsa:
    return case.execute(silo_id, silo, current_user.id)

@silo_router.delete("/{silo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_silo(silo_id: int, case: DeleteSilo = Depends(get_user_case("delete")), current_user: Usuario = Depends(get_current_user)) -> None:
    case.execute(silo_id, current_user.id)


