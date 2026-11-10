with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
admin_menus = re.findall(r'role === "admin"[\s\S]*?\];', text)
if admin_menus:
    print("Admin menu snippet:\n", admin_menus[0][:1000])

prn_menus = re.findall(r'role === "principal"[\s\S]*?\];', text)
if prn_menus:
    print("\nPrincipal menu snippet:\n", prn_menus[0][:1000])

