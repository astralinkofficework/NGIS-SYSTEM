with open('test_principal_e2e.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[60:130]):
    print(f"{i+61}: {line.strip()}")

