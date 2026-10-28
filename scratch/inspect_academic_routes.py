with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '/api/academic' in line or '/api/grades' in line or '/api/attendance' in line:
        print(f"Line {i+1}: {line.strip()}")
        # print next 10 lines
        for j in range(i+1, min(i+15, len(lines))):
            print(f"  {lines[j].strip()}")
        print("-" * 50)
