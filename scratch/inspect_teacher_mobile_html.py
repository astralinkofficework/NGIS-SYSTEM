with open(r'pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('class="teacher-mobile-view"')
if pos == -1:
    pos = text.find("class='teacher-mobile-view'")
if pos == -1:
    pos = text.find('teacher-mobile-view', 3600)
print("Found HTML at", pos)
print(text[pos:pos+1000].encode('ascii', errors='replace').decode('ascii'))

