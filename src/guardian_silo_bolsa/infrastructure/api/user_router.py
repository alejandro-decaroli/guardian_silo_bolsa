from fastapi import APIRouter

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.get("/")
async def get_users():
    return {"message": "Get users"}
    
@user_router.post("/")
async def create_user():
    return {"message": "Create user"}
    
@user_router.put("/{user_id}")
async def update_user(user_id: int):
    return {"message": "Update user"}
    
@user_router.delete("/{user_id}")
async def delete_user(user_id: int):
    return {"message": "Delete user"}
