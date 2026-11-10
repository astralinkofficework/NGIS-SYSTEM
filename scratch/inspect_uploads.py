with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '/api/lost-found/upload' in line or 'UPLOAD' in line or 'upload' in line.lower():
        if 'def ' in line or '@app.route' in line:
            print(f"Line {i+1}: {line.strip()}")
            print("".join(lines[i:i+25]))

