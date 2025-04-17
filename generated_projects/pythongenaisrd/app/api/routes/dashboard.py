from fastapi import APIRouter
from app.services.dashboard import get_dashboard_tiles

router = APIRouter(prefix="/tiles")

@router.get("/")
def get_tiles():
    return get_dashboard_tiles()