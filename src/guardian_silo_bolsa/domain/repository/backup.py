from abc import ABC, abstractmethod
from typing import Any, Dict

class IBackup(ABC):
    """Interfaz base para el backup."""
    def __init__(self, client: Any):
        self.client = client

    @abstractmethod
    def create_backup(self) -> Dict:
        """Crea un backup de la base de datos."""
        pass

    @abstractmethod
    def restore_backup(self) -> Dict:
        """Restaura un backup de la base de datos."""
        pass
