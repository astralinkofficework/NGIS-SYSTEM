with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j, l in enumerate(lines):
    if 'function actorHeader(' in l:
        print(f'actorHeader at {j+1}')
        for k in range(j, min(len(lines), j + 15)):
            print(f'{k+1}: {lines[k].rstrip()[:110]}')
        break
