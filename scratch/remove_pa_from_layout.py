with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = '        { id: "assignments", label: "Assignment & Students", icon: "description", href: "pages/principal/principal-assignments.html" },\n'

if target in text:
    text = text.replace(target, '')
    with open('assets/js/layout.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated assets/js/layout.js successfully.')
else:
    # Try alternative spacing
    import re
    text, n = re.subn(r'\s*\{\s*id:\s*"assignments",\s*label:\s*"Assignment & Students",\s*icon:\s*"description",\s*href:\s*"pages/principal/principal-assignments\.html"\s*\},?', '', text)
    if n > 0:
        with open('assets/js/layout.js', 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'Updated assets/js/layout.js with regex ({n} matches).')
    else:
        print('Target not found in assets/js/layout.js')

with open('layout.js', 'r', encoding='utf-8') as f:
    text_root = f.read()

target_root = '        { id: "assignments", label: "Assignment & Students", icon: "description", href: "pages/principal/principal-assignments.html" },\n'

if target_root in text_root:
    text_root = text_root.replace(target_root, '')
    with open('layout.js', 'w', encoding='utf-8') as f:
        f.write(text_root)
    print('Updated layout.js successfully.')
else:
    import re
    text_root, n = re.subn(r'\s*\{\s*id:\s*"assignments",\s*label:\s*"Assignment & Students",\s*icon:\s*"description",\s*href:\s*"pages/principal/principal-assignments\.html"\s*\},?', '', text_root)
    if n > 0:
        with open('layout.js', 'w', encoding='utf-8') as f:
            f.write(text_root)
        print(f'Updated layout.js with regex ({n} matches).')
    else:
        print('Target not found in layout.js')

