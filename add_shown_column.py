import sqlite3

conn = sqlite3.connect("companion.db")
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE user_alerts ADD COLUMN shown INTEGER DEFAULT 0")
    print("✅ 'shown' column added successfully")
except Exception as e:
    print("⚠️ Maybe already exists:", e)

conn.commit()
conn.close()