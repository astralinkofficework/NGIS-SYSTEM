with open('pages/teacher/teacher-roster.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx_before_nm = text.find('<!-- ═════════════════════════════════════════════════════════════\n\n       SEND NOTICE MODAL')
idx_main_close = text.find('</main>', idx_before_nm)
if idx_before_nm != -1 and idx_main_close != -1:
    text = text[:idx_before_nm] + '\n\n' + text[idx_main_close:]
    print('Successfully removed noticeModal and enrollModal!')

# Also make table rows clickable
# In renderRosterTable:
old_tr = '<tr class="border-b border-surface-container hover:bg-surface-container-lowest transition-colors group">'
new_tr = '<tr onclick="if(!event.target.closest(\'button, a, input\')) openStudentModal(\'${s.id}\')" class="border-b border-surface-container hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors group cursor-pointer">'
if old_tr in text:
    text = text.replace(old_tr, new_tr)
    print('Replaced table row markup!')
else:
    print('old_tr not found, looking for tr in renderRosterTable:')
    idx_r = text.find('function renderRosterTable')
    idx_tr = text.find('<tr', idx_r)
    print(repr(text[idx_tr:idx_tr+150]))

with open('pages/teacher/teacher-roster.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated teacher-roster.html!')
