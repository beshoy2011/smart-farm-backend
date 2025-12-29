"""
Migration script to add achievements table
Run this to update the database schema
"""

from app.database import engine, Base
from app import models

# Create all tables (including new Achievement table)
Base.metadata.create_all(bind=engine)

print("✅ Database migration completed!")
print("✅ Achievement table created successfully!")


