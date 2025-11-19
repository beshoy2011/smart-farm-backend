"""
Migration script to add advanced features columns to analyses table
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

# List of new columns to add (including all columns from the model)
new_columns = [
    ("water_level_percent", "REAL"),
    ("soil_moisture_percent", "REAL"),
    ("soil_ph", "REAL"),
    ("soil_nitrogen", "REAL"),
    ("soil_phosphorus", "REAL"),
    ("soil_potassium", "REAL"),
    ("disease_probability", "REAL"),
    ("predicted_diseases", "TEXT"),  # JSON stored as TEXT
    ("nutrient_profile", "TEXT"),  # JSON stored as TEXT - MISSING!
    ("nitrogen_level", "REAL"),
    ("phosphorus_level", "REAL"),
    ("potassium_level", "REAL"),
    ("recommended_fertilizer_amount", "REAL"),
    ("fertilizer_type", "TEXT"),
    ("fertilizer_need_percent", "REAL"),
    ("leaf_damage_percent", "REAL"),
    ("growth_stage", "TEXT"),  # JSON stored as TEXT
    ("dryness_factor", "REAL"),
    ("leaf_color_index", "REAL"),
    ("ai_summary_arabic", "TEXT"),
    ("explainability", "TEXT"),  # JSON stored as TEXT
    ("analysis_metadata", "TEXT"),  # JSON stored as TEXT
    ("weekly_recommendations", "TEXT"),  # JSON stored as TEXT
    ("irrigation_needed", "BOOLEAN"),
    ("irrigation_duration_minutes", "REAL"),
    ("warnings", "TEXT"),  # JSON stored as TEXT
    ("temperature_alert", "BOOLEAN"),
    ("water_alert", "BOOLEAN"),
    ("fertilizer_alert", "BOOLEAN"),
    ("disease_alert", "BOOLEAN"),
    ("estimated_water_cost", "REAL"),
    ("estimated_fertilizer_cost", "REAL"),
    ("cost_savings", "REAL"),
    ("efficiency_percentage", "REAL"),
]

try:
    # Check existing columns
    cursor.execute("PRAGMA table_info(analyses)")
    existing_columns = [column[1] for column in cursor.fetchall()]
    
    print(f"Found {len(existing_columns)} existing columns in analyses table")
    
    # Add missing columns
    added_count = 0
    for column_name, column_type in new_columns:
        if column_name not in existing_columns:
            print(f"Adding '{column_name}' column...")
            # SQLite doesn't support adding NOT NULL columns to existing tables easily
            # So we'll add them as nullable
            cursor.execute(f"ALTER TABLE analyses ADD COLUMN {column_name} {column_type}")
            print(f"[OK] Added '{column_name}' column")
            added_count += 1
        else:
            print(f"[SKIP] Column '{column_name}' already exists")
    
    # Create new tables if they don't exist
    print("\nChecking for new tables...")
    
    # Check if plant_comparisons table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='plant_comparisons'")
    if not cursor.fetchone():
        print("Creating 'plant_comparisons' table...")
        cursor.execute("""
            CREATE TABLE plant_comparisons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                analysis_id_1 INTEGER,
                analysis_id_2 INTEGER,
                comparison_results TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (analysis_id_1) REFERENCES analyses(id),
                FOREIGN KEY (analysis_id_2) REFERENCES analyses(id)
            )
        """)
        print("[OK] Created 'plant_comparisons' table")
    else:
        print("[SKIP] 'plant_comparisons' table already exists")
    
    # Check if ai_accuracy_tracking table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ai_accuracy_tracking'")
    if not cursor.fetchone():
        print("Creating 'ai_accuracy_tracking' table...")
        cursor.execute("""
            CREATE TABLE ai_accuracy_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                analysis_id INTEGER,
                prediction_type TEXT NOT NULL,
                predicted_value REAL,
                actual_value REAL,
                accuracy_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (analysis_id) REFERENCES analyses(id)
            )
        """)
        print("[OK] Created 'ai_accuracy_tracking' table")
    else:
        print("[SKIP] 'ai_accuracy_tracking' table already exists")
    
    # Check if weekly_recommendations table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weekly_recommendations'")
    if not cursor.fetchone():
        print("Creating 'weekly_recommendations' table...")
        cursor.execute("""
            CREATE TABLE weekly_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                week_start_date TIMESTAMP NOT NULL,
                recommendations TEXT,
                plant_ids TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        print("[OK] Created 'weekly_recommendations' table")
    else:
        print("[SKIP] 'weekly_recommendations' table already exists")
    
    # Commit changes
    conn.commit()
    
    print(f"\n{'='*60}")
    print(f"[OK] Migration completed successfully!")
    print(f"Added {added_count} new columns to analyses table")
    print(f"{'='*60}")
    print("You can now restart your backend server.")
    
except sqlite3.Error as e:
    print(f"\n[ERROR] Error during migration: {e}")
    conn.rollback()
    exit(1)
finally:
    conn.close()

