with open('assets/js/school-information.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find("font-mono\">License:")
print(text[pos:pos+2000])

