from fastapi import APIRouter, Depends
from app.services.auth_service import AuthService
from app.schemas.auth import LoginCredentials, User

router = APIRouter()

@router.post("/login")
async def login(login_credentials: LoginCredentials, auth_service: AuthService = Depends()):
    return await auth_service.login(login_credentials)

@router.get("/user")
async def get_current_user(auth_service: AuthService = Depends()):
    return await auth_service.get_current_user()