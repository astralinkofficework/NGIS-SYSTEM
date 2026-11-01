with open('pages/teacher/teacher-reports.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "modalReportCard" in line and ("=" in line or "const" in line or "let" in line or "var" in line):
        print(f"Match at line {i+1}: {line.strip()[:100]}".encode('ascii', errors='replace').decode('ascii'))
        for j in range(max(0, i-4), min(i+25, len(lines))):
            clean = lines[j].strip()[:100].encode('ascii', errors='replace').decode('ascii')
            print(f"  {j+1}: {clean}")
