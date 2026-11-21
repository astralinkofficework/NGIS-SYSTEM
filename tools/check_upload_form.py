with open('pages/teacher/teacher-lessons.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="uploadModal"')
idx_form_end = text.find('</form>', idx)
print(text[idx:idx_form_end+10])
