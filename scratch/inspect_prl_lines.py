with open('pages/principal/principal-timetables.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('Total lines in principal-timetables:', len(lines))
for i in range(120, 240):
    if i < len(lines):
        print(f'{i+1}: {lines[i]}', end='')

