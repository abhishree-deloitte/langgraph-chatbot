from fastapi import APIRouter, Depends
from app.services.lms import LmsService
from app.schemas.lms import LeaveApplication, LeaveStatus

router = APIRouter(prefix="/leaves", tags=["LMS"])

@router.post("/apply")
async def apply_for_leave(leave: LeaveApplication):
    service = LmsService()
    return service.apply_for_leave(leave)

@router.get("/status")
async def get_leave_status():
    service = LmsService()
    return service.get_leave_status()

@router.patch("/{leave_id}/approve")
async def approve_leave(leave_id: int, status: LeaveStatus):
    service = LmsService()
    return service.approve_leave(leave_id, status)