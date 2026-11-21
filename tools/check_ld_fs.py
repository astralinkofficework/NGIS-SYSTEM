with open('pages/shared/js/lesson-details.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function ldToggleFullscreen')
print(text[pos:pos+1500])
