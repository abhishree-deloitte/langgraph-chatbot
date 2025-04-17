from fastapi import APIRouter, Depends
from app.services.lms import apply_for_leave, get_leave_status, approve_leave
from app.schemas.lms import LeaveApply, LeaveStatus
from app.dependencies import get_db

router = APIRouter(prefix="/leaves")

@router.post("/apply")
def apply_for_leave(leave: LeaveApply, db=Depends(get_db)):
    return apply_for_leave(db, leave)

@router.get("/status")
def get_leave_status(db=Depends(get_db)):
    return get_leave_status(db)

@router.patch("/{leave_id}/approve")
def approve_leave(leave_id: int, status: LeaveStatus, db=Depends(get_db)):
    return approve_leave(db, leave_id, status)