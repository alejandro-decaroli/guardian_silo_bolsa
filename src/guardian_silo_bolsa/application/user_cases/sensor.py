from ...domain.repository.database import IUserDatabase
from ...domain.models.models import Sensor, SensorBase
from typing import List, Optional
from ...domain.services.auth_interface import IAuthService

class GetSensor:
    """ Caso de uso para obtener un sensor """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, sensor_id: int, current_user_id: int) -> Sensor:
        return self.repo.get_entity(current_user_id, sensor_id, Sensor)
    
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
    
    def execute(self, sensor: SensorBase, current_user_id: int) -> Sensor:
        sensor = Sensor.model_validate(sensor, update={"usuario_id": current_user_id})
        db_sensor = self.repo.create_entity(sensor)
        # Generate API key
        api_key = self.auth_service.create_token(data={"sensor_id": db_sensor.id, "usuario_id": current_user_id}, sensor=True)
        db_sensor.api_key = api_key
        return self.repo.update_entity(current_user_id, db_sensor.id, Sensor, db_sensor)


class UpdateSensor:
    """ Caso de uso para actualizar un sensor """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, sensor_id: int, model: SensorBase, current_user_id: int) -> Optional[Sensor]:
        return self.repo.update_entity(current_user_id, sensor_id, Sensor, model)

class DeleteSensor:
    """ Caso de uso para eliminar un sensor """
    def __init__(self, repo: IUserDatabase):
        self.repo = repo
    
    def execute(self, sensor_id: int, current_user_id: int) -> None:
        self.repo.delete_entity(current_user_id, sensor_id, Sensor)
