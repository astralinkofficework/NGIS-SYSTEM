with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
scripts = re.findall(r'<script.*?</script>', text, re.DOTALL)
print(f'Total script tags: {len(scripts)}')
for s in scripts:
    clean = s.replace('\n', ' ')[:100]
    print(' ', clean.encode('ascii', errors='replace').decode('ascii'))
