from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import UserCreate, UserLogin, UserResponse, Token, UserDocument
from app.auth import (
    authenticate_user, 
    create_access_token, 
    get_password_hash,
    get_current_user
)
from services.users_services import UserService
from config import settings

router = APIRouter()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate):
    """
    Customer signup endpoint
    Only allows customers to sign up (role_id = 3)
    """
    # Hash the password before creating user
    hashed_password = get_password_hash(user_data.password)
    
    # Create user data with hashed password
    user_data_with_hash = UserCreate(
        name=user_data.name,
        email=user_data.email,
        phone_number=user_data.phone_number,
        password=hashed_password
    )
    
    # Create new user using the service (role_id = 3 for customers)
    new_user = await UserService.create_user(user_data_with_hash, role_id=3)
    
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or phone number already exists"
        )
    
    return new_user

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """
    User login endpoint
    Returns JWT token for authenticated users
    """
    user = await authenticate_user(user_credentials.email, user_credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Convert UserDocument to UserResponse for response
    user_response = UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        phone_number=user.phone_number,
        role_id=user.role_id,
        shift=user.shift,
        salary=user.salary,
        status=user.status,
        address=user.address,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserDocument = Depends(get_current_user)):
    """
    Get current user information
    """
    # Convert UserDocument to UserResponse for response
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        phone_number=current_user.phone_number,
        role_id=current_user.role_id,
        shift=current_user.shift,
        salary=current_user.salary,
        status=current_user.status,
        address=current_user.address,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user: UserDocument = Depends(get_current_user)):
    """
    Get user profile with role information
    """
    # Convert UserDocument to UserResponse for response
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        phone_number=current_user.phone_number,
        role_id=current_user.role_id,
        shift=current_user.shift,
        salary=current_user.salary,
        status=current_user.status,
        address=current_user.address,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )
