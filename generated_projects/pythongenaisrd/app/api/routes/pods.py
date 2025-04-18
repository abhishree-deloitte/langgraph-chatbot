from fastapi import APIRouter, Depends, HTTPException
from app.services.pod_service import PodService
from app.schemas.pod import PodCreate
from sqlalchemy.orm import Session
from app.database import get_db

pods_router = APIRouter()

@pods_router.post("/assign")
def assign_employee_to_pod(pod_id: int, user_id: int, db: Session = Depends(get_db)):
    pod_service = PodService()
    pod_service.assign_employee_to_pod(db, pod_id, user_id)
    return {"message": "Employee assigned to pod successfully"}

@pods_router.get("/{pod_id}/details")
def get_pod_details(pod_id: int, db: Session = Depends(get_db)):
    pod_service = PodService()
    pod = pod_service.get_pod(db, pod_id)
    if not pod:
        raise HTTPException(status_code=404, detail="Pod not found")
    return {"pod": pod}

@pods_router.post("/{pod_id}/recommend")
def recommend_employee_for_pod(pod_id: int, user_id: int, db: Session = Depends(get_db)):
    pod_service = PodService()
    pod = pod_service.get_pod(db, pod_id)
    if not pod:
        raise HTTPException(status_code=404, detail="Pod not found")
    pod_service.assign_employee_to_pod(db, pod_id, user_id)
    return {"message": "Employee recommended for pod successfully"}