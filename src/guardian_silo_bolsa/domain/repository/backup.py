from abc import ABC, abstractmethod

class IBackup(ABC):
    """Interfaz base para el backup."""
    def __init__(self, client: Any):
        self.client = client

    @abstractmethod
    def create_backup(self):
        """Crea un backup de la base de datos."""
        pass

    @abstractmethod
    def restore_backup(self):
        """Restaura un backup de la base de datos."""
        pass
