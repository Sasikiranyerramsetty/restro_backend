from fastapi import APIRouter, HTTPException, status
from app.schemas import UserCreate, UserResponse, UserLogin
from services.users_services import UserService
import logging

# Create router
router = APIRouter()

# Set up logging
logger = logging.getLogger(__name__)

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate):
    """
    Create a new user account in MongoDB
    
    Args:
        user_data: User registration data (name, email, phone_number, password)
        
    Returns:
        UserResponse: Created user information (without password)
        
    Raises:
        HTTPException: If user creation fails
    """
    try:
        logger.info(f"Signup attempt for email: {user_data.email}")
        
        # Create user using the service
        new_user = await UserService.create_user(user_data)
        
        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User creation failed. Email or phone number may already exist."
            )
        
        logger.info(f"User created successfully with ID: {new_user.id}")
        return new_user
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during user creation"
        )

@router.post("/login", response_model=UserResponse)
async def login(login_data: UserLogin):
    """
    Authenticate user login
    
    Args:
        login_data: User login data (email, password)
        
    Returns:
        UserResponse: User information if authentication successful
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        logger.info(f"Login attempt for email: {login_data.email}")
        
        # Authenticate user using the service
        user = await UserService.authenticate_user(login_data.email, login_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        logger.info(f"User authenticated successfully: {user.email}")
        return user
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication"
        )

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """
    Get user by ID
    
    Args:
        user_id: User's MongoDB ObjectId as string
        
    Returns:
        UserResponse: User information
        
    Raises:
        HTTPException: If user not found
    """
    try:
        user = await UserService.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/users", response_model=list[UserResponse])
async def get_users(skip: int = 0, limit: int = 100):
    """
    Get all users with pagination
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of UserResponse objects
    """
    try:
        users = await UserService.get_all_users(skip, limit)
        return users
        
    except Exception as e:
        logger.error(f"Error getting users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.patch("/users/{user_id}/status")
async def update_user_status(user_id: str, status: str):
    """
    Update user status
    
    Args:
        user_id: User's MongoDB ObjectId as string
        status: New status
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If update fails
    """
    try:
        success = await UserService.update_user_status(user_id, status)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or update failed"
            )
        
        return {"message": f"User status updated to {status} successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
