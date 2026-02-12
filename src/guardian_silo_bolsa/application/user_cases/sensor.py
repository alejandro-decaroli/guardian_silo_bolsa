from ...domain.repository.database import UserDatabaseInterface
from ...domain.models.models import Sensor, SensorBase
from typing import List, Optional

class GetSensor:
    """ Caso de uso para obtener un sensor """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, sensor_id: int) -> Sensor:
        return self.repo.get_entity(sensor_id, Sensor)

class GetSensors:
    """ Caso de uso para obtener todos los sensores """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self) -> Optional[List[Sensor]]:
        return self.repo.get_entities(Sensor)

class CreateSensor:
    """ Caso de uso para crear un sensor """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, sensor: SensorBase) -> Sensor:
        return self.repo.create_entity(sensor)

class UpdateSensor:
    """ Caso de uso para actualizar un sensor """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, sensor_id: int, model: SensorBase) -> Optional[Sensor]:
        return self.repo.update_entity(sensor_id, Sensor, model)

class DeleteSensor:
    """ Caso de uso para eliminar un sensor """
    def __init__(self, repo: UserDatabaseInterface):
        self.repo = repo
    
    def execute(self, sensor_id: int) -> None:
        self.repo.delete_entity(sensor_id, Sensor)
