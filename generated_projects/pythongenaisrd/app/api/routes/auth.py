from fastapi import APIRouter, Depends, HTTPException
from app.services.user_service import UserService
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from app.database import get_db

auth_router = APIRouter()

@auth_router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService()
    user = user_service.get_user(db, 1)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"token": "token"}

@auth_router.get("/user")
def get_current_user(db: Session = Depends(get_db)):
    user_service = UserService()
    user = user_service.get_current_user(db, 1)
    return {"user": user}