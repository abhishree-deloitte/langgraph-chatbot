from fastapi import APIRouter, Depends
from app.services.pods import assign_employee_to_pod, get_pod_details, recommend_employee_for_pod
from app.schemas.pods import PodAssign, PodRecommend
from app.dependencies import get_db

router = APIRouter(prefix="/pods")

@router.post("/assign")
def assign_employee_to_pod(pod: PodAssign, db=Depends(get_db)):
    return assign_employee_to_pod(db, pod)

@router.get("/{pod_id}/details")
def get_pod_details(pod_id: int, db=Depends(get_db)):
    return get_pod_details(db, pod_id)

@router.post("/{pod_id}/recommend")
def recommend_employee_for_pod(pod_id: int, pod: PodRecommend, db=Depends(get_db)):
    return recommend_employee_for_pod(db, pod_id, pod)