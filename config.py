from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # MongoDB Configuration
    MONGODB_URL: str = "mongodb+srv://Jagadish:Ammananna@cluster0.6evyrdj.mongodb.net/"
    MONGODB_DATABASE: str = "users_db"
    
    # Application Configuration
    APP_NAME: str = "Restro Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

# Create settings instance
settings = Settings()
