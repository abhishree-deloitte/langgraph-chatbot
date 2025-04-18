from fastapi import APIRouter, Depends
from app.services.pods import PodsService
from app.schemas.pods import PodAssignment, PodRecommendation

router = APIRouter(prefix="/pods", tags=["PODs"])

@router.post("/assign")
async def assign_employee_to_pod(assignment: PodAssignment):
    service = PodsService()
    return service.assign_employee_to_pod(assignment)

@router.get("/{pod_id}/details")
async def get_pod_details(pod_id: int):
    service = PodsService()
    return service.get_pod_details(pod_id)

@router.post("/{pod_id}/recommend")
async def recommend_employee_for_pod(pod_id: int, recommendation: PodRecommendation):
    service = PodsService()
    return service.recommend_employee_for_pod(pod_id, recommendation)