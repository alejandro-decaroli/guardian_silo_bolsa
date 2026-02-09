from ...application.interfaces.database import UserDatabaseInterface
from ..models.models import Usuario, UsuarioBase
from typing import List, Optional

class UserService:

    """ Servicio de usuarios """

    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo

    def get_user(self, user_id: int) -> Usuario:
        """ Obtiene un usuario por su ID. """
        return self.repo.get_entity(user_id, Usuario)
        
    def get_users(self) -> Optional[List[Usuario]]:
        """Obtiene todos los usuarios."""
        return self.repo.get_entities(Usuario)
        
    def create_user(self, model: UsuarioBase) -> Optional[Usuario]:
        """Crea un nuevo usuario."""
        return self.repo.create_entity(model)

    def update_user(self, user_id: int, model: UsuarioBase) -> Optional[Usuario]:
        """Actualiza un usuario existente."""
        return self.repo.update_entity(user_id,  Usuario, model)

    def delete_user(self, user_id: int) -> None:
        """Elimina un usuario existente."""
        self.repo.delete_entity(user_id, Usuario)