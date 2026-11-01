import re

user_card_regex = re.compile(
    r'\s*<div class="side-user-card" id="sideUserCard"[^>]*>.*?</div>\s*</div>\s*<span class="material-symbols-outlined side-user-caret">expand_more</span>\s*</div>',
    re.DOTALL
)

for file_path in ['assets/js/layout.js', 'layout.js']:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Search for side-user-card block
    start_str = '<div class="side-user-card" id="sideUserCard"'
    if start_str in content:
        start_idx = content.find(start_str)
        # Find closing tag of this div
        # It ends right before `<nav class="side-nav`
        nav_idx = content.find('<nav class="side-nav', start_idx)
        if nav_idx != -1:
            # We want to remove from start_str up to nav_idx, preserving clean indentation
            block = content[start_idx:nav_idx]
            content = content[:start_idx] + content[nav_idx:]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Successfully removed sideUserCard from {file_path}')
        else:
            print(f'Could not find nav after sideUserCard in {file_path}')
    else:
        print(f'sideUserCard not found in {file_path}')

