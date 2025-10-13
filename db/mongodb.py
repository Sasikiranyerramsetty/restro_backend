from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import logging
from typing import Optional
from config import settings

logger = logging.getLogger(__name__)

class MongoDB:
    """MongoDB connection manager"""
    
    client: Optional[AsyncIOMotorClient] = None
    database = None

# MongoDB connection string from config
MONGODB_URL = settings.MONGODB_URL
DATABASE_NAME = settings.MONGODB_DATABASE

async def connect_to_mongo():
    """Create database connection"""
    try:
        MongoDB.client = AsyncIOMotorClient(MONGODB_URL)
        MongoDB.database = MongoDB.client[DATABASE_NAME]
        
        # Test the connection
        await MongoDB.client.admin.command('ping')
        logger.info(f"Connected to MongoDB database: {DATABASE_NAME}")
        
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error connecting to MongoDB: {str(e)}")
        raise e

async def close_mongo_connection():
    """Close database connection"""
    if MongoDB.client:
        MongoDB.client.close()
        logger.info("Disconnected from MongoDB")

def get_database():
    """Get database instance"""
    return MongoDB.database

def get_users_collection():
    """Get users collection"""
    return MongoDB.database.users
