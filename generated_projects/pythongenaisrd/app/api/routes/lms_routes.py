from fastapi import APIRouter, Depends
from app.services.lms_service import LMSservice
from app.schemas.lms import LeaveApplication, LeaveStatus, LeaveApproval

router = APIRouter()

@router.post("/leaves/apply")
async def apply_for_leave(leave_application: LeaveApplication, lms_service: LMSservice = Depends()):
    return await lms_service.apply_for_leave(leave_application)

@router.get("/leaves/status")
async def get_leave_status(lms_service: LMSservice = Depends()):
    return await lms_service.get_leave_status()

@router.patch("/leaves/{leave_id}/approve")
async def approve_leave(leave_id: int, leave_approval: LeaveApproval, lms_service: LMSservice = Depends()):
    return await lms_service.approve_leave(leave_id, leave_approval)