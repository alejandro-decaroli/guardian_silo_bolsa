from fastapi import FastAPI
from dotenv import load_dotenv
from .infrastructure.api.main_router import main_router

load_dotenv()

app = FastAPI(
        debug=True,
        title="Guardián Silo Bolsa API",
        description="Sistema de monitoreo escalable para el agro",
        version="1.0.0"
    )

# Registro de rutas
app.include_router(router=main_router, prefix="/api/v1")




