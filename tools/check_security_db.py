import sqlite3
con = sqlite3.connect('data/security.sqlite3')
cur = con.cursor()
tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print('Tables:', tables)
for t in tables:
    rows = cur.execute(f"SELECT * FROM {t[0]}").fetchall()
    print(f"Table {t[0]}: {len(rows)} rows")
    if len(rows) > 0 and len(rows) <= 10:
        print("  ", rows)
con.close()
