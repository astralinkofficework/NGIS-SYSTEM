with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    text = f.read()

for line in text.splitlines()[:50]:
    if 'root' in line:
        print(line)
