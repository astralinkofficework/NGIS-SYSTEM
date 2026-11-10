with open('assets/css/design-tokens.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l.lower() for k in ['--font', '--token-font', 'typography system']):
        print(f'{i+1}: {l.strip()}'.encode('ascii', 'replace').decode('ascii'))
