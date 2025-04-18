from pydantic import BaseModel

class ApplyLeaveSchema(BaseModel):
    start_date: str
    end_date: str
    reason: str

class LeaveStatusSchema(BaseModel):
    leave_id: int
    status: str