from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from app.services.auth import AuthService
from app.schemas.auth import LoginSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

router = APIRouter()

@router.post("/login")
async def login(data: LoginSchema):
    service = AuthService()
    return service.login(data)

@router.get("/user")
async def get_current_user(user: User = Depends()):
    return user