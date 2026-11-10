with open('assets/css/hero.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1675, 1700):
    print(f'{i+1}: {lines[i].strip()}'.encode('ascii', 'replace').decode('ascii'))

