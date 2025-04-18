from fastapi import APIRouter, Depends
from app import services
from app.schemas import User
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/tiles")
async def get_dashboard_tiles(current_user: User = Depends(services.get_current_user)):
    return {"message": "Dashboard tiles"}