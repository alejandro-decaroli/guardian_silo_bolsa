from abc import ABC, abstractmethod
from typing import List, Any, Optional
from ..models.models import Usuario
from sqlmodel import SQLModel

class DatabaseInterface(ABC):
    """Interfaz base para la base de datos."""
    def __init__(self, client: Any):
        self.client = client

    @abstractmethod
    def create_db_and_tables(self):
        """Crea la base de datos y las tablas."""
        pass

    @abstractmethod
    def connect(self):
        """Conecta a la base de datos."""
        pass

    @abstractmethod
    def close(self):
        """Cierra la conexión a la base de datos."""
        pass

    @abstractmethod
    def get_status(self):
        """Obtiene el estado de la base de datos."""
        pass


class UserDatabaseInterface(DatabaseInterface):
    """Interfaz para la base de datos de usuarios. Encargada de manejar todos los datos relacionados con los usuarios."""

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un usuario por su email."""
        pass

    @abstractmethod
    def get_entity(self, entity_id: int) -> SQLModel:
        """Obtiene una entidad por su ID."""
        pass

    @abstractmethod
    def get_entities(self) -> List[SQLModel]:
        """Obtiene todas las entidades."""
        pass

    @abstractmethod
    def create_entity(self, model: SQLModel) -> SQLModel:
        """Crea una entidad."""
        pass

    @abstractmethod
    def update_entity(self, data: SQLModel) -> SQLModel:
        """Actualiza una entidad."""
        pass

    @abstractmethod
    def delete_entity(self, entity_id: int) -> None:
        """Elimina una entidad."""
        pass

class SensorDatabaseInterface(DatabaseInterface):
    """Interfaz para la base de datos para series temporales. Encargada de manejar los datos de los sensores."""
    @abstractmethod
    def write(self, data: dict) -> bool:
        """Escribe datos en el TSDB."""
        pass
    
    @abstractmethod
    def read(self, query: str) -> bool:
        """Lee datos del TSDB."""
        pass
    
    @abstractmethod
    def get_data(self, query: str) -> bool:
        """Obtiene datos del TSDB."""
        pass