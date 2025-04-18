from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from typing import List
from datetime import datetime, timedelta
import os

# Replace the old import with the correct one
from jose.backends import RSAKeyStore

# Define the database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlalchemy.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define the models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum('employee', 'manager', name='user_role'), nullable=False)

    leaves = relationship('Leave', backref='user')
    pod_memberships = relationship('PodMember', backref='user')

class Leave(Base):
    __tablename__ = 'leaves'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(Enum('pending', 'approved', 'rejected', name='leave_status'), nullable=False)

class Pod(Base):
    __tablename__ = 'pods'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    members = relationship('PodMember', backref='pod')

class PodMember(Base):
    __tablename__ = 'pod_members'
    id = Column(Integer, primary_key=True)
    pod_id = Column(Integer, ForeignKey('pods.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Define the FastAPI app
app = FastAPI()

# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Define the token settings
SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define the token verification function
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Define the login endpoint
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Replace the old import with the correct one
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")
    db = SessionLocal()
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": user.email, "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Define the dashboard endpoint
@app.get("/api/dashboard/tiles")
async def get_dashboard_tiles(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    return {"message": "Hello, World!"}

# Define the leave application endpoint
@app.post("/api/lms/leaves/apply")
async def apply_for_leave(data: dict, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    db = SessionLocal()
    user = db.query(User).filter(User.email == payload["sub"]).first()
    leave = Leave(user_id=user.id, start_date=data["start_date"], end_date=data["end_date"], reason=data["reason"], status="pending")
    db.add(leave)
    db.commit()
    db.close()
    return {"message": "Leave applied successfully"}

# Define the leave status endpoint
@app.get("/api/lms/leaves/status")
async def get_leave_status(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    db = SessionLocal()
    user = db.query(User).filter(User.email == payload["sub"]).first()
    leaves = db.query(Leave).filter(Leave.user_id == user.id).all()
    return [{"id": leave.id, "start_date": leave.start_date, "end_date": leave.end_date, "reason": leave.reason, "status": leave.status} for leave in leaves]

# Define the leave approval endpoint
@app.patch("/api/lms/leaves/{leave_id}/approve")
async def approve_leave(leave_id: int, data: dict, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    db = SessionLocal()
    user = db.query(User).filter(User.email == payload["sub"]).first()
    if user.role != "manager":
        raise HTTPException(
            status_code=401,
            detail="Only managers can approve leaves",
            headers={"WWW-Authenticate": "Bearer"},
        )
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    leave.status = data["status"]
    db.commit()
    db.close()
    return {"message": "Leave approved successfully"}

# Define the pod assignment endpoint
@app.post("/api/pods/assign")
async def assign_employee_to_pod(data: dict, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    db = SessionLocal()
    user = db.query(User).filter(User.email == payload["sub"]).first()
    if user.role != "manager":
        raise HTTPException(
            status_code=401,
            detail="Only managers can assign employees to pods",
            headers={"WWW-Authenticate": "Bearer"},
        )
    pod = db.query(Pod).filter(Pod.id == data["pod_id"]).first()
    if not pod:
        raise HTTPException(
            status_code=404,
            detail="Pod not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    employee = db.query(User).filter(User.id == data["employee_id"]).first()
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    pod_member = PodMember(pod_id=pod.id, user_id=employee.id)
    db.add(pod_member)
    db.commit()
    db.close()
    return {"message": "Employee assigned to pod successfully"}

# Define the pod details endpoint
@app.get("/api/pods/{pod_id}/details")
async def get_pod_details(pod_id: int, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    db = SessionLocal()
    pod = db.query(Pod).filter(Pod.id == pod_id).first()
    if not pod:
        raise HTTPException(
            status_code=404,
            detail="Pod not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    members = db.query(PodMember).filter(PodMember.pod_id == pod.id).all()
    return {"name": pod.name, "members": [member.user_id for member in members]}

# Define the pod recommendation endpoint
@app.post("/api/pods/{pod_id}/recommend")
async def recommend_employee_for_pod(pod_id: int, data: dict, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    db = SessionLocal()
    pod = db.query(Pod).filter(Pod.id == pod_id).first()
    if not pod:
        raise HTTPException(
            status_code=404,
            detail="Pod not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    employee = db.query(User).filter(User.id == data["recommended_user_id"]).first()
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    pod_member = PodMember(pod_id=pod.id, user_id=employee.id)
    db.add(pod_member)
    db.commit()
    db.close()
    return {"message": "Employee recommended for pod successfully"}

# Define the user login endpoint
@app.post("/api/auth/login")
async def login(data: dict):
    db = SessionLocal()
    user = db.query(User).filter(User.email == data["email"]).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.password == data["password"]:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": user.email, "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Define the user details endpoint
@app.get("/api/auth/user")
async def get_user_details(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    db = SessionLocal()
    user = db.query(User).filter(User.email == payload["sub"]).first()
    return {"email": user.email, "role": user.role}