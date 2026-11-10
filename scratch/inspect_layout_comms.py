with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('pages/admin/admin-news.html')
print(text[pos-250:pos+250])
