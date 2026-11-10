import os

terms = ["Unscheduled Classes", "unscheduled classes", "distribute-all", "Distribute All"]

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or 'scratch' in root:
        continue
    for f in files:
        if f.endswith(('.html', '.js', '.py')):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as fl:
                    c = fl.read()
                for t in terms:
                    if t in c:
                        print(f"Found '{t}' in {path}")
            except Exception:
                pass

