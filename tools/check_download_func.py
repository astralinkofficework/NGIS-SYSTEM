with open('pages/shared/js/lesson-data.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('ngisDownloadFile')
print(pos)
if pos != -1:
    print(text[pos:pos+400])
