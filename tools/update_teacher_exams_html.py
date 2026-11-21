with open('pages/teacher/teacher-exams.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace(
    '<title>NGIS — Exam Schedule Management</title>',
    '<title>NGIS — Examination & Quiz Notices</title>'
)
html = html.replace(
    '<h1 class="text-sm font-medium text-slate-900 leading-tight truncate">Exam Schedule Management</h1>',
    '<h1 class="text-sm font-medium text-slate-900 leading-tight truncate">Examination &amp; Quiz Notices</h1>'
)
html = html.replace(
    "title: 'Exam Schedule Management',",
    "title: 'Examination & Quiz Notices',"
)
html = html.replace(
    "greeting: 'Create and manage examination schedules for your assigned subjects and classes.',",
    "greeting: 'Publish examination notices, quiz schedules, and revision guidelines for student cohorts.',"
)
html = html.replace(
    "breadcrumbs: [{ label: 'Assessment' }, { label: 'Examinations' }],",
    "breadcrumbs: [{ label: 'Academics' }, { label: 'Examination & Quiz Notices' }],"
)

with open('pages/teacher/teacher-exams.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated teacher-exams.html successfully.")
