from fastapi import APIRouter

campo_router = APIRouter(prefix="/campos", tags=["campos"])

@campo_router.get("/")
async def get_campos():
    return {"message": "Get campos"}
    
@campo_router.post("/")
async def create_campo():
    return {"message": "Create campo"}
    
@campo_router.put("/{campo_id}")
async def update_campo(campo_id: int):
    return {"message": "Update campo"}
    
@campo_router.delete("/{campo_id}")
async def delete_campo(campo_id: int):
    return {"message": "Delete campo"}
    
