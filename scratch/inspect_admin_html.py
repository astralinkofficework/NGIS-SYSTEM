with open('pages/admin/admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'<main|<header|<div class="page"|<section', text)]
for pos in matches[:15]:
    line_no = text[:pos].count('\n') + 1
    print(f"Line {line_no}: {text[pos:pos+70].replace(chr(10), ' ')}")

