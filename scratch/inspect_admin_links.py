with open('pages/admin/admin.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(3705, 3730):
    if i < len(lines):
        print(f'{i+1}: {lines[i].strip()}'.encode('ascii', 'replace').decode('ascii'))

