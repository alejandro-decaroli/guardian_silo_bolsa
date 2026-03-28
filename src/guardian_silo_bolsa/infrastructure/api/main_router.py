from fastapi import APIRouter # type: ignore
from .user_router import user_router
from .sensor_router import sensor_router
from .silo_router import silo_router
from .campo_router import campo_router
from .telemetry_router import telemetry_router
from .alerta_router import alerta_router
from fastapi.responses import JSONResponse # type: ignore
from fastapi import status # type: ignore
 
main_router = APIRouter()

router_list = [user_router, sensor_router, silo_router, campo_router, telemetry_router, alerta_router]

for route in router_list:
    main_router.include_router(route)


@main_router.get("/home", tags=["Home"])
def root() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Bienvenido a Guardián silo bolsa"})
