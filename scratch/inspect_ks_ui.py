import re

with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'function render[A-Za-z0-9_]+', text)
print('Render functions:', matches)

modules = ['builder', 'viewer', 'subjects', 'records', 'wizard']
for mod in modules:
    print(f"\n--- MODULE: {mod} ---")
    pos = text.find(f"'{mod}'")
    if pos == -1:
        pos = text.find(f'"{mod}"')
    if pos != -1:
        print(text[max(0, pos-100):min(len(text), pos+300)])

