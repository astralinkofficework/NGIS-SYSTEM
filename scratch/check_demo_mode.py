with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'SERVICE_REQUESTS_FILE' in l or 'PRINCIPAL_DEMO_MODE' in l:
        print(f"{i+1}: {l.strip()}")

