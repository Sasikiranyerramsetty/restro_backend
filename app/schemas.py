from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

# Base schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        # Basic phone number validation
        if not v.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError('Phone number must contain only digits, +, -, and spaces')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    roles_id: int
    shift: Optional[str] = None
    salary: Optional[str] = None
    status: Optional[str] = None
    address: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserWithRole(UserResponse):
    role: dict

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None

# Role schemas
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
