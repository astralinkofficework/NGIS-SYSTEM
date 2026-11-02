import sys
with open('pages/teacher/teacher-classes.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Academic & Student Operations')
sys.stdout.buffer.write(text[idx-200:idx+1200].encode('utf-8'))

