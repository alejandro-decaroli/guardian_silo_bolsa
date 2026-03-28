from .domain.models.models import (
    Usuario, 
    UsuarioBase, 
    UsuarioValidation, 
    CampoBase, 
    Campo,
    Sensor,
    SensorBase,
    Silobolsa,
    SilobolsaBase,
    Grano,
    EstadoSensor,
    )
from .domain.repository.database import IUserDatabase
from .domain.services.auth_interface import IAuthService

def create_user(db: IUserDatabase, auth_service: IAuthService) -> bool:
    """
    Crea un usuario admin si no existe
    """
    admin_validation = UsuarioValidation(email="admin@example.com", password="admin")
    try:
        user = db.get_user_by_email(admin_validation)
    except Exception:
    
        admin_data = {
            "nombre": "admin",
            "apellido": "fake lastname",
            "password": "admin",
            "email": "admin@example.com",
            "telefono": "123456789"
        }
        admin = UsuarioBase(**admin_data)
        db_admin = Usuario.model_validate(admin)
        db_admin.password = auth_service.hash_password(admin.password)
        db_admin.role = "admin"
        db.create_entity(db_admin)
        return False
    return True

def create_campo(db: IUserDatabase) -> None:
    """
    Crea un campo para el usuario admin
    """
    campo_data = {
        "ubicacion": "Armstrong, Santa Fe, Argentina",
        "nombre": "Campo Admin"
    }
    campo = CampoBase(**campo_data)
    db_campo = Campo.model_validate(campo, update={"usuario_id": 1})
    db.create_entity(db_campo)


def create_sensores(db: IUserDatabase, auth_service: IAuthService) -> None:
    """
    Crea sensores para el campo
    """
    sensor_data = [
        {
            "modelo": "LoRa T100",
            "estado": EstadoSensor.ACTIVO,
            "mac_address": "00:11:22:33:44:55"
        },
        {
            "modelo": "LoRa T100",
            "estado": EstadoSensor.ACTIVO,
            "mac_address": "00:11:22:33:44:56"
        },
        {
            "modelo": "LoRa T100",
            "estado": EstadoSensor.ACTIVO,
            "mac_address": "00:11:22:33:44:57"
        },
        {
            "modelo": "LoRa T100",
            "estado": EstadoSensor.ACTIVO,
            "mac_address": "00:11:22:33:44:58"
        },
        {
            "modelo": "LoRa T100",
            "estado": EstadoSensor.ACTIVO,
            "mac_address": "00:11:22:33:44:59"
        },
        {
            "modelo": "LoRa T100",
            "estado": EstadoSensor.ACTIVO,
            "mac_address": "00:11:22:33:44:60"
        }
    ]
    for sensor_data_item in sensor_data:
        sensor = SensorBase(**sensor_data_item)
        db_sensor = Sensor.model_validate(sensor, update={"campo_id": 1})
        db_sensor = db.create_entity(db_sensor)
        # Generate API key
        api_key = auth_service.create_token(data={"sensor_id": db_sensor.id}, sensor=True)
        db_sensor.api_key = api_key
        db.update_entity(db_sensor.id, Sensor, db_sensor)

def create_silobolsa(db: IUserDatabase) -> None:
    """
    Crea silobolsas para el campo
    """
    silobolsa_data = [
        {
            "marca": "Silobolsa Admin",
            "capacidad_max": 1000.0,
            "almacenado": 500.0,
            "ubicacion": "Parcela norte",
            "observaciones": "Silobolsa de prueba",
            "grano": Grano.GIRASOL
        },
        {
            "marca": "Silobolsa Admin 2",
            "capacidad_max": 1000.0,
            "almacenado": 100.0,
            "ubicacion": "Parcela sur",
            "observaciones": "Silobolsa de prueba",
            "grano": Grano.ARROZ
        },
        {
            "marca": "Silobolsa Admin 3",
            "capacidad_max": 1000.0,
            "almacenado": 200.0,
            "ubicacion": "Parcela este",
            "observaciones": "Silobolsa de prueba",
            "grano": Grano.MAIZ
        },
        {
            "marca": "Silobolsa Admin 4",
            "capacidad_max": 1000.0,
            "almacenado": 400.0,
            "ubicacion": "Parcela oeste",
            "observaciones": "Silobolsa de prueba",
            "grano": Grano.TRIGO
        },
        {
            "marca": "Silobolsa Admin 5",
            "capacidad_max": 1000.0,
            "almacenado": 600.0,
            "ubicacion": "Parcela norte",
            "observaciones": "Silobolsa de prueba",
            "grano": Grano.SOJA
        },
        {
            "marca": "Silobolsa Admin 6",
            "capacidad_max": 1000.0,
            "almacenado": 700.0,
            "ubicacion": "Parcela norte",
            "observaciones": "Silobolsa de prueba",
            "grano": Grano.SOJA
        }
    ]
    sensor_id = 1
    for silobolsa_data_item in silobolsa_data:
        silobolsa = SilobolsaBase(**silobolsa_data_item)
        db_silobolsa = Silobolsa.model_validate(silobolsa, update={"campo_id": 1, "sensor_id": sensor_id})
        sensor_id = sensor_id + 1
        db.create_entity(db_silobolsa)


def create_sintetic_data(db: IUserDatabase, auth_service: IAuthService) -> None:

    """Crea datos sintéticos para simulación y pruebas"""

    user_exist: bool = create_user(db, auth_service)
    if not user_exist:
        create_campo(db)
        create_sensores(db, auth_service)
        create_silobolsa(db)
  
    
