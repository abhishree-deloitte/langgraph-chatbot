from fastapi import APIRouter
from app.services import dashboard_service

dashboard_router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@dashboard_router.get("/tiles")
async def get_dashboard_tiles():
    return dashboard_service.get_dashboard_tiles()