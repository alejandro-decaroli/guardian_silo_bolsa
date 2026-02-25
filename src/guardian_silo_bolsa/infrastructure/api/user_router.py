from fastapi import APIRouter, Depends, status, Response
from ...application.user_cases.user import (
    GetUser, 
    GetUsers, 
    UpdateUser, 
    DeleteUser,
    LoginUser,
    SignUpUser
)
from ..database.deps import postgres_db
from ..security.auth_handler import auth_service_instance
from ...domain.models.models import Usuario, UsuarioBase, UsuarioValidation
from typing import List, Dict, Any
from ..security.deps import get_current_user

def get_user_case(case_type: str) -> callable:
    """
    Factory function to get the appropriate user case service
    """
    def _get_case():
        if case_type == "get": return GetUser(postgres_db)
        if case_type == "get_all": return GetUsers(postgres_db)
        if case_type == "update": return UpdateUser(postgres_db, auth_service_instance)
        if case_type == "delete": return DeleteUser(postgres_db)
        if case_type == "login": return LoginUser(postgres_db, auth_service_instance)
        if case_type == "signup": return SignUpUser(postgres_db, auth_service_instance)
    return _get_case

def set_auth_cookie(response: Response, token: str) -> None:
    """
    setea la cookie de autenticación en la respuesta
    """
    response.set_cookie(
        key="access_token", 
        value=token, 
        httponly=True,
        max_age=None, # Cookie de sesión
        samesite="lax",
        secure=False 
    )

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/signup", status_code=status.HTTP_200_OK)
def signup(
    response: Response, 
    credentials: UsuarioBase, 
    case: SignUpUser = Depends(get_user_case("signup"))
) -> Dict[str, Any]:
    token, user = case.execute(credentials)
    set_auth_cookie(response, token)

    return {
        "message": "signup exitoso",
        "user": user
    }

@user_router.post("/login", status_code=status.HTTP_200_OK)
def login(
    response: Response, 
    credentials: UsuarioValidation, 
    case: LoginUser = Depends(get_user_case("login"))
) -> Dict[str, Any]:
    token, user = case.execute(credentials)
    set_auth_cookie(response, token)
    
    return {
        "message": "login exitoso",
        "user": user
    }

@user_router.get("/{user_id}", response_model=Usuario, status_code=status.HTTP_200_OK)
def get_user(user_id: int, case: GetUser = Depends(get_user_case("get")), current_user: Usuario = Depends(get_current_user)) -> Usuario:
    return case.execute(user_id, current_user.role)

@user_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Usuario])
def get_users(case: GetUsers = Depends(get_user_case("get_all")), current_user: Usuario = Depends(get_current_user)) -> List[Usuario]:
    return case.execute(current_user.role)

@user_router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: UsuarioBase, case: UpdateUser = Depends(get_user_case("update")), current_user: Usuario = Depends(get_current_user)) -> Usuario:
    db_user = Usuario.model_validate(user)
    return case.execute(user_id, current_user.id, db_user)

@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, case: DeleteUser = Depends(get_user_case("delete")), current_user: Usuario = Depends(get_current_user)) -> None:
    case.execute(user_id, current_user.id)

@user_router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    response: Response,
    current_user: Usuario = Depends(get_current_user) 
) -> Dict[str, str]:

    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=False
    )

    return {"message": "Logout exitoso, cookie eliminada"}