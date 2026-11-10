import sqlite3

conn = sqlite3.connect(".data/academic.sqlite3")
c = conn.cursor()
c.execute("SELECT id, name, is_current, created_at FROM academic_years")
rows = c.fetchall()
print("Academic years in sqlite:", rows)
conn.close()

