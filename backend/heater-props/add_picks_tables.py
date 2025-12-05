# add_picks_tables.py
import sqlite3

# Direct connection to your database file
# Replace 'database.db' with your actual database filename
DATABASE_FILE = 'heater.db'  # or whatever your database is called

print("Adding picks tracking tables...")

# Connect directly
conn = sqlite3.connect(DATABASE_FILE)

# Read and execute schema
with open('app/schema.sql', 'r') as f:
    conn.executescript(f.read())

conn.commit()

# Verify new tables
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('picks', 'pick_history', 'user_stats');")
tables = cursor.fetchall()

print("\n✓ New tables created:")
for table in tables:
    print(f"  - {table[0]}")

conn.close()

print("\nDone! Your existing tables are untouched.")