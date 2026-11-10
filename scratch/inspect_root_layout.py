with open('layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('pages/admin/admin-news.html')
if pos != -1:
    print(text[pos-100:pos+250])
else:
    print("Not found in layout.js")

