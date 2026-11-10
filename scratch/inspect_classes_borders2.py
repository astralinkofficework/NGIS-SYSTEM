with open('pages/principal/principal-classes.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'border-' in l or 'rounded-' in l:
        print(f'{i+1}: {l.strip()[:100]}')
        if i > 250: break

