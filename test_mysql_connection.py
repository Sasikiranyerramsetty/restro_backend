#!/usr/bin/env python3
"""
Test different MySQL connection options
"""

import pymysql
from sqlalchemy import create_engine

def test_connection_options():
    """Test different MySQL connection configurations"""
    
    # Common connection options to try
    connection_options = [
        {
            "name": "Root with no password",
            "url": "mysql+pymysql://root@localhost:3306/restaurant_app"
        },
        {
            "name": "Root with password 'root'",
            "url": "mysql+pymysql://root:root@localhost:3306/restaurant_app"
        },
        {
            "name": "Root with password 'password'",
            "url": "mysql+pymysql://root:password@localhost:3306/restaurant_app"
        },
        {
            "name": "Root with password '123456'",
            "url": "mysql+pymysql://root:123456@localhost:3306/restaurant_app"
        }
    ]
    
    print("Testing MySQL connection options...")
    print("=" * 50)
    
    for option in connection_options:
        print(f"\nTesting: {option['name']}")
        try:
            engine = create_engine(option['url'])
            with engine.connect() as connection:
                result = connection.execute("SELECT 1")
                print(f"✅ SUCCESS: {option['name']}")
                print(f"   Connection string: {option['url']}")
                return option['url']
        except Exception as e:
            print(f"❌ Failed: {str(e)[:100]}...")
    
    print("\n" + "=" * 50)
    print("None of the common options worked.")
    print("Please provide your MySQL root password manually.")
    return None

if __name__ == "__main__":
    working_url = test_connection_options()
    if working_url:
        print(f"\n🎉 Working connection found!")
        print(f"Update your .env file with:")
        print(f"DATABASE_URL={working_url}")
