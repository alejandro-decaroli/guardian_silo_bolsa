from fastapi import APIRouter
from .user_router import user_router
from .sensor_router import sensor_router
from .silo_router import silo_router
from .lote_router import lote_router
from .campo_router import campo_router
from .telemetry_router import telemetry_router
from fastapi.responses import JSONResponse
from fastapi import status

main_router = APIRouter()

router_list = [user_router,sensor_router,silo_router,lote_router,campo_router,telemetry_router]

for route in router_list:
    main_router.include_router(route)


@main_router.get("/home", tags=["Home"])
def root() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Bienvenido a Guardián silo bolsa"})
