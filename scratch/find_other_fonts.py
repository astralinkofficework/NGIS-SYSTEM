import glob
import re

files = glob.glob('**/*.html', recursive=True) + glob.glob('assets/css/**/*.css', recursive=True) + glob.glob('pages/**/css/*.css', recursive=True)

other_fonts = ['Roboto', 'Open Sans', 'Outfit', 'Poppins', 'JetBrains Mono', 'Helvetica Neue']

for font in other_fonts:
    matches = []
    for p in files:
        if 'scratch' in p or 'test' in p:
            continue
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        if font.lower() in c.lower():
            matches.append(p)
    print(f'Font "{font}": found in {len(matches)} files')
    for m in matches[:5]:
        print('  ', m)

