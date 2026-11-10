with open("pages/admin/admin-system-school-info.html", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
print('\n'.join(lines[100:]))

