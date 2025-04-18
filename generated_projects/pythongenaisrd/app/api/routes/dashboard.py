from fastapi import APIRouter
from app.services.dashboard import DashboardService

router = APIRouter()

@router.get("/tiles")
async def get_dashboard_tiles():
    service = DashboardService()
    return service.get_tiles()