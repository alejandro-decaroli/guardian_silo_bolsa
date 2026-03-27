from pydantic import EmailStr, PositiveFloat # type: ignore
from typing import Optional, List
from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship, Column # type: ignore
from sqlalchemy import String # type ignore
from sqlalchemy import Enum as SAEnum # type: ignore

class TelemetrySchema(SQLModel):
    """Esquema para los datos de telemetría."""
    co2: Optional[float] = None
    hum: Optional[float] = None
    temp: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    api_key: str

class TelemetryRecord(SQLModel, table=True): # type: ignore
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

class SensorBase(SQLModel):
    """Base para la tabla de sensor."""
    modelo: str
    estado: EstadoSensor
    mac_address: str = Field(unique=True, index=True) 

class Sensor(SensorBase, table=True): # type: ignore
    """
    Tabla de sensor.
    """
    id: int | None = Field(default=None, primary_key=True)
    api_key: Optional[str] = Field(default=None)
    estado: EstadoSensor = Field(default=EstadoSensor.ACTIVO, sa_column=Column(SAEnum(EstadoSensor), nullable=False)) # type: ignore
    campo_id: int | None = Field(default=None, foreign_key="campo.id", ondelete="CASCADE")
    campo: Optional[Campo] = Relationship(back_populates="sensores")
    
class SilobolsaBase(SQLModel):
    """Base para la tabla de silobolsa."""
    marca: str
    capacidad_max: PositiveFloat
    almacenado: PositiveFloat
    grano: Grano
    ubicacion: str
    observaciones: Optional[str]

class SensorSilo(SQLModel):
    """Base para la tabla de sensor-silo."""
    sensor_id: int
    silobolsa_id: int

class Silobolsa(SilobolsaBase, table=True): # type: ignore
    """
    Tabla de silobolsa.
    """
    id: int | None = Field(default=None, primary_key=True)
    sensor_id: int | None = Field(default=None, foreign_key="sensor.id", unique=True, ondelete="CASCADE")
    campo_id: int | None = Field(default=None, foreign_key="campo.id", ondelete="CASCADE") 
    campo: Optional[Campo] = Relationship(back_populates="silobolsas")
    

class CampoBase(SQLModel):
    """Base para la tabla de campo."""
    ubicacion: str
    nombre: str

class Campo(CampoBase, table=True): # type: ignore
    """
    Tabla de campo. 
    """
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", ondelete="CASCADE")
    usuario: Optional[Usuario] = Relationship(back_populates="campos")
    silobolsas: Optional[List[Silobolsa]] = Relationship(back_populates="campo", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    sensores: Optional[List[Sensor]] = Relationship(back_populates="campo", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

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

class Usuario(UsuarioBase, table=True): # type: ignore
    """
    Tabla de usuario.
    """
    id: int | None = Field(default=None, primary_key=True)
    campos: Optional[List[Campo]] = Relationship(back_populates="usuario", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    role: str = Field(default="user")





