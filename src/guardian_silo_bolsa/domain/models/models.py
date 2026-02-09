from pydantic import EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship

class EstadoSilobolsa(Enum):
    """Estado del silobolsa."""
    VACIO = "VACIO"
    LLENO = "LLENO"
    DAÑADO = "DAÑADO"
    ALTERADO = "ALTERADO"

class EstadoSensor(Enum):
    """Estado del sensor."""
    OPERATIVO = "OPERATIVO"
    INOPERATIVO = "INOPERATIVO"
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

class Sensor(SensorBase, table=True):
    """
    Tabla de sensor.
    """
    id: int | None = Field(default=None, primary_key=True)
    silobolsa: Optional[Silobolsa] = Relationship(back_populates="sensor")

class SilobolsaLoteLink(SQLModel, table=True):
    """Tabla intermedia para la relación Muchos a Muchos entre Silobolsa y Lote"""
    silobolsa_id: Optional[int] = Field(
        default=None, foreign_key="silobolsa.id", primary_key=True
    )
    lote_id: Optional[int] = Field(
        default=None, foreign_key="lote.id", primary_key=True
    )

class LoteBase(SQLModel):
    """Base para la tabla de lote."""
    nombre: str
    grano: Grano
    fecha_cosecha: datetime
    observaciones: str

class Lote(LoteBase, table=True):
    """
    Tabla de lote.
    """
    id: int | None = Field(default=None, primary_key=True)
    silobolsas: List[Silobolsa] = Relationship(
        back_populates="lotes", 
        link_model=SilobolsaLoteLink
    )

class SilobolsaBase(SQLModel):
    """Base para la tabla de silobolsa."""
    marca: str
    capacidad_max: float
    peso_actual: float
    latitud: float
    longitud: float
    observaciones: Optional[str]
    estado: EstadoSilobolsa

class Silobolsa(SilobolsaBase, table=True):
    """
    Tabla de silobolsa.
    """
    id: int | None = Field(default=None, primary_key=True)
    campo_id: int | None = Field(default=None, foreign_key="campo.id")
    sensor_id: Optional[int] = Field(default=None, foreign_key="sensor.id", unique=True)
    lotes: List[Lote] = Relationship(
        back_populates="silobolsas", 
        link_model=SilobolsaLoteLink
    )
    sensor: Optional[Sensor] = Relationship(back_populates="silobolsa")
    campo: Optional[Campo] = Relationship(back_populates="silobolsas")    
    

class LecturaSilo(SQLModel, table=True):
    """
    Tabla de lectura de silo.
    """
    id: int | None = Field(default=None, primary_key=True)
    sensor_id: int
    timestamp: Optional[datetime]
    temp: Optional[float]
    hum: Optional[float]
    co2: Optional[float]


class CampoBase(SQLModel):
    """Base para la tabla de campo."""
    latitud: float
    longitud: float
    nombre: str

class Campo(CampoBase, table=True):
    """
    Tabla de campo.
    """
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(default=None, foreign_key="usuario.id")
    usuario: Optional[Usuario] = Relationship(back_populates="campos")
    silobolsas: Optional[List[Silobolsa]] = Relationship(back_populates="campo")


class UsuarioBase(SQLModel):
    """Base para la tabla de usuario."""
    nombre: str
    apellido: str
    email: EmailStr
    password: str

class Usuario(UsuarioBase, table=True):
    """
    Tabla de usuario.
    """
    id: int | None = Field(default=None, primary_key=True)
    campos: Optional[List[Campo]] = Relationship(back_populates="usuario")



