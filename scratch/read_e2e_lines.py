with open('test_principal_e2e.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[:60]):
    print(f"{i+1}: {line.strip()}")

