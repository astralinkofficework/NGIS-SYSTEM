with open('pages/principal/principal-reports.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '<h1' in l:
        print('=== reports.html H1 area ===')
        for j in range(max(0, i-5), min(len(lines), i+30)):
            print(f'{j+1}: {lines[j]}', end='')
        break

