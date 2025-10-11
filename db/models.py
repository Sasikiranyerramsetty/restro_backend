from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with users
    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone_number = Column(String(15), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    roles_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    shift = Column(String(50))
    salary = Column(String(20))  # Changed to String to match existing structure
    status = Column(String(20))
    address = Column(String(500))
    
    # Relationship with role
    role = relationship("Role", back_populates="users")
