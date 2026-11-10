import glob, re

for path in sorted(glob.glob('pages/**/*.html', recursive=True)):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if '<table' in content:
        # Check if table has an Actions header or th
        has_actions_th = bool(re.search(r'<th[^>]*>.*?(?:action|manage|operation|control).*?</th>', content, re.IGNORECASE))
        # Find any text inside buttons within tbody or JS template
        # Let's inspect
        print(f"Table in {path} (Actions TH: {has_actions_th})")

