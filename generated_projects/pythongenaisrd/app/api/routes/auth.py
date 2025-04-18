from fastapi import APIRouter, Depends
from fastapi import HTTPException
from app.services import auth_service
from app.schemas import LoginSchema
from app.dependencies import get_db

auth_router = APIRouter(prefix="/api/auth", tags=["Auth"])

@auth_router.post("/login")
async def user_login(login: LoginSchema, db = Depends(get_db)):
    return auth_service.user_login(login, db)

@auth_router.get("/user")
async def fetch_current_user_details(db = Depends(get_db)):
    return auth_service.fetch_current_user_details(db)