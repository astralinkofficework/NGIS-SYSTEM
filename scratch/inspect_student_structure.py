with open(r'pages/student/student.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('class="dash-overlap"')
pos2 = text.find('class="dash"', pos1)
print("=== In student.html ===")
print(text[pos2-500:pos2+100].encode('ascii', errors='replace').decode('ascii'))
