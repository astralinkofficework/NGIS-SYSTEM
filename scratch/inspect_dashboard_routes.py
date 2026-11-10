with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '/api/dashboard/<role>' in line or '/api/student/dashboard' in line or '/api/announcements' in line:
        print(f"=== Match at line {i+1} ===")
        print("".join(lines[i:i+40]))

