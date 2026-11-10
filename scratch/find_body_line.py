with open('pages/admin/admin.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '<body' in l:
        print(f'{i+1}: {l}')

