with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j, l in enumerate(lines):
    if 'function shell(' in l:
        print(f'shell at {j+1}')
        for k in range(j, min(len(lines), j + 40)):
            print(f'{k+1}: {lines[k].rstrip()[:110]}')
        break
