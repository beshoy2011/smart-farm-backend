"""
Migration script to add fcm_token column to users table
"""

from app.database import engine
from sqlalchemy import text

def migrate():
    """Add fcm_token column to users table"""
    try:
        with engine.connect() as conn:
            # Check if column already exists
            result = conn.execute(text("PRAGMA table_info(users)"))
            columns = [row[1] for row in result]
            
            if 'fcm_token' not in columns:
                print("Adding fcm_token column to users table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN fcm_token VARCHAR"))
                conn.commit()
                print("Successfully added fcm_token column")
            else:
                print("fcm_token column already exists")
    except Exception as e:
        print(f"Error during migration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    migrate()

