from abc import ABC, abstractmethod
from typing import List, Any, Optional, Type
from ..models.models import Usuario, UsuarioValidation, UsuarioBase
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
    def get_user_by_email(self, usuario_data: UsuarioValidation) -> Optional[Usuario]:
        """Obtiene un usuario por su email."""
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        """Elimina un usuario."""
        pass

    @abstractmethod
    def get_all_users(self) -> List[Usuario]:
        """Obtiene todos los usuarios."""
        pass

    @abstractmethod
    def update_user(self, user_id: int, data: UsuarioBase) -> Usuario:
        """Actualiza un usuario."""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Usuario:
        """Obtiene un usuario por su ID."""
        pass

    @abstractmethod
    def create_user(self, usuario_data: Usuario) -> Usuario:
        """Crea un usuario."""
        pass

    @abstractmethod
    def get_entity(self, current_user_id: int, entity_id: int, model: type[SQLModel]) -> SQLModel:
        """Obtiene una entidad por su ID."""
        pass

    @abstractmethod
    def get_entities(self, current_user_id: int, model: type[SQLModel]) -> List[SQLModel]:
        """Obtiene todas las entidades."""
        pass

    @abstractmethod
    def create_entity(self, current_user_id: int, model: SQLModel) -> SQLModel:
        """Crea una entidad."""
        pass

    @abstractmethod
    def update_entity(self, current_user_id: int, entity_id: int, model_class: Type[SQLModel], data: SQLModel) -> SQLModel:
        """Actualiza una entidad."""
        pass

    @abstractmethod
    def delete_entity(self, current_user_id: int, entity_id: int, model: Type[SQLModel]) -> None:
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