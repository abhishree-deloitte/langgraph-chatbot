from fastapi import APIRouter, Depends
from app.services.auth import login, get_current_user
from app.schemas.auth import UserLogin
from app.dependencies import get_db

router = APIRouter(prefix="/auth")

@router.post("/login")
def login(user: UserLogin, db=Depends(get_db)):
    return login(db, user)

@router.get("/user")
def get_current_user(db=Depends(get_db)):
    return get_current_user(db)