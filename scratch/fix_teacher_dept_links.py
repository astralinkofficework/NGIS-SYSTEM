with open(r'pages/teacher/teacher-departments.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('teacher-assignments.html', 'teacher-submissions.html')
content = content.replace(
    'href="../shared/chat.html?portal=teacher&to=',
    'href="javascript:void(0)" onclick="if(window.NGISUI)NGISUI.showNotice(\'Faculty messaging is currently offline for semester maintenance.\', \'info\');else alert(\'Faculty messaging is currently offline for semester maintenance.\');" data-recipient="'
)
content = content.replace(
    "chatLink: '../shared/chat.html?portal=teacher'",
    "chatLink: 'javascript:void(0)'"
)

with open(r'pages/teacher/teacher-departments.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(content)

print('Updated pages/teacher/teacher-departments.html')

