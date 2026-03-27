import jwt # type: ignore
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
from passlib.context import CryptContext # type: ignore
from fastapi import HTTPException, status # type: ignore
import os
from ...domain.services.auth_interface import IAuthService

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "clave_secreta_super_segura") 
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

class AuthService(IAuthService):
    """
    Implementación de la interfaz IAuthService.
    """
    def __init__(self):
        self.pwd_context = pwd_context

    def hash_password(self, password: str) -> str:
        """Hashea la contraseña usando Argon2."""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica si la contraseña coincide con el hash almacenado."""
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_token(self, data: dict, sensor: bool, expires_delta: Optional[timedelta] = None) -> str:
        """
        Crea un token JWT firmado.
        El 'sub' (subject) del data debería ser el ID del usuario.
        """
        to_encode = data.copy()
        if not sensor:
            if expires_delta:
                expire = datetime.now(timezone.utc) + expires_delta
            else:
                expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
            to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def decode_token(self, token: str) -> Optional[Dict]:
        """
        Decodifica y valida un token. 
        Si el token expiró o es inválido, devuelve None o levanta una excepción.
        """
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return decoded_token if decoded_token["exp"] >= datetime.now(timezone.utc).timestamp() else None
        except jwt.ExpiredSignatureError:
            return None  
        except jwt.PyJWTError:
            return None

auth_service_instance: AuthService = AuthService()
