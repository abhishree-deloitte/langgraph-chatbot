from fastapi import APIRouter, Depends
from app.services.user_service import UserService
from sqlalchemy.orm import Session
from app.database import get_db

dashboard_router = APIRouter()

@dashboard_router.get("/tiles")
def get_dashboard_tiles(db: Session = Depends(get_db)):
    user_service = UserService()
    user = user_service.get_current_user(db, 1)
    return {"tiles": []}