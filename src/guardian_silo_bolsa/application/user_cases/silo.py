from ...domain.repository.database import UserDatabaseInterface
from ...domain.models.models import Silobolsa, SilobolsaBase, Campo
from typing import List, Optional

class GetSilo:
    """ Caso de uso para obtener un silo """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, silo_id: int, current_user_id: int) -> Silobolsa:
        return self.repo.get_entity(current_user_id, silo_id, Silobolsa)

class GetSilos:
    """ Caso de uso para obtener todos los silos """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, current_user_id: int) -> Optional[List[Silobolsa]]:
        return self.repo.get_entities(current_user_id, Silobolsa)

class CreateSilo:
    """ Caso de uso para crear un silo """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, silo: SilobolsaBase, current_user_id: int) -> Silobolsa:
        campo = self.repo.get_entity(current_user_id, silo.campo_id, Campo)
        silo = Silobolsa.model_validate(silo, update={"usuario_id": current_user_id, "campo_id": silo.campo_id})
        return self.repo.create_entity(silo)

class UpdateSilo:
    """ Caso de uso para actualizar un silo """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, silo_id: int, model: SilobolsaBase, current_user_id: int) -> Optional[Silobolsa]:
        return self.repo.update_entity(current_user_id, silo_id, Silobolsa, model)

class DeleteSilo:
    """ Caso de uso para eliminar un silo """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, silo_id: int, current_user_id: int) -> None:
        self.repo.delete_entity(current_user_id, silo_id, Silobolsa)
