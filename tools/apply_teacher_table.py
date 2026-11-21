import re

file_path = 'assets/js/ngis-profiles.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Replace teacherRowHtml
pattern_teacher_row = r'/\* ---------- Teacher Row Card & Inline Accordion Editor ---------- \*/\s*function teacherRowHtml\(r\) \{[\s\S]*?\}\n\s*function toggleRowAccordion\(id\)'

replacement_teacher_row = '''/* ---------- Teacher Row Table Architecture ---------- */
  function teacherRowHtml(r) {
    var teacherCode = r.code || r.id || 'TCH';
    var subjectColor = getSubjectColor(r.subject);
    var classesAssigned = (r.assignments && r.assignments.length) ? r.assignments.length : (r.classesAssigned != null ? r.classesAssigned : (r.classes ? r.classes.length : 0));
    var isActive = String(r.status || '').toLowerCase() === 'active';

    var deptSummary = esc(r.department || 'MoEYS Faculty');
    var subjectLabel = esc(r.subject || 'General');
    if (r.assignments && r.assignments.length > 0) {
      var dMap = {};
      r.assignments.forEach(function (a) {
        var d = (a.department || '').replace(' Studies', '').replace(' Language', '').replace(' Department', '');
        dMap[d] = dMap[d] || [];
        var c = (a.class || '').replace('Grade ', '');
        if (c && dMap[d].indexOf(c) === -1) dMap[d].push(c);
      });
      var dKeys = Object.keys(dMap);
      if (dKeys.length > 1) {
        deptSummary = dKeys.map(function (k) { return k + ': ' + dMap[k].join(', '); }).join(' · ');
      } else if (dKeys.length === 1 && dMap[dKeys[0]].length > 0) {
        deptSummary = dKeys[0] + ': ' + dMap[dKeys[0]].join(', ');
      }
      var distinctSubjs = [];
      r.assignments.forEach(function (a) {
        if (a.subject && distinctSubjs.indexOf(a.subject) === -1) distinctSubjs.push(a.subject);
      });
      if (distinctSubjs.length > 1) {
        subjectLabel = esc(distinctSubjs.slice(0, 2).join(', ')) + (distinctSubjs.length > 2 ? ' +' + (distinctSubjs.length - 2) : '');
      }
    }

    var actions = '<div class="inline-flex items-center gap-1.5">' +
      '<button type="button" data-act="view" data-id="' + esc(r.id) + '" class="px-3 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 border border-slate-200/70 rounded-lg hover:bg-[#176B45] hover:text-white hover:border-[#176B45] transition-colors cursor-pointer min-h-[32px]">' +
        'Profile' +
      '</button>' +
      '<button type="button" data-act="edit" data-id="' + esc(r.id) + '" class="px-3 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 border border-slate-200/70 rounded-lg hover:bg-[#176B45] hover:text-white hover:border-[#176B45] transition-colors cursor-pointer min-h-[32px]">' +
        'Edit' +
      '</button>' +
      '<button type="button" data-act="toggle" data-id="' + esc(r.id) + '" title="' + (isActive ? 'Deactivate record' : 'Activate record') + '" class="p-1 text-slate-400 hover:text-slate-700 rounded transition-colors cursor-pointer min-h-[32px] min-w-[32px] flex items-center justify-center" aria-label="Toggle status">' +
        '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="1" fill="currentColor"></circle><circle cx="12" cy="5" r="1" fill="currentColor"></circle><circle cx="12" cy="19" r="1" fill="currentColor"></circle></svg>' +
      '</button>' +
    '</div>';

    return '<tr class="transition-colors group hover:bg-slate-50/50" data-id="' + esc(r.id) + '">' +
      '<td class="py-3.5 pl-4 pr-2 align-middle"><input class="row-checkbox rounded border-slate-300 text-[#176B45] focus:ring-[#176B45]/20 focus:ring-offset-0 cursor-pointer accent-[#176B45]" type="checkbox" data-id="' + esc(r.id) + '"></td>' +
      '<td class="py-3.5 px-4 align-middle">' + nameCell(r) + '</td>' +
      '<td class="py-3.5 px-4 align-middle"><span class="px-2 py-0.5 rounded text-[11px] font-mono font-medium bg-slate-100 text-slate-700 border border-slate-200/80">' + esc(teacherCode) + '</span></td>' +
      '<td class="py-3.5 px-4 align-middle text-slate-700">' + esc(r.campus || 'Main Campus') + '</td>' +
      '<td class="py-3.5 px-4 align-middle text-slate-700">' + esc(r.department || 'MoEYS Faculty') + '</td>' +
      '<td class="py-3.5 px-4 align-middle">' +
        '<div class="flex items-center gap-1.5">' +
          '<span class="w-2 h-2 rounded-full shrink-0" style="background-color: ' + subjectColor + ';"></span>' +
          '<span class="font-medium text-slate-800">' + subjectLabel + '</span>' +
        '</div>' +
        '<div class="text-[11px] text-slate-500 ml-3.5">' + deptSummary + ' (' + classesAssigned + ' classes)</div>' +
      '</td>' +
      '<td class="py-3.5 px-4 align-middle">' + statusBadge(r.status) + '</td>' +
      '<td class="py-3.5 pr-4 pl-4 text-right align-middle">' + actions + '</td>' +
    '</tr>';
  }

  function toggleRowAccordion(id)'''

