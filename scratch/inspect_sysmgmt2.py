with open('system_management_api.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
print('\n'.join(lines[100:220]))

