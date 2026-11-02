with open(r'pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('class="row2"')
if pos != -1:
    print("Found row2 at", pos)
    print(text[pos-50:pos+500].encode('ascii', errors='replace').decode('ascii'))
