with open('pages/shared/design-system-preview.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect sections in content
import re
sections = [m.group(0) for m in re.finditer(r'<section[^>]+id=[\'"][^\'"]+[\'"]', content)]
print('Current sections:')
for s in sections:
    print(' ', s)
