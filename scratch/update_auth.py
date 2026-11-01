with open('assets/js/auth.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """    const stored = (localStorage.getItem("ngis_active_portal") || "").toLowerCase();
    if (DEMO_USERS[stored]) return stored;

    if (window.PAGE && window.PAGE.role && DEMO_USERS[window.PAGE.role]) {
      return window.PAGE.role;
    }"""

new_block = """    if (window.PAGE && window.PAGE.role && DEMO_USERS[window.PAGE.role]) {
      return window.PAGE.role;
    }

    const stored = (localStorage.getItem("ngis_active_portal") || "").toLowerCase();
    if (DEMO_USERS[stored]) return stored;"""

if old_block.replace('\r\n', '\n') in content.replace('\r\n', '\n'):
    content_normalized = content.replace('\r\n', '\n')
    content_updated = content_normalized.replace(old_block.replace('\r\n', '\n'), new_block.replace('\r\n', '\n'))
    with open('assets/js/auth.js', 'w', encoding='utf-8', newline='\n') as f:
        f.write(content_updated)
    print("SUCCESS")
else:
    print("NOT FOUND")

