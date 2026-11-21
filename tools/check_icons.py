with open('assets/js/action-icons.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.findall(r'["\']([a-zA-Z0-9_-]+)["\']\s*:\s*["\']<svg', js)
print('Total SVG icons in action-icons.js:', len(matches))
print('Has bell:', 'bell' in matches)
print('Has globe:', 'globe' in matches)
print('Has menu:', 'menu' in matches)
print('Has close:', 'close' in matches)
print('Has check:', 'check' in matches)
print('Sample icons:', matches[:20])
