with open('pages/admin/admin-services.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("action-icons in admin-services.html:", 'action-icons' in text)
idx = text.find('</head>')
if idx != -1:
    print(text[idx-300:idx+50])

