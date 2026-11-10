with open('pages/admin/admin-timetables.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('Length:', len(text))
print(text[:1200])

