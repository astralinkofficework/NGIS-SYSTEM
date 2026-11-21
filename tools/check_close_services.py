with open('pages/teacher/teacher-services.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function closeNewRequestModal')
if idx == -1:
    idx = text.find('closeNewRequestModal =')
print("closeNewRequestModal idx:", idx)
print(text[idx:idx+1500])
