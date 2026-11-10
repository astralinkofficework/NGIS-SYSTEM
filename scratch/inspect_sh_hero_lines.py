with open('pages/student/css/hero.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in [685, 686, 687, 688, 689, 690, 1335, 1336, 1337, 1338, 1339]:
    if i < len(lines):
        print(f'{i+1}: {lines[i].strip()}'.encode('ascii', 'replace').decode('ascii'))

