import sys
with open('pages/teacher/teacher-classes.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Academic & Student Operations')
sys.stdout.buffer.write(text[idx:idx+4000].encode('utf-8'))

