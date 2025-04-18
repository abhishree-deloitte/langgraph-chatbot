from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List
from app import models, crud

app = FastAPI()

# Create a database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlalchemy.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define the Leave model
class Leave(BaseModel):
    start_date: str
    end_date: str
    reason: str

# Define the PodAssignment model
class PodAssignment(BaseModel):
    employee_id: int
    pod_id: int

# Define the PodRecommendation model
class PodRecommendation(BaseModel):
    recommended_user_id: int

# Apply for leave
@app.post("/api/lms/leaves/apply", status_code=201)
def apply_leave(leave: Leave, db: SessionLocal = Depends(get_db)):
    db_leave = models.Leave(
        user_id=1,  # Assuming the user ID is 1 for now
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        status="pending"
    )
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return {"message": "Leave applied successfully"}

# Assign employee to pod
@app.post("/api/pods/assign", status_code=201)
def assign_employee_to_pod(pod_assignment: PodAssignment, db: SessionLocal = Depends(get_db)):
    db_pod_member = models.PodMember(
        pod_id=pod_assignment.pod_id,
        user_id=pod_assignment.employee_id,
        role="member"
    )
    db.add(db_pod_member)
    db.commit()
    db.refresh(db_pod_member)
    return {"message": "Employee assigned to pod successfully"}

# Recommend employee for pod
@app.post("/api/pods/{pod_id}/recommend", status_code=201)
def recommend_employee_for_pod(pod_id: int, pod_recommendation: PodRecommendation, db: SessionLocal = Depends(get_db)):
    db_pod_member = models.PodMember(
        pod_id=pod_id,
        user_id=pod_recommendation.recommended_user_id,
        role="recommended"
    )
    db.add(db_pod_member)
    db.commit()
    db.refresh(db_pod_member)
    return {"message": "Employee recommended for pod successfully"}