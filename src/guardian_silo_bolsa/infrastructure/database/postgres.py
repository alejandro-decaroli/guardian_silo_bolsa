from sqlalchemy.orm import selectinload # type: ignore
from sqlmodel import create_engine, Session, SQLModel, select, text # type: ignore
from dotenv import load_dotenv # type: ignore
from typing import Optional, List, Any, Type, Dict
from ...domain.repository.database import IUserDatabase
import os   
from ...domain.models.models import (
    Silobolsa,
    Sensor,
    Campo,
    Usuario,
    UsuarioBase,
    UsuarioValidation,
)
from ...domain.exceptions.exceptions import (
    EntityAsociatedError,
    EntityNotFoundError,
    EntityAlreadyExistsError,
    InvalidCredentialsError
)

load_dotenv()

host = os.getenv('POSTGRES_HOST', "postgres_guardian")
user = os.getenv('POSTGRES_USER', "postgres")
password = os.getenv('POSTGRES_PASSWORD', "postgres")
database = os.getenv('POSTGRES_DB', "guardian_db")
port = os.getenv('POSTGRES_PORT', "5432")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(DATABASE_URL)


class PostgresDatabase(IUserDatabase):

    """Implementación de la interfaz de base de datos para PostgreSQL."""

    def __init__(self, client=engine):
        self.engine = client

    def validate_api_key(self, api_key: str) -> Sensor:
        with Session(self.engine) as session:
            try:
                statement = select(Sensor).where(Sensor.api_key == api_key)
                sensor: Optional[Sensor] = session.exec(statement).first()
                if sensor is None:
                    raise EntityNotFoundError("Sensor no encontrado")
                return sensor
            except Exception as e:
                session.rollback()
                raise e

    def get_user_by_email(self, usuario_data: UsuarioValidation) -> Usuario:
        """Verifica si existe un usuario con el email proporcionado."""
        with Session(self.engine) as session:
            try:
                db_object: Optional[Usuario] = session.exec(select(Usuario).where(Usuario.email == usuario_data.email)).first()
                if db_object is None:
                    raise EntityNotFoundError("Usuario")
                return db_object
            except Exception as e:
                session.rollback()
                raise e


    def update_user(self, entity_id: int, data: UsuarioBase) -> Usuario:
        """Actualiza un usuario."""
        with Session(self.engine) as session:
            try:
                db_user = session.get(Usuario, entity_id)
                if not db_user:
                    raise EntityNotFoundError("Usuario")
                # 2. Extraemos los datos nuevos como diccionario
                # exclude_unset=True es VITAL: evita que los campos que no mandaste
                # en el JSON pisen los datos de la DB con Nones.
                update_dict = data.model_dump(exclude_unset=True)

                # 3. Actualizamos los atributos del objeto de la DB uno por uno
                for key, value in update_dict.items():
                    setattr(db_user, key, value)

                # 4. Guardamos y refrescamos
                session.add(db_user)
                session.commit()
                session.refresh(db_user)
                return db_user
            except Exception as e:
                session.rollback()
                raise e

    def get_entity(self, entity_id: int, model: type[SQLModel]) -> Optional[SQLModel]:
        """
        Obtiene una entidad en base a su id.
        
        Args:
            entity_id: ID de la entidad.
        
        Returns:
            Entidad.
        """
        with Session(self.engine) as session:
            try:
                db_object: Optional[SQLModel] = session.get(model, entity_id)
                if not db_object:
                    raise EntityNotFoundError(model.__name__)
                return db_object
            except Exception as e:
                session.rollback()
                raise e

    def get_entities(self, current_user_id: int, model: type[SQLModel]) -> Optional[List[SQLModel]]:
        """
        Obtiene una lista de entidades.
        
        Args:
            current_user_id: ID del usuario.
            model: Modelo a obtener.
        
        Returns:
            Entidades.
        """
        with Session(self.engine) as session:
            try:
                if model is Sensor or model is Silobolsa:
                    campos = session.exec(select(Campo).where(Campo.usuario_id == current_user_id)).all()
                    entities = session.exec(select(model).where(model.campo_id.in_([campo.id for campo in campos]))).all()
                    return entities
                else:
                    db_objects = session.exec(select(model).where(model.usuario_id == current_user_id)).all()
                    return db_objects
            except Exception as e:
                session.rollback()
                raise e

    def create_entity(self, model: SQLModel) -> SQLModel:
        """
        Crea una entidad.
        
        Args:
            model: Modelo a crear.
        """
        with Session(self.engine) as session:
            try:
                session.add(model)
                session.commit()
                session.refresh(model)
                return model
            except Exception as e:
                session.rollback()
                raise e

    def update_entity(self, entity_id: int, model_class: Type[SQLModel], data: SQLModel) -> SQLModel:
        """
        Actualiza una entidad.
        
        Args:
            entity_id: ID de la entidad.
            model_class: Clase del modelo a actualizar.
            data: Datos a actualizar.
        
        Returns:
            Entidad actualizada.
        """
        with Session(self.engine) as session:
            try:
                # 1. Buscamos el registro actual por ID
                db_object: SQLModel = session.get(model_class, entity_id)
                if not db_object:
                    raise EntityNotFoundError(model_class.__name__)

                # 2. Extraemos los datos nuevos como diccionario
                # exclude_unset=True es VITAL: evita que los campos que no mandaste
                # en el JSON pisen los datos de la DB con Nones.
                update_dict = data.model_dump(exclude_unset=True)

                # 3. Actualizamos los atributos del objeto de la DB uno por uno
                for key, value in update_dict.items():
                    setattr(db_object, key, value)

                # 4. Guardamos y refrescamos
                session.add(db_object)
                session.commit()
                session.refresh(db_object)
                return db_object
                
            except Exception as e:
                session.rollback()
                raise e

    def delete_entity(self, entity_id: int, model: Type[SQLModel]) -> None:
        """
        Elimina una entidad.
        
        Args:
            entity_id: ID de la entidad a eliminar.
        """
        with Session(self.engine) as session:
            try:
                db_object: Optional[SQLModel] = session.get(model, entity_id)
                if not db_object:
                    raise EntityNotFoundError(model.__name__)
                """ if not isinstance(db_object, Usuario):
                    db_object.estado = "INACTIVO" """
                session.delete(db_object)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def get_by_handshake(self, mac_address: str) -> Sensor:
        """Obtiene un sensor por su Mac address"""
        with Session(self.engine) as session:
            try:
                statement = select(Sensor).where(Sensor.mac_address == mac_address)
                result = session.exec(statement).first()
                if not result:
                    raise EntityNotFoundError("Sensor")
                return result
            except Exception as e:
                session.rollback()
                raise e

    def create_db_and_tables(self) -> None:
        """Crea la base de datos y las tablas."""
        SQLModel.metadata.create_all(self.engine)

    def connect(self) -> None:
        """
        Forza la conexión a la base de datos.
        """
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("✅ Conexión a PostgreSQL establecida con éxito.")
        except Exception as e:
            print(f"❌ Error al conectar a PostgreSQL: {e}")
            raise e

    def close(self) -> None:
        """
        Cierra el pool de conexiones del engine.
        """
        try:
            self.engine.dispose()
            print("🔌 Pool de conexiones de PostgreSQL liberado.")
        except Exception as e:
            print(f"⚠️ Error al cerrar el motor de base de datos: {e}")

    def get_status(self) -> dict:
        """
        Devuelve el estado de salud de la base de datos.
        """
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return {"status": "online", "database": "postgresql", "message": "Reachable"}
        except Exception as e:
            return {"status": "offline", "database": "postgresql", "error": str(e)}

    


