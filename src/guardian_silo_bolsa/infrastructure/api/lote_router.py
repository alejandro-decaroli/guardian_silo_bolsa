from fastapi import APIRouter

lote_router = APIRouter(prefix="/lotes", tags=["lotes"])

@lote_router.get("/")
async def get_lotes():
    return {"message": "Get lotes"}
    
@lote_router.post("/")
async def create_lote():
    return {"message": "Create lote"}
    
@lote_router.put("/{lote_id}")
async def update_lote(lote_id: int):
    return {"message": "Update lote"}
    
@lote_router.delete("/{lote_id}")
async def delete_lote(lote_id: int):
    return {"message": "Delete lote"}
