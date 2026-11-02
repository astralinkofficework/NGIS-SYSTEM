with open('pages/teacher/teacher-submissions.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = """      <div>
        <h2 class="text-xl font-medium text-slate-900 tracking-tight">Student Work Submissions</h2>
        <p class="text-xs text-slate-500 mt-1">Homeroom Grade 10A &bull; Review student submissions, evaluate rubric criteria, and provide verified academic feedback.</p>
      </div>"""

replacement = """      <div>
        <h1 class="text-2xl sm:text-3xl font-medium text-slate-900 tracking-tight">Student Work Submissions</h1>
      </div>"""

target_crlf = target.replace('\r\n', '\n').replace('\n', '\r\n')
replacement_crlf = replacement.replace('\r\n', '\n').replace('\n', '\r\n')

if target in c:
    c = c.replace(target, replacement)
    print('Replaced LF')
elif target_crlf in c:
    c = c.replace(target_crlf, replacement_crlf)
    print('Replaced CRLF')
else:
    print('Target not matched')

with open('pages/teacher/teacher-submissions.html', 'w', encoding='utf-8') as f:
    f.write(c)

