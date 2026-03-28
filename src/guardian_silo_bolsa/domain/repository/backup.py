from abc import ABC, abstractmethod
from typing import Any, Dict
from ..models.models import TelemetrySchema

class IBackup(ABC):
    """Interfaz base para el backup."""
    def __init__(self, client: Any):
        self.client = client

    @abstractmethod
    def create_backup(self, datos: TelemetrySchema, sensor_id: int) -> Dict[str,Any]:
        """Crea un backup de la base de datos."""
        pass

    @abstractmethod
    def restore_backup(self) -> Dict[str,Any]:
        """Restaura un backup de la base de datos."""
        pass
