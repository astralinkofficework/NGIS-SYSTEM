with open('test_principal_e2e.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'principal-assignments' in l:
        start = max(0, i-2)
        end = min(len(lines), i+3)
        print(f'=== Line {i+1} in test_principal_e2e.py ===')
        for j in range(start, end):
            print(f'{j+1}: {lines[j].strip()}')

