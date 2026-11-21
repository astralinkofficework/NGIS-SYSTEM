with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the quick links in ql-body
old_ql = '''        <a class="ql-item" href="student-assignments.html">
          <div class="ql-icon-wrap" style="background:#F7F9F7"><span class="mi" style="color:#29352E">assignment</span></div>
          <span class="ql-label">Assignments</span>
        </a>
        <a class="ql-item" href="../shared/announcements.html?portal=student">
          <div class="ql-icon-wrap" style="background:#F7F9F7"><span class="mi" style="color:#000000">campaign</span></div>
          <span class="ql-label">Announcements</span>
        </a>
        <a class="ql-item" href="student-timetable.html">
          <div class="ql-icon-wrap" style="background:#F7F9F7"><span class="mi" style="color:#000000">calendar_view_week</span></div>
          <span class="ql-label">Timetable</span>
        </a>
        <a class="ql-item" href="student-services.html">
          <div class="ql-icon-wrap" style="background:#F7F9F7"><span class="mi" style="color:#29352E">grid_view</span></div>
          <span class="ql-label">Student Services</span>
        </a>
        <a class="ql-item" href="student-grades.html">
          <div class="ql-icon-wrap" style="background:#F7F9F7"><span class="mi" style="color:#29352E">bar_chart</span></div>
          <span class="ql-label">Results</span>
        </a>
        <a class="ql-item" href="student-notifications.html" style="position:relative">
          <div class="ql-icon-wrap" style="background:#F7F9F7">
            <span class="mi" style="color:#000000">chat</span>
            <span class="ql-badge" style="background:#29352E">2</span>
          </div>
          <span class="ql-label">Notifications</span>
        </a>
      </div>
      <div class="ql-divider"></div>
      <div class="ql-grid">
        <a class="ql-item" href="../shared/lessons.html">
          <div class="ql-icon-wrap" style="background:#F7F9F7"><span class="mi" style="color:#29352E">menu_book</span></div>
          <span class="ql-label">E-Learning</span>
        </a>'''

new_ql = '''        <a class="ql-item" href="javascript:void(0)" onclick="openDeptSelectionModal('assignments')">
          <div class="ql-icon-wrap" style="background:#F7F9F7"><span class="mi" style="color:#29352E">assignment</span></div>
          <span class="ql-label">Assignments</span>
        </a>
        <a class="ql-item" href="../shared/announcements.html?portal=student">
          <div class="ql-icon-wrap" style="background:#F7F9F7"><span class="mi" style="color:#000000">campaign</span></div>
          <span class="ql-label">Announcements</span>
        </a>
        <a class="ql-item" href="javascript:void(0)" onclick="openDeptSelectionModal('timetable')">
          <div class="ql-icon-wrap" style="background:#F7F9F7"><span class="mi" style="color:#000000">calendar_view_week</span></div>
          <span class="ql-label">Timetable</span>
        </a>
        <a class="ql-item" href="student-services.html">
          <div class="ql-icon-wrap" style="background:#F7F9F7"><span class="mi" style="color:#29352E">grid_view</span></div>
          <span class="ql-label">Student Services</span>
        </a>
        <a class="ql-item" href="javascript:void(0)" onclick="openDeptSelectionModal('results')">
          <div class="ql-icon-wrap" style="background:#F7F9F7"><span class="mi" style="color:#29352E">bar_chart</span></div>
          <span class="ql-label">Results</span>
        </a>
        <a class="ql-item" href="student-notifications.html" style="position:relative">
          <div class="ql-icon-wrap" style="background:#F7F9F7">
            <span class="mi" style="color:#000000">chat</span>
            <span class="ql-badge" style="background:#29352E">2</span>
          </div>
          <span class="ql-label">Notifications</span>
        </a>
      </div>
      <div class="ql-divider"></div>
      <div class="ql-grid">
        <a class="ql-item" href="javascript:void(0)" onclick="openDeptSelectionModal('elearning')">
          <div class="ql-icon-wrap" style="background:#F7F9F7"><span class="mi" style="color:#29352E">menu_book</span></div>
          <span class="ql-label">E-Learning</span>
        </a>'''

