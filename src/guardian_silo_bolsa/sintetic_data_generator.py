from .domain.models.models import (
    Usuario, 
    UsuarioBase, 
    UsuarioValidation, 
    CampoBase, 
    Campo,
    Sensor,
    SensorBase,
    Lote,
    LoteBase,
    Silobolsa,
    SilobolsaBase,
    SiloLoteData,
    SiloSensorData,
    SilobolsaLoteLink,
    SilobolsaSensorLink,
    Grano,
    EstadoSensor,
    EstadoSilobolsa
    )
from .domain.repository.database import IUserDatabase
from .domain.services.auth_interface import IAuthService

def create_user(db: IUserDatabase, auth_service: IAuthService) -> bool:
    """
    Crea un usuario admin si no existe
    """
    admin_validation = UsuarioValidation(email="admin@example.com", password="admin")
    user = db.get_user_by_email(admin_validation)
    if user:
        return True
    admin_data = {
        "nombre": "admin",
        "apellido": "fake lastname",
        "password": "admin",
        "email": "admin@example.com"
    }
    admin = UsuarioBase(**admin_data)
    db_admin = Usuario.model_validate(admin)
    db_admin.password = auth_service.hash_password(admin.password)
    db_admin.role = "admin"
    db.create_user(db_admin)
    return False


def create_campo(db: IUserDatabase) -> None:
    """
    Crea un campo para el usuario admin
    """
    campo_data = {
        "latitud": -34.6037,
        "longitud": -58.3816,
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
            "modelo": "Sensor Admin",
            "estado": EstadoSensor.ACTIVO,
            "mac_address": "00:11:22:33:44:55"
        },
        {
            "modelo": "Sensor Admin 2",
            "estado": EstadoSensor.ACTIVO,
            "mac_address": "00:11:22:33:44:56"
        },
        {
            "modelo": "Sensor Admin 3",
            "estado": EstadoSensor.ACTIVO,
            "mac_address": "00:11:22:33:44:57"
        },
        {
            "modelo": "Sensor Admin 4",
            "estado": EstadoSensor.ACTIVO,
            "mac_address": "00:11:22:33:44:58"
        },
        {
            "modelo": "Sensor Admin 5",
            "estado": EstadoSensor.ACTIVO,
            "mac_address": "00:11:22:33:44:59"
        },
        {
            "modelo": "Sensor Admin 6",
            "estado": EstadoSensor.ACTIVO,
            "mac_address": "00:11:22:33:44:60"
        }
    ]
    for sensor_data_item in sensor_data:
        sensor = SensorBase(**sensor_data_item)
        db_sensor = Sensor.model_validate(sensor, update={"usuario_id": 1})
        db_sensor = db.create_entity(db_sensor)
        # Generate API key
        api_key = auth_service.create_token(data={"sensor_id": db_sensor.id, "usuario_id": 1}, sensor=True)
        db_sensor.api_key = api_key
        db.update_entity(1, db_sensor.id, Sensor, db_sensor)

