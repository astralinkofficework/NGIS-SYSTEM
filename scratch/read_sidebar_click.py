with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('sidebar.addEventListener("click"')
print(text[idx-100:idx+800].encode('ascii', errors='replace').decode('ascii'))

