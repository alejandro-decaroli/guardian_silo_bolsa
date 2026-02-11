from ...domain.repository.database import UserDatabaseInterface
from ...domain.models.models import Usuario, UsuarioBase
from typing import List, Optional

class GetUser:
    """ Caso de uso para obtener un usuario """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, user_id: int) -> Usuario:
        return self.repo.get_entity(user_id, Usuario)

class GetUsers:
    """ Caso de uso para obtener todos los usuarios """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self) -> Optional[List[Usuario]]:
        return self.repo.get_entities(Usuario)

class CreateUser:
    """ Caso de uso para crear un usuario """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, user: UsuarioBase) -> Usuario:
        return self.repo.create_entity(user)

class UpdateUser:
    """ Caso de uso para actualizar un usuario """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, user_id: int, model: UsuarioBase) -> Optional[Usuario]:
        return self.repo.update_entity(user_id, Usuario, model)

class DeleteUser:
    """ Caso de uso para eliminar un usuario """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, user_id: int) -> None:
        self.repo.delete_entity(user_id, Usuario)
