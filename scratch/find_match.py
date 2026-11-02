with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
match = re.search(r'if not PRINCIPAL_DEMO_MODE:\s*_saved_sr[\s\S]*?DB\[.students.\]\s*=\s*_saved_students', text)
if match:
    print("Found match! Raw:")
    print(repr(match.group(0)))
else:
    print("Not found with regex")

