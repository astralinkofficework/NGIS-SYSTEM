with open(r'pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'dash-overlap' in l and '<div' in l:
        print(f"dash-overlap starts at L{i+1}")
        for j in range(i, min(len(lines), i+80)):
            print(f"L{j+1}: {lines[j].strip()[:90]}")
        break

