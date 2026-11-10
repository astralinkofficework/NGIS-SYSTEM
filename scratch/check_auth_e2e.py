with open('test_principal_e2e.py', 'r', encoding='utf-8') as f:
    text = f.read()

for line in text.splitlines():
    if 'auth' in line.lower() or 'token' in line.lower() or 'roster' in line.lower() or 'login' in line.lower():
        print(line)

