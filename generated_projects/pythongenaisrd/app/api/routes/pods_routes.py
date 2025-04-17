from fastapi import APIRouter, Depends
from app.services.pods_service import PodsService
from app.schemas.pods import PodAssignment, PodDetails, PodRecommendation

router = APIRouter()

@router.post("/pods/assign")
async def assign_to_pod(pod_assignment: PodAssignment, pods_service: PodsService = Depends()):
    return await pods_service.assign_to_pod(pod_assignment)

@router.get("/pods/{pod_id}/details")
async def get_pod_details(pod_id: int, pods_service: PodsService = Depends()):
    return await pods_service.get_pod_details(pod_id)

@router.post("/pods/{pod_id}/recommend")
async def recommend_for_pod(pod_id: int, pod_recommendation: PodRecommendation, pods_service: PodsService = Depends()):
    return await pods_service.recommend_for_pod(pod_recommendation)