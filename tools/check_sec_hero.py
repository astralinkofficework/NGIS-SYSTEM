with open('pages/admin/admin-security.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('heroBanner')
print("heroBanner in admin-security.html:", idx)
if idx != -1:
    print(text[idx-50:idx+400])

idx_top = text.find('hero-topbar')
print("hero-topbar in admin-security.html:", idx_top)
if idx_top != -1:
    print(text[idx_top-50:idx_top+400])
