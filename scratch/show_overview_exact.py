with open('assets/js/school-information.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(250, 310):
    print(f'{i+1}: {repr(lines[i])}')

