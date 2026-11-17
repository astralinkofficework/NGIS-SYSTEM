import os, re

modal_re = re.compile(r'data-open-(drawer|modal)=[\'"]([^\'"]*)[\'"]')

for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['node_modules', '.git', '.gemini', 'brain', 'tools']):
        continue
    for file in files:
        if file.endswith('.html') or file.endswith('.js'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_no, line in enumerate(f, 1):
                    for m in modal_re.finditer(line):
                        val = m.group(2)
                        if not val or val.startswith('#') or ' ' in val:
                            print(f"{path}:{line_no}: data-open-{m.group(1)}='{val}'")
