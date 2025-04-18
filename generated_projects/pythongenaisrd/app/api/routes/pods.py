from fastapi import APIRouter, Depends
from fastapi import HTTPException
from app.services import pods_service
from app.schemas import AssignEmployeeSchema, RecommendEmployeeSchema
from app.dependencies import get_db

pods_router = APIRouter(prefix="/api/pods", tags=["PODs"])

@pods_router.post("/assign")
async def assign_employee_to_pod(assign: AssignEmployeeSchema, db = Depends(get_db)):
    return pods_service.assign_employee_to_pod(assign, db)

@pods_router.get("/{pod_id}/details")
async def get_pod_details(pod_id: int, db = Depends(get_db)):
    return pods_service.get_pod_details(pod_id, db)

@pods_router.post("/{pod_id}/recommend")
async def recommend_employee_for_pod(pod_id: int, recommend: RecommendEmployeeSchema, db = Depends(get_db)):
    return pods_service.recommend_employee_for_pod(pod_id, recommend, db)