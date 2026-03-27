from ...domain.repository.database import IUserDatabase
from ...domain.models.models import Usuario, UsuarioBase, UsuarioValidation
from typing import List, Optional
from ...domain.exceptions.exceptions import InvalidCredentialsError, EntityAlreadyExistsError
from ...domain.services.auth_interface import IAuthService


class GetUser:
    """ Caso de uso para obtener un usuario """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, user_id: int, role: str) -> Usuario:
        if role != "admin":
            raise InvalidCredentialsError("No tienes permisos para obtener este usuario")
        db_user = self.repo.get_entity(user_id, Usuario)
        db_user.password = ""
        return db_user


class UpdateUser:
    """ Caso de uso para actualizar un usuario """
    def __init__(self, repo: IUserDatabase, auth_service: IAuthService):
        self.repo = repo
        self.auth_service = auth_service
    
    def execute(self, user_id: int, current_user_id: int, model: UsuarioBase) -> Usuario:
        if current_user_id != user_id:
            raise InvalidCredentialsError("No tienes permisos para actualizar este usuario")
        model.password = self.auth_service.hash_password(model.password)
        usuario_validation = UsuarioValidation(email=model.email, password=model.password)
        duplicated_user = self.repo.get_user_by_email(usuario_validation)
        if duplicated_user and duplicated_user.id != user_id:
            raise EntityAlreadyExistsError(usuario_validation.email)
        db_user = self.repo.update_user(user_id, model)
        db_user.password = ""
        return db_user

class DeleteUser:
    """ Caso de uso para eliminar un usuario """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, user_id: int, current_user_id: int) -> None:
        if current_user_id != user_id:
            raise InvalidCredentialsError("No tienes permisos para eliminar este usuario")
        self.repo.delete_entity(user_id, Usuario)

class LoginUser:
    """ Caso de uso para iniciar sesión """
    def __init__(self, repo: IUserDatabase, auth_service: IAuthService):
        self.repo = repo
        self.auth_service = auth_service

    def execute(self, usuario_validation: UsuarioValidation) -> tuple[str, Usuario]:
        user = self.repo.get_user_by_email(usuario_validation) 
        
        if not user or not self.auth_service.verify_password(usuario_validation.password, user.password):
            raise InvalidCredentialsError() 

        token = self.auth_service.create_token(data={"sub": str(user.id)}, sensor=False)
    
        user.password = ""
        return token, user

class SignUpUser:
    """ Caso de uso para registrar un usuario """
    def __init__(self, repo: IUserDatabase, auth_service: IAuthService):
        self.repo = repo
        self.auth_service = auth_service
    
    def execute(self, user_in: UsuarioBase) -> tuple[str, Usuario]:
        # Hasheamos antes de mandar al repo
        user_in.password = self.auth_service.hash_password(user_in.password)
        user = Usuario.model_validate(user_in)
        usuario_validation = UsuarioValidation(email=user_in.email, password=user_in.password)
        duplicated_user = self.repo.get_user_by_email(usuario_validation)
        if duplicated_user:
            raise EntityAlreadyExistsError(usuario_validation.email)
        db_user = self.repo.create_entity(user) 
        db_user.password = ""
        token = self.auth_service.create_token(data={"sub": str(db_user.id)}, sensor=False)
        return token, db_user