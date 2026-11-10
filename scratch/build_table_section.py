profiles_path = r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\assets\js\ngis-profiles.js'

with open(profiles_path, 'r', encoding='utf-8') as f:
    code = f.read()

idx_start = code.find("  function renderTable() {")
idx_end = code.find("  function renderPager() {")
assert idx_start != -1 and idx_end != -1, "table bounds not found"

replacement = '''  /* ---------- Teacher Row Card & Inline Accordion Editor ---------- */
  function teacherRowHtml(r) {
    var teacherCode = r.code || r.id || 'TCH';
    var subjectColor = getSubjectColor(r.subject);
    var targetHours = r.target || (r.classesAssigned ? r.classesAssigned * 3 : 17);
    var maxDaily = r.max_daily || 5;
    var classesAssigned = r.classesAssigned != null ? r.classesAssigned : 0;
    var isActive = String(r.status || '').toLowerCase() === 'active';
    var isLeave = String(r.status || '').toLowerCase().indexOf('leave') !== -1;
    var statusTone = isActive ? 'bg-[#E8F3ED] text-[#176B45]' : (isLeave ? 'bg-[#ffeadb] text-[#822714]' : 'bg-slate-100 text-slate-600');
    var statusDot = isActive ? 'bg-[#176B45]' : (isLeave ? 'bg-[#b8541f]' : 'bg-slate-400');
    var gender = r.gender || 'Male';

    return [
      '<div class="teacher-row-card bg-white rounded-xl border border-[#E1E9E3] hover:border-slate-300 transition-all shadow-2xs overflow-hidden" data-id="' + esc(r.id) + '" id="teacherCard_' + esc(r.id) + '">',
      // Row Bar (Clickable to toggle expand)
      '  <div class="p-3 sm:p-4 flex flex-col lg:grid lg:grid-cols-12 gap-3 lg:gap-4 items-start lg:items-center cursor-pointer select-none transition-colors hover:bg-slate-50/50" data-act="toggle-expand" data-id="' + esc(r.id) + '">',
      '    <!-- Col 1: Avatar, Name, Code, ID -->',
      '    <div class="lg:col-span-4 flex items-center gap-3 min-w-0 w-full">',
      '      <div class="w-10 h-10 rounded-full bg-[#E8F3ED] text-[#176B45] flex items-center justify-center font-medium text-xs shrink-0 shadow-2xs border border-[#176B45]/15">',
      '        ' + esc(initials(r.name)),
      '      </div>',
      '      <div class="min-w-0 flex-1">',
      '        <div class="flex items-center gap-2 flex-wrap">',
      '          <span class="font-medium text-sm text-slate-900 hover:text-[#176B45] transition-colors truncate" data-act="view" data-id="' + esc(r.id) + '">' + esc(r.name) + '</span>',
      '          <span class="px-1.5 py-0.5 rounded text-[10px] font-mono font-medium bg-slate-100 text-slate-700 border border-slate-200/80">' + esc(teacherCode) + '</span>',
      '        </div>',
      '        <div class="text-[11px] text-slate-500 flex items-center gap-1.5 truncate mt-0.5">',
      '          <span>' + esc(r.id) + '</span>',
      '          <span class="text-slate-300">•</span>',
      '          <span>' + esc(r.role || 'Faculty') + '</span>',
      '        </div>',
      '      </div>',
      '    </div>',

      '    <!-- Col 2: Department & Subject -->',
      '    <div class="lg:col-span-3 min-w-0 w-full flex flex-col justify-center">',
      '      <div class="flex items-center gap-1.5">',
      '        <span class="w-2 h-2 rounded-full shrink-0" style="background-color: ' + subjectColor + ';"></span>',
      '        <span class="font-medium text-xs text-slate-800 truncate">' + esc(r.subject || 'General') + '</span>',
      '      </div>',
      '      <span class="text-[11px] text-slate-500 truncate ml-3.5">' + esc(r.department || 'MoEYS Faculty') + '</span>',
      '    </div>',

      '    <!-- Col 3: Workload & Classes -->',
      '    <div class="lg:col-span-2 min-w-0 w-full flex items-center gap-2">',
      '      <div class="flex flex-col">',
      '        <span class="text-xs font-medium text-slate-700">' + targetHours + ' hrs/wk</span>',
      '        <span class="text-[11px] text-slate-400">' + classesAssigned + ' classes assigned</span>',
      '      </div>',
      '    </div>',

      '    <!-- Col 4: Status -->',
      '    <div class="lg:col-span-1 min-w-0 flex items-center">',
      '      <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium ' + statusTone + '">',
      '        <span class="w-1.5 h-1.5 rounded-full ' + statusDot + '"></span>' + esc(r.status || 'Active') + '',
      '      </span>',
      '    </div>',

      '    <!-- Col 5: Actions -->',
      '    <div class="lg:col-span-2 flex items-center justify-end gap-1.5 w-full shrink-0" onclick="event.stopPropagation()">',
      '      <button type="button" data-act="edit-row" data-id="' + esc(r.id) + '" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-[#E8F3ED] hover:text-[#176B45] hover:border-[#176B45]/40 transition-colors cursor-pointer flex items-center gap-1 min-h-[32px]">',
      '        <span class="material-symbols-outlined text-[15px]">edit</span>',
      '        <span>Edit</span>',
      '      </button>',
      '      <button type="button" data-act="view" data-id="' + esc(r.id) + '" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors cursor-pointer flex items-center gap-1 min-h-[32px]" title="View Full Profile">',
      '        <span>Profile</span>',
      '      </button>',
      '      <button type="button" data-act="toggle" data-id="' + esc(r.id) + '" title="' + (isActive ? 'Deactivate record' : 'Activate record') + '" class="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors cursor-pointer min-h-[32px] min-w-[32px] flex items-center justify-center" aria-label="Toggle status">',
      '        <span class="material-symbols-outlined text-[18px]">more_vert</span>',
      '      </button>',
      '      <button type="button" data-act="toggle-expand" data-id="' + esc(r.id) + '" class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-all cursor-pointer min-h-[32px] min-w-[32px] flex items-center justify-center" title="Expand Details" aria-label="Expand Details">',
      '        <span class="material-symbols-outlined text-[20px] transition-transform duration-200 chevron-icon" id="chevron_' + esc(r.id) + '">expand_more</span>',
      '      </button>',
      '    </div>',
      '  </div>',

      // Inline Expandable Details Editor
      '  <div class="teacher-inline-editor border-t border-[#E1E9E3] bg-[#F7F9F7]/90 p-4 sm:p-5 rounded-b-xl hidden" id="editor_' + esc(r.id) + '" onclick="event.stopPropagation()">',
      '    <div class="flex items-center justify-between pb-3.5 mb-5 border-b border-slate-200/90">',
      '      <div class="flex items-center gap-2.5">',
      '        <div class="w-2.5 h-2.5 rounded-full bg-[#176B45]"></div>',
      '        <h3 class="text-xs font-medium uppercase tracking-wider text-[#29352E]">',
      '          Faculty Member Record Editor — ' + esc(r.name) + ' <span class="text-slate-400 font-normal">(' + esc(r.id) + ')</span>',
      '        </h3>',
      '      </div>',
      '      <span class="text-[11px] text-slate-500 hidden sm:inline">Inline editor · Instant synchronization to Live Timetable</span>',
      '    </div>',

      '    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-left">',
      '      <!-- SECTION A — Basic Information -->',
      '      <div class="bg-white p-3.5 rounded-xl border border-[#E1E9E3] space-y-3 shadow-2xs">',
      '        <div class="flex items-center gap-1.5 pb-1 border-b border-slate-100 text-xs font-medium text-slate-700">',
      '          <span class="material-symbols-outlined text-[16px] text-[#176B45]">person</span>',
      '          <span>Section A — Basic Information</span>',
      '        </div>',
      '        <div>',
      '          <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edName_' + r.id + '">Full Name <span class="text-rose-500">*</span></label>',
      '          <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edName_' + r.id + '" type="text" value="' + esc(r.name || '') + '">',
      '        </div>',
      '        <div class="grid grid-cols-2 gap-2">',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edGender_' + r.id + '">Gender</label>',
      '            <select class="w-full text-xs py-2 px-2 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edGender_' + r.id + '">',
      '              <option value="Male"' + (gender === 'Male' ? ' selected' : '') + '>Male</option>',
      '              <option value="Female"' + (gender === 'Female' ? ' selected' : '') + '>Female</option>',
      '            </select>',
      '          </div>',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edPhone_' + r.id + '">Phone</label>',
      '            <input class="w-full text-xs py-2 px-2 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edPhone_' + r.id + '" type="text" value="' + esc(r.phone || '') + '">',
      '          </div>',
      '        </div>',
      '        <div>',
      '          <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edEmail_' + r.id + '">Email Address <span class="text-rose-500">*</span></label>',
      '          <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edEmail_' + r.id + '" type="email" value="' + esc(r.email || '') + '">',
      '        </div>',
      '      </div>',

      '      <!-- SECTION B — Employment -->',
      '      <div class="bg-white p-3.5 rounded-xl border border-[#E1E9E3] space-y-3 shadow-2xs">',
      '        <div class="flex items-center gap-1.5 pb-1 border-b border-slate-100 text-xs font-medium text-slate-700">',
      '          <span class="material-symbols-outlined text-[16px] text-[#176B45]">work</span>',
      '          <span>Section B — Employment</span>',
      '        </div>',
      '        <div>',
      '          <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edRole_' + r.id + '">Position / Role</label>',
      '          <select class="w-full text-xs py-2 px-2.5 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edRole_' + r.id + '">',
      '            <option value="Faculty"' + (r.role === 'Faculty' ? ' selected' : '') + '>Faculty</option>',
      '            <option value="Senior Faculty"' + (r.role === 'Senior Faculty' ? ' selected' : '') + '>Senior Faculty</option>',
      '            <option value="Head of Department"' + (r.role === 'Head of Department' ? ' selected' : '') + '>Head of Department</option>',
      '            <option value="Coordinator"' + (r.role === 'Coordinator' ? ' selected' : '') + '>Coordinator</option>',
      '          </select>',
      '        </div>',
      '        <div class="grid grid-cols-2 gap-2">',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edEmploy_' + r.id + '">Category</label>',
      '            <select class="w-full text-xs py-2 px-2 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edEmploy_' + r.id + '">',
      '              <option value="Full-time"' + (r.employmentType === 'Full-time' ? ' selected' : '') + '>Full-time</option>',
      '              <option value="Part-time"' + (r.employmentType === 'Part-time' ? ' selected' : '') + '>Part-time</option>',
      '              <option value="Contract"' + (r.employmentType === 'Contract' ? ' selected' : '') + '>Contract</option>',
      '            </select>',
      '          </div>',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edYears_' + r.id + '">Years at School</label>',
      '            <input class="w-full text-xs py-2 px-2 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edYears_' + r.id + '" type="number" min="0" value="' + (r.yearsAtSchool || 0) + '">',
      '          </div>',
      '        </div>',
      '        <div>',
      '          <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edRank_' + r.id + '">Rank / Classification</label>',
      '          <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edRank_' + r.id + '" type="text" value="' + esc(r.rank || 'Senior Faculty') + '">',
      '        </div>',
      '      </div>',

      '      <!-- SECTION C — Academic Information -->',
      '      <div class="bg-white p-3.5 rounded-xl border border-[#E1E9E3] space-y-3 shadow-2xs">',
      '        <div class="flex items-center gap-1.5 pb-1 border-b border-slate-100 text-xs font-medium text-slate-700">',
      '          <span class="material-symbols-outlined text-[16px] text-[#176B45]">menu_book</span>',
      '          <span>Section C — Academic Information</span>',
      '        </div>',
      '        <div>',
      '          <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edDept_' + r.id + '">Department <span class="text-rose-500">*</span></label>',
      '          <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edDept_' + r.id + '" type="text" value="' + esc(r.department || '') + '">',
      '        </div>',
      '        <div class="grid grid-cols-2 gap-2">',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edSubject_' + r.id + '">Primary Subject <span class="text-rose-500">*</span></label>',
      '            <input class="w-full text-xs py-2 px-2.5 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edSubject_' + r.id + '" type="text" value="' + esc(r.subject || '') + '">',
      '          </div>',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edCode_' + r.id + '">Teacher Code</label>',
      '            <input class="w-full text-xs py-2 px-2.5 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] font-mono font-medium" id="edCode_' + r.id + '" type="text" value="' + esc(r.code || teacherCode) + '">',
      '          </div>',
      '        </div>',
      '        <div>',
      '          <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edQualified_' + r.id + '">Qualified Subjects</label>',
      '          <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edQualified_' + r.id + '" type="text" placeholder="e.g. Khmer, Literature, History" value="' + esc(r.qualifiedSubjects || r.subject || '') + '">',
      '        </div>',
      '      </div>',

      '      <!-- SECTION D & E — Scheduling & Status -->',
      '      <div class="bg-white p-3.5 rounded-xl border border-[#E1E9E3] space-y-3 shadow-2xs">',
      '        <div class="flex items-center gap-1.5 pb-1 border-b border-slate-100 text-xs font-medium text-slate-700">',
      '          <span class="material-symbols-outlined text-[16px] text-[#176B45]">tune</span>',
      '          <span>Section D &amp; E — Scheduling &amp; Status</span>',
      '        </div>',
      '        <div class="grid grid-cols-2 gap-2">',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edTarget_' + r.id + '">Target (hrs/wk)</label>',
      '            <input class="w-full text-xs py-2 px-2.5 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edTarget_' + r.id + '" type="number" min="1" max="40" value="' + (r.target || 17) + '">',
      '          </div>',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edMaxDaily_' + r.id + '">Max / Day</label>',
      '            <input class="w-full text-xs py-2 px-2.5 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edMaxDaily_' + r.id + '" type="number" min="1" max="10" value="' + (r.max_daily || 5) + '">',
      '          </div>',
      '        </div>',
      '        <div class="grid grid-cols-2 gap-2">',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edClasses_' + r.id + '">Classes</label>',
      '            <input class="w-full text-xs py-2 px-2 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edClasses_' + r.id + '" type="number" min="0" value="' + (r.classesAssigned != null ? r.classesAssigned : 0) + '">',
      '          </div>',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edStatus_' + r.id + '">Status</label>',
      '            <select class="w-full text-xs py-2 px-2 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edStatus_' + r.id + '">',
      '              <option value="Active"' + (String(r.status || '').toLowerCase() === 'active' ? ' selected' : '') + '>Active</option>',
      '              <option value="On Leave"' + (String(r.status || '').toLowerCase().indexOf('leave') !== -1 ? ' selected' : '') + '>On Leave</option>',
      '              <option value="Inactive"' + (String(r.status || '').toLowerCase() === 'inactive' ? ' selected' : '') + '>Inactive</option>',
      '            </select>',
      '          </div>',
      '        </div>',
      '        <div>',
      '          <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edNotes_' + r.id + '">Scheduling Notes</label>',
      '          <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edNotes_' + r.id + '" type="text" placeholder="Special availability or notes..." value="' + esc(r.notes || '') + '">',
      '        </div>',
      '      </div>',
      '    </div>',

      '    <!-- Bottom Action Bar -->',
      '    <div class="mt-5 pt-4 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-3">',
      '      <div class="flex items-center gap-2 text-xs text-slate-500">',
      '        <span class="material-symbols-outlined text-[16px] text-[#176B45]">check_circle</span>',
      '        <span>Click Save Changes to commit directly to the faculty database.</span>',
      '      </div>',
      '      <div class="flex items-center gap-2 w-full sm:w-auto justify-end">',
      '        <button type="button" data-act="reset-editor" data-id="' + esc(r.id) + '" class="px-3 py-2 text-xs font-medium text-slate-500 hover:text-slate-800 transition cursor-pointer">',
      '          Reset',
      '        </button>',
      '        <button type="button" data-act="cancel-editor" data-id="' + esc(r.id) + '" class="px-4 py-2 rounded-lg border border-[#E1E9E3] bg-white text-xs font-medium text-slate-700 hover:bg-slate-50 transition cursor-pointer">',
      '          Cancel',
      '        </button>',
      '        <button type="button" data-act="save-editor" data-id="' + esc(r.id) + '" class="px-5 py-2 rounded-lg bg-[#176B45] hover:bg-[#125638] text-white text-xs font-medium shadow-xs flex items-center gap-1.5 transition active:scale-[0.98] cursor-pointer" id="btnSaveEd_' + esc(r.id) + '">',
      '          <span class="material-symbols-outlined text-[16px]">save</span>',
      '          <span>Save Changes</span>',
      '        </button>',
      '      </div>',
      '    </div>',
      '  </div>',
      '</div>'
    ].join('\\n');
  }

  function toggleRowAccordion(id) {
    var editor = $id('editor_' + id);
    var chevron = $id('chevron_' + id);
    if (!editor) return;
    var isHidden = editor.classList.contains('hidden');
    if (isHidden) {
      editor.classList.remove('hidden');
      if (chevron) chevron.classList.add('is-open');
    } else {
      editor.classList.add('hidden');
      if (chevron) chevron.classList.remove('is-open');
    }
  }

  function openRowEditor(id) {
    var editor = $id('editor_' + id);
    var chevron = $id('chevron_' + id);
    if (!editor) return;
    editor.classList.remove('hidden');
    if (chevron) chevron.classList.add('is-open');
    var firstInput = $id('edName_' + id);
    if (firstInput) setTimeout(function () { firstInput.focus(); }, 50);
  }

  function closeRowEditor(id) {
    var editor = $id('editor_' + id);
    var chevron = $id('chevron_' + id);
    if (editor) editor.classList.add('hidden');
    if (chevron) chevron.classList.remove('is-open');
  }

  function resetRowEditor(id) {
    var r = state.all.filter(function (x) { return String(x.id) === String(id); })[0];
    if (!r) return;
    var nameEl = $id('edName_' + id); if (nameEl) nameEl.value = r.name || '';
    var genderEl = $id('edGender_' + id); if (genderEl) genderEl.value = r.gender || 'Male';
    var phoneEl = $id('edPhone_' + id); if (phoneEl) phoneEl.value = r.phone || '';
    var emailEl = $id('edEmail_' + id); if (emailEl) emailEl.value = r.email || '';
    var roleEl = $id('edRole_' + id); if (roleEl) roleEl.value = r.role || 'Faculty';
    var empEl = $id('edEmploy_' + id); if (empEl) empEl.value = r.employmentType || 'Full-time';
    var yearsEl = $id('edYears_' + id); if (yearsEl) yearsEl.value = r.yearsAtSchool || 0;
    var rankEl = $id('edRank_' + id); if (rankEl) rankEl.value = r.rank || 'Senior Faculty';
    var deptEl = $id('edDept_' + id); if (deptEl) deptEl.value = r.department || '';
    var subjEl = $id('edSubject_' + id); if (subjEl) subjEl.value = r.subject || '';
    var codeEl = $id('edCode_' + id); if (codeEl) codeEl.value = r.code || id;
    var qualEl = $id('edQualified_' + id); if (qualEl) qualEl.value = r.qualifiedSubjects || r.subject || '';
    var targetEl = $id('edTarget_' + id); if (targetEl) targetEl.value = r.target || 17;
    var maxDailyEl = $id('edMaxDaily_' + id); if (maxDailyEl) maxDailyEl.value = r.max_daily || 5;
    var clsEl = $id('edClasses_' + id); if (clsEl) clsEl.value = r.classesAssigned != null ? r.classesAssigned : 0;
    var stEl = $id('edStatus_' + id); if (stEl) stEl.value = r.status || 'Active';
    var notesEl = $id('edNotes_' + id); if (notesEl) notesEl.value = r.notes || '';
    toast('Fields reset to saved values.');
  }

  function saveRowEditor(id) {
    var name = fv('edName_' + id);
    var email = fv('edEmail_' + id);
    var department = fv('edDept_' + id);
    var subject = fv('edSubject_' + id);

    if (!name || !department || !subject || !email) {
      toast('Name, Department, Subject, and Email are required.', true);
      return;
    }

    var payload = {
      name: name,
      email: email,
      department: department,
      subject: subject,
      gender: fv('edGender_' + id),
      phone: fv('edPhone_' + id),
      role: fv('edRole_' + id),
      employmentType: fv('edEmploy_' + id),
      yearsAtSchool: parseInt(fv('edYears_' + id), 10) || 0,
      rank: fv('edRank_' + id),
      code: fv('edCode_' + id) || id,
      qualifiedSubjects: fv('edQualified_' + id),
      target: parseInt(fv('edTarget_' + id), 10) || 17,
      max_daily: parseInt(fv('edMaxDaily_' + id), 10) || 5,
      classesAssigned: parseInt(fv('edClasses_' + id), 10) || 0,
      status: fv('edStatus_' + id),
      notes: fv('edNotes_' + id)
    };

    var btn = $id('btnSaveEd_' + id);
    if (btn) btn.disabled = true;

    api(API_BASE + '/' + encodeURIComponent(id), { method: 'PUT', body: JSON.stringify(payload) })
      .then(function (res) {
        if (btn) btn.disabled = false;
        // Update in memory
        state.all.forEach(function (t) {
          if (String(t.id) === String(id)) Object.assign(t, payload);
        });
        state.filtered.forEach(function (t) {
          if (String(t.id) === String(id)) Object.assign(t, payload);
        });
        // Close editor & re-render table to reflect updated indicators
        closeRowEditor(id);
        renderTable();
        renderKpis();
        toast('Record for ' + payload.name + ' saved successfully.');
      })
      .catch(function (err) {
        if (btn) btn.disabled = false;
        toast(apiError(err, 'Failed to save teacher updates'), true);
      });
  }

  /* ---------- Inline New Teacher Form ---------- */
  function toggleNewTeacherRow() {
    var wrap = $id('newTeacherRowWrap');
    if (!wrap) return;
    var isHidden = wrap.classList.contains('hidden');
    if (!isHidden) {
      wrap.classList.add('hidden');
      return;
    }
    wrap.innerHTML = [
      '<div class="bg-white rounded-xl border-2 border-[#176B45]/40 p-5 shadow-sm space-y-4 mb-3 animate-fade-in">',
      '  <div class="flex items-center justify-between pb-3 border-b border-slate-200">',
      '    <div class="flex items-center gap-2">',
      '      <span class="w-2.5 h-2.5 rounded-full bg-[#176B45] animate-ping"></span>',
      '      <h3 class="text-sm font-medium text-slate-900">Register New Faculty Member</h3>',
      '    </div>',
      '    <button type="button" id="btnCancelNewTeacher" class="text-slate-400 hover:text-slate-600 cursor-pointer p-1 rounded-lg hover:bg-slate-100">',
      '      <span class="material-symbols-outlined text-[18px]">close</span>',
      '    </button>',
      '  </div>',
      '  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3.5 text-left text-xs">',
      '    <div>',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="new_name">Full Name <span class="text-rose-500">*</span></label>',
      '      <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45]" id="new_name" type="text" placeholder="e.g. Sok Dara">',
      '    </div>',
      '    <div>',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="new_email">Email <span class="text-rose-500">*</span></label>',
      '      <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45]" id="new_email" type="email" placeholder="e.g. sok.dara@ngis.edu.kh">',
      '    </div>',
      '    <div>',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="new_dept">Department <span class="text-rose-500">*</span></label>',
      '      <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45]" id="new_dept" type="text" placeholder="e.g. Khmer Literature">',
      '    </div>',
      '    <div>',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="new_subject">Primary Subject <span class="text-rose-500">*</span></label>',
      '      <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45]" id="new_subject" type="text" placeholder="e.g. Khmer Literature">',
      '    </div>',
      '    <div>',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="new_code">Teacher Code</label>',
      '      <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 font-mono" id="new_code" type="text" placeholder="e.g. K2">',
      '    </div>',
      '    <div>',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="new_role">Position / Role</label>',
      '      <select class="w-full text-xs py-2 px-2.5 rounded-lg border border-[#E1E9E3] bg-white text-slate-800" id="new_role">',
      '        <option value="Faculty">Faculty</option>',
      '        <option value="Senior Faculty">Senior Faculty</option>',
      '        <option value="Head of Department">Head of Department</option>',
      '        <option value="Coordinator">Coordinator</option>',
      '      </select>',
      '    </div>',
      '    <div>',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="new_target">Target Workload (hrs/wk)</label>',
      '      <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800" id="new_target" type="number" value="17" min="1" max="40">',
      '    </div>',
      '    <div>',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="new_phone">Phone</label>',
      '      <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800" id="new_phone" type="text" placeholder="+855 ...">',
      '    </div>',
      '  </div>',
      '  <div class="flex items-center justify-between pt-3 border-t border-slate-200">',
      '    <span class="text-xs text-rose-600 font-medium" id="newTeacherError"></span>',
      '    <div class="flex items-center gap-2">',
      '      <button type="button" id="btnDiscardNewTeacher" class="px-4 py-2 text-xs font-medium text-slate-700 bg-white border border-[#E1E9E3] rounded-lg hover:bg-slate-50 cursor-pointer">Cancel</button>',
      '      <button type="button" id="btnSubmitNewTeacher" class="px-5 py-2 text-xs font-medium text-white bg-[#176B45] hover:bg-[#125638] rounded-lg shadow-xs cursor-pointer flex items-center gap-1.5"><span class="material-symbols-outlined text-[16px]">person_add</span><span>Register Teacher</span></button>',
      '    </div>',
      '  </div>',
      '</div>'
    ].join('\\n');

    wrap.classList.remove('hidden');

    $id('btnCancelNewTeacher').addEventListener('click', function () { wrap.classList.add('hidden'); });
    $id('btnDiscardNewTeacher').addEventListener('click', function () { wrap.classList.add('hidden'); });
    $id('btnSubmitNewTeacher').addEventListener('click', submitNewTeacher);
  }

  function submitNewTeacher() {
    var name = fv('new_name');
    var email = fv('new_email');
    var dept = fv('new_dept');
    var subject = fv('new_subject');
    var errEl = $id('newTeacherError');

    if (!name || !email || !dept || !subject) {
      if (errEl) errEl.textContent = 'Name, email, department, and subject are required.';
      return;
    }

    var body = {
      name: name,
      email: email,
      department: dept,
      subject: subject,
      role: fv('new_role') || 'Faculty',
      code: fv('new_code') || '',
      target: parseInt(fv('new_target'), 10) || 17,
      phone: fv('new_phone') || '',
      status: 'active'
    };

    var btn = $id('btnSubmitNewTeacher');
    if (btn) btn.disabled = true;

    api(API_BASE, { method: 'POST', body: JSON.stringify(body) })
      .then(function (res) {
        if (btn) btn.disabled = false;
        var newRec = (res && res.data) || body;
        state.all.unshift(newRec);
        $id('newTeacherRowWrap').classList.add('hidden');
        applyFilters();
        toast('Teacher ' + name + ' registered successfully.');
      })
      .catch(function (err) {
        if (btn) btn.disabled = false;
        if (errEl) errEl.textContent = apiError(err, 'Failed to create teacher record');
      });
  }

  /* ---------- Excel Bulk Import Workflow ---------- */
  var parsedExcelTeachers = [];
  function openExcelImportModal() {
    var m = $id('excelImportModal');
    if (!m) return;
    $id('excelPasteInput').value = '';
    $id('excelPreviewSection').classList.add('hidden');
    $id('excelImportError').textContent = '';
    $id('btnExecuteExcelImport').disabled = true;
    parsedExcelTeachers = [];
    m.classList.remove('hidden');
  }

  function closeExcelImportModal() {
    var m = $id('excelImportModal');
    if (m) m.classList.add('hidden');
  }
  window.__ngisCloseExcelModal = closeExcelImportModal;

  function renderTable() {
    if (IS_TEACHER) {
      var rowsContainer = $id('dirRows');
      if (!rowsContainer) return;
      if (state.loading) {
        rowsContainer.innerHTML = '<div class="py-12 text-center text-slate-500 bg-white rounded-xl border border-[#E1E9E3]"><div class="flex flex-col items-center justify-center gap-2"><span class="material-symbols-outlined text-4xl text-[#94a3b8] animate-spin opacity-60">progress_active</span><p class="font-medium text-sm">Loading live directory...</p></div></div>';
        renderPager(); return;
      }
      if (state.error) {
        rowsContainer.innerHTML = '<div class="py-12 text-center text-rose-600 bg-white rounded-xl border border-[#E1E9E3]"><div class="flex flex-col items-center justify-center gap-2"><span class="material-symbols-outlined text-4xl text-[#B3261E] opacity-70">cloud_off</span><p class="font-medium text-sm text-[#B3261E]">' + esc(state.error) + '</p></div></div>';
        renderPager(); return;
      }
      if (!state.filtered.length) {
        rowsContainer.innerHTML = '<div class="py-12 text-center text-slate-500 bg-white rounded-xl border border-[#E1E9E3]"><div class="flex flex-col items-center justify-center gap-2"><span class="material-symbols-outlined text-4xl text-[#94a3b8] opacity-40">person_search</span><p class="font-medium text-sm">No teachers match your active filters</p><button type="button" class="text-xs text-[#176B45] hover:underline mt-1 font-medium cursor-pointer" id="emptyReset">Reset Filters</button></div></div>';
        var er = $id('emptyReset');
        if (er) er.addEventListener('click', resetAllFilters);
        renderPager(); return;
      }
      var start = (state.page - 1) * PER_PAGE;
      var pageRows = state.filtered.slice(start, start + PER_PAGE);
      rowsContainer.innerHTML = pageRows.map(teacherRowHtml).join('\\n');
      renderPager();
      return;
    }

    var body = $id('dirBody');
    if (!body) return;
    if (state.loading) {
      body.innerHTML = '<tr><td colspan="9" class="py-12 text-center text-slate-500"><div class="flex flex-col items-center justify-center gap-2"><span class="material-symbols-outlined text-4xl text-[#94a3b8] animate-spin opacity-60">progress_active</span><p class="font-medium text-sm">Loading live directory...</p></div></td></tr>';
      renderPager(); return;
    }
    if (state.error) {
      body.innerHTML = '<tr><td colspan="9" class="py-12 text-center text-rose-600"><div class="flex flex-col items-center justify-center gap-2"><span class="material-symbols-outlined text-4xl text-[#B3261E] opacity-70">cloud_off</span><p class="font-medium text-sm text-[#B3261E]">' + esc(state.error) + '</p></div></td></tr>';
      renderPager(); return;
    }
    if (!state.filtered.length) {
      body.innerHTML = '<tr><td colspan="9" class="py-12 text-center text-slate-500"><div class="flex flex-col items-center justify-center gap-2"><span class="material-symbols-outlined text-4xl text-[#94a3b8] opacity-40">person_search</span><p class="font-medium text-sm">No ' + PLURAL_LABEL.toLowerCase() + ' match your active filters</p><button type="button" class="text-xs text-slate-600 hover:underline mt-1 font-medium cursor-pointer" id="emptyReset">Reset Filters</button></div></td></tr>';
      var er2 = $id('emptyReset');
      if (er2) er2.addEventListener('click', resetAllFilters);
      renderPager(); return;
    }
    var start2 = (state.page - 1) * PER_PAGE;
    var pageRows2 = state.filtered.slice(start2, start2 + PER_PAGE);
    body.innerHTML = pageRows2.map(function (r) {
      var isActive2 = String(r.status || '').toLowerCase() === 'active';
      var actions2 = '<div class="inline-flex items-center gap-1.5">' +
        '<button type="button" data-act="view" data-id="' + esc(r.id) + '" class="px-3 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 border border-slate-200/70 rounded-lg hover:bg-[#176B45] hover:text-white hover:border-[#176B45] transition-colors cursor-pointer min-h-[32px]">' +
          'Profile' +
        '</button>' +
        '<button type="button" data-act="edit" data-id="' + esc(r.id) + '" class="px-3 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 border border-slate-200/70 rounded-lg hover:bg-[#176B45] hover:text-white hover:border-[#176B45] transition-colors cursor-pointer min-h-[32px]">' +
          'Edit' +
        '</button>' +
        '<button type="button" data-act="toggle" data-id="' + esc(r.id) + '" title="' + (isActive2 ? 'Deactivate record' : 'Activate record') + '" class="p-1 text-slate-400 hover:text-slate-700 rounded transition-colors cursor-pointer min-h-[32px] min-w-[32px] flex items-center justify-center" aria-label="Toggle status">' +
          '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="1" fill="currentColor"></circle><circle cx="12" cy="5" r="1" fill="currentColor"></circle><circle cx="12" cy="19" r="1" fill="currentColor"></circle></svg>' +
        '</button>' +
        '</div>';
      return '<tr class="transition-colors group" data-id="' + esc(r.id) + '"><td class="py-3.5 pl-4 pr-2 align-middle"><input class="row-checkbox rounded border-slate-300 text-[#176B45] focus:ring-[#176B45]/20 focus:ring-offset-0 cursor-pointer accent-[#176B45]" type="checkbox" data-id="' + esc(r.id) + '"></td>' +
        '<td class="py-3.5 px-4 align-middle">' + nameCell(r) + '</td>' +
        '<td class="py-3.5 px-4 align-middle"><div class="font-medium text-sm text-slate-900">' + esc(r.grade || '—') + '</div><div class="text-[11px] text-slate-500">' + esc(r.class || '—') + '</div></td>' +
        '<td class="py-3.5 px-4 align-middle font-medium text-sm text-slate-800">' + esc(r.advisor || '—') + '</td>' +
        '<td class="py-3.5 px-4 align-middle font-headline-sm text-sm font-medium text-[#176B45]">' + (r.gpaLive == null ? '—' : num(r.gpaLive)) + '</td>' +
        '<td class="py-3.5 px-4 align-middle"><span class="inline-flex items-center px-2 py-0.5 rounded-full font-medium text-xs bg-slate-50 font-medium ' + (Number(r.attendancePct) < 85 ? 'text-[#B3261E]' : 'text-slate-600') + '">' + (r.attendancePct == null ? '—' : num(r.attendancePct, 1) + '%') + '</span></td>' +
        '<td class="py-3.5 px-4 align-middle font-medium text-sm text-slate-800">' + (r.openRequests || 0) + '</td>' +
        '<td class="py-3.5 px-4 align-middle">' + statusBadge(r.status) + '</td>' +
        '<td class="py-3.5 pr-4 pl-4 text-right align-middle">' + actions2 + '</td></tr>';
    }).join('');
    renderPager();
  }
'''

code = code[:idx_start] + replacement + code[idx_end:]
print("Replaced renderTable and added teacherRowHtml")

with open(profiles_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Saved ngis-profiles.js checkpoint 2")

