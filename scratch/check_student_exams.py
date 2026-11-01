with open('pages/student/student-exams.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('PAGE = { role: role')
print(text[max(0, idx-200):min(len(text), idx+200)].encode('ascii', errors='replace').decode('ascii'))

