with open('assets/js/action-icons.js', 'r', encoding='utf-8') as f:
    text = f.read()

for icon_name in ['menu', 'calendar', 'bell', 'mail', 'search']:
    idx = text.find(f'{icon_name}:')
    if idx != -1:
        print(f"Found {icon_name} in PATHS: {text[idx:idx+120]}")
    else:
        print(f"NOT FOUND: {icon_name}")
