from ...domain.repository.database import UserDatabaseInterface
from ...domain.models.models import Campo, CampoBase
from typing import List, Optional

class GetCampo:
    """ Caso de uso para obtener un campo """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, campo_id: int) -> Campo:
        return self.repo.get_entity(campo_id, Campo)

class GetCampos:
    """ Caso de uso para obtener todos los campos """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self) -> Optional[List[Campo]]:
        return self.repo.get_entities(Campo)

class CreateCampo:
    """ Caso de uso para crear un campo """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, campo: CampoBase) -> Campo:
        return self.repo.create_entity(campo)

class UpdateCampo:
    """ Caso de uso para actualizar un campo """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, campo_id: int, model: CampoBase) -> Optional[Campo]:
        return self.repo.update_entity(campo_id, Campo, model)

class DeleteCampo:
    """ Caso de uso para eliminar un campo """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, campo_id: int) -> None:
        self.repo.delete_entity(campo_id, Campo)
