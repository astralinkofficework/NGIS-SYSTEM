with open(r'pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('teacher-mobile-view')
if pos != -1:
    print("Found teacher-mobile-view at", pos)
    print(text[pos:pos+1200].encode('ascii', errors='replace').decode('ascii'))

