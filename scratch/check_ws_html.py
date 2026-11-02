import sys
with open('pages/teacher/teacher-classes.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('data-purpose="workspace-masthead"')
end = text.find('</section>', idx) + 10
sys.stdout.buffer.write(text[idx-50:end].encode('utf-8'))

