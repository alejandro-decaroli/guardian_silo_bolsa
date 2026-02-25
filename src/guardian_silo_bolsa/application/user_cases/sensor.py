from ...domain.repository.database import UserDatabaseInterface
from ...domain.models.models import Sensor, SensorBase
from typing import List, Optional

class GetSensor:
    """ Caso de uso para obtener un sensor """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, sensor_id: int, current_user_id: int) -> Sensor:
        return self.repo.get_entity(current_user_id, sensor_id, Sensor)

class GetSensors:
    """ Caso de uso para obtener todos los sensores """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, current_user_id: int) -> Optional[List[Sensor]]:
        return self.repo.get_entities(current_user_id, Sensor)

class CreateSensor:
    """ Caso de uso para crear un sensor """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, sensor: SensorBase, current_user_id: int) -> Sensor:
        sensor = Sensor.model_validate(sensor, update={"usuario_id": current_user_id})
        return self.repo.create_entity(current_user_id, sensor)

class UpdateSensor:
    """ Caso de uso para actualizar un sensor """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, sensor_id: int, model: SensorBase, current_user_id: int) -> Optional[Sensor]:
        return self.repo.update_entity(current_user_id, sensor_id, Sensor, model)

class DeleteSensor:
    """ Caso de uso para eliminar un sensor """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, sensor_id: int, current_user_id: int) -> None:
        self.repo.delete_entity(current_user_id, sensor_id, Sensor)
