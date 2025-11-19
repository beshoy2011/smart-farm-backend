"""
Migration script to add ai_summary_english column to analyses table
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'smartfarm.db')

if not os.path.exists(db_path):
    print(f"Database file not found at {db_path}")
    exit(0)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("PRAGMA table_info(analyses)")
    existing_columns = [column[1] for column in cursor.fetchall()]
    
    if 'ai_summary_english' not in existing_columns:
        print("Adding 'ai_summary_english' column...")
        cursor.execute("ALTER TABLE analyses ADD COLUMN ai_summary_english TEXT")
        print("[OK] Added 'ai_summary_english' column")
    else:
        print("[SKIP] Column 'ai_summary_english' already exists")
    
    conn.commit()
    print("\n[OK] Migration completed successfully!")
except sqlite3.Error as e:
    print(f"\n[ERROR] Error during migration: {e}")
    conn.rollback()
    exit(1)
finally:
    conn.close()

