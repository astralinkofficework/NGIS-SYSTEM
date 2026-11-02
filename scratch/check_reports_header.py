import sys

with open('pages/teacher/teacher-reports.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'Official Academic Reports</h2>' in l:
        for j in range(max(0, i-5), min(len(lines), i+15)):
            sys.stdout.buffer.write((f'{j+1}: {lines[j].rstrip()[:120]}\n').encode('utf-8'))

