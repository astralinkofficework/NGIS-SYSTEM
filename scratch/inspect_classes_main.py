with open('pages/principal/principal-classes.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(100, 140):
    print(f'{i+1}: {lines[i]}', end='')

