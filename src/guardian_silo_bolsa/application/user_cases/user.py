from ...domain.repository.database import UserDatabaseInterface
from ...domain.models.models import Usuario, UsuarioBase, UsuarioValidation
from typing import List, Optional
from ...domain.exceptions.exceptions import InvalidCredentialsError
from ...domain.services.auth_interface import AuthServiceInterface


class GetUser:
    """ Caso de uso para obtener un usuario """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, user_id: int) -> Usuario:
        db_user = self.repo.get_entity(user_id, Usuario)
        db_user.password = ""
        return db_user

class GetUsers:
    """ Caso de uso para obtener todos los usuarios """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self) -> Optional[List[Usuario]]:
        db_users = self.repo.get_entities(Usuario)
        for user in db_users:
            user.password = ""
        return db_users

class UpdateUser:
    """ Caso de uso para actualizar un usuario """
    def __init__(self, repo: UserDatabaseInterface, auth_service: AuthServiceInterface):
        self.repo = repo
        self.auth_service = auth_service
    
    def execute(self, user_id: int, model: UsuarioBase) -> Optional[Usuario]:
        model.password = self.auth_service.hash_password(model.password)
        db_user = self.repo.update_entity(user_id, Usuario, model)
        db_user.password = ""
        return db_user

class DeleteUser:
    """ Caso de uso para eliminar un usuario """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, user_id: int) -> None:
        self.repo.delete_entity(user_id, Usuario)

class LoginUser:
    """ Caso de uso para iniciar sesión """
    def __init__(self, repo: UserDatabaseInterface, auth_service: AuthServiceInterface):
        self.repo = repo
        self.auth_service = auth_service

    def execute(self, usuario_validation: UsuarioValidation) -> tuple[str, Usuario]:
        user = self.repo.get_user_by_email(usuario_validation) 
        
        if not user or not self.auth_service.verify_password(usuario_validation.password, user.password):
            raise InvalidCredentialsError() 

        token = self.auth_service.create_token(data={"sub": str(user.id)})
        db_user = self.repo.get_entity(user.id, Usuario)
        db_user.password = ""
        return token, db_user

class SignUpUser:
    """ Caso de uso para registrar un usuario """
    def __init__(self, repo: UserDatabaseInterface, auth_service: AuthServiceInterface):
        self.repo = repo
        self.auth_service = auth_service
    
    def execute(self, user_in: UsuarioBase) -> tuple[str, Usuario]:
        # Hasheamos antes de mandar al repo
        user_in.password = self.auth_service.hash_password(user_in.password)
        user = Usuario.model_validate(user_in)
        db_user = self.repo.create_entity(user) 
        db_user.password = ""
        token = self.auth_service.create_token(data={"sub": str(db_user.id)})
        return token, db_user