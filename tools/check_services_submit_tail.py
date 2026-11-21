with open('pages/teacher/teacher-services.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('async function handleNewRequestSubmit')
print(text[idx+500:idx+2000])
