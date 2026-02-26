from ...domain.repository.database import UserDatabaseInterface
from ...domain.models.models import Lote, LoteBase, Campo
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
        # el get entity valida que el campo pertenece al usuario
        campo = self.repo.get_entity(current_user_id, lote.campo_id, Campo)
        lote = Lote.model_validate(lote, update={"usuario_id": current_user_id, "campo_id": lote.campo_id})
        return self.repo.create_entity(lote)

class UpdateLote:
    """ Caso de uso para actualizar un lote """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, lote_id: int, model: LoteBase, current_user_id: int) -> Optional[Lote]:
        return self.repo.update_entity(current_user_id, lote_id, Lote, model)
    
    def update_cantidad_almacenada(self, lote_id: int, lote: Lote, current_user_id: int) -> None:
        self.repo.update_entity(current_user_id, lote_id, Lote, lote)

class DeleteLote:
    """ Caso de uso para eliminar un lote """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, lote_id: int, current_user_id: int) -> None:
        self.repo.delete_entity(current_user_id, lote_id, Lote)

