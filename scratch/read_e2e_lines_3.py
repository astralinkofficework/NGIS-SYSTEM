with open('test_principal_e2e.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[130:200]):
    print(f"{i+131}: {line.strip()}")

