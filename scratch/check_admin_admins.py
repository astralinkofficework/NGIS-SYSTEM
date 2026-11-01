with open('pages/admin/admin-admins.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('Length of admin-admins.html:', len(text))
print(text[:300].encode('ascii', errors='replace').decode('ascii'))

