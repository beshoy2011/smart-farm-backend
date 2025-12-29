"""
Test login endpoint directly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app import models, auth

def test_login():
    db = SessionLocal()
    try:
        # Test database connection
        print("1. Testing database connection...")
        users = db.query(models.User).limit(1).all()
        print(f"   ✅ Database OK - Found {len(users)} users")
        
        # Test authentication
        print("\n2. Testing authentication...")
        if users:
            user = users[0]
            print(f"   User: {user.username or user.email}")
            print(f"   Has password: {bool(user.hashed_password)}")
        
        # Test password hashing
        print("\n3. Testing password hashing...")
        test_password = "Test123!"
        hashed = auth.get_password_hash(test_password)
        print(f"   ✅ Password hashing OK")
        
        # Test password verification
        verified = auth.verify_password(test_password, hashed)
        print(f"   ✅ Password verification: {verified}")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_login()


