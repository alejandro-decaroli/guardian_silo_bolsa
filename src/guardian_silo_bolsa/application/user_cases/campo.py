from ...domain.repository.database import IUserDatabase
from ...domain.models.models import Campo, CampoBase
from typing import List, Optional
from ...domain.exceptions.exceptions import EntityNotFoundError

class GetCampo:
    """ Caso de uso para obtener un campo """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, campo_id: int, current_user_id: int) -> Campo:
        campo = self.repo.get_entity(campo_id, Campo)
        if campo.usuario_id != current_user_id:
            raise EntityNotFoundError("Campo")
        return campo

class GetCampos:
    """ Caso de uso para obtener todos los campos """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, current_user_id: int) -> Optional[List[Campo]]:
        return self.repo.get_entities(current_user_id, Campo)

class CreateCampo:
    """ Caso de uso para crear un campo """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, campo: CampoBase, current_user_id: int) -> Campo:
        campo = Campo.model_validate(campo, update={"usuario_id": current_user_id})
        return self.repo.create_entity(campo)

class UpdateCampo:
    """ Caso de uso para actualizar un campo """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, campo_id: int, model: CampoBase, current_user_id: int) -> Campo:
        campo = self.repo.get_entity(campo_id, Campo)
        if campo.usuario_id != current_user_id:
            raise EntityNotFoundError("Campo")
        return self.repo.update_entity(campo_id, Campo, model)

class DeleteCampo:
    """ Caso de uso para eliminar un campo """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, campo_id: int, current_user_id: int) -> None:
        campo = self.repo.get_entity(campo_id, Campo)
        if campo.usuario_id != current_user_id:
            raise EntityNotFoundError("Campo")
        self.repo.delete_entity(campo_id, Campo)
