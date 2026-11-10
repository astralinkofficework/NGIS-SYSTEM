import re

with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

keywords = ['dept', 'class', 'timetable', 'assign', 'attendance', 'submission', 'principal']

for kw in keywords:
    matches = re.findall(r'@app\.route\([^\)]+' + kw + r'[^\)]*\)', text, re.IGNORECASE)
    print(f"=== Matches for '{kw}': ===")
    for m in set(matches):
        print(" ", m.strip().replace('\n', ' '))

