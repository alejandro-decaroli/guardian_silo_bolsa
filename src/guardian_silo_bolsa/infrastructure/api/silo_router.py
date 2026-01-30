from fastapi import APIRouter

silo_router = APIRouter(prefix="/silos", tags=["silos"])

@silo_router.get("/")
async def get_silos():
    return {"message": "Get silos"}
    
@silo_router.post("/")
async def create_silo():
    return {"message": "Create silo"}
    
@silo_router.put("/{silo_id}")
async def update_silo(silo_id: int):
    return {"message": "Update silo"}
    
@silo_router.delete("/{silo_id}")
async def delete_silo(silo_id: int):
    return {"message": "Delete silo"}
