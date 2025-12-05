import sqlite3

conn = sqlite3.connect('heater-props.db')

with open('app/schema.sql', 'r') as f:
    conn.executescript(f.read())

conn.commit()

# Verify
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('picks', 'pick_history', 'user_stats');")
tables = cursor.fetchall()

print("✓ Tables created in heater-props.db:")
for table in tables:
    print(f"  - {table[0]}")

conn.close()