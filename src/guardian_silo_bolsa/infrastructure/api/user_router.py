from fastapi import APIRouter, Depends, status
from ...application.user_cases.user import (
    CreateUser, 
    GetUser, 
    GetUsers, 
    UpdateUser, 
    DeleteUser
)
from ..database.deps import postgres_db
from ...domain.models.models import Usuario, UsuarioBase
from typing import List, Dict

def get_user_case(case_type: str):
    def _get_case():
        if case_type == "get": return GetUser(postgres_db)
        if case_type == "get_all": return GetUsers(postgres_db)
        if case_type == "create": return CreateUser(postgres_db)
        if case_type == "update": return UpdateUser(postgres_db)
        if case_type == "delete": return DeleteUser(postgres_db)
    return _get_case

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.get("/{user_id}", response_model=Usuario)
def get_user(user_id: int, service: GetUser = Depends(get_user_case("get"))) -> Usuario:
    return service.execute(user_id)

@user_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Usuario])
def get_users(service: GetUsers = Depends(get_user_case("get_all"))) -> List[Usuario]:
    return service.execute()

@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Usuario)
def create_user(user: UsuarioBase, service: CreateUser = Depends(get_user_case("create"))) -> Usuario:
    db_user = Usuario.model_validate(user)
    return service.execute(db_user)

@user_router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: UsuarioBase, service: UpdateUser = Depends(get_user_case("update"))) -> Usuario:
    db_user = Usuario.model_validate(user)
    return service.execute(user_id, db_user)

@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: DeleteUser = Depends(get_user_case("delete"))) -> None:
    service.execute(user_id)
