import sqlite3

conn = sqlite3.connect("campus_energy.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS energy_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room TEXT,
    temperature INTEGER,
    power INTEGER,
    status TEXT
)
""")


conn.commit()
conn.close()

print("Database and table created successfully.")