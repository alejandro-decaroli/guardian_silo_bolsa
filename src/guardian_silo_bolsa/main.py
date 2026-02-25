from fastapi import FastAPI, Request
from dotenv import load_dotenv
from .infrastructure.api.main_router import main_router
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from .domain.exceptions.exceptions import AppError
from .infrastructure.database.deps import postgres_db
from .create_admin import create_admin
from .infrastructure.security.auth_handler import AuthService

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    print(f"🚀 Iniciando {app.title}...")
    
    # Verificamos conexión y creamos tablas
    postgres_db.connect()
    postgres_db.create_db_and_tables()
    
    # Creamos el admin
    create_admin(postgres_db, AuthService())
    
    yield 
    
    # --- SHUTDOWN ---
    print(f"🛑 Apagando {app.title}...")
    postgres_db.close()

app = FastAPI(
        debug=True,
        title="Guardián Silo Bolsa API",
        description="Sistema de monitoreo escalable para el agro",
        version="1.7.0",
        lifespan=lifespan
    )

# Registro de rutas
app.include_router(router=main_router, prefix="/api/v1")

@app.exception_handler(AppError)
async def app_exception_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.code,
        content={
            "status": "error",
            "type": exc.__class__.__name__,
            "message": exc.message
        }
    )

# 2. Handler para errores desconocidos (Cualquier otra cosa)
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Aquí podrías usar un logger para guardar el error real en Arch
    print(f"🔥 Error no controlado: {str(exc)}") 
    
    return JSONResponse(
        status_code=500,
        content={
            "status": "critical",
            "message": "Ocurrió un error inesperado en el servidor."
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

'''

7500 merceria y 2500 farmacia

1ra FASE: interconectar

TODO: 1) Implementar JWT para autenticacion [x]

TODO: 2) Un Usuario debe poder crear campos y sensores. Para esto los routers de cada uno deben extraer un id de usuario del token y crearlos con ese id.

Se deben modificar los casos de uso para que reciban el id de usuario, y modifica postgres para que los acepte y haga la operacion correspondiente.

TODO: 3) Dentro de cada campo se deben poder crear silobolsas y lotes, para esto se les tiene que pasar el id del campo.

TODO: 4) A travez del campo se debe poder acceder a un silo y asignarle uno o varios lotes o varios sensores, pasandole el id de silo

2da FASE: lecturas

TODO: 1) Implementar endpoint para que el sensor pueda enviar sus lecturas (agregar id de usuario).

TODO: 2) Implementar endpoint para que el usuario pueda ver las lecturas de sus sensores.

TODO: 3) Simular lecturas de sensores para probar el endpoint.

TODO: 4) Crear frontend

'''