with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('promoSlideshow')
while pos != -1:
    print(f"Found promoSlideshow at {pos}:")
    print(text[pos-100:pos+400])
    print("=" * 60)
    pos = text.find('promoSlideshow', pos + 1)

