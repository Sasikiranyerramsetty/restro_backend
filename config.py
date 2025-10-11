from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./restro_backend.db"
    
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

# Create settings instance
settings = Settings()
