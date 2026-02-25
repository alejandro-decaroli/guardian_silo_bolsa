from fastapi import status

class AppError(Exception):
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code
        super().__init__(self.message)

class EntityAlreadyExistsError(AppError):
    """Excepción lanzada cuando se intenta registrar un email ya existente."""
    def __init__(self, email: str):
        email = email
        message = f"El usuario con email {email} ya se encuentra registrado."
        code = status.HTTP_409_CONFLICT
        super().__init__(message, code)

class EntityNotFoundError(AppError):
    """Excepción lanzada cuando se buscar una entidad pero no existe o no se encuentra."""
    def __init__(self, entity_name: str):
        entity_name = entity_name
        message = f"La entidad {entity_name} no existe o no se encuentra."
        code = status.HTTP_404_NOT_FOUND
        super().__init__(message, code)

class EntityAsociatedError(AppError):
    """Excepción lanzada cuando se intenta eliminar una entidad que tiene asociaciones."""
    def __init__(self, entity_name: str):
        entity_name = entity_name
        message = f"La entidad {entity_name} tiene asociaciones y no se puede eliminar."
        code = status.HTTP_409_CONFLICT
        super().__init__(message, code)

class EntityConflictError(AppError):
    """Excepción lanzada cuando se intenta realizar una operacion con una entidad que provoca un conflicto con las reglas de negocio."""
    def __init__(self, entity_name: str, rule: str):
        entity_name = entity_name
        rule = rule
        message = f"La entidad {entity_name} provoca un conflicto con la regla: {rule}."
        code = status.HTTP_409_CONFLICT
        super().__init__(message, code)

class InvalidCredentialsError(AppError):
    """Excepción lanzada cuando las credenciales son inválidas."""
    def __init__(self, message: str = "Credenciales inválidas."):
        code = status.HTTP_401_UNAUTHORIZED
        super().__init__(message, code)
