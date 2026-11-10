with open('assets/css/hero.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '30px' in l:
        start = max(0, i-5)
        end = min(len(lines), i+6)
        print(f'=== Line {i+1} in hero.css ===')
        for j in range(start, end):
            print(f'{j+1}: {lines[j].strip()}'.encode('ascii', 'replace').decode('ascii'))

