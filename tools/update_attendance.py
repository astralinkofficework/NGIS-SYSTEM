with open('pages/teacher/teacher-attendance.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add student search bar in toolbar before View Mode Selector
old_toolbar_spot = '<!-- Sheet / Card View Mode Selector -->'
search_markup = """<!-- Student Fast Search (Section 5) -->
        <div class="relative flex-1 min-w-[160px] max-w-xs">
          <input type="text" id="searchAttendanceStudent" oninput="window.onAttendanceSearch(this.value)" placeholder="Search student name, ID..." class="w-full text-xs py-1.5 pl-8 pr-2.5 border border-slate-300 rounded-lg focus:border-[#0F5132] focus:ring-1 focus:ring-[#0F5132] bg-white text-slate-800 shadow-xs">
          <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
        </div>

        <!-- Sheet / Card View Mode Selector -->"""

assert old_toolbar_spot in text, "Could not find old_toolbar_spot"
text = text.replace(old_toolbar_spot, search_markup, 1)

# 2. Update table tag min-w-[980px] to be responsive
text = text.replace('min-w-[980px]', 'w-full min-w-0 max-w-full')

# 3. Add Quick Attendance Status Picker floating markup before closing body tag
picker_html = """
  <!-- ════════ QUICK ATTENDANCE STATUS PICKER POPUP (Section 5) ════════ -->
  <div id="attendanceStatusPopup" class="fixed z-[9999] bg-white dark:bg-slate-900 rounded-xl shadow-xl border border-slate-200 dark:border-slate-800 p-1.5 flex flex-col gap-1 min-w-[145px] hidden transition-all animate-scale-in" style="z-index: 9999;">
    <button type="button" onclick="window.applyAttendanceStatus('P')" class="flex items-center gap-2.5 px-3 py-2 text-xs rounded-lg text-slate-800 dark:text-slate-100 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 text-left transition cursor-pointer">
      <span class="w-5 h-5 rounded bg-emerald-600 text-white font-medium text-[11px] flex items-center justify-center">P</span>
      <span class="font-normal">Present</span>
    </button>
    <button type="button" onclick="window.applyAttendanceStatus('L')" class="flex items-center gap-2.5 px-3 py-2 text-xs rounded-lg text-slate-800 dark:text-slate-100 hover:bg-amber-50 dark:hover:bg-amber-950/40 text-left transition cursor-pointer">
      <span class="w-5 h-5 rounded bg-amber-500 text-white font-medium text-[11px] flex items-center justify-center">L</span>
      <span class="font-normal">Late</span>
    </button>
    <button type="button" onclick="window.applyAttendanceStatus('A')" class="flex items-center gap-2.5 px-3 py-2 text-xs rounded-lg text-slate-800 dark:text-slate-100 hover:bg-rose-50 dark:hover:bg-rose-950/40 text-left transition cursor-pointer">
      <span class="w-5 h-5 rounded bg-rose-600 text-white font-medium text-[11px] flex items-center justify-center">A</span>
      <span class="font-normal">Absent</span>
    </button>
    <button type="button" onclick="window.applyAttendanceStatus('E')" class="flex items-center gap-2.5 px-3 py-2 text-xs rounded-lg text-slate-800 dark:text-slate-100 hover:bg-blue-50 dark:hover:bg-blue-950/40 text-left transition cursor-pointer">
      <span class="w-5 h-5 rounded bg-blue-500 text-white font-medium text-[11px] flex items-center justify-center">E</span>
      <span class="font-normal">Excused</span>
    </button>
  </div>
"""
text = text.replace('</body>', picker_html + '\n</body>', 1)

# 4. Add search filtering and quick status popup JS logic
js_logic = """
  let attendanceSearchQuery = '';
  let activePickerStudentIdx = null;
  let activePickerDayIdx = null;

  window.onAttendanceSearch = function(val) {
    attendanceSearchQuery = (val || '').toLowerCase().trim();
    renderSpreadsheet();
    renderCardsView();
  };

  window.openAttendanceStatusPicker = function(event, studentIdx, dayIdx) {
    event.stopPropagation();
    activePickerStudentIdx = studentIdx;
    activePickerDayIdx = dayIdx;

    const popup = document.getElementById('attendanceStatusPopup');
    if (!popup) return;

    const rect = event.currentTarget.getBoundingClientRect();
    popup.style.top = Math.min(window.innerHeight - 170, rect.bottom + 6) + 'px';
    popup.style.left = Math.min(window.innerWidth - 160, Math.max(10, rect.left - 40)) + 'px';
    popup.classList.remove('hidden');

    const closeHandler = (e) => {
      if (!popup.contains(e.target)) {
        popup.classList.add('hidden');
        document.removeEventListener('click', closeHandler);
      }
    };
    setTimeout(() => document.addEventListener('click', closeHandler), 10);
  };

  window.applyAttendanceStatus = function(code) {
    const popup = document.getElementById('attendanceStatusPopup');
    if (popup) popup.classList.add('hidden');

    if (activePickerStudentIdx !== null && activePickerDayIdx !== null) {
      if (rosterData[activePickerStudentIdx]) {
        rosterData[activePickerStudentIdx].days[activePickerDayIdx] = code;
        renderSpreadsheet();
        renderCardsView();
        updateKpisAndFooters();
        if (window.toast) window.toast(`Marked ${code === 'P' ? 'Present' : (code === 'A' ? 'Absent' : (code === 'L' ? 'Late' : 'Excused'))}`, 'info');
      }
    }
  };
"""

target_interactive = "// Window-level interactive utilities"
assert target_interactive in text, "Could not find target_interactive"
text = text.replace(target_interactive, js_logic + "\n  " + target_interactive, 1)

# 5. In renderSpreadsheet, day buttons currently call window.cycleCell(${sIdx}, d)
# Replace cycleCell with openAttendanceStatusPicker(event, ${sIdx}, d)
for d in range(5):
    old_call = f'onclick="window.cycleCell(${{sIdx}}, {d})"'
    new_call = f'onclick="window.openAttendanceStatusPicker(event, ${{sIdx}}, {d})"'
    text = text.replace(old_call, new_call)

# 6. In renderSpreadsheet and renderCardsView, filter by attendanceSearchQuery
old_render_spread = "tbody.innerHTML = rosterData.map((s, sIdx) => {"
new_render_spread = """const filteredRoster = rosterData.map((s, idx) => ({ ...s, origIdx: idx })).filter(s => {
      if (!attendanceSearchQuery) return true;
      return (s.name && s.name.toLowerCase().includes(attendanceSearchQuery)) || 
             (s.id && s.id.toLowerCase().includes(attendanceSearchQuery));
    });

    tbody.innerHTML = filteredRoster.map((s, itemIdx) => {
      const sIdx = s.origIdx;"""
assert old_render_spread in text, "Could not find old_render_spread"
text = text.replace(old_render_spread, new_render_spread, 1)

with open('pages/teacher/teacher-attendance.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated teacher-attendance.html successfully!')
