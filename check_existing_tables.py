#!/usr/bin/env python3
"""
Check existing tables in restaurant_app database
Run this to see what tables already exist before creating new ones
"""

import sys
from sqlalchemy import create_engine, text, inspect
from config import settings

def check_existing_tables():
    """Check what tables already exist in the database"""
    try:
        print(f"Connecting to: {settings.DATABASE_URL}")
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as connection:
            # Check if database exists
            result = connection.execute(text("SHOW DATABASES LIKE 'restaurant_app'"))
            if not result.fetchone():
                print("❌ Database 'restaurant_app' does not exist!")
                return False
            
            print("✅ Database 'restaurant_app' exists!")
            
            # Get list of existing tables
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            
            print(f"\n📋 Existing tables in restaurant_app:")
            if existing_tables:
                for table in existing_tables:
                    print(f"  - {table}")
                    
                    # Show table structure
                    columns = inspector.get_columns(table)
                    print(f"    Columns:")
                    for col in columns:
                        print(f"      - {col['name']} ({col['type']})")
                    print()
            else:
                print("  No tables found.")
            
            # Check if our required tables exist
            required_tables = ['roles', 'users']
            missing_tables = [table for table in required_tables if table not in existing_tables]
            
            if missing_tables:
                print(f"⚠️  Missing required tables: {missing_tables}")
                print("You can create them by running: python db/init_db.py")
            else:
                print("✅ All required tables (roles, users) exist!")
                
                # Check if roles table has data
                if 'roles' in existing_tables:
                    result = connection.execute(text("SELECT COUNT(*) FROM roles"))
                    role_count = result.fetchone()[0]
                    print(f"📊 Roles table has {role_count} records")
                    
                    if role_count > 0:
                        result = connection.execute(text("SELECT name FROM roles"))
                        roles = [row[0] for row in result.fetchall()]
                        print(f"   Available roles: {', '.join(roles)}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

if __name__ == "__main__":
    success = check_existing_tables()
    sys.exit(0 if success else 1)
