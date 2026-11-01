with open('pages/teacher/teacher-reports.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(410, min(530, len(lines))):
    print(f"{i+1}: {lines[i].strip()[:100]}")

