from fastapi import APIRouter
from app.database import SessionLocal
from app.database.models import Pod, PodMember
from app.schemas import PodAssign, PodDetails, PodRecommend

router = APIRouter()

@router.post("/assign")
def assign_employee_to_pod(pod_assign: PodAssign):
    db = SessionLocal()
    pod = db.query(Pod).filter(Pod.id == pod_assign.pod_id).first()
    if pod:
        pod_member = PodMember(
            pod_id=pod_assign.pod_id,
            user_id=pod_assign.employee_id,
        )
        db.add(pod_member)
        db.commit()
        return {"message": "Employee assigned to pod successfully"}
    return {"message": "Pod not found"}

@router.get("/{pod_id}/details")
def get_pod_details(pod_id: int):
    db = SessionLocal()
    pod = db.query(Pod).filter(Pod.id == pod_id).first()
    if pod:
        pod_details = PodDetails(
            id=pod.id,
            name=pod.name,
        )
        return pod_details
    return {"message": "Pod not found"}

@router.post("/{pod_id}/recommend")
def recommend_employee_for_pod(pod_id: int, pod_recommend: PodRecommend):
    db = SessionLocal()
    pod = db.query(Pod).filter(Pod.id == pod_id).first()
    if pod:
        pod_member = PodMember(
            pod_id=pod_id,
            user_id=pod_recommend.recommended_user_id,
        )
        db.add(pod_member)
        db.commit()
        return {"message": "Employee recommended for pod successfully"}
    return {"message": "Pod not found"}