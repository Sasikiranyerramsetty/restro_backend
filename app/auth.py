from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import settings
from app.schemas import TokenData, UserDocument
from services.users_services import UserService
import hashlib
import secrets

# JWT token security
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    # Extract salt and hash from stored password
    try:
        salt, hash_part = hashed_password.split('$')
        # Hash the plain password with the same salt
        test_hash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return test_hash.hex() == hash_part
    except:
        return False

def get_password_hash(password: str) -> str:
    """Hash a password using PBKDF2"""
    # Generate a random salt
    salt = secrets.token_hex(16)
    # Hash the password with the salt
    hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    # Return salt$hash format
    return f"{salt}${hash_obj.hex()}"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    """Verify JWT token and return token data"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserDocument:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    token_data = verify_token(token, credentials_exception)
    
    user = await UserService.get_user_by_email(token_data.email)
    if user is None:
        raise credentials_exception
    
    return user

async def authenticate_user(email: str, password: str) -> Optional[UserDocument]:
    """Authenticate user with email and password"""
    user = await UserService.get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
