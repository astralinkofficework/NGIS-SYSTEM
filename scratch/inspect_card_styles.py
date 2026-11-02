with open(r'pages/student/css/overlap.css', 'r', encoding='utf-8') as f:
    text = f.read()

for term in ['.ov-profile', '.ov-upcoming', '.ov-deadlines']:
    pos = text.find(term)
    print(f"=== {term} ===")
    print(text[pos:pos+400].encode('ascii', errors='replace').decode('ascii'))

