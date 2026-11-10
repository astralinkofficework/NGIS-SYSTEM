import sqlite3, os

db_path = ".data/academic.sqlite3"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in c.fetchall()]
    print(f"Tables in {db_path} ({len(tables)} tables):")
    for t in sorted(tables):
        c.execute(f"SELECT count(*) FROM `{t}`")
        cnt = c.fetchone()[0]
        print(f"   - {t}: {cnt} rows")
    conn.close()
else:
    print(f"{db_path} not found")

