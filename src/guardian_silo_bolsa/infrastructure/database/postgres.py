from sqlalchemy.orm import selectinload
from sqlmodel import create_engine, Session, SQLModel, select, text
from dotenv import load_dotenv
from typing import Optional, List, Any, Type
from ...domain.repository.database import UserDatabaseInterface
import os   
from ...domain.models.models import (
    Silobolsa,
    Sensor,
    Lote,
    Campo,
    Usuario,
    UsuarioBase,
    UsuarioValidation,
    SiloLoteData,
    SilobolsaLoteLink,
    SilobolsaSensorLink,
    SiloSensorData
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


class PostgresDatabase(UserDatabaseInterface):

    """Implementación de la interfaz de base de datos para PostgreSQL."""

    def __init__(self, client=engine):
        self.engine = client

    def get_user_by_email(self, usuario_data: UsuarioValidation) -> Optional[Usuario]:
        """Verifica si existe un usuario con el email proporcionado."""
        with Session(self.engine) as session:
            try:
                db_object: Optional[SQLModel] = session.exec(select(Usuario).where(Usuario.email == usuario_data.email)).first()
                return db_object
            except Exception as e:
                session.rollback()
                raise e

    def get_user_by_id(self, user_id: int) -> Usuario:
        """Obtiene un usuario por su ID."""
        with Session(self.engine) as session:
            try:
                db_object: Optional[SQLModel] = session.exec(select(Usuario).where(Usuario.id == user_id)).first()
                return db_object
            except Exception as e:
                session.rollback()
                raise e

    def get_all_users(self) -> List[Usuario]:
        """Obtiene todos los usuarios."""
        with Session(self.engine) as session:
            try:
                db_objects: List[SQLModel] = session.exec(select(Usuario)).all()
                return db_objects
            except Exception as e:
                session.rollback()
                raise e

    def create_user(self, usuario_data: Usuario) -> Usuario:
        """Crea un usuario."""
        with Session(self.engine) as session:
            try:
                session.add(usuario_data)
                session.commit()
                session.refresh(usuario_data)
                return usuario_data
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

    def delete_user(self, user_id: int) -> None:
        """Elimina un usuario."""
        with Session(self.engine) as session:
            try:
                db_user = session.get(Usuario, user_id)
                if not db_user:
                    raise EntityNotFoundError("Usuario")
                session.delete(db_user)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def get_entity(self, current_user_id: int, entity_id: int, model: type[SQLModel]) -> Optional[SQLModel]:
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
                if db_object.usuario_id != current_user_id:
                    raise EntityNotFoundError(model.__name__)
                return db_object
            except Exception as e:
                session.rollback()
                raise e

    def get_entities(self, current_user_id: int, model: type[SQLModel]) -> Optional[List[SQLModel]]:
        """
        Obtiene una lista de entidades.
        
        Args:
            user_id: ID del usuario.
            model: Modelo a obtener.
        
        Returns:
            Entidades.
        """
        with Session(self.engine) as session:
            try:
                db_objects: Optional[List[SQLModel]] = session.exec(select(model).where(model.usuario_id == current_user_id)).all()
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

    def update_entity(self, current_user_id: int, entity_id: int, model_class: Type[SQLModel], data: SQLModel) -> SQLModel:
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
                db_object = session.get(model_class, entity_id)
                if not db_object:
                    raise EntityNotFoundError(model_class.__name__)
                if db_object.usuario_id != current_user_id:
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

    def delete_entity(self, current_user_id: int, entity_id: int, model: Type[SQLModel]) -> None:
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
                if db_object.usuario_id != current_user_id:
                    raise EntityNotFoundError(model.__name__)
                if not isinstance(db_object, Usuario):
                    db_object.estado = "INACTIVO"
                    session.add(db_object)
                else:
                    session.delete(db_object)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def setear_lote(self, current_user_id: int, data: SiloLoteData) -> SilobolsaLoteLink:
        """
        Setea el lote de un silo.
        
        Args:
            data: Datos del silo y lote.
        """
        with Session(self.engine) as session:
            try:
                silo_lote = SilobolsaLoteLink(
                    usuario_id=current_user_id,
                    silobolsa_id=data.silobolsa_id,
                    lote_id=data.lote_id,
                    cantidad=data.cantidad
                )
                session.add(silo_lote)
                session.commit()
                session.refresh(silo_lote)
                return silo_lote
            except Exception as e:
                session.rollback()
                raise e

    def setear_sensor(self, current_user_id: int, data: SiloSensorData) -> SilobolsaSensorLink:
        """
        Setea el sensor de un silo.
        
        Args:
            data: Datos del silo y sensor.
        """
        with Session(self.engine) as session:
            try:
                silo_sensor = SilobolsaSensorLink(
                    usuario_id=current_user_id,
                    silobolsa_id=data.silobolsa_id,
                    sensor_id=data.sensor_id
                )
                session.add(silo_sensor)
                session.commit()
                session.refresh(silo_sensor)
                return silo_sensor
            except Exception as e:
                session.rollback()
                raise e

    def get_silo_and_sensor(self, current_user_id: int, entity_id: int) -> Silobolsa:
        """
        Obtiene un silo y su sensor.
        
        Args:
            entity_id: ID del silo.
        """
        with Session(self.engine) as session:
            try:
                statement = select(Silobolsa).where(Silobolsa.id == entity_id).options(selectinload(Silobolsa.sensor_links))
                result = session.exec(statement).first()
                if not result:
                    raise EntityNotFoundError("Silobolsa")
                if result.usuario_id != current_user_id:
                    raise EntityNotFoundError("Silobolsa")
                return result
            except Exception as e:
                session.rollback()
                raise e
    
    def get_silo_and_lotes(self, current_user_id: int, entity_id: int) -> Silobolsa:
        """
        Obtiene un silo y sus lotes.
        
        Args:
            entity_id: ID del silo.
        """
        with Session(self.engine) as session:
            try:
                statement = select(Silobolsa).where(Silobolsa.id == entity_id).options(selectinload(Silobolsa.lotes_links))
                result = session.exec(statement).first()
                if not result:
                    raise EntityNotFoundError("Silobolsa")
                if result.usuario_id != current_user_id:
                    raise EntityNotFoundError("Silobolsa")
                return result
            except Exception as e:
                session.rollback()
                raise e
    
    def get_lote_and_silos(self, current_user_id: int, entity_id: int) -> Lote:
        """
        Obtiene un lote y sus silos.
        
        Args:
            entity_id: ID del lote.
        """
        with Session(self.engine) as session:
            try:
                statement = select(Lote).where(Lote.id == entity_id).options(selectinload(Lote.silobolsas_links))
                result = session.exec(statement).first()
                if not result:
                    raise EntityNotFoundError("Lote")
                if result.usuario_id != current_user_id:
                    raise EntityNotFoundError("Lote")
                return result
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

    


