from pydantic import EmailStr, PositiveFloat, PositiveInt
from typing import Optional, List
from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship, Column
from sqlalchemy import String

class EstadoSilobolsa(Enum):
    """Estado del silobolsa."""
    VACIO = "VACIO"
    LLENO = "LLENO"
    DAÑADO = "DAÑADO"
    ALTERADO = "ALTERADO"
    INACTIVO = "INACTIVO"

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

class SiloSensorData(SQLModel):
    """Datos para la relación entre silo y sensor"""
    silobolsa_id: int
    sensor_id: int
    fecha_instalacion: datetime = Field(default_factory=datetime.now)

class Sensor(SensorBase, table=True):
    """
    Tabla de sensor.
    """
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    usuario: Optional["Usuario"] = Relationship(back_populates="sensores")
    silobolsa_links: List[SilobolsaSensorLink] = Relationship(back_populates="sensor")
    estado: str = Field(default="ACTIVO", sa_column=Column(String(20), nullable=False))
    
class SiloLoteData(SQLModel):
    """Datos para la relación entre silo y lote"""
    silobolsa_id: int
    lote_id: int
    cantidad: PositiveFloat 

class SilobolsaSensorLink(SQLModel, table=True):
    """Tabla intermedia para la relación Muchos a Muchos entre Silobolsa y Sensor"""
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", ondelete="CASCADE")
    usuario: Optional["Usuario"] = Relationship(back_populates="silobolsa_sensores")
    silobolsa_id: Optional[int] = Field(foreign_key="silobolsa.id", ondelete="CASCADE")
    sensor_id: Optional[int] = Field(foreign_key="sensor.id", ondelete="CASCADE")
    silobolsa: Silobolsa = Relationship(back_populates="sensor_links")
    sensor: Sensor = Relationship(back_populates="silobolsa_links")
    fecha_instalacion: datetime = Field(default_factory=datetime.now)
    estado: str = Field(default="ACTIVO", sa_column=Column(String(20), nullable=False))

class SilobolsaLoteLink(SQLModel, table=True):
    """Tabla intermedia para la relación Muchos a Muchos entre Silobolsa y Lote"""
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", ondelete="CASCADE")
    usuario: Optional["Usuario"] = Relationship(back_populates="silobolsa_lotes")
    silobolsa_id: Optional[int] = Field(foreign_key="silobolsa.id", ondelete="CASCADE")
    lote_id: Optional[int] = Field(foreign_key="lote.id", ondelete="CASCADE")
    silobolsa: Silobolsa = Relationship(back_populates="lotes_links")
    lote: Lote = Relationship(back_populates="silobolsas_links")
    cantidad: PositiveFloat 
    fecha_carga: datetime = Field(default_factory=datetime.now)
    estado: str = Field(default="ACTIVO", sa_column=Column(String(20), nullable=False))

class LoteBase(SQLModel):
    """Base para la tabla de lote."""
    nombre: str
    grano: Grano
    fecha_cosecha: datetime
    observaciones: str
    campo_id: int
    cantidad_cosechada: PositiveFloat 

class Lote(LoteBase, table=True):
    """
    Tabla de lote.
    """
    id: int | None = Field(default=None, primary_key=True)
    estado: str = Field(default="ACTIVO", sa_column=Column(String(20), nullable=False))
    usuario_id: int = Field(foreign_key="usuario.id", ondelete="CASCADE")
    usuario: Optional["Usuario"] = Relationship(back_populates="lotes")
    campo_id: int | None = Field(default=None, foreign_key="campo.id")
    campo: Optional["Campo"] = Relationship(back_populates="lotes")
    silobolsas_links: Optional[List[SilobolsaLoteLink]] = Relationship(back_populates="lote")

    @property
    def cosecha_almacenada(self) -> PositiveFloat:
        """Calcula la cosecha almacenada sumando las cantidades de todos los silos."""
        cant = 0
        for silo in self.silobolsas_links:
            if silo.estado == "ACTIVO":
                cant += silo.cantidad
        return cant


class SilobolsaBase(SQLModel):
    """Base para la tabla de silobolsa."""
    marca: str
    capacidad_max: PositiveFloat
    latitud: float
    longitud: float
    observaciones: Optional[str]
    estado: EstadoSilobolsa
    campo_id: int

class Silobolsa(SilobolsaBase, table=True):
    """
    Tabla de silobolsa.
    """
    id: int | None = Field(default=None, primary_key=True)
    campo_id: int | None = Field(default=None, foreign_key="campo.id")
    usuario_id: int = Field(foreign_key="usuario.id", ondelete="CASCADE")
    usuario: Optional[Usuario] = Relationship(back_populates="silobolsas")   
    lotes_links: List[SilobolsaLoteLink] = Relationship(back_populates="silobolsa")
    sensor_links: List[SilobolsaSensorLink] = Relationship(back_populates="silobolsa")
    campo: Campo = Relationship(back_populates="silobolsas")    

    @property
    def peso_actual(self) -> PositiveFloat:
        """Calcula el peso actual sumando las cantidades de todos los lotes."""
        peso = 0
        for lote in self.lotes_links:
            if lote.estado == "ACTIVO":
                peso += lote.cantidad
        return peso
    
    @property
    def porcentaje_llenado(self) -> PositiveFloat:
        """Calcula el porcentaje de llenado."""
        return (self.peso_actual / self.capacidad_max) * 100
    

    def vaciar(self) -> None:
        """Vacía el silobolsa."""
        self.estado = EstadoSilobolsa.VACIO
        for lote in self.lotes_links:
            if lote.estado == "ACTIVO":
                lote.estado = "INACTIVO"
    
    def llenar(self) -> None:
        """Llena el silobolsa."""
        self.estado = EstadoSilobolsa.LLENO


class LecturaSilo(SQLModel, table=True):
    """
    Tabla de lectura de silo.
    """
    id: int | None = Field(default=None, primary_key=True)
    sensor_id: int
    timestamp: Optional[datetime]
    temp: Optional[PositiveFloat]
    hum: Optional[PositiveFloat]
    co2: Optional[PositiveFloat]


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
    usuario_id: int = Field(foreign_key="usuario.id", ondelete="CASCADE")
    usuario: Optional[Usuario] = Relationship(back_populates="campos")
    silobolsas: Optional[List[Silobolsa]] = Relationship(back_populates="campo", cascade_delete=True)
    lotes: Optional[List[Lote]] = Relationship(back_populates="campo", cascade_delete=True)
    estado: str = Field(default="ACTIVO")

class UsuarioBase(SQLModel):
    """Base para la tabla de usuario."""
    nombre: str
    apellido: str
    email: EmailStr
    password: str


class UsuarioValidation(SQLModel):
    """Base para la validación de usuario."""
    email: EmailStr
    password: str

class Usuario(UsuarioBase, table=True):
    """
    Tabla de usuario.
    """
    id: int | None = Field(default=None, primary_key=True,)
    campos: Optional[List[Campo]] = Relationship(back_populates="usuario", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    sensores: Optional[List[Sensor]] = Relationship(back_populates="usuario", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    lotes: Optional[List[Lote]] = Relationship(back_populates="usuario", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    silobolsas: Optional[List[Silobolsa]] = Relationship(back_populates="usuario", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    silobolsa_lotes: Optional[List[SilobolsaLoteLink]] = Relationship(back_populates="usuario", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    silobolsa_sensores: Optional[List[SilobolsaSensorLink]] = Relationship(back_populates="usuario", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    role: str = Field(default="user")





