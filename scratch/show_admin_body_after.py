with open('pages/admin/admin.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(883, min(920, len(lines))):
    print(f'{i+1}: {lines[i]}', end='')

