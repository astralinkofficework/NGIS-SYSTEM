with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(850, min(len(lines), 900)):
    print(f'{j+1}: {lines[j].rstrip()[:110]}')
