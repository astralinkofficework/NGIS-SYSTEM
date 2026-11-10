with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('--- Admin Timetable Nav ---')
for i in range(110, 125):
    print(f'{i+1}: {repr(lines[i])}')

print('--- Principal Timetable Nav ---')
for i in range(318, 332):
    print(f'{i+1}: {repr(lines[i])}')

