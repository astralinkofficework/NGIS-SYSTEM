with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('idModal')
print(text[idx-250:idx+50].encode('ascii', errors='replace').decode('ascii'))
