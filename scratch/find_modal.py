with open('pages/teacher/teacher-reports.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'modalReportCard' in line and '<' in line and 'style' not in line:
        print(f"Line {i+1}: {line.strip()[:100]}")
        for j in range(i, min(i+100, len(lines))):
            print(f"{j+1}: {lines[j].strip()[:110]}")
        break

