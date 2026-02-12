from ...domain.repository.database import UserDatabaseInterface
from ...domain.models.models import Silobolsa, SilobolsaBase
from typing import List, Optional

class GetSilo:
    """ Caso de uso para obtener un silo """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, silo_id: int) -> Silobolsa:
        return self.repo.get_entity(silo_id, Silobolsa)

class GetSilos:
    """ Caso de uso para obtener todos los silos """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self) -> Optional[List[Silobolsa]]:
        return self.repo.get_entities(Silobolsa)

class CreateSilo:
    """ Caso de uso para crear un silo """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, silo: SilobolsaBase) -> Silobolsa:
        return self.repo.create_entity(silo)

class UpdateSilo:
    """ Caso de uso para actualizar un silo """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, silo_id: int, model: SilobolsaBase) -> Optional[Silobolsa]:
        return self.repo.update_entity(silo_id, Silobolsa, model)

class DeleteSilo:
    """ Caso de uso para eliminar un silo """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, silo_id: int) -> None:
        self.repo.delete_entity(silo_id, Silobolsa)
