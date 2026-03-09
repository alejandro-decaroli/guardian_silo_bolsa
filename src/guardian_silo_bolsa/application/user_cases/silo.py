from ...domain.repository.database import IUserDatabase
from ...domain.models.models import (
    Silobolsa, 
    SilobolsaBase, 
    Campo, 
    SiloLoteData, 
    Lote, 
    SilobolsaLoteLink, 
    SiloSensorData, 
    Sensor,
    SilobolsaSensorLink
)
from typing import List, Optional
from ...domain.exceptions.exceptions import InsufficientCapacityError, EntityAsociatedError
from .lote import UpdateLote


class GetSilo:
    """ Caso de uso para obtener un silo """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, silo_id: int, current_user_id: int) -> Silobolsa:
        return self.repo.get_entity(current_user_id, silo_id, Silobolsa)

class GetSilos:
    """ Caso de uso para obtener todos los silos """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, current_user_id: int) -> Optional[List[Silobolsa]]:
        return self.repo.get_entities(current_user_id, Silobolsa)

class CreateSilo:
    """ Caso de uso para crear un silo """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, silo: SilobolsaBase, current_user_id: int) -> Silobolsa:
        campo = self.repo.get_entity(current_user_id, silo.campo_id, Campo)
        silo = Silobolsa.model_validate(silo, update={"usuario_id": current_user_id, "campo_id": silo.campo_id})
        return self.repo.create_entity(silo)

class UpdateSilo:
    """ Caso de uso para actualizar un silo """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, silo_id: int, model: SilobolsaBase, current_user_id: int) -> Optional[Silobolsa]:
        return self.repo.update_entity(current_user_id, silo_id, Silobolsa, model)

    def update_peso_actual(self, silo_id: int, silo: Silobolsa, current_user_id: int) -> None:
        self.repo.update_entity(current_user_id, silo_id, Silobolsa, silo)
    
    def update_sensor_id(self, silo_id: int, silo: Silobolsa, current_user_id: int) -> None:
        self.repo.update_entity(current_user_id, silo_id, Silobolsa, silo)

class DeleteSilo:
    """ Caso de uso para eliminar un silo """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, silo_id: int, current_user_id: int) -> None:
        self.repo.delete_entity(current_user_id, silo_id, Silobolsa)


class SetearLote:
    """ Caso de uso para setear el lote de un silo """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, data: SiloLoteData, current_user_id: int) -> SilobolsaLoteLink:
        silo: Silobolsa = self.repo.get_silo_and_lotes(current_user_id, data.silobolsa_id)
        lote: Lote = self.repo.get_lote_and_silos(current_user_id, data.lote_id)
        if lote.cantidad_cosechada - lote.cosecha_almacenada < data.cantidad:
            raise InsufficientCapacityError("Ya se almaceno la totalidad de la cosecha del lote. Cantidad disponible: {}, cantidad a agregar: {}".format(lote.cantidad_cosechada - lote.cosecha_almacenada, data.cantidad))
        if silo.capacidad_max - silo.peso_actual < data.cantidad:
            raise InsufficientCapacityError("El silo no tiene capacidad suficiente. Capacidad máxima: {}, peso actual: {}, cantidad a agregar: {}".format(silo.capacidad_max, silo.peso_actual, data.cantidad))
        silo.llenar()
        self.repo.update_entity(current_user_id, silo.id, Silobolsa, silo)
        return self.repo.setear_lote(current_user_id, data)


class SetearSensor:
    """ Caso de uso para setear el sensor de un silo """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, data: SiloSensorData, current_user_id: int) -> SilobolsaSensorLink:
        silo = self.repo.get_silo_and_sensor(current_user_id, data.silobolsa_id)
        sensor = self.repo.get_entity(current_user_id, data.sensor_id, Sensor)
        for silo_sensor in silo.sensor_links:
            if silo_sensor.sensor_id == sensor.id and silo_sensor.estado == "ACTIVO":
                raise EntityAsociatedError("El silo ya tiene este sensor asignado")
        return self.repo.setear_sensor(current_user_id, data)

        
class VaciarSilo:
    """ Caso de uso para vaciar un silo """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, silo_id: int, current_user_id: int) -> None:
        silo: Silobolsa = self.repo.get_silo_and_lotes(current_user_id, silo_id)
        silo.vaciar()
        UpdateSilo(self.repo).execute(silo.id, silo, current_user_id)
      
