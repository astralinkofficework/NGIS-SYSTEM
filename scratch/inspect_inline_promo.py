with open('pages/student/js/student-inline.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('promoPrev')
if pos != -1:
    print(text[pos-600:pos+100])
