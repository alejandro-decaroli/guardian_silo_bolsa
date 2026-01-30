from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class EstadoSilobolsa(Enum):
    VACIO = "VACIO"
    LLENO = "LLENO"
    DAÑADO = "DAÑADO"
    ALTERADO = "ALTERADO"

class EstadoSensor(Enum):
    OPERATIVO = "OPERATIVO"
    INOPERATIVO = "INOPERATIVO"
    FALLA = "FALLA"

    
class Grano(Enum):
    TRIGO = "TRIGO"
    MAIZ = "MAIZ"
    SOJA = "SOJA"
    GIRASOL = "GIRASOL"
    ARROZ = "ARROZ"

class Lote(BaseModel):
    id: int
    nombre: str
    grano: Grano
    fecha_cosecha: datetime
    observaciones: str    

class Sensor(BaseModel):
    id: int
    modelo: str
    estado: EstadoSensor

class Silobolsa(BaseModel):
    id: int
    marca: str
    capacidad_max: float
    peso_actual: float
    latitud: float
    longitud: float
    lote: Optional[Lote]
    estado: EstadoSilobolsa
    sensor: Optional[Sensor]
    observaciones: Optional[str]

class LecturaSilo(BaseModel):
    sensor_id: int
    timestamp: Optional[datetime]
    temp: Optional[float]
    hum: Optional[float]
    co2: Optional[float]

class Campo(BaseModel):
    id: int
    latitud: float
    longitud: float
    nombre: str
    silobolsas: list[Silobolsa] = []

class Usuario(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: EmailStr
    password: str
    campos: List[Campo] = []



