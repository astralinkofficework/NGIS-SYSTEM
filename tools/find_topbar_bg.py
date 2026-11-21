import glob, re

css_files = glob.glob('assets/**/*.css', recursive=True)
js_files = glob.glob('assets/**/*.js', recursive=True)

for path in css_files + js_files:
    try:
        content = open(path, encoding='utf-8', errors='ignore').read()
        matches = re.findall(r'[^{}]*(?:hero-topbar|htb-right-controls|htb-ctrl-btn)[^{}]*\{[^}]*\}', content)
        for m in matches:
            if 'background' in m or 'position' in m or 'white' in m or '#fff' in m or '#FFF' in m or 'fixed' in m or 'shadow' in m:
                print(f"File: {path}")
                print(m.strip()[:300])
                print("-" * 40)
    except Exception as e:
        pass
