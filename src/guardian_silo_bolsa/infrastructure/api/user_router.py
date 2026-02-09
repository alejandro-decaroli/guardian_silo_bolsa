from fastapi import APIRouter, Depends, status
from ...domain.services.UserService import UserService
from ..database.deps import postgres_db
from ...domain.models.models import Usuario, UsuarioBase
from typing import List, Dict

def get_user_service():
    return UserService(postgres_db)

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.get("/{user_id}", response_model=Usuario)
def get_user(user_id: int, service: UserService = Depends(get_user_service)) -> Usuario:
    return service.get_user(user_id)

@user_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Usuario])
def get_users(service: UserService = Depends(get_user_service)) -> List[Usuario]:
    return service.get_users()

@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Usuario)
def create_user(user: UsuarioBase, service: UserService = Depends(get_user_service)) -> Usuario:
    db_user = Usuario.model_validate(user)
    return service.create_user(db_user)

@user_router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: UsuarioBase, service: UserService = Depends(get_user_service)) -> Usuario:
    db_user = Usuario.model_validate(user)
    return service.update_user(user_id, db_user)

@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)) -> None:
    service.delete_user(user_id)
