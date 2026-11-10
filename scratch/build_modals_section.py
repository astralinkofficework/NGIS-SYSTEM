profiles_path = r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\assets\js\ngis-profiles.js'

with open(profiles_path, 'r', encoding='utf-8') as f:
    code = f.read()

idx_start = code.find("  function mountModals() {")
idx_end = code.find("  function boot() {")
assert idx_start != -1 and idx_end != -1, "modal bounds not found"

replacement = '''  function mountModals() {
    var wrap = document.createElement('div');
    wrap.innerHTML = [
      // Profile modal
      '<div id="profileModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 md:p-8 bg-slate-900/40 backdrop-blur-sm transition-opacity" role="dialog" aria-modal="true" aria-labelledby="profileModalTitle" onclick="if(event.target===this)__ngisCloseProfile()">',
      '  <div id="profileModalInner" class="w-full max-w-2xl bg-white rounded-2xl shadow-2xl border border-slate-200/90 overflow-hidden max-h-[90vh] flex flex-col relative animate-fade-in"></div>',
      '</div>',
      // Add/edit form modal
      '<div id="formModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 md:p-8 bg-slate-900/40 backdrop-blur-sm transition-opacity" role="dialog" aria-modal="true" onclick="if(event.target===this)window.__ngisCloseForm()">',
      '  <div class="w-full max-w-lg bg-white rounded-2xl shadow-2xl border border-slate-200/90 overflow-hidden max-h-[90vh] flex flex-col relative animate-fade-in">',
      '    <div class="px-6 sm:px-7 pt-6 pb-5 border-b border-[#E1E9E3] flex items-center justify-between">',
      '      <div class="flex items-center gap-2"><span class="material-symbols-outlined text-slate-400 text-[18px]">edit_note</span><h3 class="text-base font-medium text-slate-900" id="formTitle">Edit Record</h3></div>',
      '      <button type="button" onclick="window.__ngisCloseForm()" class="text-slate-400 hover:text-slate-600 rounded-lg p-1.5 hover:bg-slate-100 transition-colors cursor-pointer min-h-[36px] min-w-[36px] flex items-center justify-center" aria-label="Close modal">',
      '        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>',
      '      </button>',
      '    </div>',
      '    <div class="p-4 sm:p-6 overflow-y-auto pf-scroll" id="formFields"></div>',
      '    <div class="px-6 sm:px-7 py-4 border-t border-[#E1E9E3] bg-[#F7F9F7]/50 flex items-center justify-between gap-2">',
      '      <span class="text-xs text-[#B3261E] font-medium" id="formError"></span>',
      '      <div class="flex items-center gap-2 ml-auto">',
      '        <button type="button" onclick="window.__ngisCloseForm()" class="px-4 py-2 text-xs font-medium text-slate-700 bg-white border border-[#E1E9E3] rounded-lg hover:bg-[#F7F9F7] transition-all cursor-pointer min-h-[40px]">Cancel</button>',
      '        <button type="button" id="formSaveBtn" class="px-4 py-2 text-xs font-medium text-white bg-[#176B45] hover:bg-[#125638] rounded-lg shadow-xs active:scale-95 transition-all cursor-pointer min-h-[40px] flex items-center justify-center gap-2"><span class="material-symbols-outlined text-[16px]">save</span><span>Save</span></button>',
      '      </div>',
      '    </div>',
      '  </div>',
      '</div>',
      // Bulk Excel Import Modal
      '<div id="excelImportModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 md:p-8 bg-slate-900/40 backdrop-blur-sm transition-opacity" role="dialog" aria-modal="true" onclick="if(event.target===this)window.__ngisCloseExcelModal()">',
      '  <div class="w-full max-w-2xl bg-white rounded-2xl shadow-2xl border border-slate-200/90 overflow-hidden max-h-[90vh] flex flex-col relative animate-fade-in">',
      '    <div class="px-6 sm:px-7 pt-6 pb-4 border-b border-[#E1E9E3] flex items-center justify-between">',
      '      <div class="flex items-center gap-2.5">',
      '        <span class="material-symbols-outlined text-[#176B45] text-[24px]">content_paste</span>',
      '        <div>',
      '          <h3 class="text-base font-medium text-slate-900 leading-tight">Paste &amp; Import from Excel</h3>',
      '          <p class="text-[11px] text-slate-500 mt-0.5">Copy columns from Excel or Google Sheets (Name, Subject, Department, Email, Code, Workload) and paste below</p>',
      '        </div>',
      '      </div>',
      '      <button type="button" onclick="window.__ngisCloseExcelModal()" class="text-slate-400 hover:text-slate-600 rounded-lg p-1.5 hover:bg-slate-100 transition-colors cursor-pointer" aria-label="Close modal">',
      '        <span class="material-symbols-outlined text-[20px]">close</span>',
      '      </button>',
      '    </div>',
      '    <div class="p-6 space-y-4 overflow-y-auto pf-scroll">',
      '      <div>',
      '        <label class="block text-xs font-medium text-slate-700 mb-1.5" for="excelPasteInput">Paste Tabular Data (Ctrl+V)</label>',
      '        <textarea id="excelPasteInput" rows="6" class="w-full text-xs font-mono p-3 rounded-xl border border-[#E1E9E3] bg-[#F7F9F7] text-slate-800 placeholder:text-slate-400 focus:bg-white focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] transition-all" placeholder="Sok Dara\\tKhmer Literature\\tMoEYS Faculty\\tsok.dara@ngis.edu.kh\\tK1\\t17\\nChou Meng\\tMathematics\\tScience & Math\\tchou.meng@ngis.edu.kh\\tM1\\t18"></textarea>',
      '      </div>',
      '      <div id="excelPreviewSection" class="hidden space-y-2">',
      '        <div class="flex items-center justify-between text-xs font-medium text-slate-700">',
      '          <span>Parsed Records Preview (<span id="excelParsedCount">0</span> teachers detected)</span>',
      '          <span class="text-[11px] text-emerald-700 font-medium" id="excelValidCount"></span>',
      '        </div>',
      '        <div class="border border-[#E1E9E3] rounded-xl overflow-hidden max-h-48 overflow-y-auto">',
      '          <table class="w-full text-left text-xs whitespace-nowrap min-w-full">',
      '            <thead class="bg-slate-50 border-b border-slate-200 text-slate-500 font-medium text-[11px]">',
      '              <tr><th class="py-2 px-3">Name</th><th class="py-2 px-3">Subject</th><th class="py-2 px-3">Department</th><th class="py-2 px-3">Email</th><th class="py-2 px-3">Code</th><th class="py-2 px-3">Workload</th></tr>',
      '            </thead>',
      '            <tbody id="excelPreviewBody" class="divide-y divide-slate-100 bg-white"></tbody>',
      '          </table>',
      '        </div>',
      '      </div>',
      '    </div>',
      '    <div class="px-6 py-4 border-t border-[#E1E9E3] bg-[#F7F9F7]/50 flex items-center justify-between gap-2">',
      '      <span class="text-xs text-rose-600 font-medium" id="excelImportError"></span>',
      '      <div class="flex items-center gap-2 ml-auto">',
      '        <button type="button" onclick="window.__ngisCloseExcelModal()" class="px-4 py-2 text-xs font-medium text-slate-700 bg-white border border-[#E1E9E3] rounded-lg hover:bg-[#F7F9F7] transition-all cursor-pointer">Cancel</button>',
      '        <button type="button" id="btnExecuteExcelImport" disabled class="px-5 py-2 text-xs font-medium text-white bg-[#176B45] hover:bg-[#125638] disabled:opacity-40 disabled:cursor-not-allowed rounded-lg shadow-xs transition-all cursor-pointer flex items-center gap-1.5"><span class="material-symbols-outlined text-[16px]">file_download</span><span>Import Records</span></button>',
      '      </div>',
      '    </div>',
      '  </div>',
      '</div>',
      // Confirm / reason dialog
      '<div id="confirmModal" class="hidden fixed inset-0 z-[70] flex items-center justify-center p-4 sm:p-6 bg-black/40 backdrop-blur-xs">',
      '  <div class="bg-white rounded-2xl shadow-sm border border-[#E1E9E3] max-w-md w-full p-6">',
      '    <h3 class="text-base font-medium text-[#29352E] mb-1.5"></h3>',
      '    <p class="text-sm text-slate-600 mb-4" id="cfMessage"></p>',
      '    <div id="cfReasonWrap" class="mb-4">',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="cfReason">Written reason <span class="text-[#B3261E]">*</span> <span class="text-xs text-slate-400 normal-case">(required by audit policy)</span></label>',
      '      <textarea class="w-full text-xs py-2 pl-3 pr-4 rounded-lg border border-[#E1E9E3] bg-white text-slate-700 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="cfReason" rows="2" placeholder="e.g. Contract ended per HR letter dated 2026-09-30"></textarea>',
      '      <span class="text-[11px] text-[#B3261E] hidden" id="cfReasonError">A reason is required before this action can be confirmed.</span>',
      '    </div>',
      '    <div class="flex items-center justify-end gap-2">',
      '      <button type="button" id="cfCancel" class="px-4 py-2 text-xs font-medium text-slate-700 bg-white border border-[#E1E9E3] rounded-lg hover:bg-[#F7F9F7] transition-all cursor-pointer min-h-[40px]">Cancel</button>',
      '      <button type="button" id="cfOk" class="px-4 py-2 text-xs font-medium text-white bg-[#176B45] hover:bg-[#125638] rounded-lg shadow-xs transition-all cursor-pointer min-h-[40px]">Confirm</button>',
      '    </div>',
      '  </div>',
      '</div>',
      // Toast
      '<div id="ngisToast" role="status" aria-live="polite" class="fixed bottom-24 right-24 bg-[#29352E] text-white px-4 py-3 rounded-lg font-medium text-xs shadow-lg z-1200 hidden">Toast</div>'
    ].join('\\n');
    while (wrap.firstChild) document.body.appendChild(wrap.firstChild);

    window.__ngisCloseForm = closeForm;
    $id('formSaveBtn').addEventListener('click', saveForm);
    $id('cfCancel').addEventListener('click', function () { closeConfirm(null); });
    $id('cfOk').addEventListener('click', function () {
      var requireReason = $id('cfReasonWrap').style.display !== 'none';
      var reason = $id('cfReason').value.trim();
      if (requireReason && !reason) { $id('cfReasonError').classList.remove('hidden'); return; }
      closeConfirm(requireReason ? reason : true);
    });
    $id('confirmModal').addEventListener('click', function (e) {
      if (e.target === this) closeConfirm(null);
    });

    // Excel import textarea parsing
    var pasteArea = $id('excelPasteInput');
    if (pasteArea) {
      pasteArea.addEventListener('input', function () {
        var raw = pasteArea.value.trim();
        if (!raw) {
          $id('excelPreviewSection').classList.add('hidden');
          $id('btnExecuteExcelImport').disabled = true;
          return;
        }
        var lines = raw.split(/\\r?\\n/).filter(function (l) { return l.trim().length > 0; });
        parsedExcelTeachers = [];
        lines.forEach(function (line) {
          var parts = line.split(/[\\t,]/).map(function (p) { return p.trim(); });
          if (parts.length >= 2) {
            // Ignore header row if detected
            if (parts[0].toLowerCase() === 'name' || parts[0].toLowerCase() === 'full name') return;
            var rec = {
              name: parts[0] || '',
              subject: parts[1] || 'General',
              department: parts[2] || 'Faculty',
              email: parts[3] || (parts[0].toLowerCase().replace(/\\s+/g, '.') + '@ngis.edu.kh'),
              code: parts[4] || '',
              target: parseInt(parts[5], 10) || 17,
              role: 'Faculty',
              status: 'active'
            };
            if (rec.name) parsedExcelTeachers.push(rec);
          }
        });

        $id('excelParsedCount').textContent = parsedExcelTeachers.length;
        $id('excelValidCount').textContent = parsedExcelTeachers.length + ' ready to import';
        var pBody = $id('excelPreviewBody');
        if (pBody) {
          pBody.innerHTML = parsedExcelTeachers.slice(0, 15).map(function (t) {
            return '<tr class="border-b border-slate-100"><td class="py-2 px-3 font-medium text-slate-800">' + esc(t.name) + '</td><td class="py-2 px-3">' + esc(t.subject) + '</td><td class="py-2 px-3">' + esc(t.department) + '</td><td class="py-2 px-3 font-mono text-[11px]">' + esc(t.email) + '</td><td class="py-2 px-3 font-mono">' + esc(t.code || '—') + '</td><td class="py-2 px-3">' + t.target + ' hrs</td></tr>';
          }).join('') + (parsedExcelTeachers.length > 15 ? '<tr><td colspan="6" class="py-1 px-3 text-center text-slate-400 text-[11px]">... and ' + (parsedExcelTeachers.length - 15) + ' more records</td></tr>' : '');
        }
        $id('excelPreviewSection').classList.remove('hidden');
        $id('btnExecuteExcelImport').disabled = parsedExcelTeachers.length === 0;
      });
    }

    var btnExecExcel = $id('btnExecuteExcelImport');
    if (btnExecExcel) {
      btnExecExcel.addEventListener('click', function () {
        if (!parsedExcelTeachers.length) return;
        btnExecExcel.disabled = true;
        var importedCount = 0;
        var promises = parsedExcelTeachers.map(function (t) {
          return api(API_BASE, { method: 'POST', body: JSON.stringify(t) })
            .then(function (res) {
              importedCount++;
              if (res && res.data) state.all.unshift(res.data);
            })
            .catch(function () {});
        });

        Promise.all(promises).then(function () {
          btnExecExcel.disabled = false;
          closeExcelImportModal();
          applyFilters();
          toast('Successfully imported ' + importedCount + ' teachers from Excel.');
        });
      });
    }

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        if (!$id('confirmModal').classList.contains('hidden')) closeConfirm(null);
        else if (!$id('formModal').classList.contains('hidden')) closeForm();
        else if (!$id('profileModal').classList.contains('hidden')) closeProfile();
        else if (!$id('excelImportModal').classList.contains('hidden')) closeExcelImportModal();
      }
    });
  }
'''

code = code[:idx_start] + replacement + code[idx_end:]
print("Replaced mountModals and wired Excel import")

with open(profiles_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Saved ngis-profiles.js checkpoint 3")

