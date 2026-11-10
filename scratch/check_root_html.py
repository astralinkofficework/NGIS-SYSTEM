import os

root_files = []
for f in os.listdir('.'):
    if f.endswith('.html'):
        root_files.append(f)

print(f"Root HTML files: {root_files}")
for rf in root_files:
    with open(rf, 'r', encoding='utf-8') as fp:
        txt = fp.read()
    has_header = '<header' in txt
    print(f"  {rf}: has_header={has_header}")

