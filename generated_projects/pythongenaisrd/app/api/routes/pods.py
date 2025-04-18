from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from app.services.pods import PodService
from app.db.models import User
from app.schemas.pods import AssignPodSchema, RecommendPodSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

router = APIRouter()

@router.post("/assign")
async def assign_employee_to_pod(data: AssignPodSchema, user: User = Depends()):
    service = PodService()
    return service.assign_employee_to_pod(user, data)

@router.get("/{pod_id}/details")
async def get_pod_details(pod_id: int, user: User = Depends()):
    service = PodService()
    return service.get_pod_details(user, pod_id)

@router.post("/{pod_id}/recommend")
async def recommend_employees_for_pod(pod_id: int, data: RecommendPodSchema, user: User = Depends()):
    service = PodService()
    return service.recommend_employees_for_pod(user, pod_id, data)