with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
funcs = re.findall(r'function (render[A-Za-z0-9_]*)\(', text)
print("All render functions:", funcs)

# Find where MODULE is checked or routed
lines = text.split('\n')
for i, line in enumerate(lines):
    if 'MODULE ===' in line or 'switch (MODULE)' in line or 'MODULE ==' in line or 'function render(' in line:
        print(f"Line {i+1}: {line}")

