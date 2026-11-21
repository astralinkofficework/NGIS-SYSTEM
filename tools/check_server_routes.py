import re

with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'@app\.route\([\'"](/api/[^\'"]+)', text):
    print(m.group(1))
