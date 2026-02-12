from ...domain.repository.database import UserDatabaseInterface
from ...domain.models.models import Lote, LoteBase
from typing import List, Optional

class GetLote:
    """ Caso de uso para obtener un lote """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, lote_id: int) -> Lote:
        return self.repo.get_entity(lote_id, Lote)

class GetLotes:
    """ Caso de uso para obtener todos los lotes """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self) -> Optional[List[Lote]]:
        return self.repo.get_entities(Lote)

class CreateLote:
    """ Caso de uso para crear un lote """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, lote: LoteBase) -> Lote:
        return self.repo.create_entity(lote)

class UpdateLote:
    """ Caso de uso para actualizar un lote """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, lote_id: int, model: LoteBase) -> Optional[Lote]:
        return self.repo.update_entity(lote_id, Lote, model)

class DeleteLote:
    """ Caso de uso para eliminar un lote """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, lote_id: int) -> None:
        self.repo.delete_entity(lote_id, Lote)
