with open('pages/teacher/teacher-roster.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove "Send Class Notice" and "Enroll Student" buttons
btn_block_start = '<button type="button" onclick="openNoticeModal()"'
btn_block_end = '<span>Enroll Student</span>\n\n        </button>'
idx_s = text.find(btn_block_start)
idx_e = text.find(btn_block_end)
if idx_s != -1 and idx_e != -1:
    end_pos = idx_e + len(btn_block_end)
    text = text[:idx_s] + text[end_pos:]
    print('Removed Enroll Student & Send Class Notice buttons!')
else:
    print('Could not find btn_block!')

# 2. Remove "Curriculum: Cambridge IGCSE"
curric_str = '<span>Curriculum: <strong class="text-on-surface font-medium">Cambridge IGCSE</strong></span>'
if curric_str in text:
    text = text.replace(curric_str, '')
    print('Removed Curriculum: Cambridge IGCSE!')

# 3. Remove "100% capacity reached"
cap_str = '<span id="kpiCapacityNote">100% capacity reached</span>'
if cap_str in text:
    text = text.replace(cap_str, '<span>Active Class Enrollment</span>')
    print('Replaced 100% capacity reached!')

# 4. Remove noticeModal HTML
nm_start = '<!-- ═════════════════════════════════════════════════════════════\n\n       SEND NOTICE MODAL'
nm_end = 'id="noticeModal"'
idx_nm = text.find(nm_start)
if idx_nm != -1:
    idx_nm_close = text.find('</form>\n\n    </div>\n\n  </div>', idx_nm)
    if idx_nm_close != -1:
        end_nm = idx_nm_close + len('</form>\n\n    </div>\n\n  </div>')
        text = text[:idx_nm] + text[end_nm:]
        print('Removed noticeModal!')

# 5. Remove enrollModal HTML
em_start = '<!-- ═════════════════════════════════════════════════════════════\n\n       ENROLL STUDENT MODAL'
idx_em = text.find(em_start)
if idx_em != -1:
    idx_em_close = text.find('</form>\n\n    </div>\n\n  </div>', idx_em)
    if idx_em_close != -1:
        end_em = idx_em_close + len('</form>\n\n    </div>\n\n  </div>')
        text = text[:idx_em] + text[end_em:]
        print('Removed enrollModal!')

# 6. Make table rows clickable and restore body scroll on modal close
old_row = """        return `

        <tr class="border-b border-surface-container hover:bg-surface-container-lowest transition-colors group">"""

new_row = """        return `

        <tr onclick="if(!event.target.closest('button, a, input')) openStudentModal('${s.id}')" class="border-b border-surface-container hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors group cursor-pointer">"""

if old_row in text:
    text = text.replace(old_row, new_row, 1)
    print('Made table rows clickable!')

# 7. Update closeStudentModal to restore scroll
old_close = """  window.closeStudentModal = function() {

    const modal = document.getElementById('studentDetailModal');

    if (modal) modal.classList.add('hidden');

  };"""

new_close = """  window.closeStudentModal = function() {

    const modal = document.getElementById('studentDetailModal');

    if (modal) modal.classList.add('hidden');

    document.body.classList.remove('modal-open');
    document.body.style.overflow = '';

  };"""

if old_close in text:
    text = text.replace(old_close, new_close, 1)
    print('Updated closeStudentModal!')

with open('pages/teacher/teacher-roster.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated teacher-roster.html successfully!')
