import glob
import re

files = glob.glob('**/*.html', recursive=True) + glob.glob('assets/css/**/*.css', recursive=True) + glob.glob('pages/**/css/*.css', recursive=True)

inter_files = []
for p in files:
    if 'scratch' in p or 'test' in p:
        continue
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'Inter' in c:
        inter_files.append(p)

print(f'{len(inter_files)} files contain "Inter":')
for p in inter_files:
    print(' ', p)

