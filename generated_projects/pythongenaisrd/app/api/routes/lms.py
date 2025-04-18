from fastapi import APIRouter, Depends
from app.services.lms import apply_leave, get_leave_status, approve_leave
from app.schemas.lms import LeaveApply, LeaveStatus
from app.dependencies import get_db_session

router = APIRouter()

@router.post("/apply")
async def apply_for_leave(leave: LeaveApply, db_session=Depends(get_db_session)):
    return apply_leave(leave, db_session)

@router.get("/status")
async def get_leave_status(db_session=Depends(get_db_session)):
    return get_leave_status(db_session)

@router.patch("/{leave_id}/approve")
async def approve_leave_request(leave_id: int, status: LeaveStatus, db_session=Depends(get_db_session)):
    return approve_leave(leave_id, status, db_session)