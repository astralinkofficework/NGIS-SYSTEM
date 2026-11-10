with open('pages/student/css/overlap.css', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('dash-banner-section')
if pos != -1:
    print(text[pos:pos+1500])
else:
    pos2 = text.find('promo-slideshow')
    if pos2 != -1:
        print(text[pos2:pos2+1500])

