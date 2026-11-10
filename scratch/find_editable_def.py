with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'TEACHER_EDITABLE_FIELDS' in line:
        print(f"{i+1}: {line.rstrip()}")

