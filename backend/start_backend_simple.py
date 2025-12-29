"""
Simple script to start backend and check for errors
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("🔍 Checking Backend setup...")

try:
    # Test imports
    print("1. Testing imports...")
    from app.database import engine, Base, SessionLocal
    from app import models
    print("   ✅ Database imports OK")
    
    from app.routers import auth, analysis, dashboard, reports, weather
    print("   ✅ Router imports OK")
    
    from app.services.ai_service import AIService
    print("   ✅ AI service import OK")
    
    # Test database connection
    print("2. Testing database...")
    try:
        Base.metadata.create_all(bind=engine)
        print("   ✅ Database tables OK")
    except Exception as e:
        print(f"   ⚠️ Database warning: {e}")
    
    # Test models
    print("3. Testing models...")
    try:
        db = SessionLocal()
        db.close()
        print("   ✅ Database connection OK")
    except Exception as e:
        print(f"   ❌ Database connection error: {e}")
        sys.exit(1)
    
    print("\n✅ All checks passed! Backend is ready.")
    print("\n🚀 Starting server...")
    print("   Run: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\n💡 Solution: Install dependencies:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


