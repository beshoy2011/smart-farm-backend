"""
Quick test script to check if backend is working
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app.database import engine, Base
    from app import models
    
    print("✅ Database imports successful")
    
    # Try to create tables
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/updated")
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    # Test model imports
    try:
        user = models.User
        analysis = models.Analysis
        achievement = models.Achievement
        print("✅ All models imported successfully")
    except Exception as e:
        print(f"❌ Model import error: {e}")
    
    # Test service imports
    try:
        from app.services.achievement_service import AchievementService
        print("✅ AchievementService imported")
    except Exception as e:
        print(f"❌ AchievementService error: {e}")
    
    try:
        from app.services.email_service import EmailService
        print("✅ EmailService imported")
    except Exception as e:
        print(f"❌ EmailService error: {e}")
    
    # Test router imports
    try:
        from app.routers import websocket, achievements, notifications
        print("✅ All routers imported")
    except Exception as e:
        print(f"❌ Router import error: {e}")
    
    print("\n✅ Backend check complete!")
    
except Exception as e:
    print(f"❌ Critical error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


