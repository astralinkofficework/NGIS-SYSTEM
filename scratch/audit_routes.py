import os, re

with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

bps = re.findall(r'register_blueprint.*', text)
print("Blueprints registered:", bps)

routes = re.findall(r'@(?:app|[\w_]+)\.route\([^\)]+\)', text)
print(f"Total routes defined: {len(routes)}")

py_files = [f for f in os.listdir('.') if f.endswith('.py')]
print("Python files in root:", py_files)
