
import sqlite3

connection = sqlite3.connect("jobshield.db")
cursor = connection.cursor()

cursor.execute("""
    SELECT
        s.id,
        u.username,
        s.user_id,
        s.risk_level
    FROM scan_history AS s
    LEFT JOIN users AS u ON s.user_id = u.id
    ORDER BY s.id DESC
""")

print("ALL SCAN RECORDS:")
for row in cursor.fetchall():
    print(row)

connection.close()
