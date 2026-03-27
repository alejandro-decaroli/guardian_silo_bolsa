from abc import ABC, abstractmethod
from typing import List, Any, Optional, Type, Tuple
from ..models.models import (
    Usuario, 
    UsuarioValidation, 
    UsuarioBase, 
    Sensor,
    Silobolsa
)
from sqlmodel import SQLModel # type: ignore

class IDatabase(ABC):
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


class IUserDatabase(IDatabase):
    """Interfaz para la base de datos de usuarios. Encargada de manejar todos los datos relacionados con los usuarios."""

    @abstractmethod
    def get_silo_by_sensor(self, sensor: Sensor) -> Silobolsa:
        """Obtiene el silobolsa vinculado al sensor"""
        pass

    @abstractmethod
    def validate_api_key(self, api_key: str) -> Sensor:
        """Valida la API key de un sensor, devuelve el sensor y su silobolsa asociado."""
        pass

    @abstractmethod
    def get_by_handshake(self, mac_address: str) -> Sensor:
        """Obtiene un sensor por su dirección MAC."""
        pass

    @abstractmethod
    def get_user_by_email(self, usuario_data: UsuarioValidation) -> Usuario:
        """Obtiene un usuario por su email."""
        pass

    @abstractmethod
    def update_user(self, user_id: int, data: UsuarioBase) -> Usuario:
        """Actualiza un usuario."""
        pass

    @abstractmethod
    def get_entity(self, entity_id: int, model: type[SQLModel]) -> SQLModel:
        """Obtiene una entidad por su ID."""
        pass

    @abstractmethod
    def get_entities(self, current_user_id: int, model: type[SQLModel]) -> Optional[List[SQLModel]]:
        """Obtiene todas las entidades."""
        pass

    @abstractmethod
    def create_entity(self, model: SQLModel) -> SQLModel:
        """Crea una entidad."""
        pass

    @abstractmethod
    def update_entity(self, entity_id: int, model_class: Type[SQLModel], data: SQLModel) -> SQLModel:
        """Actualiza una entidad."""
        pass

    @abstractmethod
    def delete_entity(self, entity_id: int, model: Type[SQLModel]) -> None:
        """Elimina una entidad."""
        pass
    

class ISensorDatabase(IDatabase):
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