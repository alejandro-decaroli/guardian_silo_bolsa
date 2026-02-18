from fastapi import APIRouter, Depends, status
from ...application.user_cases.campo import (
    CreateCampo, 
    GetCampo, 
    GetCampos, 
    UpdateCampo, 
    DeleteCampo
)
from ..database.deps import postgres_db
from ...domain.models.models import CampoBase, Campo
from typing import List
from ..security.deps import get_current_user

def get_user_case(case_type: str):
    def _get_case():
        if case_type == "get": return GetCampo(postgres_db)
        if case_type == "get_all": return GetCampos(postgres_db)
        if case_type == "create": return CreateCampo(postgres_db)
        if case_type == "update": return UpdateCampo(postgres_db)
        if case_type == "delete": return DeleteCampo(postgres_db)
    return _get_case

campo_router = APIRouter(prefix="/campos", tags=["campos"], dependencies=[Depends(get_current_user)])

@campo_router.get("/{campo_id}", response_model=Campo)
def get_campo(campo_id: int, service: GetCampo = Depends(get_user_case("get"))) -> Campo:
    return service.execute(campo_id)

@campo_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Campo])
def get_campos(service: GetCampos = Depends(get_user_case("get_all"))) -> List[Campo]:
    return service.execute()

@campo_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Campo)
def create_campo(campo: CampoBase, service: CreateCampo = Depends(get_user_case("create"))) -> Campo:
    db_campo = Campo.model_validate(campo)
    return service.execute(db_campo)

@campo_router.put("/{campo_id}", status_code=status.HTTP_200_OK)
def update_campo(campo_id: int, campo: CampoBase, service: UpdateCampo = Depends(get_user_case("update"))) -> Campo:
    db_campo = Campo.model_validate(campo)
    return service.execute(campo_id, db_campo)

@campo_router.delete("/{campo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campo(campo_id: int, service: DeleteCampo = Depends(get_user_case("delete"))) -> None:
    service.execute(campo_id)

    
