import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from db.database import engine, SessionLocal
from db.models import Base, Role, User
from app.auth import get_password_hash

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def init_roles():
    """Initialize default roles"""
    db = SessionLocal()
    try:
        # Check if roles already exist
        existing_roles = db.query(Role).all()
        if existing_roles:
            print(f"Found {len(existing_roles)} existing roles:")
            for role in existing_roles:
                print(f"  - {role.name}: {role.description}")
            print("Skipping role initialization")
            return
        
        # Create default roles
        roles = [
            Role(name="admin", description="Administrator role with full access"),
            Role(name="employee", description="Employee role with limited access"),
            Role(name="customer", description="Customer role for restaurant customers")
        ]
        
        for role in roles:
            db.add(role)
        
        db.commit()
        print("Default roles created successfully")
        
    except Exception as e:
        print(f"Error creating roles: {e}")
        db.rollback()
    finally:
        db.close()

def create_admin_user():
    """Create default admin user"""
    db = SessionLocal()
    try:
        # Check if admin role exists
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not admin_role:
            print("Admin role not found, please run init_roles() first")
            return
        
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.email == "admin@restro.com").first()
        if existing_admin:
            print("Admin user already exists:")
            print(f"  Email: {existing_admin.email}")
            print(f"  Name: {existing_admin.name}")
            return
        
        # Create admin user
        admin_user = User(
            name="Admin User",
            email="admin@restro.com",
            phone_number="+1234567890",
            password=get_password_hash("admin123"),
            roles_id=admin_role.id
        )
        
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully")
        print("Email: admin@restro.com")
        print("Password: admin123")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

def init_database():
    """Initialize the entire database"""
    print("Initializing database...")
    create_tables()
    init_roles()
    create_admin_user()
    print("Database initialization completed!")

if __name__ == "__main__":
    init_database()
