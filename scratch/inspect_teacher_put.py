with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_func = False
for i, line in enumerate(lines):
    if "/api/principal/roster/teachers/<teacher_id>" in line:
        in_func = True
    if in_func:
        print(f"{i+1}: {line.rstrip()}")
        if line.strip().startswith('@app.route') and i > 50 and "/api/principal/roster/teachers/<teacher_id>" not in line:
            break
        if "def " in line and i > 50 and not line.strip().startswith('def update_') and not line.strip().startswith('def get_'):
            break

