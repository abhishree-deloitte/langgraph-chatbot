from fastapi import APIRouter, Depends
from app.services.dashboard_service import DashboardService

router = APIRouter()

@router.get("/tiles")
async def get_dashboard_tiles(dashboard_service: DashboardService = Depends()):
    return await dashboard_service.get_tiles()