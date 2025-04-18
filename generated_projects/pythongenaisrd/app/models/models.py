from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(Enum('manager', 'employee'))

    leaves = relationship('Leave', backref='user', name='enum_manager_employee_Leave_user')
    pod_memberships = relationship('PodMember', backref='user')

class Leave(Base):
    __tablename__ = 'leaves'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    reason = Column(String)
    status = Column(Enum('pending', 'approved', 'rejected'))

class Pod(Base):, name='enum_pending_approved_rejected')
    __tablename__ = 'pods'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    members = relationship('PodMember', backref='pod')

class PodMember(Base):
    __tablename__ = 'pod_members'
    id = Column(Integer, primary_key=True)
    pod_id = Column(Integer, ForeignKey('pods.id'))
    user_id = Column(Integer, ForeignKey('users.id'))