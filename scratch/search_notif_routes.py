with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'@app\.route\([^\)]*notif[^\)]*\)[^:]*:', text)
print('Notification routes in server.py:')
for m in matches:
    print(' ', m)

