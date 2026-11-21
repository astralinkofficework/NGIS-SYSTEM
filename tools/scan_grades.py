with open('pages/student/student-grades.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, l in enumerate(lines):
    if any(k in l.lower() for k in ['<main', '</main', 'reportcard', 'breakdown', 'gpa', 'transcript', 'published', 'filter', 'document']):
        print(f"Line {i+1}: {l.strip()[:100]}")