modal_and_js = '''
<!-- ═══════════════ DEPARTMENT SELECTION MODAL ═══════════════ -->
<div id="deptSelectionModal" class="hidden fixed inset-0 z-[10000] flex items-center justify-center p-3 sm:p-4 bg-black/60 backdrop-blur-xs transition-opacity" role="dialog" aria-modal="true" aria-labelledby="deptModalTitle" style="z-index: 10000;">
  <div class="fixed inset-0 cursor-pointer" onclick="closeDeptSelectionModal()"></div>
  <div class="relative w-full max-w-lg bg-white dark:bg-slate-900 rounded-2xl sm:rounded-3xl shadow-xl border border-slate-200 dark:border-slate-800 p-5 sm:p-6 flex flex-col z-10 max-h-[90vh] overflow-hidden">
    <div class="flex items-center justify-between pb-3.5 border-b border-surface-border">
      <div>
        <div class="text-[11px] font-normal text-forest-700 dark:text-emerald-400 mb-0.5" id="deptModalKicker">Quick Link Department Selection</div>
        <h3 id="deptModalTitle" class="text-base sm:text-lg font-normal text-forest-800 dark:text-slate-100 font-display">
          Choose Academic Department
        </h3>
      </div>
      <button type="button" onclick="closeDeptSelectionModal()" class="w-8 h-8 rounded-full bg-surface-subtle hover:bg-surface-border flex items-center justify-center text-ink-muted hover:text-forest-800 transition cursor-pointer" title="Close (Esc)" aria-label="Close">
        <span class="material-symbols-outlined text-[18px]">close</span>
      </button>
    </div>

    <div class="flex-1 overflow-y-auto py-4 space-y-2.5" id="deptModalList">
      <!-- Options rendered dynamically with authentic enrollments -->
    </div>

    <div class="pt-3 border-t border-surface-border flex items-center justify-between text-xs text-ink-soft">
      <span>Enrolled Student: Grade 10A • Science Stream</span>
      <button type="button" onclick="selectDepartment('all')" class="text-forest-800 dark:text-emerald-400 font-medium hover:underline cursor-pointer">
        View All Departments →
      </button>
    </div>
  </div>
</div>

<script>
var activeDeptNavTarget = 'assignments';

function openDeptSelectionModal(targetKey) {
  activeDeptNavTarget = targetKey || 'assignments';
  const modal = document.getElementById('deptSelectionModal');
  const title = document.getElementById('deptModalTitle');
  const kicker = document.getElementById('deptModalKicker');
  const list = document.getElementById('deptModalList');

  const targetTitles = {
    assignments: { title: 'Select Department for Coursework', kicker: 'Assignments & Tasks' },
    timetable: { title: 'Select Department Timetable', kicker: 'Weekly Class Schedule' },
    results: { title: 'Select Department Academic Results', kicker: 'Official Transcripts & Evaluations' },
    elearning: { title: 'Select Subject for E-Learning', kicker: 'Course Materials & Library' }
  };

  const cfg = targetTitles[activeDeptNavTarget] || targetTitles.assignments;
  if (title) title.textContent = cfg.title;
  if (kicker) kicker.textContent = cfg.kicker;

  const enrollments = [
    { id: 'math', name: 'Mathematics Department', nameKh: 'ដេប៉ាតឺម៉ង់គណិតវិទ្យា', subject: 'Advanced Mathematics (Calculus)', icon: 'calculate' },
    { id: 'english', name: 'English Department', nameKh: 'ដេប៉ាតឺម៉ង់អង់គ្លេស', subject: 'English Literature & Composition', icon: 'menu_book' },
    { id: 'physics', name: 'Science & Physics Department', nameKh: 'ដេប៉ាតឺម៉ង់រូបវិទ្យា', subject: 'Physics & Experimental Lab', icon: 'science' },
    { id: 'khmer', name: 'Khmer Studies Department', nameKh: 'ដេប៉ាតឺម៉ង់អក្សរសាស្ត្រខ្មែរ', subject: 'Classical Khmer Literature', icon: 'history_edu' },
    { id: 'chinese', name: 'Chinese Language Department', nameKh: 'ដេប៉ាតឺម៉ង់ភាសាចិន', subject: 'Chinese Language (HSK 3)', icon: 'translate' },
    { id: 'history', name: 'Social Studies & History', nameKh: 'ដេប៉ាតឺម៉ង់ប្រវត្តិវិទ្យា', subject: 'World History & Civilizations', icon: 'public' },
    { id: 'cs', name: 'Computer Science & ICT', nameKh: 'ដេប៉ាតឺម៉ង់បច្ចេកវិទ្យា', subject: 'Data Structures & Python', icon: 'terminal' }
  ];

  if (list) {
    list.innerHTML = `
      <button type="button" onclick="selectDepartment('all')" class="w-full p-3 rounded-2xl border border-surface-border hover:border-forest-400 bg-surface-subtle/40 hover:bg-surface-subtle flex items-center justify-between gap-3 text-left transition cursor-pointer">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-forest-100 text-forest-800 flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[18px]">apps</span>
          </div>
          <div>
            <div class="text-xs font-medium text-forest-800">All Enrolled Departments</div>
            <div class="text-[11px] text-ink-soft">Full comprehensive overview across all subjects</div>
          </div>
        </div>
        <span class="material-symbols-outlined text-ink-muted text-[18px]">chevron_right</span>
      </button>
    ` + enrollments.map(d => `
      <button type="button" onclick="selectDepartment('${d.id}')" class="w-full p-3 rounded-2xl border border-surface-border hover:border-forest-400 bg-white hover:bg-forest-50/40 flex items-center justify-between gap-3 text-left transition cursor-pointer">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-surface-subtle text-forest-700 flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[18px]">${d.icon}</span>
          </div>
          <div class="min-w-0">
            <div class="text-xs font-medium text-slate-800 dark:text-slate-100 truncate">${d.name} <span class="font-normal text-[11px] text-ink-soft">(${d.nameKh})</span></div>
            <div class="text-[11px] text-ink-muted truncate">${d.subject} • Class 10A</div>
          </div>
        </div>
        <span class="material-symbols-outlined text-ink-muted text-[18px]">chevron_right</span>
      </button>
    `).join('');
  }

  if (modal) {
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    document.body.classList.add('modal-open');
    document.body.style.overflow = 'hidden';
  }
}

function closeDeptSelectionModal() {
  const modal = document.getElementById('deptSelectionModal');
  if (modal) {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
  }
  document.body.classList.remove('modal-open');
  document.body.style.overflow = '';
}

function selectDepartment(deptKey) {
  closeDeptSelectionModal();
  const param = (deptKey === 'all' || !deptKey) ? '' : '?dept=' + encodeURIComponent(deptKey);
  const elearnParam = (deptKey === 'all' || !deptKey) ? '?portal=student' : '?dept=' + encodeURIComponent(deptKey) + '&portal=student';

  switch (activeDeptNavTarget) {
    case 'assignments':
      window.location.href = 'student-assignments.html' + param;
      break;
    case 'timetable':
      window.location.href = 'student-timetable.html' + param;
      break;
    case 'results':
      window.location.href = 'student-grades.html' + param;
      break;
    case 'elearning':
      window.location.href = '../shared/lessons.html' + elearnParam;
      break;
    default:
      window.location.href = 'student-assignments.html' + param;
  }
}
</script>
'''

# Replace quick links
if old_ql in text:
    text = text.replace(old_ql, new_ql)
    print('Updated Quick Links markup')
else:
    print('Could not find old_ql in student.html')

# Also update mobile buttons
text = text.replace("window.location.href='student-grades.html'", "openDeptSelectionModal('results')")
text = text.replace("window.location.href='student-assignments.html'", "openDeptSelectionModal('assignments')")
text = text.replace("window.location.href='student-timetable.html'", "openDeptSelectionModal('timetable')")

# Insert modal before </body>
idx = text.rfind('</body>')
if idx != -1:
    text = text[:idx] + modal_and_js + '\n' + text[idx:]
    with open('pages/student/student.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Successfully inserted Department Selection modal and script into student.html')
else:
    print('Could not find </body> in student.html')
