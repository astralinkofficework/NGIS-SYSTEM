with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r"'serviceRequests'\s*:\s*\[", text)]
print("Matches found:", len(matches))
for idx in matches:
    print(text[idx:idx+400])
    print("="*40)

