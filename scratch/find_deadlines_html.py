with open(r'pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(320, 440):
    print(f"L{j+1}: {lines[j].strip()[:90]}")

