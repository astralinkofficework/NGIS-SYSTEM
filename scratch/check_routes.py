import re

with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

routes = re.findall(r'@app\.route\([\'"]([^\'"]+)', content)
print(f"Total routes: {len(routes)}")
for r in routes:
    if any(k in r for k in ['grade', 'attend', 'academic', 'report', 'class', 'student', 'teacher', 'admin']):
        print(r)
