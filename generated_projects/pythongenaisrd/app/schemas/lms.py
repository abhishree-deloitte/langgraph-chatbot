from pydantic import BaseModel
from datetime import date

class LeaveApplication(BaseModel):
    start_date: date
    end_date: date
    reason: str

class LeaveStatus(BaseModel):
    id: int
    status: str

class LeaveApproval(BaseModel):
    status: str