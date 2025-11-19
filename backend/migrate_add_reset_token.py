"""
Migration script to add reset_token and reset_token_expires columns to users table
Run this script once to update your existing database
"""
import sqlite3
import os

# Database path
db_path = os.path.join(os.path.dirname(__file__), 'smartfarm.db')

if not os.path.exists(db_path):
    print(f"Database file not found at {db_path}")
    print("The database will be created automatically when you start the server.")
    exit(0)

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'reset_token' in columns and 'reset_token_expires' in columns:
        print("[OK] Columns 'reset_token' and 'reset_token_expires' already exist.")
        conn.close()
        exit(0)
    
    # Add reset_token column if it doesn't exist
    if 'reset_token' not in columns:
        print("Adding 'reset_token' column...")
        cursor.execute("ALTER TABLE users ADD COLUMN reset_token TEXT")
        print("[OK] Added 'reset_token' column")
    else:
        print("[OK] 'reset_token' column already exists")
    
    # Add reset_token_expires column if it doesn't exist
    if 'reset_token_expires' not in columns:
        print("Adding 'reset_token_expires' column...")
        cursor.execute("ALTER TABLE users ADD COLUMN reset_token_expires TIMESTAMP")
        print("[OK] Added 'reset_token_expires' column")
    else:
        print("[OK] 'reset_token_expires' column already exists")
    
    # Commit changes
    conn.commit()
    print("\n[OK] Migration completed successfully!")
    print("You can now restart your backend server.")
    
except sqlite3.Error as e:
    print(f"[ERROR] Error during migration: {e}")
    conn.rollback()
    exit(1)
finally:
    conn.close()

