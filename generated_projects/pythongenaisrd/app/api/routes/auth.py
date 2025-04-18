from fastapi import APIRouter, Depends
from app.services.auth import AuthService
from app.schemas.auth import LoginCredentials, User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login(credentials: LoginCredentials):
    service = AuthService()
    return service.login(credentials)

@router.get("/user")
async def get_current_user_details():
    service = AuthService()
    return service.get_current_user_details()