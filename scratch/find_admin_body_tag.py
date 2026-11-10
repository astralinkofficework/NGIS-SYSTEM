with open('pages/admin/admin.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(100, 200):
    if i < len(lines):
        if '<body' in lines[i] or '<main' in lines[i] or 'id="heroBanner"' in lines[i]:
            print(f'{i+1}: {lines[i]}')