def create_silobolsa(db: IUserDatabase) -> None:
    """
    Crea silobolsas para el campo
    """
    silobolsa_data = [
        {
            "marca": "Silobolsa Admin",
            "capacidad_max": 1000.0,
            "latitud": -34.6037,
            "longitud": -58.3816,
            "observaciones": "Silobolsa de prueba",
            "campo_id": 1,
            "estado": EstadoSilobolsa.LLENO
        },
        {
            "marca": "Silobolsa Admin 2",
            "capacidad_max": 1000.0,
            "latitud": -4.6037,
            "longitud": -18.3816,
            "observaciones": "Silobolsa de prueba",
            "campo_id": 1,
            "estado": EstadoSilobolsa.LLENO
        },
        {
            "marca": "Silobolsa Admin 3",
            "capacidad_max": 1000.0,
            "latitud": -24.6037,
            "longitud": -48.3816,
            "observaciones": "Silobolsa de prueba",
            "campo_id": 1,
            "estado": EstadoSilobolsa.LLENO
        },
        {
            "marca": "Silobolsa Admin 4",
            "capacidad_max": 1000.0,
            "latitud": -14.6037,
            "longitud": -28.3816,
            "observaciones": "Silobolsa de prueba",
            "campo_id": 1,
            "estado": EstadoSilobolsa.LLENO
        },
        {
            "marca": "Silobolsa Admin 5",
            "capacidad_max": 1000.0,
            "latitud": -74.6037,
            "longitud": -88.3816,
            "observaciones": "Silobolsa de prueba",
            "campo_id": 1,
            "estado": EstadoSilobolsa.LLENO
        },
        {
            "marca": "Silobolsa Admin 6",
            "capacidad_max": 1000.0,
            "latitud": -44.6037,
            "longitud": -68.3816,
            "observaciones": "Silobolsa de prueba",
            "campo_id": 1,
            "estado": EstadoSilobolsa.LLENO
        }
    ]
    for silobolsa_data_item in silobolsa_data:
        silobolsa = SilobolsaBase(**silobolsa_data_item)
        db_silobolsa = Silobolsa.model_validate(silobolsa, update={"usuario_id": 1})
        db.create_entity(db_silobolsa)


def create_lote(db: IUserDatabase) -> None:
    """
    Crea un lote para el campo
    """
    lote_data = {
            "nombre": "Lote Admin",
            "grano": Grano.GIRASOL,
            "observaciones": "Lote de prueba",
            "campo_id": 1,
            "cantidad_cosechada": 1000.0,
            "fecha_cosecha": datetime.datetime.today()
        }
    lote = LoteBase(**lote_data)
    db_lote = Lote.model_validate(lote, update={"usuario_id": 1})
    db.create_entity(db_lote)

def create_silo_lote(db: IUserDatabase) -> None:
    """
    Crea asignaciones de silobolsas a lotes
    """

    silo_lote_data = [
        {
        "silobolsa_id": 1,
        "lote_id": 1,
        "cantidad": 200.0
        },
        {
        "silobolsa_id": 2,
        "lote_id": 1,
        "cantidad": 200.0
        },
        {
        "silobolsa_id": 3,
        "lote_id": 1,
        "cantidad": 200.0
        },
        {
        "silobolsa_id": 4,
        "lote_id": 1,
        "cantidad": 200.0
        },
        {
        "silobolsa_id": 5,
        "lote_id": 1,
        "cantidad": 100.0
        },
        {
        "silobolsa_id": 6,
        "lote_id": 1,
        "cantidad": 100.0
        }
    ]
    for silo_lote_data_item in silo_lote_data:
        silo_lote = SiloLoteData(**silo_lote_data_item)
        db_silo_lote = SilobolsaLoteLink.model_validate(silo_lote, update={"usuario_id": 1})
        db.create_entity(db_silo_lote)


def create_silo_sensor(db: IUserDatabase) -> None:
    """
    Crea asignaciones de silobolsas a sensores
    """

    silo_sensor_data = [
        {
        "silobolsa_id": 1,
        "sensor_id": 1
        },
        {
        "silobolsa_id": 2,
        "sensor_id": 2
        },
        {
        "silobolsa_id": 3,
        "sensor_id": 3
        },
        {
        "silobolsa_id": 4,
        "sensor_id": 4
        },
        {
        "silobolsa_id": 5,
        "sensor_id": 5
        },
        {
        "silobolsa_id": 6,
        "sensor_id": 6
        }
    ]
    
    for silo_sensor_data_item in silo_sensor_data:
        silo_sensor = SiloSensorData(**silo_sensor_data_item)
        db_silo_sensor = SilobolsaSensorLink.model_validate(silo_sensor, update={"usuario_id": 1})
        db.create_entity(db_silo_sensor)


def create_sintetic_data(db: IUserDatabase, auth_service: IAuthService) -> None:

    """Crea datos sintéticos para simulación y pruebas"""

    user_exist: bool = create_user(db, auth_service)
    if not user_exist:
        create_campo(db)
        create_sensores(db, auth_service)
        create_silobolsa(db)
        create_lote(db)
        create_silo_lote(db)
        create_silo_sensor(db)
  
    
