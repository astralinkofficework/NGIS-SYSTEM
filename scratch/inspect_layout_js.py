with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Mentions principal:", "principal" in text.lower())
# Find where sidebar is created
for m in re.finditer(r'function\s+([a-zA-Z0-9_]+)\s*\([^)]*\)', text):
    fn = m.group(1)
    if 'sidebar' in fn.lower() or 'init' in fn.lower() or 'nav' in fn.lower():
        print("Function:", fn)

# Find if layout.js generates sidebar markup
if 'document.createElement' in text or 'sidebarHTML' in text or '<aside' in text:
    print("layout.js contains HTML generation for sidebar!")

