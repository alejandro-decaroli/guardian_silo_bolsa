from fastapi import APIRouter, Depends, status # type: ignore
from ...application.user_cases.campo import (
    CreateCampo, 
    GetCampo, 
    GetCampos, 
    UpdateCampo, 
    DeleteCampo
)
from ..database.deps import postgres_db
from ...domain.models.models import CampoBase, Campo, Usuario
from typing import List, Optional
from ..security.deps import get_current_user

def get_user_case(case_type: str):
    def _get_case():
        if case_type == "get": return GetCampo(postgres_db)
        if case_type == "get_all": return GetCampos(postgres_db)
        if case_type == "create": return CreateCampo(postgres_db)
        if case_type == "update": return UpdateCampo(postgres_db)
        if case_type == "delete": return DeleteCampo(postgres_db)
    return _get_case

campo_router = APIRouter(prefix="/campos", tags=["campos"])

@campo_router.get("/{campo_id}", response_model=Campo)
def get_campo(campo_id: int, current_user: Usuario = Depends(get_current_user), case: GetCampo = Depends(get_user_case("get"))) -> Campo:
    return case.execute(campo_id, current_user.id)

@campo_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Campo])
def get_campos(case: GetCampos = Depends(get_user_case("get_all")), current_user: Usuario = Depends(get_current_user)) -> Optional[List[Campo]]:
    return case.execute(current_user.id)

@campo_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=Campo)
def create_campo(campo: CampoBase, case: CreateCampo = Depends(get_user_case("create")), current_user: Usuario = Depends(get_current_user)) -> Campo:
    return case.execute(campo, current_user.id)

@campo_router.put("/update/{campo_id}", status_code=status.HTTP_200_OK)
def update_campo(campo_id: int, campo: CampoBase, case: UpdateCampo = Depends(get_user_case("update")), current_user: Usuario = Depends(get_current_user)) -> Campo:
    return case.execute(campo_id, campo, current_user.id)

@campo_router.delete("/delete/{campo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campo(campo_id: int, case: DeleteCampo = Depends(get_user_case("delete")), current_user: Usuario = Depends(get_current_user)) -> None:
    case.execute(campo_id, current_user.id)

    
