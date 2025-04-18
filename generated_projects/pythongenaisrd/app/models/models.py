from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum('employee', 'manager', name='user_role'), nullable=False)

    leaves = relationship('Leave', backref='user')
    pod_memberships = relationship('PodMember', backref='user')
    leave_approvals = relationship('LeaveApproval', backref='manager')

class Leave(Base):
    __tablename__ = 'leaves'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(Enum('pending', 'approved', 'rejected', name='leave_status'), nullable=False)

    approvals = relationship('LeaveApproval', backref='leave')

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
    role = Column(Enum('lead', 'member', name='pod_role'), nullable=False)

class LeaveApproval(Base):
    __tablename__ = 'leave_approvals'
    id = Column(Integer, primary_key=True)
    leave_id = Column(Integer, ForeignKey('leaves.id'), nullable=False)
    manager_id = Column(Integer, ForeignKey('users.id'), nullable=False)