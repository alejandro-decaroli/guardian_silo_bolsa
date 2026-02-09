from .postgres import PostgresDatabase

# Instanciamos aquí, lejos del main.py
postgres_db: PostgresDatabase = PostgresDatabase()

# Opcional: una función para FastAPI
def get_db() -> PostgresDatabase:
    return postgres_db