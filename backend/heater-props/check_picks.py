# check_picks.py
import sqlite3
   
conn = sqlite3.connect('heater-props-new.db')
cursor = conn.cursor()
   
cursor.execute('SELECT * FROM picks')
picks = cursor.fetchall()
   
print(f"Total picks in database: {len(picks)}")
for pick in picks:
    print(pick)
   
conn.close()