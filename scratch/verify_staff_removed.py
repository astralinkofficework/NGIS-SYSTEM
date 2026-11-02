import os, re, io

# Portal-level staff references (links, roles, APIs) — not generic "staff member" copy
pat = re.compile(r'pages/staff|/staff\b|portal=staff|role.{0,3}staff|staff@ngis|staff\.html|staff-services|staff-profile|staffStats|staff_tasks|api/staff', re.I)
skipdirs = {'scratch', '_concepts', '.git', 'node_modules', '__pycache__', '.data', '.vscode', '.claude', '.agents', '.devin', '.ux', 'uploads'}
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in skipdirs]
    for fn in files:
        if not fn.endswith(('.py', '.js', '.html', '.json', '.md', '.css')):
            continue
        p = os.path.join(root, fn)
        try:
            src = io.open(p, encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        for i, ln in enumerate(src.splitlines(), 1):
            if pat.search(ln):
                print(f'{p}:{i}: {ln.strip()[:130]}')
