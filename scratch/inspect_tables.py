with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
creates = re.findall(r'CREATE TABLE IF NOT EXISTS\s+([a-zA-Z_0-9]+)', text)
print('Academic tables:', creates)

