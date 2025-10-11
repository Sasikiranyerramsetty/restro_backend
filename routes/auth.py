from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import User, Role
from app.schemas import UserCreate, UserLogin, UserResponse, Token
from app.auth import (
    authenticate_user, 
    create_access_token, 
    get_password_hash,
    get_current_user
)
from config import settings

router = APIRouter()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Customer signup endpoint
    Only allows customers to sign up (role_id = 3)
    """
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.phone_number == user_data.phone_number)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or phone number already exists"
        )
    
    # Get customer role (assuming role_id = 3 for customers)
    customer_role = db.query(Role).filter(Role.name == "customer").first()
    if not customer_role:
        # Create customer role if it doesn't exist
        customer_role = Role(name="customer", description="Customer role")
        db.add(customer_role)
        db.commit()
        db.refresh(customer_role)
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        phone_number=user_data.phone_number,
        password=hashed_password,
        roles_id=customer_role.id
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    User login endpoint
    Returns JWT token for authenticated users
    """
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    return current_user

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get user profile with role information
    """
    return current_user
