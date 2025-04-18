from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from app.services.lms import LeaveService
from app.db.models import User
from app.schemas.lms import ApplyLeaveSchema, LeaveStatusSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

router = APIRouter()

@router.post("/leaves/apply")
async def apply_for_leave(data: ApplyLeaveSchema, user: User = Depends()):
    service = LeaveService()
    return service.apply_for_leave(user, data)

@router.get("/leaves/status")
async def retrieve_leave_status(user: User = Depends()):
    service = LeaveService()
    return service.retrieve_leave_status(user)

@router.patch("/{leave_id}/approve")
async def approve_leave(leave_id: int, user: User = Depends()):
    service = LeaveService()
    return service.approve_leave(user, leave_id)