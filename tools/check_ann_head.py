with open('pages/shared/announcements.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(min(35, len(lines))):
    print(f'{i+1}: {lines[i]}', end='')
