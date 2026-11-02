with open('pages-directory.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('<header class="dir-header"')
print("Found at pos", pos)
print(text[pos:pos+700])

