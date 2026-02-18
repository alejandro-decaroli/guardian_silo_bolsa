from abc import ABC, abstractmethod

class AuthServiceInterface(ABC):
    """ Interfaz para servicios de autenticación """
    @abstractmethod
    def hash_password(self, password: str) -> str: pass
    """ Hashea una contraseña """

    @abstractmethod
    def verify_password(self, plain: str, hashed: str) -> bool: pass
    """ Verifica si una contraseña coincide con el hash """

    @abstractmethod
    def create_token(self, data: dict) -> str: pass
    """ Crea un token JWT """

    @abstractmethod
    def decode_token(self, token: str) -> dict: pass
    """ Decodifica un token JWT """