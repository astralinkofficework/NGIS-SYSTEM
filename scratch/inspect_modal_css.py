with open('assets/css/khmer-suite.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '.ks-modal' in l:
        print(f'{i+1}: {l.strip()}')
        for j in range(i+1, min(len(lines), i+25)):
            print(f'{j+1}: {lines[j]}', end='')
        break

