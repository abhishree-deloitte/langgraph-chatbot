from fastapi import APIRouter, Depends
from app.services.auth import login, get_current_user
from app.schemas.auth import Login, User
from app.dependencies import get_db_session

router = APIRouter()

@router.post("/login")
async def login_user(credentials: Login, db_session=Depends(get_db_session)):
    return login(credentials, db_session)

@router.get("/user")
async def get_current_user(db_session=Depends(get_db_session)):
    return get_current_user(db_session)