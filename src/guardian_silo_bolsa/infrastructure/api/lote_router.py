from fastapi import APIRouter, Depends, status
from ...application.user_cases.lote import (
    CreateLote, 
    GetLote, 
    GetLotes, 
    UpdateLote, 
    DeleteLote
)
from ..database.deps import postgres_db
from ...domain.models.models import Lote, LoteBase, Usuario
from typing import List
from ..security.deps import get_current_user

def get_user_case(case_type: str):
    def _get_case():
        if case_type == "get": return GetLote(postgres_db)
        if case_type == "get_all": return GetLotes(postgres_db)
        if case_type == "create": return CreateLote(postgres_db)
        if case_type == "update": return UpdateLote(postgres_db)
        if case_type == "delete": return DeleteLote(postgres_db)
    return _get_case

lote_router = APIRouter(prefix="/lotes", tags=["lotes"], dependencies=[Depends(get_current_user)])

@lote_router.get("/{lote_id}", response_model=Lote)
def get_lote(lote_id: int, case: GetLote = Depends(get_user_case("get")), current_user: Usuario = Depends(get_current_user)) -> Lote:
    return case.execute(lote_id, current_user.id)

@lote_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Lote])
def get_lotes(case: GetLotes = Depends(get_user_case("get_all")), current_user: Usuario = Depends(get_current_user)) -> List[Lote]:
    return case.execute(current_user.id)

@lote_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=Lote)
def create_lote(lote: LoteBase, case: CreateLote = Depends(get_user_case("create")), current_user: Usuario = Depends(get_current_user)) -> Lote:
    return case.execute(lote, current_user.id)

@lote_router.put("/update/{lote_id}", status_code=status.HTTP_200_OK)
def update_lote(lote_id: int, lote: LoteBase, case: UpdateLote = Depends(get_user_case("update")), current_user: Usuario = Depends(get_current_user)) -> Lote:
    return case.execute(lote_id, lote, current_user.id)

@lote_router.delete("/delete/{lote_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lote(lote_id: int, case: DeleteLote = Depends(get_user_case("delete")), current_user: Usuario = Depends(get_current_user)) -> None:
    case.execute(lote_id, current_user.id)


