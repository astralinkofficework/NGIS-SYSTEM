with open('pages/student/css/overlap.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[400:700], 401):
    if 'border' in l:
        print(f"Line {i}: {l.strip()}")

