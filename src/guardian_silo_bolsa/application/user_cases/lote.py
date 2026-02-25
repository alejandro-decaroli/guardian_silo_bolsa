from ...domain.repository.database import UserDatabaseInterface
from ...domain.models.models import Lote, LoteBase
from typing import List, Optional

class GetLote:
    """ Caso de uso para obtener un lote """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, lote_id: int, current_user_id: int) -> Lote:
        return self.repo.get_entity(current_user_id, lote_id, Lote)

class GetLotes:
    """ Caso de uso para obtener todos los lotes """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, current_user_id: int) -> Optional[List[Lote]]:
        return self.repo.get_entities(current_user_id, Lote)

class CreateLote:
    """ Caso de uso para crear un lote """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, lote: LoteBase, current_user_id: int) -> Lote:
        lote = Lote.model_validate(lote, update={"usuario_id": current_user_id})
        return self.repo.create_entity(current_user_id, lote)

class UpdateLote:
    """ Caso de uso para actualizar un lote """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, lote_id: int, model: LoteBase, current_user_id: int) -> Optional[Lote]:
        return self.repo.update_entity(current_user_id, lote_id, Lote, model)

class DeleteLote:
    """ Caso de uso para eliminar un lote """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, lote_id: int, current_user_id: int) -> None:
        self.repo.delete_entity(current_user_id, lote_id, Lote)

