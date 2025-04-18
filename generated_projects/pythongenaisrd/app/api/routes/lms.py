from fastapi import APIRouter, Depends, HTTPException
from app.services.leave_service import LeaveService
from app.schemas.leave import LeaveCreate
from sqlalchemy.orm import Session
from app.database import get_db

lms_router = APIRouter()

@lms_router.post("/leaves/apply")
def apply_for_leave(leave: LeaveCreate, db: Session = Depends(get_db)):
    leave_service = LeaveService()
    leave_service.create_leave(db, leave, 1)
    return {"message": "Leave applied successfully"}

@lms_router.get("/leaves/status")
def get_leave_status(db: Session = Depends(get_db)):
    leave_service = LeaveService()
    leaves = leave_service.get_leaves(db, 1)
    return {"leaves": leaves}

@lms_router.patch("/leaves/{leave_id}/approve")
def approve_leave(leave_id: int, status: str, db: Session = Depends(get_db)):
    leave_service = LeaveService()
    leave = leave_service.get_leave(db, leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    leave_service.update_leave(db, leave_id, status)
    return {"message": "Leave approved successfully"}