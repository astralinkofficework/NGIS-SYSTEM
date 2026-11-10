with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
db_start = text.find('DB = {')
if db_start != -1:
    print(text[db_start:db_start+1500])
