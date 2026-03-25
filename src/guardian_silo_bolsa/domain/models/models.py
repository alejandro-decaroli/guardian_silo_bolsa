from pydantic import EmailStr, PositiveFloat
from typing import Optional, List
from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship, Column
from sqlalchemy import String

class TelemetrySchema(SQLModel):
    """Esquema para los datos de telemetría."""
    co2: Optional[float] = None
    hum: Optional[float] = None
    temp: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    api_key: str

class TelemetryRecord(SQLModel, table=True):
    """Esquema de los datos para las "alertas" y "visto" de los registros"""
    id: int| None = Field(default=None, primary_key=True)
    alerta: bool = Field(default="False")
    visto: bool = Field(default=False)

class Mac_Address(SQLModel):
    """Dirección MAC del sensor."""
    mac_address: str

class EstadoSensor(Enum):
    """Estado del sensor."""
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"
    FALLA = "FALLA"
    
class Grano(Enum):
    """Tipo de grano."""
    TRIGO = "TRIGO"
    MAIZ = "MAIZ"
    SOJA = "SOJA"
    GIRASOL = "GIRASOL"
    ARROZ = "ARROZ"

class SiloSensorData(SQLModel):
    """Datos para la relación entre silo y sensor"""
    silobolsa_id: int
    sensor_id: int
    fecha_instalacion: datetime = Field(default_factory=datetime.now)

class SensorBase(SQLModel):
    """Base para la tabla de sensor."""
    modelo: str
    estado: EstadoSensor
    mac_address: str = Field(unique=True, index=True) 

class Sensor(SensorBase, table=True):
    """
    Tabla de sensor.
    """
    id: int | None = Field(default=None, primary_key=True)
    api_key: Optional[str] = Field(default=None)
    estado: str = Field(default="ACTIVO", sa_column=Column(String(20), nullable=False))
    
class SilobolsaBase(SQLModel):
    """Base para la tabla de silobolsa."""
    marca: str
    capacidad_max: PositiveFloat
    almacenado: PositiveFloat
    grano: Grano
    ubicacion: str
    observaciones: Optional[str]
    campo_id: int

class Silobolsa(SilobolsaBase, table=True):
    """
    Tabla de silobolsa.
    """
    id: int | None = Field(default=None, primary_key=True)
    campo_id: int | None = Field(default=None, foreign_key="campo.id")
    sensor_id: int | None = Field(default=None, foreign_key="sensor.id", unique=True)
    campo: Campo = Relationship(back_populates="silobolsas")    
    sensor: Sensor = Relationship(back_populates="silobolsas")    


class CampoBase(SQLModel):
    """Base para la tabla de campo."""
    ubicacion: str
    nombre: str

class Campo(CampoBase, table=True):
    """
    Tabla de campo.
    """
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", ondelete="CASCADE")
    usuario: Optional[Usuario] = Relationship(back_populates="campos")
    silobolsas: Optional[List[Silobolsa]] = Relationship(back_populates="campo", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    sensores: Optional[List[Sensor]] = Relationship(back_populates="campo", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    estado: str = Field(default="ACTIVO")

class UsuarioBase(SQLModel):
    """Base para la tabla de usuario."""
    nombre: str
    apellido: str
    email: EmailStr
    password: str
    telefono: str

class UsuarioValidation(SQLModel):
    """Base para la validación de usuario."""
    email: EmailStr
    password: str

class Usuario(UsuarioBase, table=True):
    """
    Tabla de usuario.
    """
    id: int | None = Field(default=None, primary_key=True)
    campos: Optional[List[Campo]] = Relationship(back_populates="usuario", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    role: str = Field(default="user")





