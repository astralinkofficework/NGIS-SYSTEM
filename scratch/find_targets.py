import os

targets = [
    'viewSwitcher',
    'Cambodian MoEYS Guidelines',
    'វិទ្យាល័យ ហ្គេតវេ អន្តរជាតិថ្មី',
    'Standard Cambodian National Curriculum (MoEYS)',
    'Standard Cambodian National Curriculum'
]

for root, dirs, files in os.walk('.'):
    if any(x in root for x in ['.git', 'node_modules', 'scratch', '.gemini', 'brain']):
        continue
    for f in files:
        if f.endswith(('.js', '.html', '.css', '.py')):
            path = os.path.join(root, f)
            try:
                with open(path, encoding='utf-8') as file:
                    content = file.read()
                    for t in targets:
                        if t in content:
                            print(f'Found "{t}" in {path}')
            except Exception:
                pass

