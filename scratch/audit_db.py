import sqlite3, os, json

print("Checking database files...")
db_files = [f for f in os.listdir('.') if f.endswith('.db') or f.endswith('.sqlite')]
print("DB files:", db_files)

for db in db_files:
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in c.fetchall()]
    print(f"\nTables in {db} ({len(tables)} tables):")
    for t in sorted(tables):
        try:
            c.execute(f"SELECT count(*) FROM `{t}`")
            cnt = c.fetchone()[0]
            print(f"   - {t}: {cnt} rows")
        except Exception as e:
            print(f"   - {t}: error ({e})")
    conn.close()

data_dir = "data"
if os.path.exists(data_dir):
    print("\nFiles in data/:")
    for f in os.listdir(data_dir):
        print("  ", f)

