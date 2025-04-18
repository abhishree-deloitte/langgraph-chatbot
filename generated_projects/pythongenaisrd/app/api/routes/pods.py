from fastapi import APIRouter, Depends, HTTPException
from app import services
from app.schemas import PodCreate, PodMemberCreate
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/api/pods", tags=["pods"])

@router.post("/assign")
async def assign_employee_to_pod(pod_member: PodMemberCreate, db: Session = Depends(), current_user: User = Depends(services.get_current_user)):
    db_pod_member = services.create_pod_member(db, pod_member)
    return db_pod_member

@router.get("/{pod_id}/details")
async def get_pod_details(pod_id: int, db: Session = Depends(), current_user: User = Depends(services.get_current_user)):
    pod = services.get_pod(db, pod_id)
    return pod

@router.post("/{pod_id}/recommend")
async def recommend_employee_for_pod(pod_id: int, recommended_user_id: int, db: Session = Depends(), current_user: User = Depends(services.get_current_user)):
    pod_member = PodMemberCreate(pod_id=pod_id, user_id=recommended_user_id)
    db_pod_member = services.create_pod_member(db, pod_member)
    return db_pod_member