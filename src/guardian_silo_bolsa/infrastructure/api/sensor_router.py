from fastapi import APIRouter

sensor_router = APIRouter(prefix="/sensores", tags=["sensores"])

@sensor_router.get("/")
async def get_sensores():
    return {"message": "Get sensores"}
    
@sensor_router.post("/")
async def create_sensor():
    return {"message": "Create sensor"}
    
@sensor_router.put("/{sensor_id}")
async def update_sensor(sensor_id: int):
    return {"message": "Update sensor"}
    
@sensor_router.delete("/{sensor_id}")
async def delete_sensor(sensor_id: int):
    return {"message": "Delete sensor"}
