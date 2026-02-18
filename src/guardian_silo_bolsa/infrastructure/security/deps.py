from fastapi import Request, HTTPException, status
from ..security.auth_handler import auth_service_instance 
from ..database.deps import postgres_db 
from ...domain.models.models import Usuario

# src/infrastructure/api/deps.py

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Se requiere iniciar sesión"
        )
    
    payload = auth_service_instance.decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Sesión expirada o inválida"
        )
    
    user_id = payload.get("sub")
    # Importante: Buscamos en el repo usando la clase Usuario
    user = postgres_db.get_entity(int(user_id), Usuario) 
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario inexistente")
        
    return user