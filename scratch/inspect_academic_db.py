import sqlite3, io

conn = sqlite3.connect('.data/academic.sqlite3')
conn.row_factory = sqlite3.Row
out = io.open('scratch/db_report.txt', 'w', encoding='utf-8')
tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
out.write(f'TABLES: {tables}\n\n')
for t in tables:
    try:
        n = conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
        out.write(f'{t}: {n} rows\n')
    except Exception as e:
        out.write(f'{t}: ERR {e}\n')

out.write('\n--- grades workflow distribution ---\n')
try:
    for r in conn.execute("SELECT workflow, COUNT(*) c FROM grades GROUP BY workflow"):
        out.write(f"{r['workflow']}: {r['c']}\n")
except Exception as e:
    out.write(f'ERR {e}\n')

out.write('\n--- distinct students in enrollments ---\n')
try:
    out.write(str(conn.execute("SELECT COUNT(DISTINCT student_id) FROM enrollments").fetchone()[0]) + '\n')
    out.write('distinct teachers: ' + str(conn.execute("SELECT COUNT(DISTINCT teacher_id) FROM teacher_assignments").fetchone()[0]) + '\n')
    out.write('classes: ' + str(conn.execute("SELECT COUNT(*) FROM classes").fetchone()[0]) + '\n')
except Exception as e:
    out.write(f'ERR {e}\n')

out.write('\n--- sample students table? ---\n')
if 'students' in tables:
    for r in conn.execute('SELECT * FROM students LIMIT 3'):
        out.write(str(dict(r)) + '\n')
out.write('\n--- audit_events sample ---\n')
if 'audit_events' in tables:
    for r in conn.execute('SELECT * FROM audit_events ORDER BY id DESC LIMIT 5'):
        out.write(str(dict(r)) + '\n')
out.close()
print('written')
