from ...domain.repository.database import IUserDatabase
from ...domain.models.models import Sensor, SensorBase, Campo
from typing import List, Optional
from ...domain.services.auth_interface import IAuthService
from ...domain.exceptions.exceptions import EntityNotFoundError

class GetSensor:
    """ Caso de uso para obtener un sensor """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, sensor_id: int, current_user_id: int) -> Sensor:

        sensor = self.repo.get_entity(sensor_id, Sensor)
        campos: Optional[List[Campo]] = self.repo.get_entities(current_user_id, Campo)
        lista_ids = []
        if campos:
            for campo in campos:
                lista_ids.append(campo.id)
            if not sensor.campo_id in lista_ids:
                raise EntityNotFoundError("Sensor")
        return sensor
    
    def get_by_handshake(self, mac_address: str) -> Sensor:
        return self.repo.get_by_handshake(mac_address)

class GetSensors:
    """ Caso de uso para obtener todos los sensores """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, current_user_id: int) -> Optional[List[Sensor]]:
        return self.repo.get_entities(current_user_id, Sensor)

class CreateSensor:
    """ Caso de uso para crear un sensor """
    def __init__(self, repo: IUserDatabase, auth_service: IAuthService):
        self.repo = repo
        self.auth_service = auth_service
    
    def execute(self, campo_id: int, sensor: SensorBase, current_user_id: int) -> Sensor:
        campo = self.repo.get_entity(campo_id, Campo)
        if campo.usuario_id != current_user_id:
            raise EntityNotFoundError("Campo")
        sensor = Sensor.model_validate(sensor, update={"campo_id": campo_id})
        db_sensor = self.repo.create_entity(sensor)
        # Generate API key
        api_key = self.auth_service.create_token(data={"sensor_id": db_sensor.id}, sensor=True)
        db_sensor.api_key = api_key
        return self.repo.update_entity(db_sensor.id, Sensor, db_sensor)


class UpdateSensor:
    """ Caso de uso para actualizar un sensor """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, sensor_id: int, model: SensorBase, current_user_id: int) -> Sensor:
        sensor = self.repo.get_entity(sensor_id, Sensor)
        campo = self.repo.get_entity(sensor.campo_id, Campo)
        if campo.usuario_id != current_user_id:
            raise EntityNotFoundError("Campo")
        return self.repo.update_entity(sensor_id, Sensor, model)

class DeleteSensor:
    """ Caso de uso para eliminar un sensor """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, sensor_id: int, current_user_id: int) -> None:
        sensor = self.repo.get_entity(sensor_id, Sensor)
        campo = self.repo.get_entity(sensor.campo_id, Campo)
        if campo.usuario_id != current_user_id:
            raise EntityNotFoundError("Sensor") 
        self.repo.delete_entity(sensor_id, Sensor)
