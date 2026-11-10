with open('pages/admin/admin.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(''.join(lines[-40:]))

