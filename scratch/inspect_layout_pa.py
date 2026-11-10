with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'principal-assignments' in l:
        start = max(0, i-3)
        end = min(len(lines), i+4)
        print(f'=== Line {i+1} in assets/js/layout.js ===')
        for j in range(start, end):
            print(f'{j+1}: {lines[j].strip()}')

