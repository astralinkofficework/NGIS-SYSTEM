with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<div class="ov-upcoming' in line or '<div class="ov-deadlines' in line:
        print(f"Line {i+1}: {line.strip()}")
        for j in range(i, min(i+40, len(lines))):
            print(f"  {j+1}: {lines[j].strip().encode('ascii', 'ignore').decode()}")

