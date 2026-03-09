from abc import ABC, abstractmethod

class IAuthService(ABC):
    """ Interfaz para servicios de autenticación """
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """ Hashea una contraseña """
        pass

    @abstractmethod
    def verify_password(self, plain: str, hashed: str) -> bool:
        """ Verifica si una contraseña coincide con el hash """
        pass

    @abstractmethod
    def create_token(self, data: dict, sensor: bool) -> str:
        """ Crea un token JWT """
        pass

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        """ Decodifica un token JWT """
        pass