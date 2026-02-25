from .domain.models.models import Usuario, UsuarioBase, UsuarioValidation
from .domain.repository.database import UserDatabaseInterface
from .domain.services.auth_interface import AuthServiceInterface

def create_admin(db: UserDatabaseInterface, auth_service: AuthServiceInterface) -> None:

    """Crea un usuario con role de administrador en caso de no existir uno con el mismo email y contraseña"""

    admin_validation = UsuarioValidation(email="admin@example.com", password="admin")

    user = db.get_user_by_email(admin_validation)
    if user:
        return
    
    admin_data = {
        "nombre": "admin",
        "apellido": "fake lastname",
        "password": "admin",
        "email": "admin@example.com"
    }

    admin = UsuarioBase(**admin_data)

    db_admin = Usuario.model_validate(admin)
    
    # Hashear la contraseña antes de guardarla
    db_admin.password = auth_service.hash_password(admin.password)
    db_admin.role = "admin"
    
    db.create_user(db_admin)
    
