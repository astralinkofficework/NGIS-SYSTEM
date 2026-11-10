import os, glob

terms = [
    'ks-workflow-bar',
    'Build weekly class and teacher schedules',
    'Class 11B Timetable',
    'Remaining Periods ('
]

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or 'scratch' in root or '.gemini' in root:
        continue
    for f in files:
        if f.endswith(('.html', '.js', '.css', '.py')):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as fl:
                    content = fl.read()
                for t in terms:
                    if t in content:
                        print(f"Found '{t}' in {path}")
            except Exception:
                pass

