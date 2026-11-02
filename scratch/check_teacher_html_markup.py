with open(r'pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="promoDots"')
print(text[pos:pos+600].encode('ascii', errors='replace').decode('ascii'))
