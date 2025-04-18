from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import SessionLocal
from app.database.models import User
from app.schemas import UserLogin, UserResponse

router = APIRouter()

@router.post("/login")
def login(user: UserLogin):
    db = SessionLocal()
    user_obj = db.query(User).filter(User.email == user.email).first()
    if user_obj and user_obj.password == user.password:
        return UserResponse(
            id=user_obj.id,
            name=user_obj.name,
            email=user_obj.email,
        )
    return {"message": "Invalid email or password"}

@router.get("/user")
def get_current_user():
    db = SessionLocal()
    user_obj = db.query(User).first()
    if user_obj:
        return UserResponse(
            id=user_obj.id,
            name=user_obj.name,
            email=user_obj.email,
        )
    return {"message": "User not found"}