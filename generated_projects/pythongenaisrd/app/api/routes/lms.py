from fastapi import APIRouter, Depends
from fastapi import HTTPException
from app.services import lms_service
from app.schemas import LeaveApplySchema, LeaveStatusSchema
from app.dependencies import get_db

lms_router = APIRouter(prefix="/api/lms", tags=["LMS"])

@lms_router.post("/leaves/apply")
async def apply_for_leave(leave: LeaveApplySchema, db = Depends(get_db)):
    return lms_service.apply_for_leave(leave, db)

@lms_router.get("/leaves/status")
async def retrieve_leave_status(db = Depends(get_db)):
    return lms_service.retrieve_leave_status(db)

@lms_router.patch("/leaves/{leave_id}/approve")
async def approve_leave(leave_id: int, leave_status: LeaveStatusSchema, db = Depends(get_db)):
    return lms_service.approve_leave(leave_id, leave_status, db)