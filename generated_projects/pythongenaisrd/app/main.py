from fastapi import FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from typing import List
import jwt
from datetime import datetime, timedelta

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
    role = Column(Enum('manager', 'employee', name='user_role'), nullable=False)

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

# Define the authentication scheme
security = HTTPBearer()

# Define the token secret key
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define the login and registration endpoints
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/api/auth/login", response_model=Token)
async def login_for_access_token(email: str, password: str):
    db = next(get_db())
    user = db.query(User).filter(User.email == email).first()
    if not user or user.password != password:
        return {"access_token": "", "token_type": "bearer"}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Define the authentication dependency
async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    db = next(get_db())
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

# Define the dashboard endpoint
@app.get("/api/dashboard/tiles")
async def get_dashboard_tiles(current_user: User = Depends(get_current_user)):
    return {"message": "Hello, World!"}

# Define the leave management endpoints
@app.post("/api/lms/leaves/apply")
async def apply_for_leave(start_date: str, end_date: str, reason: str, current_user: User = Depends(get_current_user)):
    db = next(get_db())
    leave = Leave(user_id=current_user.id, start_date=start_date, end_date=end_date, reason=reason, status="pending")
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return {"id": leave.id}

@app.get("/api/lms/leaves/status")
async def get_leave_status(current_user: User = Depends(get_current_user)):
    db = next(get_db())
    leaves = db.query(Leave).filter(Leave.user_id == current_user.id).all()
    return [{"id": leave.id, "status": leave.status} for leave in leaves]

@app.patch("/api/lms/leaves/{leave_id}/approve")
async def approve_leave(leave_id: int, status: str, current_user: User = Depends(get_current_user)):
    db = next(get_db())
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if leave:
        leave.status = status
        db.commit()
        db.refresh(leave)
        return {"id": leave.id}
    return {"error": "Leave not found"}

# Define the pod management endpoints
@app.post("/api/pods/assign")
async def assign_employee_to_pod(pod_id: int, employee_id: int, current_user: User = Depends(get_current_user)):
    db = next(get_db())
    pod = db.query(Pod).filter(Pod.id == pod_id).first()
    employee = db.query(User).filter(User.id == employee_id).first()
    if pod and employee:
        pod_member = PodMember(pod_id=pod_id, user_id=employee_id)
        db.add(pod_member)
        db.commit()
        db.refresh(pod_member)
        return {"id": pod_member.id}
    return {"error": "Pod or employee not found"}

@app.get("/api/pods/{pod_id}/details")
async def get_pod_details(pod_id: int, current_user: User = Depends(get_current_user)):
    db = next(get_db())
    pod = db.query(Pod).filter(Pod.id == pod_id).first()
    if pod:
        return {"id": pod.id, "name": pod.name}
    return {"error": "Pod not found"}

@app.post("/api/pods/{pod_id}/recommend")
async def recommend_employee_for_pod(pod_id: int, recommended_user_id: int, current_user: User = Depends(get_current_user)):
    db = next(get_db())
    pod = db.query(Pod).filter(Pod.id == pod_id).first()
    recommended_user = db.query(User).filter(User.id == recommended_user_id).first()
    if pod and recommended_user:
        # Add logic to recommend employee for pod
        return {"id": pod.id}
    return {"error": "Pod or employee not found"}

# Define the authentication endpoint
@app.get("/api/auth/user")
async def get_current_user_details(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}