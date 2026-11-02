import re

btn_html = '<button class="icon-btn menu-btn hamburger-btn mobile-hamburger-btn htb-hamburger" data-action="toggle-sidebar" aria-label="Open menu" aria-expanded="false" title="Open navigation"><i class="ph ph-list text-xl" aria-hidden="true"></i><span class="mi" style="display:none">menu</span></button>\n        '

for p in ['pages/admin/admin-accounts.html', 'pages/admin/admin-audit.html']:
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()
    if 'data-action="toggle-sidebar"' not in text:
        text = text.replace('<div class="htb-left">\n        <a href="/"', f'<div class="htb-left">\n        {btn_html}<a href="/"')
        text = text.replace('<div class="htb-left"><a href="/"', f'<div class="htb-left">{btn_html}<a href="/"')
        with open(p, 'w', encoding='utf-8', newline='\r\n') as f:
            f.write(text)
        print(f"Added hamburger button to {p}")

