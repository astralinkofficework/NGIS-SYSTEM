with open('pages/admin/admin-timetables.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(100, len(lines)):
    print(f'{i+1}: {lines[i]}', end='')

