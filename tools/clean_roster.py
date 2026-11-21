with open('pages/teacher/teacher-roster.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove noticeModal and enrollModal HTML between idx_prev_comment and </main>
idx_nm = text.find('id="noticeModal"')
if idx_nm != -1:
    idx_prev_comment = text.rfind('<!-- ══════════════', 0, idx_nm)
    idx_main = text.find('</main>', idx_nm)
    if idx_prev_comment != -1 and idx_main != -1:
        text = text[:idx_prev_comment] + '\n\n' + text[idx_main:]
        print('Removed noticeModal and enrollModal HTML!')

# 2. Update tr in renderTable to be clickable
old_tr = '<tr class=" transition-colors shadow-[0_1px_0_0_#F7F9F7]" data-student-id="${s.id}">'
new_tr = '<tr onclick="if(!event.target.closest(\'button, a, input\')) openStudentModal(\'${s.id}\')" class="transition-colors hover:bg-slate-50 dark:hover:bg-slate-800/50 cursor-pointer" data-student-id="${s.id}">'
if old_tr in text:
    text = text.replace(old_tr, new_tr, 1)
    print('Updated tr to be clickable!')

with open('pages/teacher/teacher-roster.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated teacher-roster.html successfully!')
