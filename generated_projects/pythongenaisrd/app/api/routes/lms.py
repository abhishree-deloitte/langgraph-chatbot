from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import SessionLocal
from app.database.models import Leave, User
from app.schemas import LeaveApply, LeaveStatus, LeaveApprove
from app.services import lms_service

router = APIRouter()

@router.post("/leaves/apply")
def apply_for_leave(leave: LeaveApply):
    db = SessionLocal()
    user = db.query(User).filter(User.id == leave.user_id).first()
    if user:
        leave_obj = Leave(
            user_id=leave.user_id,
            start_date=leave.start_date,
            end_date=leave.end_date,
            reason=leave.reason,
        )
        db.add(leave_obj)
        db.commit()
        return {"message": "Leave applied successfully"}
    return {"message": "User not found"}

@router.get("/leaves/status")
def get_leave_status():
    db = SessionLocal()
    leaves = db.query(Leave).all()
    leave_status = []
    for leave in leaves:
        status = LeaveStatus(
            id=leave.id,
            user_id=leave.user_id,
            start_date=leave.start_date,
            end_date=leave.end_date,
            reason=leave.reason,
            status=leave.status,
        )
        leave_status.append(status)
    return leave_status

@router.patch("/leaves/{leave_id}/approve")
def approve_leave(leave_id: int, leave: LeaveApprove):
    db = SessionLocal()
    leave_obj = db.query(Leave).filter(Leave.id == leave_id).first()
    if leave_obj:
        leave_obj.status = leave.status
        db.commit()
        return {"message": "Leave approved/rejected successfully"}
    return {"message": "Leave not found"}