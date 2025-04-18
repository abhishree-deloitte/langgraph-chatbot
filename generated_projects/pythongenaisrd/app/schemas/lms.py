from pydantic import BaseModel

class LeaveApply(BaseModel):
    start_date: str
    end_date: str
    reason: str

class LeaveStatus(BaseModel):
    status: str