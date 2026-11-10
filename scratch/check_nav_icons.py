import re

with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

icons = re.findall(r'icon:\s*["\']([^"\']+)["\']', text)
print('Total icons defined in NAV:', len(icons))
print('Unique icons count:', len(set(icons)))
print('List of unique icons:', sorted(list(set(icons))))

