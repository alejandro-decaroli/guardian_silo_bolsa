from fastapi import APIRouter
from .user_router import user_router
from .sensor_router import sensor_router
from .silo_router import silo_router
from .lote_router import lote_router
from .campo_router import campo_router
from fastapi.responses import JSONResponse
from fastapi import status

main_router = APIRouter()

router_list = [user_router,sensor_router,silo_router,lote_router,campo_router]

for route in router_list:
    main_router.include_router(route)


@main_router.get("/")
async def root() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Bienvenido a Guardián silo bolsa"})

""" @app.post("/ingest")
async def guardar_registro(datos: LecturaSilo, background_tasks: BackgroundTasks) -> JSONResponse: 

    try:

        fields = {}

        if datos.co2 != None:
            fields["co2"] = datos.co2
        if datos.hum != None:
            fields["hum"] = datos.hum
        if datos.temp != None:
            fields["temp"] = datos.temp

        point = {
                    "measurement": "sensores_silo",
                    "tags": {
                        "grano": datos.grano, 
                        "sensor_id": datos.sensor_id, 
                        "silo": datos.silo
                    },
                    "fields": fields,
                    "timestamp": datos.timestamp
                }


        background_tasks.add_task(chequear_umbrales, datos)

        if not fields:

            guardar_en_csv(datos)

            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED, 
                content="Aceptado, pero hay valores nulos en todos los 'fields'. No se registra el punto en influxdb3, pero si en el archivo csv"
                )

        client.write(record=point) 
        
        guardar_en_csv(datos)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Registro creado con éxito en influxdb3 y archivo csv")
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
"""