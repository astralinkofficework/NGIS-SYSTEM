import sys
with open('pages/teacher/teacher-classes.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('workspace-masthead')
start = text.rfind('\n', 0, idx - 200)
end = text.find('</section>', idx) + 300
sys.stdout.buffer.write(text[start:end].encode('utf-8'))
