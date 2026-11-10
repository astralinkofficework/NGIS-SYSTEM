with open('pages/principal/principal-departments.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '<h1' in l:
        print('=== departments.html H1 area ===')
        for j in range(max(0, i-5), min(len(lines), i+30)):
            print(f'{j+1}: {lines[j]}', end='')
        break

