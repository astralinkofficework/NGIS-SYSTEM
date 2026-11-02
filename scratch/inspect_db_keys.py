with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
db_section = text[text.find('DB = {'):text.find('\n# ──')]
keys = re.findall(r"^\s*'([a-zA-Z_0-9]+)':", db_section, re.MULTILINE)
print('DB keys:', keys)

