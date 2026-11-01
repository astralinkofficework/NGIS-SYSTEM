with open('pages/teacher/teacher-departments.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<!-- 4-KPI Metric Strip -->')
print(repr(text[idx:idx+1500]))

