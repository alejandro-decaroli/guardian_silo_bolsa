from fastapi import APIRouter, Depends, status
from ...application.user_cases.lote import (
    CreateLote, 
    GetLote, 
    GetLotes, 
    UpdateLote, 
    DeleteLote
)
from ..database.deps import postgres_db
from ...domain.models.models import Lote, LoteBase
from typing import List, Dict

def get_user_case(case_type: str):
    def _get_case():
        if case_type == "get": return GetLote(postgres_db)
        if case_type == "get_all": return GetLotes(postgres_db)
        if case_type == "create": return CreateLote(postgres_db)
        if case_type == "update": return UpdateLote(postgres_db)
        if case_type == "delete": return DeleteLote(postgres_db)
    return _get_case

lote_router = APIRouter(prefix="/lotes", tags=["lotes"])

@lote_router.get("/{lote_id}", response_model=Lote)
def get_lote(lote_id: int, service: GetLote = Depends(get_user_case("get"))) -> Lote:
    return service.execute(lote_id)

@lote_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Lote])
def get_lotes(service: GetLotes = Depends(get_user_case("get_all"))) -> List[Lote]:
    return service.execute()

@lote_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Lote)
def create_lote(lote: LoteBase, service: CreateLote = Depends(get_user_case("create"))) -> Lote:
    db_lote = Lote.model_validate(lote)
    return service.execute(db_lote)

@lote_router.put("/{lote_id}", status_code=status.HTTP_200_OK)
def update_lote(lote_id: int, lote: LoteBase, service: UpdateLote = Depends(get_user_case("update"))) -> Lote:
    db_lote = Lote.model_validate(lote)
    return service.execute(lote_id, db_lote)

@lote_router.delete("/{lote_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lote(lote_id: int, service: DeleteLote = Depends(get_user_case("delete"))) -> None:
    service.execute(lote_id)


