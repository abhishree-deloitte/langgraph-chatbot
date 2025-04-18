from fastapi import APIRouter, Depends, HTTPException
from app import services
from app.schemas import LeaveCreate, Leave
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/api/lms", tags=["lms"])

@router.post("/leaves/apply")
async def apply_leave(leave: LeaveCreate, db: Session = Depends(), current_user: User = Depends(services.get_current_user)):
    db_leave = services.create_leave(db, leave, current_user.id)
    return db_leave

@router.get("/leaves/status")
async def get_leave_status(db: Session = Depends(), current_user: User = Depends(services.get_current_user)):
    leaves = services.get_leaves(db, current_user.id)
    return leaves

@router.patch("/leaves/{leave_id}/approve")
async def approve_leave(leave_id: int, status: str, db: Session = Depends(), current_user: User = Depends(services.get_current_user)):
    db_leave = services.update_leave(db, leave_id, status)
    return db_leave