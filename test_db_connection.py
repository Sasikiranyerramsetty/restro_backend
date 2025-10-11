#!/usr/bin/env python3
"""
Test database connection script
Run this to verify your MySQL connection is working
"""

import sys
from sqlalchemy import create_engine, text
from config import settings

def test_connection():
    """Test database connection"""
    try:
        print(f"Testing connection to: {settings.DATABASE_URL}")
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful!")
            return True
            
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("\nPlease check:")
        print("1. MySQL server is running")
        print("2. Database 'restaurant_app' exists")
        print("3. User credentials are correct")
        print("4. Update DATABASE_URL in .env file if needed")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
