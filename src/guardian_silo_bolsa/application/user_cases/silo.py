from ...domain.repository.database import UserDatabaseInterface
from ...domain.models.models import Silobolsa, SilobolsaBase, Campo, SiloLoteData, Lote, SilobolsaLoteLink
from typing import List, Optional
from ...domain.exceptions.exceptions import InsufficientCapacityError
from .lote import UpdateLote


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

    def update_peso_actual(self, silo_id: int, silo: Silobolsa, current_user_id: int) -> None:
        self.repo.update_entity(current_user_id, silo_id, Silobolsa, silo)

class DeleteSilo:
    """ Caso de uso para eliminar un silo """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, silo_id: int, current_user_id: int) -> None:
        self.repo.delete_entity(current_user_id, silo_id, Silobolsa)

class SetearLote:
    """ Caso de uso para setear el lote de un silo """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, data: SiloLoteData, current_user_id: int) -> SilobolsaLoteLink:
        silo = self.repo.get_entity(current_user_id, data.silobolsa_id, Silobolsa)
        lote = self.repo.get_entity(current_user_id, data.lote_id, Lote)
        if lote.cantidad_almacenada == 0:
            raise InsufficientCapacityError("El lote no tiene suficiente cantidad. Cantidad disponible: {}, cantidad a agregar: {}".format(lote.cantidad_almacenada, data.cantidad))
        if lote.cantidad_almacenada < data.cantidad:
            raise InsufficientCapacityError("El lote no tiene suficiente cantidad. Cantidad disponible: {}, cantidad a agregar: {}".format(lote.cantidad_almacenada, data.cantidad))
        if silo.capacidad_max - silo.peso_actual < data.cantidad:
            raise InsufficientCapacityError("El silo no tiene capacidad suficiente. Capacidad máxima: {}, peso actual: {}, cantidad a agregar: {}".format(silo.capacidad_max, silo.peso_actual, data.cantidad))
        lote.cantidad_almacenada -= data.cantidad
        silo.peso_actual += data.cantidad
        UpdateLote(self.repo).update_cantidad_almacenada(data.lote_id, lote, current_user_id)
        UpdateSilo(self.repo).update_peso_actual(silo.id, silo, current_user_id)
        return self.repo.setear_lote(current_user_id, data)