code, count1 = re.subn(pattern_teacher_row, replacement_teacher_row, code, count=1)
print(f"Substituted teacherRowHtml: {count1}")

# 2. Replace renderTable
pattern_render_table = r'function renderTable\(\) \{[\s\S]*?renderPager\(\);\s*\}\s*function renderPager'

replacement_render_table = '''function renderTable() {
    var body = $id('dirBody');
    if (!body) return;
    var colSpanCount = IS_TEACHER ? 8 : 9;
    if (state.loading) {
      body.innerHTML = (function() {
        if (window.NGIS_SKELETON) {
          var out = '';
          for (var k = 0; k < 6; k++) {
            out += '<tr><td colspan="' + colSpanCount + '" class="p-3">' +
              '<div class="flex items-center gap-3">' +
                window.NGIS_SKELETON.avatar({ size: "sm" }) +
                '<div class="flex-1 flex flex-col gap-1">' +
                  window.NGIS_SKELETON.text({ width: (40 + (k % 3) * 20) + "%", size: "sm" }) +
                  window.NGIS_SKELETON.text({ width: "25%", size: "xs" }) +
                '</div>' +
                window.NGIS_SKELETON.badge({ width: "70px" }) +
              '</div>' +
            '</td></tr>';
          }
          return out;
        }
        return '<tr><td colspan="' + colSpanCount + '" class="p-4"></td></tr>';
      })();
      renderPager(); return;
    }
    if (state.error) {
      body.innerHTML = '<tr><td colspan="' + colSpanCount + '" class="py-12 text-center text-rose-600"><div class="flex flex-col items-center justify-center gap-2.5"><span class="material-symbols-outlined text-4xl text-[#B3261E] opacity-70">cloud_off</span><p class="font-medium text-sm text-[#B3261E]">' + esc(state.error) + '</p><button type="button" class="mt-2 px-3.5 py-1.5 rounded-lg bg-[#176B45] text-white hover:bg-[#125638] text-xs font-medium transition cursor-pointer" id="btnRetryLoad">Retry</button></div></td></tr>';
      var rb = $id('btnRetryLoad');
      if (rb) rb.addEventListener('click', loadDirectory);
      renderPager(); return;
    }
    if (!state.filtered.length) {
      body.innerHTML = '<tr><td colspan="' + colSpanCount + '" class="py-12 text-center text-slate-500"><div class="flex flex-col items-center justify-center gap-2"><span class="material-symbols-outlined text-4xl text-[#94a3b8] opacity-40">person_search</span><p class="font-medium text-sm">No ' + PLURAL_LABEL.toLowerCase() + ' match your active filters</p><button type="button" class="text-xs text-slate-600 hover:underline mt-1 font-medium cursor-pointer" id="emptyReset">Reset Filters</button></div></td></tr>';
      var er = $id('emptyReset');
      if (er) er.addEventListener('click', resetAllFilters);
      renderPager(); return;
    }
    var start = (state.page - 1) * PER_PAGE;
    var pageRows = state.filtered.slice(start, start + PER_PAGE);
    if (IS_TEACHER) {
      body.innerHTML = pageRows.map(teacherRowHtml).join('');
    } else {
      body.innerHTML = pageRows.map(function (r) {
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
        return '<tr class="transition-colors group hover:bg-slate-50/50" data-id="' + esc(r.id) + '"><td class="py-3.5 pl-4 pr-2 align-middle"><input class="row-checkbox rounded border-slate-300 text-[#176B45] focus:ring-[#176B45]/20 focus:ring-offset-0 cursor-pointer accent-[#176B45]" type="checkbox" data-id="' + esc(r.id) + '"></td>' +
          '<td class="py-3.5 px-4 align-middle">' + nameCell(r) + '</td>' +
          '<td class="py-3.5 px-4 align-middle"><div class="font-medium text-sm text-slate-900">' + esc(r.grade || '—') + '</div><div class="text-[11px] text-slate-500">' + esc(r.class || '—') + '</div></td>' +
          '<td class="py-3.5 px-4 align-middle font-medium text-sm text-slate-800">' + esc(r.advisor || '—') + '</td>' +
          '<td class="py-3.5 px-4 align-middle font-headline-sm text-sm font-medium text-[#176B45]">' + (r.gpaLive == null ? '—' : num(r.gpaLive)) + '</td>' +
          '<td class="py-3.5 px-4 align-middle"><span class="inline-flex items-center px-2 py-0.5 rounded-full font-medium text-xs bg-slate-50 font-medium ' + (Number(r.attendancePct) < 85 ? 'text-[#B3261E]' : 'text-slate-600') + '">' + (r.attendancePct == null ? '—' : num(r.attendancePct, 1) + '%') + '</span></td>' +
          '<td class="py-3.5 px-4 align-middle font-medium text-sm text-slate-800">' + (r.openRequests || 0) + '</td>' +
          '<td class="py-3.5 px-4 align-middle">' + statusBadge(r.status) + '</td>' +
          '<td class="py-3.5 pr-4 pl-4 text-right align-middle">' + actions2 + '</td></tr>';
      }).join('');
    }
    renderPager();
  }
  function renderPager'''

code, count2 = re.subn(pattern_render_table, replacement_render_table, code, count=1)
print(f"Substituted renderTable: {count2}")

if count1 == 1 and count2 == 1:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Successfully updated assets/js/ngis-profiles.js!")
else:
    print("Failed to replace pattern.")
