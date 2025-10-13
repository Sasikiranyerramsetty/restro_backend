from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from app.schemas import UserCreate, UserDocument, UserResponse
from db.mongodb import get_users_collection
from typing import Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class UserService:
    """Service class for user-related MongoDB operations"""
    
    @staticmethod
    async def create_user(user_data: UserCreate, role_id: int = 1) -> Optional[UserResponse]:
        """
        Create a new user in MongoDB
        
        Args:
            user_data: User creation data
            role_id: Role ID to assign to user (default: 1 for regular user)
            
        Returns:
            UserResponse object if created successfully, None otherwise
        """
        try:
            collection = get_users_collection()
            
            # Check if user with email already exists
            existing_user = await collection.find_one({"email": user_data.email})
            if existing_user:
                logger.warning(f"User with email {user_data.email} already exists")
                return None
            
            # Check if user with phone number already exists
            existing_phone = await collection.find_one({"phone_number": user_data.phone_number})
            if existing_phone:
                logger.warning(f"User with phone number {user_data.phone_number} already exists")
                return None
            
            # Create new user document (without password hashing as requested)
            user_doc = {
                "name": user_data.name,
                "email": user_data.email,
                "phone_number": user_data.phone_number,
                "password": user_data.password,  # Storing password as plain text
                "role_id": role_id,
                "status": "active",
                "shift": None,
                "salary": None,
                "address": None,
                "created_at": datetime.utcnow(),
                "updated_at": None
            }
            
            # Insert user document
            result = await collection.insert_one(user_doc)
            
            if result.inserted_id:
                # Fetch the created user
                created_user = await collection.find_one({"_id": result.inserted_id})
                if created_user:
                    logger.info(f"User created successfully with ID: {result.inserted_id}")
                    return UserResponse(**created_user)
            
            return None
            
        except DuplicateKeyError as e:
            logger.error(f"Duplicate key error while creating user: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while creating user: {str(e)}")
            return None
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[UserDocument]:
        """
        Get user by email address
        
        Args:
            email: User's email address
            
        Returns:
            UserDocument object if found, None otherwise
        """
        try:
            collection = get_users_collection()
            user = await collection.find_one({"email": email})
            if user:
                return UserDocument(**user)
            return None
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {str(e)}")
            return None
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[UserResponse]:
        """
        Get user by ID
        
        Args:
            user_id: User's ObjectId as string
            
        Returns:
            UserResponse object if found, None otherwise
        """
        try:
            collection = get_users_collection()
            user = await collection.find_one({"_id": ObjectId(user_id)})
            if user:
                return UserResponse(**user)
            return None
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {str(e)}")
            return None
    
    @staticmethod
    async def get_user_by_phone(phone_number: str) -> Optional[UserDocument]:
        """
        Get user by phone number
        
        Args:
            phone_number: User's phone number
            
        Returns:
            UserDocument object if found, None otherwise
        """
        try:
            collection = get_users_collection()
            user = await collection.find_one({"phone_number": phone_number})
            if user:
                return UserDocument(**user)
            return None
        except Exception as e:
            logger.error(f"Error getting user by phone {phone_number}: {str(e)}")
            return None
    
    @staticmethod
    async def get_all_users(skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """
        Get all users with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of UserResponse objects
        """
        try:
            collection = get_users_collection()
            cursor = collection.find().skip(skip).limit(limit)
            users = []
            
            async for user_doc in cursor:
                # Remove password from response
                user_doc.pop('password', None)
                users.append(UserResponse(**user_doc))
            
            return users
        except Exception as e:
            logger.error(f"Error getting all users: {str(e)}")
            return []
    
    @staticmethod
    async def update_user_status(user_id: str, status: str) -> bool:
        """
        Update user status
        
        Args:
            user_id: User's ObjectId as string
            status: New status
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            collection = get_users_collection()
            result = await collection.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "status": status,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            if result.modified_count > 0:
                logger.info(f"User {user_id} status updated to {status}")
                return True
            else:
                logger.warning(f"User with ID {user_id} not found or not updated")
                return False
            
        except Exception as e:
            logger.error(f"Error updating user status: {str(e)}")
            return False
    
    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[UserResponse]:
        """
        Authenticate user with email and password (for login)
        
        Args:
            email: User's email
            password: User's password (plain text)
            
        Returns:
            UserResponse object if authentication successful, None otherwise
        """
        try:
            collection = get_users_collection()
            user = await collection.find_one({
                "email": email,
                "password": password  # Direct comparison since no hashing
            })
            
            if user:
                # Remove password from response
                user.pop('password', None)
                return UserResponse(**user)
            
            return None
            
        except Exception as e:
            logger.error(f"Error authenticating user: {str(e)}")
            return None
