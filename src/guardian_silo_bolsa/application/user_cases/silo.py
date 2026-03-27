from ...domain.repository.database import IUserDatabase
from ...domain.models.models import (
    Silobolsa, 
    SilobolsaBase, 
    Campo, 
    Sensor,
    SensorSilo
)
from typing import List, Optional
from ...domain.exceptions.exceptions import InsufficientCapacityError, EntityAsociatedError, EntityNotFoundError


class GetSilo:
    """ Caso de uso para obtener un silo """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, silo_id: int, current_user_id: int) -> Silobolsa:
        silo = self.repo.get_entity(silo_id, Silobolsa)
        campo = self.repo.get_entity(silo.campo_id, Campo)
        if campo.usuario_id != current_user_id:
            raise EntityNotFoundError("Silo")
        return silo

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
    
    def execute(self, campo_id: int, silo: SilobolsaBase, current_user_id: int) -> Silobolsa:
        campo = self.repo.get_entity(campo_id, Campo)
        if campo.usuario_id != current_user_id:
            raise EntityNotFoundError("Campo")
        silo = Silobolsa.model_validate(silo, update={"campo_id": campo_id})
        return self.repo.create_entity(silo)

class UpdateSilo:
    """ Caso de uso para actualizar un silo """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, silo_id: int, model: SilobolsaBase, current_user_id: int) -> Silobolsa:
        silo = self.repo.get_entity(silo_id, Silobolsa)
        campo = self.repo.get_entity(silo.campo_id, Campo)
        if campo.usuario_id != current_user_id:
            raise EntityNotFoundError("Silo")
        return self.repo.update_entity(silo_id, Silobolsa, model)

class DeleteSilo:
    """ Caso de uso para eliminar un silo """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, silo_id: int, current_user_id: int) -> None:
        silo = self.repo.get_entity(silo_id, Silobolsa)
        campo = self.repo.get_entity(silo.campo_id, Campo)
        if campo.usuario_id != current_user_id:
            raise EntityNotFoundError("Silo")
        self.repo.delete_entity(silo_id, Silobolsa)


class SetearSensor:
    """ Caso de uso para setear el sensor de un silo """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, data: SensorSilo, current_user_id: int) -> None:
        silo = self.repo.get_entity(data.silobolsa_id, Silobolsa)
        sensor = self.repo.get_entity(data.sensor_id, Sensor)
        campo = self.repo.get_entity(silo.campo_id, Campo)
        if campo.usuario_id != current_user_id:
            raise EntityNotFoundError("Silo")
        if silo is None or sensor is None:
            raise EntityNotFoundError("Silo o Sensor")
        silo.sensor_id = data.sensor_id
        self.repo.update_entity(silo.id, Silobolsa, silo)

      
