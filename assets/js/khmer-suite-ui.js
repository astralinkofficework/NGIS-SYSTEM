/* ============================================================================
   Khmer School Admin Suite — UI renderer
   Complete Timetable Management Replacement for Cambodian Schools
   Three-Step Workflow:
     STEP 1 — Data Entry & Academic Setup
     STEP 2 — Teacher–Class Assignment
     STEP 3 — Timetable Builder & Publishing
   ========================================================================== */
(function (global) {
  'use strict';

  var D = global.KSData, E = global.KSEngine;
  var MODULE = global.KS_MODULE || 'builder';
  var ROLE = (global.PAGE && global.PAGE.role) || 'principal';
  var root = null;
  var ctx = { state: null, stats: null, grid: {} };
  var ui = E.ui || {};

  var local = {
    selectedClass: ui.selectedClass || 'class_7A',
    selectedTeacherId: 't_K1',
    selectedChip: null,
    viewMode: 'class', // 'class' | 'teacher' | 'school'
    modeTab: ui.modeTab || 'start',
    preview: false,
    modal: null,
    quickEditKey: null,
    highlightSlotKey: null,
    selectedMobileDay: 'ច័ន្ទ',
    lastSavedAt: null,
    aiProposal: null,
    viewer: { week: ui.week || 21, day: ui.day || D.DAYS[0], period: ui.period || 'ព្រឹក|1', q: '' },
    // Step 1 Data Entry sub-tabs: 'teachers' | 'details' | 'grades' | 'subjects' | 'classes' | 'import' | 'unavail'
    dataTab: 'teachers',
    selectedGrade: 7,
    activeCell: { row: 0, col: 1 },
    teacherFilterSubject: 'all',
    teacherSearchQ: '',
    assignmentSubjectId: null,
    toastTimer: [],
    showAllTeachers: false
  };

  var rafPending = false;

  var MODULES = [
    { id: 'wizard',   n: '1', label: 'Teacher Assignment',  sub: 'Workload & Allocation', file: ROLE + '-teacher-class-assignment.html' },
    { id: 'builder',  n: '2', label: 'Timetable Builder',   sub: 'Schedule & Publish',    file: ROLE + '-timetable-builder.html' },
    { id: 'viewer',   n: '', label: 'Timetables Matrix',   sub: 'School Overview',       file: ROLE + '-timetables.html' },
    { id: 'subjects', n: '', label: 'Curriculum Subjects', sub: 'Catalog & Hours',      file: ROLE + '-subjects.html' }
  ];

  function esc(v) {
    return String(v == null ? '' : v)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  function kh(v) { return D.kh(v); }
  function clsMap(state) {
    var m = {}; (state.classes || []).forEach(function (c) { m[c.id] = c.display; }); return m;
  }
  function colorOf(state, subjectId) {
    var s = (E.index().subjects || {})[subjectId]; return s ? s.color : '#E5E7EB';
  }
  function persistUI() {
    E.setUI({
      selectedClass: local.selectedClass, modeTab: local.modeTab,
      week: local.viewer.week, day: local.viewer.day, period: local.viewer.period
    });
  }

  /* ── 1. Master 3-Step Horizontal Workflow Stepper ───────────────────────── */

  function workflowStepperHtml() {
    return '';
  }

  function headHtml() {
    var inst = ctx.state.institution || {};
    var schoolName = inst.name_en || 'New Generation International School';
    return '<div class="ks-head">' +
      '<div class="ks-head-left">' +
        '<div class="ks-mark">⌘</div>' +
        '<div class="ks-institution">' +
          '<span style="font-size:15px;font-weight:500;color:var(--ks-text,#1F2937)">' + esc(schoolName) + '</span>' +
          '<div class="ks-head-meta">' +
            '<span class="ks-tag">' + esc(inst.academic_year || 'Academic Year 2026-2027') + '</span>' +
            '<span class="ks-tag accent">' + esc(inst.package || 'Official Master Timetable') + '</span>' +
            '<span class="ks-tag">' + kh(ctx.state.classes.length) + ' Classes · ' + kh(ctx.state.subjects.length) + ' Subjects · ' + kh(ctx.state.teachers.length) + ' Teachers</span>' +
          '</div>' +
        '</div>' +
      '</div>' +
      '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">' +
        '<a href="' + ROLE + '-timetables.html" class="ks-btn sm' + (MODULE === 'viewer' ? ' primary' : '') + '">View School Matrix</a>' +
        commonActionsHtml() +
      '</div>' +
    '</div>';
  }

  /* ── Executive page chrome ────────────────────────────────────────────────
     Restores the title / KPI / module-navigation sections that were dropped
     when the builder moved to the Tailwind grid.  Everything here is derived
     from live state and uses the NGIS master design tokens (khmer-suite.css).
     ------------------------------------------------------------------------- */
  var PAGE_META = {
    wizard:   { eyebrow: 'MODULE 01 · TEACHER-CLASS ASSIGNMENT', title: 'Teacher Assignment',       kh: 'ទាត់ថ្នាក់' },
    builder:  { eyebrow: 'MODULE 02 · TIMETABLE MANAGEMENT',     title: 'Timetable Builder',      kh: 'ការវិភាគ' },
    viewer:   { eyebrow: 'MODULE 03 · SCHOOL-WIDE MATRIX',        title: 'Timetables Matrix',     kh: 'តារាងម៉ោង' },
    subjects: { eyebrow: 'MODULE 04 · CURRICULUM',                title: 'Curriculum Subjects',   kh: 'មុខវិជ្ជា' },
    records:  { eyebrow: 'MODULE 05 · STAFF & STUDENT RECORDS',   title: 'Staff & Student Records', kh: 'ព័ត៌មាន' }
  };

  /* The seed stores the academic year in Khmer; show the same "AY 2026-2027"
     style used by the other NGIS executive headers. */
  function academicYearLabel(inst) {
    var raw = String((inst && inst.academic_year) || '').replace(/[\u17E0-\u17E9]/g, function (c) {
      return String(c.charCodeAt(0) - 0x17E0);
    });
    var m = raw.match(/(20\d{2})\s*[-–]\s*(20\d{2})/);
    return m ? 'AY ' + m[1] + '–' + m[2] : 'AY 2026–2027';
  }

  function executiveHeadHtml() {
    var meta = PAGE_META[MODULE] || PAGE_META.builder;
    var state = ctx.state || {};
    var st = ctx.stats || {};
    var inst = state.institution || {};
    var conflicts = st.conflicts || 0;
    var placed = st.placed || 0;
    var total = st.total_demand || 0;
    var classes = (state.classes || []).length;
    var subjects = (state.subjects || []).length;
    var teachers = (state.teachers || []).length;
    var ok = !conflicts;

    return '<section class="ks-exec-head ks-no-print">' +
      '<div class="ks-exec-main">' +
        '<div class="ks-eyebrow">' + esc(meta.eyebrow) + '</div>' +
        '<div class="ks-title-row">' +
          '<h1 class="ks-page-title" lang="en" title="' + esc(meta.kh) + '">' + esc(meta.title) + '</h1>' +
          '<span class="ks-tag">' + esc(academicYearLabel(inst)) + '</span>' +
          '<span class="ks-badge ' + (ok ? 'ok' : 'bad') + '">' +
            '<i class="ks-dot"></i>' + (ok ? 'Zero conflicts' : conflicts + ' conflicts') +
          '</span>' +
        '</div>' +
        '<div class="ks-sub">' +
          esc(inst.name_en || 'New Gateway International School') +
          ' · ' + classes + ' classes · ' + subjects + ' subjects · ' + teachers + ' teachers' +
          ' · ' + placed + '/' + total + ' periods scheduled' +
        '</div>' +
      '</div>' +
      '<div class="ks-actions">' +
        '<button class="ks-btn sm" data-act="history" title="Revision history">' +
          '<span class="material-symbols-outlined">history</span><span>History</span></button>' +
        '<button class="ks-btn sm" data-act="export" data-type="all" title="Export Khmer Excel workbook">' +
          '<span class="material-symbols-outlined">file_download</span><span>Export Excel</span></button>' +
        '<button class="ks-btn sm" onclick="window.print()" title="Print this schedule">' +
          '<span class="material-symbols-outlined">print</span><span>Print</span></button>' +
        '<button class="ks-btn sm primary" data-act="save" title="Save changes">' +
          '<span class="material-symbols-outlined">save</span><span>Save</span></button>' +
      '</div>' +
    '</section>';
  }

  function pageHeadHtml() {
    return executiveHeadHtml();
  }

  function kpiTile(label, valueHtml, footHtml, icon, tone) {
    var t = tone ? ' ' + tone : '';
    return '<div class="ks-kpi">' +
      '<div class="ks-kpi-top">' +
        '<span class="ks-kpi-label">' + esc(label) + '</span>' +
        '<span class="ks-kpi-icon' + t + '"><span class="material-symbols-outlined">' + esc(icon) + '</span></span>' +
      '</div>' +
      '<div class="ks-kpi-value">' + valueHtml + '</div>' +
      '<div class="ks-kpi-foot"><i class="' + (tone || '') + '"></i>' + footHtml + '</div>' +
    '</div>';
  }

  function kpiHtml() {
    var st = ctx.stats || {};
    var total = st.total_demand || 0;
    var placed = st.placed || 0;
    var remaining = st.unassigned || 0;
    var conflicts = st.conflicts || 0;
    var pct = total ? Math.round((placed / total) * 100) : 0;
    var pendingClasses = (st.per_class || []).filter(function (p) { return p.remaining > 0; }).length;

    return '<div class="ks-kpi-strip ks-no-print">' +
      kpiTile('Assigned Periods', placed + '<small> / ' + total + '</small>',
        pct + '% of weekly curriculum placed', 'event_available', '') +
      kpiTile('Remaining to Place', String(remaining),
        pendingClasses + ' classes still have pending lessons', 'pending_actions', 'warn') +
      kpiTile('Hard Conflicts', String(conflicts),
        conflicts ? conflicts + ' collisions need resolving' : 'Zero conflicts · timetable is valid',
        'gpp_maybe', conflicts ? 'bad' : '') +
      kpiTile('Completion Rate', pct + '<small>%</small>',
        'Live · derived from the saved schedule', 'insights', '') +
    '</div>';
  }

  function moduleNavHtml() {
    return '<nav class="ks-modules ks-no-print" aria-label="School admin suite modules">' +
      MODULES.map(function (m) {
        var active = m.id === MODULE;
        return '<a class="ks-module' + (active ? ' active' : '') + '" href="' + esc(m.file) + '"' +
          (active ? ' aria-current="page"' : '') + '>' +
          (m.n ? '<span class="n">' + esc(m.n) + '</span>' : '') +
          '<span>' + esc(m.label) + '</span></a>';
      }).join('') +
    '</nav>';
  }

  /* Bottom analytics row — keeps the page complete on tall viewports. */
  function insightsHtml() {
    var state = ctx.state || {};
    var days = (state.settings && state.settings.days) || D.DAYS;
    var counts = {};
    days.forEach(function (d) { counts[d] = 0; });
    Object.keys(ctx.grid || {}).forEach(function (k) {
      var d = String(k).split('|')[0];
      if (counts[d] !== undefined) counts[d]++;
    });
    var max = 1;
    days.forEach(function (d) { if (counts[d] > max) max = counts[d]; });
    var dayRows = days.map(function (d) {
      var n = counts[d], w = Math.round((n / max) * 100);
      return '<div class="ks-insight-row">' +
        '<span class="ks-insight-day">' + esc(D.toEnDay(d)) + '</span>' +
        '<span class="ks-insight-track"><i style="width:' + w + '%"></i></span>' +
        '<span class="ks-insight-num">' + n + '</span></div>';
    }).join('');

    var legend = (state.subjects || []).slice(0, 14).map(function (s) {
      return '<span class="ks-legend-item"><i style="background:' + esc(s.color || '#E8F3ED') + '"></i>' +
        esc(s.code || s.name_en || s.name_kh || '') + '</span>';
    }).join('');

    var log = [];
    try { log = (E.changeLog ? E.changeLog() : []) || []; } catch (e) { log = []; }
    var changes = log.length
      ? log.slice(0, 5).map(function (c) {
          var t = c.at ? String(c.at).slice(11, 16) : '';
          return '<li><span>' + esc(c.label || 'Change') + '</span><time>' + esc(t) + '</time></li>';
        }).join('')
      : '<li><span>No changes recorded in this session yet</span></li>';

    return '<section class="ks-insights ks-no-print">' +
      '<article class="ks-insight-card">' +
        '<h3>Weekly Load by Day</h3>' +
        '<p class="ks-insight-note">Placed lessons across all cohorts</p>' + dayRows +
      '</article>' +
      '<article class="ks-insight-card">' +
        '<h3>Subject Legend</h3>' +
        '<p class="ks-insight-note">Colours come from the curriculum palette</p>' +
        '<div class="ks-legend">' + legend + '</div>' +
      '</article>' +
      '<article class="ks-insight-card">' +
        '<h3>Recent Changes</h3>' +
        '<p class="ks-insight-note">Latest edits · Ctrl+Z to undo</p>' +
        '<ul class="ks-change-list">' + changes + '</ul>' +
      '</article>' +
    '</section>';
  }

  function commonActionsHtml() {
    return '<button class="ks-icon" data-act="undo" title="Undo (Ctrl+Z)" ' + (ctx.undo ? '' : 'disabled') + '>↶</button>' +
      '<button class="ks-icon" data-act="redo" title="Redo (Ctrl+Y)" ' + (ctx.redo ? '' : 'disabled') + '>↷</button>' +
      '<button class="ks-icon" data-act="history" title="Revision History"></button>' +
      '<button class="ks-btn sm" data-act="export" data-type="all" title="Export All to Excel">Export Excel</button>' +
      '<button class="ks-btn sm primary" data-act="save">Save Changes</button>';
  }

  /* ==========================================================================
     STEP 1 — Data Entry & Academic Setup
     ========================================================================== */

  function renderDataTabs() {
    var tabs = [
      { id: 'teachers', label: 'Teachers (Excel)',          icon: 'group' },
      { id: 'details',  label: 'Teacher Details',           icon: 'badge' },
      { id: 'grades',   label: 'Grade Levels & Curriculum', icon: 'school' },
      { id: 'subjects', label: 'Subjects & Hours',          icon: 'menu_book' },
      { id: 'classes',  label: 'Classes & Rooms',           icon: 'meeting_room' },
      { id: 'import',   label: 'Assignment Import',         icon: 'content_paste' },
      { id: 'unavail',  label: 'Teacher Unavailability',    icon: 'event_busy' }
    ];
    return '<div class="ks-sheet-tabs flex items-center gap-1.5 overflow-x-auto no-scrollbar p-2 bg-surface-container-low border-b border-surface-container-high/60 max-w-full">' +
      tabs.map(function (t) {
        var active = local.dataTab === t.id;
        return '<button class="ks-sheet-tab whitespace-nowrap shrink-0 px-3.5 py-2 rounded-xl text-xs font-medium transition-all ' +
          (active ? 'bg-primary-container text-white shadow-xs' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-container') + '" ' +
          'data-act="set-datatab" data-id="' + t.id + '">' +
          '<span class="flex items-center gap-1.5">' +
            '<span class="material-symbols-outlined text-[16px]">' + t.icon + '</span>' +
            '<span>' + esc(t.label) + '</span>' +
          '</span>' +
        '</button>';
      }).join('') +
    '</div>';
  }

  function recordsTeachersTabHtml() {
    var teachers = ctx.state.teachers || [];
    var cols = D.TEACHER_SPREADSHEET_COLUMNS;
    var validCount = 0, invalidCount = 0;

    teachers.forEach(function (t) {
      if ((t.name_kh || t.name_en) && t.code) validCount++; else invalidCount++;
    });

    var toolbar = '<div class="ks-sheet-toolbar">' +
      '<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">' +
        '<span class="ks-badge ' + (invalidCount ? 'bad' : 'ok') + '">' +
          (invalidCount ? '' + kh(invalidCount) + ' rows with errors' : '' + kh(validCount) + ' valid teacher records') +
        '</span>' +
        '<span class="ks-sub">Click cell to edit · Direct copy/paste (Ctrl+V) from Excel or Google Sheets supported</span>' +
      '</div>' +
      '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">' +
        '<button class="ks-btn sm" data-act="add-teacher-row">＋ Add Teacher Row</button>' +
        '<button class="ks-btn sm" data-act="copy-teachers-clipboard">Copy All</button>' +
        '<button class="ks-btn sm" data-act="reset-teachers-data">↺ Reset Edits</button>' +
        '<button class="ks-btn sm" data-act="show-paste-help">Help</button>' +
        '<button class="ks-btn sm primary" data-act="save-teachers-spreadsheet">Save Spreadsheet</button>' +
      '</div>' +
    '</div>';

    var ths = cols.map(function (c) {
      return '<th style="min-width:' + (c.width || 80) + 'px">' + esc(c.en) + '</th>';
    }).join('');

    var trs = teachers.map(function (t, rIdx) {
      var isInvalid = (!t.name_kh && !t.name_en) || !t.code;
      var tds = cols.map(function (col, cIdx) {
        if (col.key === 'no') {
          return '<td class="row-num">' + kh(rIdx + 1) + '</td>';
        }
        var rawVal = t[col.key] != null ? t[col.key] : '';
        var displayVal = rawVal;
        if (col.key === 'name_kh') displayVal = t.name_en || D.toEnTeacher(rawVal) || rawVal;
        else if (col.key === 'gender') displayVal = D.toEnGender(rawVal);
        else if (col.key === 'position') displayVal = D.toEnPosition(rawVal);
        else if (col.key === 'category') displayVal = D.toEnCategory(rawVal);
        else if (col.key === 'rank') displayVal = D.toEnRank(rawVal);
        else if (col.key === 'specialization') displayVal = D.toEnSubject(rawVal) || rawVal;

        var active = (local.activeCell.row === rIdx && local.activeCell.col === cIdx);
        var cellCls = active ? 'cell-active' : '';
        if (col.required && !rawVal) cellCls += ' cell-invalid';
        return '<td class="' + cellCls + '" data-row="' + rIdx + '" data-col="' + cIdx + '" data-key="' + col.key + '">' +
          '<input class="ks-cell-input" value="' + esc(displayVal) + '" data-change="cell-edit" data-row="' + rIdx + '" data-col="' + cIdx + '" data-key="' + col.key + '">' +
        '</td>';
      }).join('');
      return '<tr class="' + (isInvalid ? 'invalid-row' : '') + '">' + tds + '</tr>';
    }).join('');

    return toolbar +
      '<div class="ks-grid-scroll" id="ks-spreadsheet-container">' +
        '<table class="ks-spreadsheet-table">' +
          '<thead><tr>' + ths + '</tr></thead>' +
          '<tbody>' + trs + '</tbody>' +
        '</table>' +
      '</div>';
  }

  function recordsDetailsTabHtml() {
    var teachers = ctx.state.teachers || [];
    var idx = E.index();
    var q = (local.teacherSearchQ || '').toLowerCase().trim();

    var filtered = teachers.filter(function (t) {
      var enName = t.name_en || D.toEnTeacher(t.name_kh) || '';
      return !q || ((t.name_kh || '') + ' ' + enName + ' ' + t.code + ' ' + (t.employee_id || '')).toLowerCase().indexOf(q) !== -1;
    });

    var searchBar = '<div class="ks-toolbar">' +
      '<input class="ks-input" placeholder="Search teacher by name, code, employee ID..." value="' + esc(local.teacherSearchQ) + '" data-change="teacher-search-details" style="min-width:280px">' +
      '<div class="spacer"></div>' +
      '<span class="ks-badge info">Total ' + kh(filtered.length) + ' Teachers</span>' +
    '</div>';

    var cards = filtered.map(function (t) {
      var sub = idx.subjects[t.subject_id] || {};
      var enName = t.name_en || D.toEnTeacher(t.name_kh) || t.name_kh;
      var pos = D.toEnPosition(t.position);
      var spec = D.toEnSubject(sub.name_kh || sub.name_en) || t.specialization || 'General';
      var gender = D.toEnGender(t.gender);

      return '<div class="ks-card" style="padding:14px">' +
        '<div style="display:flex;align-items:center;gap:12px">' +
          '<div class="ks-mark" style="background:' + esc(sub.color || '#176B45') + '">' + esc(t.code) + '</div>' +
          '<div style="flex:1 1 auto">' +
            '<div style="font-size:14px;font-weight:500">' + esc(enName) + ' <small style="color:var(--ks-muted)">(' + esc(t.code) + ')</small></div>' +
            '<div class="ks-sub">' + esc(pos) + ' · ' + esc(spec) + '</div>' +
          '</div>' +
          '<span class="ks-badge">' + esc(gender) + '</span>' +
        '</div>' +
        '<div style="margin-top:10px;padding-top:10px;border-top:1px solid var(--ks-border-soft);display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:11.5px">' +
          '<div><span style="color:var(--ks-muted)">Employee ID:</span> ' + esc(t.employee_id || '-') + '</div>' +
          '<div><span style="color:var(--ks-muted)">Phone:</span> ' + esc(t.phone || '-') + '</div>' +
          '<div><span style="color:var(--ks-muted)">Target Hours:</span> ' + kh(t.target || 17) + ' hrs</div>' +
          '<div><span style="color:var(--ks-muted)">Max / Day:</span> ' + kh(t.max_daily || 5) + ' hrs</div>' +
        '</div>' +
      '</div>';
    }).join('');

    return searchBar + '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;padding:12px">' + cards + '</div>';
  }

  function recordsGradesTabHtml() {
    var state = ctx.state;
    var grades = [7, 8, 9, 10, 11, 12];
    var selectedGrade = local.selectedGrade || 7;

    var gradeButtons = grades.map(function (g) {
      return '<button class="ks-class-item ' + (g === selectedGrade ? 'active' : '') + '" data-act="set-grade" data-id="' + g + '">' +
        '<div class="name">Grade ' + kh(g) + '</div>' +
        '<div class="meta">National Standard Curriculum</div>' +
      '</button>';
    }).join('');

    var subjects = state.subjects || [];
    var totalLessons = subjects.reduce(function (sum, s) { return sum + (s.lessons_per_week || 0); }, 0);

    var rows = subjects.map(function (s, i) {
      var subEn = s.name_en || D.toEnSubject(s.name_kh);
      return '<tr>' +
        '<td class="center">' + kh(i + 1) + '</td>' +
        '<td><span class="ks-subject-chip" style="background:' + esc(s.color) + '33">' +
          '<i class="swatch" style="background:' + esc(s.color) + '"></i>' + esc(subEn) +
          ' <small>(' + esc(s.code) + ')</small></span></td>' +
        '<td>' + esc(s.department || 'General') + '</td>' +
        '<td class="center"><input type="number" min="0" max="15" value="' + (s.lessons_per_week || 2) + '" data-change="subject-grade-hours" data-id="' + esc(s.id) + '" style="width:55px;text-align:center"></td>' +
        '<td class="center"><select class="ks-select" data-change="subject-consec" data-id="' + esc(s.id) + '">' +
          '<option value="none" ' + (s.consecutive_preference === 'none' ? 'selected' : '') + '>None</option>' +
          '<option value="preferred" ' + (s.consecutive_preference === 'preferred' ? 'selected' : '') + '>Double Period (2 Consecutive)</option>' +
          '<option value="required" ' + (s.consecutive_preference === 'required' ? 'selected' : '') + '>Strictly Consecutive</option>' +
        '</select></td>' +
      '</tr>';
    }).join('');

    return '<div style="display:grid;grid-template-columns:220px 1fr;gap:16px;padding:14px">' +
      '<div class="ks-card"><div class="ks-card-head"><div class="ks-card-title">Grade Levels</div></div>' +
        '<div class="ks-class-list">' + gradeButtons + '</div></div>' +
      '<div class="ks-card"><div class="ks-card-head"><div class="ks-card-title">Grade ' + kh(selectedGrade) + ' Curriculum</div>' +
        '<span class="ks-badge ok">Total ' + kh(totalLessons) + ' Periods/Week</span></div>' +
        '<div class="ks-scroll"><table class="ks-table"><thead><tr>' +
          '<th class="center">No.</th><th>Subject</th><th>Department</th><th class="center">Periods/Week</th><th class="center">Consecutive Preference</th>' +
        '</tr></thead><tbody>' + rows + '</tbody>' +
        '<tfoot><tr class="ks-total-row"><td colspan="3">Total Weekly Academic Periods</td>' +
          '<td class="center">' + kh(totalLessons) + '</td><td>Maximum school capacity: 60 periods</td></tr></tfoot></table></div></div>' +
    '</div>';
  }

  function recordsClassesTabHtml() {
    var classes = ctx.state.classes || [];
    var cls = classes.filter(function (c) { return c.id === local.selectedClass; })[0] || classes[0];
    local.selectedClass = cls.id;

    var left = '<div class="ks-card" style="width:240px"><div class="ks-card-head"><div class="ks-card-title">Class Roster</div></div>' +
      '<div class="ks-class-list">' + classes.map(function (c) {
        var clName = D.toEnClass(c.display);
        var shName = D.toEnShift(c.shift);
        var rmName = D.toEnRoom(c.room || 'General Room');
        return '<button class="ks-class-item ' + (c.id === cls.id ? 'active' : '') + '" data-act="set-class-config" data-id="' + c.id + '">' +
          '<div class="name">Class ' + esc(clName) + '</div>' +
          '<div class="meta">Shift: ' + esc(shName) + ' · ' + esc(rmName) + '</div>' +
        '</button>';
      }).join('') + '</div></div>';

    var right = '<div class="ks-card" style="flex:1 1 auto"><div class="ks-card-head">' +
      '<div class="ks-card-title">Class Settings · Class ' + esc(D.toEnClass(cls.display)) + '</div>' +
      '<span class="ks-badge info">Grade ' + kh(cls.grade) + '</span></div>' +
      '<div class="ks-card-body">' +
        '<div class="ks-fields" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px">' +
          '<div class="ks-field"><label>Class Name (Display)</label><input class="ks-input" value="' + esc(cls.display) + '" data-change="class-edit-display" data-id="' + esc(cls.id) + '"></div>' +
          '<div class="ks-field"><label>Academic Shift</label><select class="ks-select" data-change="class-edit-shift" data-id="' + esc(cls.id) + '">' +
            D.SHIFTS.map(function (sh) { return '<option value="' + esc(sh) + '" ' + (cls.shift === sh ? 'selected' : '') + '>' + esc(D.toEnShift(sh)) + '</option>'; }).join('') +
          '</select></div>' +
          '<div class="ks-field"><label>Assigned Room</label><input class="ks-input" value="' + esc(D.toEnRoom(cls.room || '')) + '" data-change="class-edit-room" data-id="' + esc(cls.id) + '"></div>' +
          '<div class="ks-field"><label>Student Enrollment</label><input class="ks-input" type="number" value="' + (cls.student_count || 32) + '" data-change="class-edit-students" data-id="' + esc(cls.id) + '"></div>' +
          '<div class="ks-field"><label>Days per Week</label><input class="ks-input" type="number" min="1" max="6" value="' + (cls.days || 6) + '" data-change="class-edit-days" data-id="' + esc(cls.id) + '"></div>' +
          '<div class="ks-field"><label>Morning Periods (AM)</label><input class="ks-input" type="number" value="5" readonly style="background:#f5f5f5"></div>' +
          '<div class="ks-field"><label>Afternoon Periods (PM)</label><input class="ks-input" type="number" value="5" readonly style="background:#f5f5f5"></div>' +
        '</div>' +
        '<div style="margin-top:16px"><button class="ks-btn sm primary" data-act="save">Save Class Settings</button></div>' +
      '</div></div>';

    return '<div style="display:flex;gap:16px;padding:14px;flex-wrap:wrap">' + left + right + '</div>';
  }

  function recordsUnavailTabHtml() {
    var teachers = ctx.state.teachers || [];
    var days = D.DAYS;
    var shifts = D.SHIFTS;

    var headerDays = days.map(function (d) {
      return '<th colspan="2" style="border:1px solid var(--ks-border)">' + esc(D.toEnDay(d)) + '</th>';
    }).join('');
    var subHeader = days.map(function () {
      return '<th style="font-size:10px;padding:3px">Morning</th><th style="font-size:10px;padding:3px">Afternoon</th>';
    }).join('');

    var rows = teachers.map(function (t) {
      var unavail = t.unavailable_slots || [];
      var tName = t.name_en || D.toEnTeacher(t.name_kh) || t.name_kh;
      var cells = days.map(function (d) {
        return shifts.map(function (sh) {
          var slotKey = d + '|' + sh;
          var isBlocked = unavail.some(function (u) { return u.indexOf(slotKey) !== -1; });
          var cls = isBlocked ? 'ks-unavail-toggle off' : 'ks-unavail-toggle on';
          var text = isBlocked ? 'Unavailable' : 'Free';
          return '<td><button class="' + cls + '" data-act="toggle-unavail" data-tid="' + esc(t.id) + '" data-slot="' + esc(slotKey) + '">' + text + '</button></td>';
        }).join('');
      }).join('');

      return '<tr>' +
        '<td style="text-align:left;padding:6px 10px;font-weight:500">' + esc(t.code) + ' — ' + esc(tName) + '</td>' +
        cells +
      '</tr>';
    }).join('');

    return '<div style="padding:14px">' +
      '<div class="ks-card-head">' +
        '<div class="ks-card-title">Teacher Unavailability Matrix</div>' +
        '<span class="ks-sub">Click any shift to toggle teacher availability for scheduling</span>' +
      '</div>' +
      '<div class="ks-scroll"><table class="ks-unavail-matrix">' +
        '<thead><tr><th rowspan="2" style="min-width:180px">Teacher</th>' + headerDays + '</tr><tr>' + subHeader + '</tr></thead>' +
        '<tbody>' + rows + '</tbody>' +
      '</table></div>' +
    '</div>';
  }

  function recordsImportTabHtml() {
    return '<div style="padding:20px;max-width:800px;margin:0 auto">' +
      '<div class="ks-card-title" style="margin-bottom:8px">Direct Excel / Google Sheets Assignment Import</div>' +
      '<p class="ks-sub" style="margin-bottom:14px">Copy assignment columns (Class, Subject, Teacher Code) from Excel and paste directly into the box below</p>' +
      '<textarea id="ks-import-paste-area" class="ks-input" style="width:100%;height:180px;font-family:monospace;font-size:12px;padding:10px" placeholder="Example:\n7A\tK\tK1\n7A\tM\tM2\n7B\tK\tK2"></textarea>' +
      '<div style="margin-top:12px;display:flex;gap:8px">' +
        '<button class="ks-btn primary" data-act="apply-assignment-paste">Import Assignments</button>' +
        '<button class="ks-btn" data-act="clear-assignment-paste">Clear</button>' +
      '</div>' +
    '</div>';
  }

  function recordsHtml() {
    var stepper = workflowStepperHtml();
    var teachersCount = (ctx.state.teachers || []).length;
    var subjectsCount = (ctx.state.subjects || []).length;
    var classesCount = (ctx.state.classes || []).length;
    var stats = ctx.stats || (E.statistics ? E.statistics() : { assigned: 0, total: 408 });
    var totalPeriods = stats.total || 408;

    var headerHtml =
      '<div class="p-4 sm:p-space-lg bg-surface-container-lowest shadow-sm mb-space-md rounded-2xl border border-slate-200/80">' +
        '<div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-space-md">' +
          '<div class="space-y-space-xs min-w-0">' +
            '<div class="flex items-center gap-space-sm flex-wrap">' +
              '<span class="font-label-sm text-label-sm bg-primary-fixed text-on-primary-fixed px-2.5 py-0.5 rounded-full font-medium uppercase tracking-wider">' +
                'Step 01 · Academic Setup &amp; Data Entry' +
              '</span>' +
              '<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-secondary-container/30 text-on-secondary-container font-label-sm text-label-sm font-medium">' +
                '<span class="w-1.5 h-1.5 rounded-full bg-secondary"></span>' +
                'AY 2026–2027 · Academic Term 1' +
              '</span>' +
            '</div>' +
            '<h1 class="font-headline-lg text-xl sm:text-2xl lg:text-3xl text-primary tracking-tight font-medium break-words">' +
              'Data Entry &amp; Academic Records' +
            '</h1>' +
            '<p class="font-body-sm text-body-sm text-on-surface-variant">' +
              'Manage teacher roster, grade levels, curriculum subjects, class allocations, and scheduling constraints' +
            '</p>' +
          '</div>' +
          '<div class="flex items-center gap-2 flex-wrap">' +
            '<a href="' + ROLE + '-teacher-class-assignment.html" class="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-forest-800 hover:bg-forest-900 text-white font-label-md text-label-md shadow-xs transition-all font-medium">' +
              '<span>Proceed to Step 2 (Teacher Assignment)</span>' +
              '<span class="material-symbols-outlined text-[16px]">arrow_forward</span>' +
            '</a>' +
          '</div>' +
        '</div>' +
      '</div>';

    var kpiCardsHtml =
      '<div class="grid grid-cols-2 lg:grid-cols-4 gap-2.5 sm:gap-4 mb-space-md">' +
        '<div class="bg-surface-container-lowest rounded-xl p-3 sm:p-4 shadow-sm flex items-center justify-between border border-slate-200/70">' +
          '<div class="space-y-1 min-w-0 pr-1">' +
            '<span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider block font-medium truncate">Teachers</span>' +
            '<div class="flex items-baseline gap-2">' +
              '<span class="font-headline-lg text-xl sm:text-2xl text-primary font-medium">' + teachersCount + '</span>' +
              '<span class="font-body-sm text-body-sm text-on-surface-variant hidden sm:inline">Active</span>' +
            '</div>' +
          '</div>' +
          '<div class="w-9 h-9 sm:w-11 sm:h-11 rounded-lg sm:rounded-xl bg-primary-fixed/40 text-primary flex items-center justify-center shrink-0">' +
            '<span class="material-symbols-outlined text-[20px] sm:text-[24px]">group</span>' +
          '</div>' +
        '</div>' +
        '<div class="bg-surface-container-lowest rounded-xl p-3 sm:p-4 shadow-sm flex items-center justify-between border border-slate-200/70">' +
          '<div class="space-y-1 min-w-0 pr-1">' +
            '<span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider block font-medium truncate">Curriculum</span>' +
            '<div class="flex items-baseline gap-2">' +
              '<span class="font-headline-lg text-xl sm:text-2xl text-on-surface font-medium">' + subjectsCount + '</span>' +
              '<span class="font-body-sm text-body-sm text-on-surface-variant hidden sm:inline">Subjects</span>' +
            '</div>' +
          '</div>' +
          '<div class="w-9 h-9 sm:w-11 sm:h-11 rounded-lg sm:rounded-xl bg-secondary-fixed/40 text-on-secondary-fixed-variant flex items-center justify-center shrink-0">' +
            '<span class="material-symbols-outlined text-[20px] sm:text-[24px]">menu_book</span>' +
          '</div>' +
        '</div>' +
        '<div class="bg-surface-container-lowest rounded-xl p-3 sm:p-4 shadow-sm flex items-center justify-between border border-slate-200/70">' +
          '<div class="space-y-1 min-w-0 pr-1">' +
            '<span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider block font-medium truncate">Classes</span>' +
            '<div class="flex items-baseline gap-2">' +
              '<span class="font-headline-lg text-xl sm:text-2xl text-on-surface font-medium">' + classesCount + '</span>' +
              '<span class="font-body-sm text-body-sm text-on-surface-variant hidden sm:inline">Cohorts</span>' +
            '</div>' +
          '</div>' +
          '<div class="w-9 h-9 sm:w-11 sm:h-11 rounded-lg sm:rounded-xl bg-surface-container-high text-on-surface flex items-center justify-center shrink-0">' +
            '<span class="material-symbols-outlined text-[20px] sm:text-[24px]">meeting_room</span>' +
          '</div>' +
        '</div>' +
        '<div class="bg-surface-container-lowest rounded-xl p-3 sm:p-4 shadow-sm flex items-center justify-between border border-slate-200/70">' +
          '<div class="space-y-1 min-w-0 pr-1">' +
            '<span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider block font-medium truncate">Periods</span>' +
            '<div class="flex items-baseline gap-2">' +
              '<span class="font-headline-lg text-xl sm:text-2xl text-secondary font-medium">' + totalPeriods + '</span>' +
              '<span class="font-body-sm text-body-sm text-on-surface-variant hidden sm:inline">Weekly</span>' +
            '</div>' +
          '</div>' +
          '<div class="w-9 h-9 sm:w-11 sm:h-11 rounded-lg sm:rounded-xl bg-secondary-container/40 text-on-secondary-container flex items-center justify-center shrink-0">' +
            '<span class="material-symbols-outlined text-[20px] sm:text-[24px]">calendar_view_week</span>' +
          '</div>' +
        '</div>' +
      '</div>';

    var tabs = renderDataTabs();
    var content = '';
    if (local.dataTab === 'teachers') content = recordsTeachersTabHtml();
    else if (local.dataTab === 'details') content = recordsDetailsTabHtml();
    else if (local.dataTab === 'grades') content = recordsGradesTabHtml();
    else if (local.dataTab === 'subjects') content = subjectsHtml();
    else if (local.dataTab === 'classes') content = recordsClassesTabHtml();
    else if (local.dataTab === 'import') content = recordsImportTabHtml();
    else if (local.dataTab === 'unavail') content = recordsUnavailTabHtml();

    return '<div class="relative w-full overflow-hidden pb-space-xl">' +
      '<div class="max-w-[1600px] w-full mx-auto px-3 sm:px-space-md lg:px-space-lg space-y-3 sm:space-y-4 pt-2 sm:pt-4">' +
        stepper +
        headerHtml +
        kpiCardsHtml +
        '<div class="bg-surface-container-lowest rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">' +
          tabs +
          content +
        '</div>' +
      '</div>' +
    '</div>';
  }

  /* ==========================================================================
     STEP 2 — Teacher–Class Assignment
     ========================================================================== */

  /* ==========================================================================
     STEP 2 — Modern Teacher–Class Assignment Workspace
     ========================================================================== */

  function wizardHtml() {
    var state = ctx.state;
    var classes = state.classes || [];
    var subjects = state.subjects || [];
    var teachers = state.teachers || [];
    var assignments = state.assignments || [];

    // Active cohort class
    var curClass = classes.filter(function (c) { return c.id === local.selectedClass; })[0] || classes[0] || { id: 'class_7A', display: '7A', shift: 'ព្រឹក' };
    var classDisplay = D.toEnClass(curClass.display || curClass.id);
    var gradeNum = curClass.grade || parseInt(classDisplay.replace(/[^0-9]/g, ''), 10) || 7;
    var secLetter = curClass.section || classDisplay.replace(/[0-9]/g, '') || 'A';
    var isAfternoon = (curClass.shift === 'រសៀល' || classDisplay.slice(-1) === 'B');
    var shiftName = isAfternoon ? 'Afternoon Shift' : 'Morning Shift';
    var shiftShort = isAfternoon ? 'Afternoon' : 'Morning';
    var shiftIcon = isAfternoon ? 'wb_twilight' : 'wb_sunny';
    var cleanRoom = curClass.room ? D.toEnRoom(curClass.room).replace(/^Room\s+/i, '') : classDisplay;
    var roomLocation = 'Room ' + cleanRoom;
    var studentCapacity = (curClass.capacity || 34) + ' Students';
    var schoolDays = curClass.days || 6;
    var mobileTab = local.wizardMobileTab || 'matrix';

    // Assignments for this class
    var classAssignments = assignments.filter(function (a) { return a.class_id === curClass.id; });
    var assignedHours = 0;
    classAssignments.forEach(function (a) { assignedHours += (a.lessons || 2); });
    var targetHours = 30;
    var remainingHours = Math.max(0, targetHours - assignedHours);

    // Workload dictionary for all teachers
    var load = (E.teacherLoad ? E.teacherLoad() : {}) || {};

    function getSubjectTheme(code, name) {
      var c = (code || '').toUpperCase();
      var n = (name || '').toLowerCase();
      if (c.indexOf('K') === 0 || n.indexOf('khmer') !== -1 || n.indexOf('ខ្មែរ') !== -1) {
        return { dot: 'bg-amber-500', bg: 'bg-amber-600', text: 'text-amber-800', lightBg: 'bg-amber-100', border: 'border-amber-200', discipline: 'Khmer Literature' };
      }
      if (c.indexOf('M') === 0 || n.indexOf('math') !== -1 || n.indexOf('គណិត') !== -1) {
        return { dot: 'bg-blue-500', bg: 'bg-blue-600', text: 'text-blue-800', lightBg: 'bg-blue-100', border: 'border-blue-200', discipline: 'Mathematics' };
      }
      if (c.indexOf('B') === 0 || n.indexOf('bio') !== -1 || n.indexOf('ជីវ') !== -1) {
        return { dot: 'bg-emerald-500', bg: 'bg-emerald-600', text: 'text-emerald-800', lightBg: 'bg-emerald-100', border: 'border-emerald-200', discipline: 'Biology' };
      }
      if (c.indexOf('P') === 0 || n.indexOf('phys') !== -1 || n.indexOf('រូប') !== -1) {
        return { dot: 'bg-purple-500', bg: 'bg-purple-600', text: 'text-purple-800', lightBg: 'bg-purple-100', border: 'border-purple-200', discipline: 'Physics' };
      }
      if (c.indexOf('C') === 0 || n.indexOf('chem') !== -1 || n.indexOf('គីមី') !== -1) {
        return { dot: 'bg-rose-500', bg: 'bg-rose-600', text: 'text-rose-800', lightBg: 'bg-rose-100', border: 'border-rose-200', discipline: 'Chemistry' };
      }
      if (c.indexOf('IT') === 0 || n.indexOf('sport') !== -1 || n.indexOf('pe') !== -1 || n.indexOf('កីឡា') !== -1) {
        return { dot: 'bg-rose-600', bg: 'bg-rose-600', text: 'text-rose-800', lightBg: 'bg-rose-100', border: 'border-rose-200', discipline: 'Sports / PE' };
      }
      if (c.indexOf('ES') === 0 || c.indexOf('G') === 0 || n.indexOf('geo') !== -1 || n.indexOf('earth') !== -1 || n.indexOf('ភូមិ') !== -1) {
        return { dot: 'bg-amber-600', bg: 'bg-amber-700', text: 'text-amber-800', lightBg: 'bg-amber-100', border: 'border-amber-200', discipline: 'Geography' };
      }
      if (c.indexOf('EN') === 0 || n.indexOf('eng') !== -1 || n.indexOf('អង់') !== -1) {
        return { dot: 'bg-teal-500', bg: 'bg-teal-600', text: 'text-teal-800', lightBg: 'bg-teal-100', border: 'border-teal-200', discipline: 'English Language' };
      }
      if (c.indexOf('H') === 0 || n.indexOf('hist') !== -1 || n.indexOf('ប្រវត្តិ') !== -1) {
        return { dot: 'bg-amber-600', bg: 'bg-amber-600', text: 'text-amber-800', lightBg: 'bg-amber-100', border: 'border-amber-200', discipline: 'History' };
      }
      return { dot: 'bg-indigo-500', bg: 'bg-indigo-600', text: 'text-indigo-800', lightBg: 'bg-indigo-100', border: 'border-indigo-200', discipline: 'General' };
    }

    // Cohort Cards for Column 1
    var cohortCardsHtml = classes.map(function (cls) {
      var cDisp = D.toEnClass(cls.display || cls.id);
      var cIsAfternoon = (cls.shift === 'រសៀល' || cDisp.slice(-1) === 'B');
      var cShiftLabel = cIsAfternoon ? 'Afternoon Shift' : 'Morning Shift';
      var cAsgs = assignments.filter(function (a) { return a.class_id === cls.id; });
      var cHours = 0;
      cAsgs.forEach(function (a) { cHours += (a.lessons || 2); });
      var cPending = Math.max(0, 30 - cHours);
      var pendingBadge = (cPending === 0)
        ? '<span class="px-2 py-0.5 rounded-md bg-secondary-fixed/40 text-on-secondary-fixed-variant text-[11px] font-medium shrink-0">0 Pending</span>'
        : '<span class="px-2 py-0.5 rounded-md bg-amber-50 text-amber-800 border border-amber-200 text-[11px] font-medium shrink-0">' + cPending + 'h Open</span>';
      var isActive = (cls.id === curClass.id);
      var cardStyle = isActive
        ? 'border-emerald-500/40 bg-emerald-50/50 text-emerald-900 shadow-2xs'
        : 'border-slate-100 bg-white hover:border-slate-300 hover:bg-slate-50/60';

      return '<button type="button" class="w-full text-left p-3 rounded-xl border transition-all flex items-center justify-between group cursor-pointer cohort-item ' + cardStyle + '" data-act="select-wizard-class" data-cid="' + esc(cls.id) + '" data-search="' + esc(cDisp.toLowerCase() + ' ' + (cls.display || '').toLowerCase() + ' ' + (cIsAfternoon ? 'afternoon' : 'morning')) + '">' +
        '<div class="flex flex-col min-w-0 pr-2">' +
          '<div class="flex items-center gap-2">' +
            '<span class="font-medium text-[14px] ' + (isActive ? 'text-primary' : 'text-on-surface group-hover:text-primary') + '">' + esc(cDisp) + '</span>' +
            '<span class="px-1.5 py-0.5 rounded text-[10px] font-medium bg-surface-container text-on-surface-variant">' + esc(cShiftLabel) + '</span>' +
          '</div>' +
          '<span class="text-[11px] text-outline font-normal mt-0.5">' + (cls.days || 6) + ' Days · ' + cHours + '/30 hrs</span>' +
        '</div>' +
        pendingBadge +
      '</button>';
    }).join('');

    // Allocation Table Rows for Column 2
    var tableRows = classAssignments.map(function (a, idx) {
      var sub = subjects.filter(function (s) { return s.id === a.subject_id; })[0] || { name_kh: a.subject_id, name_en: 'Subject', code: 'SUB' };
      var tchr = teachers.filter(function (t) { return t.id === a.teacher_id; })[0] || { code: 'TR', name_kh: 'គ្រូ', name_en: 'Teacher', target: 17 };
      var tAssigned = load[tchr.id] || 0;
      var tTarget = tchr.target || 17;
      var subNameEn = sub.name_en || D.toEnSubject(sub.name_kh);
      var subTheme = getSubjectTheme(sub.code || a.subject_id, subNameEn);
      var tName = tchr.name_en || D.toEnTeacher(tchr.name_kh) || tchr.name_kh;
      var shiftText = D.toEnShift(a.shift || curClass.shift);
      var rowNum = (idx + 1 < 10 ? '0' + (idx + 1) : '' + (idx + 1));

      var statusBadge = '';
      if (tAssigned <= 20) {
        statusBadge = '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full bg-secondary-fixed/40 text-on-secondary-fixed-variant text-[11px] font-medium">' + tAssigned + '/' + tTarget + 'h (Optimal)</span>';
      } else if (tAssigned <= 23) {
        statusBadge = '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-800 border border-amber-200 text-[11px] font-medium">' + tAssigned + '/' + tTarget + 'h (Near Max)</span>';
      } else {
        statusBadge = '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full bg-rose-50 text-rose-700 border border-rose-200 text-[11px] font-medium">' + tAssigned + '/' + tTarget + 'h (Overload)</span>';
      }

      return '<tr class="hover:bg-slate-50/50 transition-colors border-b border-slate-100 last:border-0">' +
        '<td class="py-3 px-3.5 text-center text-slate-400 font-medium text-xs">' + rowNum + '</td>' +
        '<td class="py-3 px-3.5">' +
          '<div class="flex items-center gap-2.5">' +
            '<span class="w-2.5 h-2.5 rounded-full ' + subTheme.dot + ' shrink-0"></span>' +
            '<div class="flex flex-col">' +
              '<span class="font-medium text-slate-900 text-[13px]">' + esc(subNameEn) + '</span>' +
              '<span class="text-[11px] text-slate-400 font-normal">' + esc(subTheme.discipline || 'Academic') + ' · Code: ' + esc(sub.code || sub.id) + '</span>' +
            '</div>' +
          '</div>' +
        '</td>' +
        '<td class="py-3 px-3.5">' +
          '<div class="flex items-center gap-2">' +
            '<span class="w-6 h-6 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200/50 font-medium text-[10px] flex items-center justify-center shrink-0">' + esc(tchr.code) + '</span>' +
            '<span class="font-medium text-slate-900 text-[13px]">' + esc(tName) + '</span>' +
          '</div>' +
        '</td>' +
        '<td class="py-3 px-3 text-center">' +
          '<span class="inline-block px-2.5 py-0.5 rounded-md bg-slate-100 font-medium text-slate-700 text-xs">' + (a.lessons || 2) + ' hrs</span>' +
        '</td>' +
        '<td class="py-3 px-3 text-center text-on-surface-variant text-[12px] font-medium">' + esc(shiftText) + '</td>' +
        '<td class="py-3 px-3.5 text-center">' +
          statusBadge +
        '</td>' +
        '<td class="py-3 px-3 text-center">' +
          '<div class="flex items-center justify-center gap-1">' +
            '<button type="button" class="p-1.5 rounded-lg text-outline hover:text-primary hover:bg-surface-container transition-colors cursor-pointer" data-act="prompt-change-instructor" data-cid="' + esc(curClass.id) + '" data-sid="' + esc(a.subject_id) + '" data-tid="' + esc(a.teacher_id) + '" title="Change Educator">' +
              '<span class="material-symbols-outlined text-[16px]">sync_alt</span>' +
            '</button>' +
            '<button type="button" class="p-1.5 rounded-lg text-outline hover:text-red-600 hover:bg-red-50 transition-colors cursor-pointer" data-act="clear-assignment" data-cid="' + esc(curClass.id) + '" data-sid="' + esc(a.subject_id) + '" title="Remove Allocation">' +
              '<span class="material-symbols-outlined text-[16px]">delete</span>' +
            '</button>' +
          '</div>' +
        '</td>' +
      '</tr>';
    }).join('');

    // Faculty Capacity Cards for Column 3
    var facultyCardsHtml = teachers.map(function (tc) {
      var tAssigned = load[tc.id] || 0;
      var tTarget = tc.target || 17;
      var tRemaining = tTarget - tAssigned;
      var tPct = Math.min(100, Math.round((tAssigned / (tTarget || 1)) * 100));
      var tName = tc.name_en || D.toEnTeacher(tc.name_kh) || tc.name_kh;
      var theme = getSubjectTheme(tc.code, tc.specialization || tc.name_kh);

      var specEn = D.toEnSubject(tc.specialization) || theme.discipline || 'General';

      var barColor = 'bg-secondary';
      var remainText = '';
      if (tRemaining < 0) {
        barColor = 'bg-rose-500';
        remainText = '<span class="text-rose-600 font-medium">' + Math.abs(tRemaining) + 'h over</span>';
      } else if (tRemaining <= 2) {
        barColor = 'bg-amber-500';
        remainText = '<span class="text-amber-700 font-medium">Remaining: ' + tRemaining + 'h</span>';
      } else {
        barColor = 'bg-secondary';
        remainText = '<span class="text-secondary font-medium">Remaining: ' + tRemaining + 'h</span>';
      }

      return '<div class="faculty-card p-3.5 rounded-xl bg-white border border-slate-200/60 hover:border-emerald-300 hover:bg-emerald-50/20 transition-all flex flex-col gap-2.5 shadow-2xs" data-name="' + esc((tName + ' ' + tc.name_kh + ' ' + tc.code + ' ' + (tc.specialization || '')).toLowerCase()) + '">' +
        '<div class="flex items-center justify-between">' +
          '<div class="flex items-center gap-2.5 min-w-0 pr-2">' +
            '<div class="w-7 h-7 rounded-lg ' + theme.lightBg + ' ' + theme.text + ' font-medium text-[11px] flex items-center justify-center shrink-0 border border-slate-200/50">' +
              esc(tc.code) +
            '</div>' +
            '<div class="flex flex-col min-w-0">' +
              '<span class="font-medium text-[13px] text-slate-900 leading-tight truncate">' + esc(tName) + '</span>' +
              '<span class="text-[11px] text-slate-400 font-normal truncate">' + esc(specEn) + '</span>' +
            '</div>' +
          '</div>' +
          '<span class="font-medium text-[12px] text-emerald-800 shrink-0">' + tAssigned + ' / ' + tTarget + ' hrs</span>' +
        '</div>' +
        '<div class="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">' +
          '<div class="' + barColor + ' h-full rounded-full transition-all" style="width:' + tPct + '%"></div>' +
        '</div>' +
        '<div class="flex items-center justify-between text-[11px] text-slate-500 font-normal">' +
          '<span>Assigned: <span class="text-slate-800 font-medium">' + tAssigned + 'h</span></span>' +
          remainText +
        '</div>' +
      '</div>';
    }).join('');

    return '<div class="relative w-full space-y-6 pb-20 sm:pb-12">' +
      // Section 1: Standard NGIS Page Header & Primary Actions (Matching other pages)
      '<section class="flex flex-col md:flex-row md:items-end justify-between gap-4 pb-2 border-b border-slate-200/70">' +
        '<div>' +
          '<div class="flex items-center gap-2 text-xs text-slate-500 font-normal mb-1.5">' +
            '<span>Academics</span>' +
            '<span class="text-slate-300">/</span>' +
            '<a href="' + ROLE + '-timetables.html" class="hover:text-primary transition-colors">Timetable Management</a>' +
            '<span class="text-slate-300">/</span>' +
            '<span class="text-slate-700 font-medium">Teacher Assignment</span>' +
          '</div>' +
          '<h1 class="text-2xl lg:text-[26px] font-medium text-slate-900 tracking-tight flex items-center gap-2.5" style="font-family:\'Manrope\',sans-serif;">' +
            '<span class="w-9 h-9 rounded-xl bg-emerald-50 text-emerald-800 flex items-center justify-center border border-emerald-200/60 shrink-0">' +
              '<span class="material-symbols-outlined text-[20px]">swap_horiz</span>' +
            '</span>' +
            '<span>Teacher–Class Assignment</span>' +
          '</h1>' +
          '<div class="flex items-center gap-2 mt-2 flex-wrap text-xs text-slate-600">' +
            '<span class="px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 font-medium">AY 2026–2027</span>' +
            '<span class="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200 font-medium">Faculty Allocation &amp; Workload</span>' +
            '<span class="text-slate-300">·</span>' +
            '<span class="text-slate-500">' + classes.length + ' Class Cohorts · ' + teachers.length + ' Faculty Members</span>' +
          '</div>' +
        '</div>' +
        '<div class="flex items-center flex-wrap gap-2.5 shrink-0">' +
          '<a href="' + ROLE + '-timetables.html" class="inline-flex items-center gap-1.5 px-3 py-2 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 rounded-lg text-xs font-medium transition-colors shadow-xs">' +
            '<span class="material-symbols-outlined text-[16px] text-slate-500">calendar_view_week</span>' +
            '<span>Timetables Matrix</span>' +
          '</a>' +
          '<a href="' + ROLE + '-timetable-builder.html" class="inline-flex items-center gap-1.5 px-3 py-2 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 rounded-lg text-xs font-medium transition-colors shadow-xs">' +
            '<span class="material-symbols-outlined text-[16px] text-slate-500">grid_view</span>' +
            '<span>Timetable Builder</span>' +
          '</a>' +
          '<button type="button" class="inline-flex items-center gap-1.5 px-3 py-2 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 rounded-lg text-xs font-medium transition-colors shadow-xs cursor-pointer" data-act="wizard-print">' +
            '<span class="material-symbols-outlined text-[16px] text-slate-500">print</span>' +
            '<span>Print Sheet</span>' +
          '</button>' +
          '<button type="button" class="inline-flex items-center gap-1.5 px-3.5 py-2 bg-[#176B45] hover:bg-[#14532D] text-white rounded-lg text-xs font-medium transition-all shadow-xs cursor-pointer" data-act="wizard-save">' +
            '<span class="material-symbols-outlined text-[16px]">save</span>' +
            '<span>Save Changes</span>' +
          '</button>' +
        '</div>' +
      '</section>' +

      // Mobile Tab Switcher (Visible on < xl)
      '<div class="flex xl:hidden bg-slate-100 p-1.5 rounded-xl border border-slate-200/80 mb-2">' +
        '<button type="button" class="flex-1 py-2.5 text-center text-xs font-medium rounded-lg transition-all ' + (mobileTab === 'cohorts' ? 'bg-white text-emerald-800 shadow-xs border border-slate-200/60' : 'text-slate-600 hover:text-slate-900') + '" data-act="wizard-mobile-tab" data-tab="cohorts">' +
          '<span class="flex items-center justify-center gap-1.5">' +
            '<span class="material-symbols-outlined text-[16px]">view_timeline</span>' +
            '<span>Cohorts (' + classes.length + ')</span>' +
          '</span>' +
        '</button>' +
        '<button type="button" class="flex-1 py-2.5 text-center text-xs font-medium rounded-lg transition-all ' + (mobileTab === 'matrix' ? 'bg-white text-emerald-800 shadow-xs border border-slate-200/60' : 'text-slate-600 hover:text-slate-900') + '" data-act="wizard-mobile-tab" data-tab="matrix">' +
          '<span class="flex items-center justify-center gap-1.5">' +
            '<span class="material-symbols-outlined text-[16px]">grid_view</span>' +
            '<span>' + esc(classDisplay) + ' (' + classAssignments.length + ')</span>' +
          '</span>' +
        '</button>' +
        '<button type="button" class="flex-1 py-2.5 text-center text-xs font-medium rounded-lg transition-all ' + (mobileTab === 'faculty' ? 'bg-white text-emerald-800 shadow-xs border border-slate-200/60' : 'text-slate-600 hover:text-slate-900') + '" data-act="wizard-mobile-tab" data-tab="faculty">' +
          '<span class="flex items-center justify-center gap-1.5">' +
            '<span class="material-symbols-outlined text-[16px]">badge</span>' +
            '<span>Faculty (' + teachers.length + ')</span>' +
          '</span>' +
        '</button>' +
      '</div>' +

      // 3-Column Rostering Canvas
      '<div class="grid grid-cols-1 xl:grid-cols-12 gap-5 items-start">' +
          // Column 1: Cohort Directory
          '<div class="xl:col-span-3 flex flex-col ' + (mobileTab !== 'cohorts' ? 'hidden xl:flex' : 'flex') + '">' +
            '<div class="bg-white rounded-2xl border border-slate-200/60 shadow-xs p-4 sm:p-5 flex flex-col gap-4">' +
              '<div class="flex items-center justify-between">' +
                '<div class="flex items-center gap-2">' +
                  '<span class="material-symbols-outlined text-emerald-800 text-[20px]">view_timeline</span>' +
                  '<span class="font-medium text-[15px] text-slate-900">Cohorts / Classes</span>' +
                '</div>' +
                '<span class="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 font-medium text-[11px] border border-slate-200/50">' +
                  classes.length + ' Classes' +
                '</span>' +
              '</div>' +
              '<div class="relative w-full">' +
                '<span class="material-symbols-outlined absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-[18px] pointer-events-none">search</span>' +
                '<input id="cohortSearchInput" class="w-full pl-10 pr-3.5 py-2.5 bg-slate-50/70 hover:bg-slate-50 focus:bg-white border border-slate-200/70 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 rounded-xl text-xs font-normal text-slate-800 placeholder:text-slate-400 transition-all outline-none" placeholder="Search class (e.g. 8A, 9B)..." type="text">' +
              '</div>' +
              '<div id="cohortCardsList" class="flex flex-col gap-2 max-h-[calc(100vh-325px)] min-h-[280px] overflow-y-auto pr-1">' +
                cohortCardsHtml +
              '</div>' +
              '<div class="pt-2 border-t border-slate-100">' +
                '<button type="button" class="w-full py-2.5 px-3 rounded-xl border border-dashed border-emerald-600/30 hover:border-emerald-600 bg-emerald-50/30 hover:bg-emerald-50 text-emerald-800 font-medium text-[12px] flex items-center justify-center gap-2 transition-all cursor-pointer" data-act="open-assign-modal" data-cid="' + esc(curClass.id) + '">' +
                  '<span class="material-symbols-outlined text-[18px]">add_circle</span>' +
                  '<span>+ Add Subject Allocation</span>' +
                '</button>' +
              '</div>' +
            '</div>' +
          '</div>' +

          // Column 2: Active Class Assignment Matrix
          '<div class="xl:col-span-6 flex flex-col ' + (mobileTab !== 'matrix' ? 'hidden xl:flex' : 'flex') + '">' +
            '<div class="bg-white rounded-2xl border border-slate-200/60 shadow-xs p-4 sm:p-5 flex flex-col gap-5">' +
              // Header Bar of Active Cohort
              '<div class="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-slate-200/60">' +
                '<div class="flex items-center gap-3">' +
                  '<div class="w-11 h-11 rounded-2xl bg-emerald-50 border border-emerald-200/60 flex items-center justify-center text-emerald-800 shadow-2xs shrink-0">' +
                    '<span class="material-symbols-outlined text-[24px]">school</span>' +
                  '</div>' +
                  '<div class="flex flex-col">' +
                    '<div class="flex items-center gap-2.5 flex-wrap">' +
                      '<span class="font-medium text-[20px] text-slate-900 tracking-tight">Class Setup · Grade ' + esc(classDisplay) + '</span>' +
                      '<span class="px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 font-medium text-[11px]">' +
                        'Grade ' + gradeNum + ' – Section ' + secLetter +
                      '</span>' +
                    '</div>' +
                    '<span class="text-[12px] text-slate-500 font-normal mt-0.5">Subject educator rosters &amp; weekly period capacity distribution</span>' +
                  '</div>' +
                '</div>' +
                '<div class="flex items-center gap-2">' +
                  '<span class="px-3 py-1 rounded-xl bg-slate-50 border border-slate-200/60 text-slate-700 font-medium text-[12px] flex items-center gap-1.5">' +
                    '<span class="material-symbols-outlined text-[16px] text-emerald-700">' + shiftIcon + '</span>' +
                    '<span>' + esc(shiftShort) + ' · ' + schoolDays + ' Days</span>' +
                  '</span>' +
                  '<button type="button" class="px-3.5 py-1.5 rounded-xl bg-[#176B45] hover:bg-[#14532D] text-white text-xs font-medium flex items-center gap-1.5 shadow-xs transition-colors cursor-pointer" data-act="open-assign-modal" data-cid="' + esc(curClass.id) + '">' +
                    '<span class="material-symbols-outlined text-[16px]">add</span>' +
                    '<span>Assign</span>' +
                  '</button>' +
                '</div>' +
              '</div>' +

              // Parameter Bar: 5 Compact Stat Cards
              '<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2.5 p-3.5 rounded-2xl bg-slate-50/70 border border-slate-200/60">' +
                '<div class="flex flex-col gap-1">' +
                  '<span class="text-[10.5px] font-medium text-slate-400 uppercase tracking-wider">Total Periods/Wk</span>' +
                  '<div class="bg-white border border-slate-200/70 rounded-xl px-3 py-2 flex items-baseline justify-between shadow-2xs">' +
                    '<span class="font-medium text-[15px] text-emerald-800">' + assignedHours + '</span>' +
                    '<span class="text-[11px] text-slate-400 font-normal">/ ' + targetHours + ' hrs</span>' +
                  '</div>' +
                '</div>' +
                '<div class="flex flex-col gap-1">' +
                  '<span class="text-[10.5px] font-medium text-slate-400 uppercase tracking-wider">Room Assignment</span>' +
                  '<div class="bg-white border border-slate-200/70 rounded-xl px-3 py-2 shadow-2xs">' +
                    '<span class="font-medium text-[13px] text-slate-800 truncate block" title="' + esc(roomLocation) + '">' + esc(roomLocation) + '</span>' +
                  '</div>' +
                '</div>' +
                '<div class="flex flex-col gap-1">' +
                  '<span class="text-[10.5px] font-medium text-slate-400 uppercase tracking-wider">School Days</span>' +
                  '<div class="bg-white border border-slate-200/70 rounded-xl px-3 py-2 flex items-baseline justify-between shadow-2xs">' +
                    '<span class="font-medium text-[14px] text-slate-800">' + schoolDays + '</span>' +
                    '<span class="text-[11px] text-slate-400 font-normal">days</span>' +
                  '</div>' +
                '</div>' +
                '<div class="flex flex-col gap-1">' +
                  '<span class="text-[10.5px] font-medium text-slate-400 uppercase tracking-wider">Daily Periods</span>' +
                  '<div class="bg-white border border-slate-200/70 rounded-xl px-3 py-2 flex items-baseline justify-between shadow-2xs">' +
                    '<span class="font-medium text-[14px] text-slate-800">5</span>' +
                    '<span class="text-[11px] text-slate-400 font-normal">periods</span>' +
                  '</div>' +
                '</div>' +
                '<div class="flex flex-col gap-1 col-span-2 sm:col-span-1 lg:col-span-1">' +
                  '<span class="text-[10.5px] font-medium text-slate-400 uppercase tracking-wider">Shift Schedule</span>' +
                  '<div class="bg-white border border-slate-200/70 rounded-xl px-2.5 py-2 flex items-center justify-between shadow-2xs">' +
                    '<span class="font-medium text-[12px] text-emerald-800 truncate">' + esc(shiftName) + '</span>' +
                    '<span class="material-symbols-outlined text-[16px] text-slate-400 shrink-0">' + shiftIcon + '</span>' +
                  '</div>' +
                '</div>' +
              '</div>' +

              // Straight-Line Allocation Table
              '<div class="overflow-x-auto border border-slate-200/60 rounded-xl shadow-2xs bg-white">' +
                '<table class="w-full text-left border-collapse min-w-[620px]">' +
                  '<thead>' +
                    '<tr class="bg-slate-50/80 text-slate-500 text-[11px] font-medium uppercase tracking-wider border-b border-slate-200/60">' +
                      '<th class="py-3 px-3.5 text-center w-10">#</th>' +
                      '<th class="py-3 px-3.5">SUBJECT</th>' +
                      '<th class="py-3 px-3.5">EDUCATOR</th>' +
                      '<th class="py-3 px-3 text-center">HRS/WK</th>' +
                      '<th class="py-3 px-3 text-center">SHIFT</th>' +
                      '<th class="py-3 px-3.5 text-center">STATUS / LOAD</th>' +
                      '<th class="py-3 px-3 text-center w-20">ACTIONS</th>' +
                    '</tr>' +
                  '</thead>' +
                  '<tbody class="divide-y divide-slate-100 text-[13px] bg-white font-normal">' +
                    (tableRows || '<tr><td colspan="7" class="py-8 text-center text-slate-400">No subjects assigned yet. Click "+ Add Subject Allocation" to begin.</td></tr>') +
                  '</tbody>' +
                '</table>' +
              '</div>' +

              // Table Footer Toolbar
              '<div class="flex flex-wrap items-center justify-between gap-4 pt-1">' +
                '<button type="button" class="px-4 py-2 bg-[#176B45] hover:bg-[#14532D] text-white font-medium text-[13px] rounded-xl flex items-center gap-2 shadow-xs transition-all cursor-pointer" data-act="open-assign-modal" data-cid="' + esc(curClass.id) + '">' +
                  '<span class="material-symbols-outlined text-[18px]">add_circle</span>' +
                  '<span>+ Add Subject Allocation</span>' +
                '</button>' +
                '<span class="text-xs text-slate-500 font-normal">' +
                  'Showing ' + classAssignments.length + ' allocations · ' + assignedHours + '/30 hrs scheduled' +
                  (remainingHours > 0 ? (' · <span class="text-amber-700 font-medium">' + remainingHours + ' hrs remaining</span>') : ' · <span class="text-emerald-700 font-medium">Complete</span>') +
                '</span>' +
              '</div>' +
            '</div>' +
          '</div>' +

          // Column 3: Faculty Capacity Ledger
          '<div class="xl:col-span-3 flex flex-col ' + (mobileTab !== 'faculty' ? 'hidden xl:flex' : 'flex') + '">' +
            '<div class="bg-white rounded-2xl border border-slate-200/60 shadow-xs p-4 sm:p-5 flex flex-col gap-4">' +
              '<div class="flex items-center justify-between">' +
                '<div class="flex items-center gap-2">' +
                  '<span class="material-symbols-outlined text-emerald-800 text-[20px]">badge</span>' +
                  '<span class="font-medium text-[15px] text-slate-900">Faculty Workload Ledger</span>' +
                '</div>' +
                '<span class="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 font-medium text-[11px] border border-slate-200/50">' +
                  teachers.length + ' Educators' +
                '</span>' +
              '</div>' +
              '<div class="relative w-full">' +
                '<span class="material-symbols-outlined absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-[18px] pointer-events-none">person_search</span>' +
                '<input id="facultySearchInput" class="w-full pl-10 pr-3.5 py-2.5 bg-slate-50/70 hover:bg-slate-50 focus:bg-white border border-slate-200/70 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 rounded-xl text-xs font-normal text-slate-800 placeholder:text-slate-400 transition-all outline-none" placeholder="Filter teacher by name or code..." type="text">' +
              '</div>' +
              '<div id="facultyCardsList" class="flex flex-col gap-2 max-h-[calc(100vh-325px)] min-h-[280px] overflow-y-auto pr-1">' +
                facultyCardsHtml +
              '</div>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>';
  }

  function attachWizardInteractions() {
    var searchInput = document.getElementById('facultySearchInput');
    var cardsList = document.getElementById('facultyCardsList');
    if (searchInput && cardsList) {
      searchInput.oninput = function (e) {
        var query = (e.target.value || '').trim().toLowerCase();
        cardsList.querySelectorAll('.faculty-card').forEach(function (card) {
          var name = card.dataset.name || '';
          if (!query || name.indexOf(query) !== -1) {
            card.style.display = '';
          } else {
            card.style.display = 'none';
          }
        });
      };
    }

    var cohortInput = document.getElementById('cohortSearchInput');
    var cohortList = document.getElementById('cohortCardsList');
    if (cohortInput && cohortList) {
      cohortInput.oninput = function (e) {
        var query = (e.target.value || '').trim().toLowerCase();
        cohortList.querySelectorAll('.cohort-item').forEach(function (item) {
          var s = item.dataset.search || '';
          if (!query || s.indexOf(query) !== -1) {
            item.style.display = '';
          } else {
            item.style.display = 'none';
          }
        });
      };
    }
  }

        /* ==========================================================================
     STEP 3 — Modern Visual Drag-and-Drop Timetable Builder
     ========================================================================== */

  function formatKhmerSubjectName(raw) {
    if (!raw) return 'Khmer';
    var lower = String(raw).toLowerCase().trim();
    if (lower === 'khmer' || lower === 'k' || lower === 'sub_k' || lower === 'ខ្មែរ' || lower.indexOf('ភាសាខ្មែរ') !== -1) return 'Khmer';
    if (lower === 'math' || lower === 'mathematics' || lower === 'm' || lower === 'sub_m' || lower === 'គណិត' || lower.indexOf('គណិតវិទ្យា') !== -1) return 'Mathematics';
    if (lower === 'english' || lower === 'en' || lower === 'sub_en' || lower.indexOf('អង់គ្លេស') !== -1) return 'English';
    if (lower === 'physics' || lower === 'p' || lower === 'sub_p' || lower.indexOf('រូប') !== -1) return 'Physics';
    if (lower === 'chemistry' || lower === 'c' || lower === 'sub_c' || lower.indexOf('គីមី') !== -1) return 'Chemistry';
    if (lower === 'biology' || lower === 'b' || lower === 'sub_b' || lower.indexOf('ជីវ') !== -1) return 'Biology';
    if (lower === 'history' || lower === 'h' || lower === 'sub_h' || lower.indexOf('ប្រវត្តិ') !== -1) return 'History';
    if (lower === 'geography' || lower === 'geo' || lower === 'sub_geo' || lower === 'sub_es' || lower === 'es' || lower.indexOf('ភូមិ') !== -1) return 'Geography';
    if (lower === 'sports' || lower === 'pe' || lower === 'sub_pe' || lower === 'sub_it' || lower === 'it' || lower.indexOf('កីឡា') !== -1) return 'Physical Education';
    if (lower === 'ict' || lower === 'computer' || lower === 'sub_g' || lower === 'g' || lower.indexOf('ព័ត៌មាន') !== -1 || lower.indexOf('កុំព្យូទ័រ') !== -1) return 'Computer / ICT';
    if (lower === 'morals' || lower === 'civics' || lower === 'sub_mor' || lower === 'sub_i' || lower === 'i' || lower.indexOf('សីលធម៌') !== -1 || lower.indexOf('ពលរដ្ឋ') !== -1) return 'Civics & Ethics';
    if (lower === 'earth' || lower === 'earth science' || lower.indexOf('ផែនដី') !== -1) return 'Earth Science';
    if (lower === 'economics' || lower === 'sub_eco' || lower === 'sub_ed' || lower === 'ed' || lower.indexOf('សេដ្ឋកិច្ច') !== -1) return 'Economics';
    if (lower.indexOf('អប់រំសីលធម៌') !== -1) return 'Moral Education';
    return D.toEnSubject(raw) || raw;
  }

  var SUBJECT_BOX_COLORS = {
    'K':    '#FED766', // Khmer (Warm Amber Yellow)
    'M':    '#93C5FD', // Mathematics (Soft Sky Blue)
    'EN':   '#99F6E4', // English (Mint Teal)
    'P':    '#DDD6FE', // Physics (Lavender Violet)
    'C':    '#FBCFE8', // Chemistry (Soft Rose Pink)
    'B':    '#A7F3D0', // Biology (Light Emerald Green)
    'ES':   '#FED7AA', // Earth Science / Geography (Warm Peach)
    'GEO':  '#FED7AA',
    'G':    '#BAE6FD', // Computer Studies / ICT (Ice Blue)
    'H':    '#FDE68A', // History (Warm Apricot)
    'I':    '#C7D2FE', // Civics / Moral (Periwinkle Indigo)
    'IT':   '#FECDD3', // Physical Education / Sports (Coral Pink)
    'PE':   '#FECDD3',
    'ED':   '#FEF3C7', // Moral Education / Economics (Creamy Sage)
    'ECO':  '#FEF3C7',
    'SH':   '#E9D5FF'  // Social Language (Soft Lilac Purple)
  };

  function getSubjectBoxColor(subjectId, subNameKh, rawColor) {
    if (D && typeof D.getSubjectColor === 'function') {
      return D.getSubjectColor(subjectId, subNameKh, rawColor);
    }
    var sId = String(subjectId || '').trim();
    var code = sId.replace(/^sub_/, '').toUpperCase();
    if (SUBJECT_BOX_COLORS[code]) return SUBJECT_BOX_COLORS[code];
    if (SUBJECT_BOX_COLORS[sId]) return SUBJECT_BOX_COLORS[sId];

    var s = (subNameKh || '').toLowerCase();
    if (s.indexOf('ខ្មែរ') !== -1 || s.indexOf('khmer') !== -1) return '#FED766';
    if (s.indexOf('គណិត') !== -1 || s.indexOf('math') !== -1) return '#93C5FD';
    if (s.indexOf('អង់គ្លេស') !== -1 || s.indexOf('english') !== -1 || s.indexOf('eng') !== -1) return '#99F6E4';
    if (s.indexOf('រូប') !== -1 || s.indexOf('physic') !== -1) return '#DDD6FE';
    if (s.indexOf('គីមី') !== -1 || s.indexOf('chem') !== -1) return '#FBCFE8';
    if (s.indexOf('ជីវ') !== -1 || s.indexOf('bio') !== -1) return '#A7F3D0';
    if (s.indexOf('ភូមិ') !== -1 || s.indexOf('geo') !== -1 || s.indexOf('earth') !== -1 || s.indexOf('ផែនដី') !== -1) return '#FED7AA';
    if (s.indexOf('កុំព្យូទ័រ') !== -1 || s.indexOf('ព័ត៌មាន') !== -1 || s.indexOf('ict') !== -1 || s.indexOf('computer') !== -1) return '#BAE6FD';
    if (s.indexOf('ប្រវត្តិ') !== -1 || s.indexOf('histor') !== -1) return '#FDE68A';
    if (s.indexOf('ពលរដ្ឋ') !== -1 || s.indexOf('សីលធម៌') !== -1 || s.indexOf('civic') !== -1 || s.indexOf('moral') !== -1) return '#C7D2FE';
    if (s.indexOf('កីឡា') !== -1 || s.indexOf('sport') !== -1 || s.indexOf('pe') !== -1 || s.indexOf('physical') !== -1) return '#FECDD3';
    if (s.indexOf('សេដ្ឋកិច្ច') !== -1 || s.indexOf('econ') !== -1) return '#FEF3C7';
    if (s.indexOf('ភាសា') !== -1 || s.indexOf('social') !== -1) return '#E9D5FF';

    if (rawColor && rawColor !== '#E5E7EB' && rawColor !== '#e5e7eb' && rawColor !== '#ffffff' && rawColor !== '#fff' && rawColor !== 'transparent') {
      return rawColor;
    }
    return '#FED766';
  }

  function builderHtml() {
    var state = ctx.state;
    var stats = ctx.stats || E.statistics();
    var curClass = state.classes.filter(function (c) { return c.id === local.selectedClass; })[0] || state.classes[0] || { id: 'class_7A', display: '7A', shift: 'ព្រឹក' };
    var curTeacher = state.teachers.filter(function (t) { return t.id === local.selectedTeacherId; })[0] || state.teachers[0] || { id: 't_K1', code: 'K1', name_en: 'Tr. Sok Dara' };
    var classDisplay = D.toEnClass(curClass.display || curClass.id);
    var teacherDisplay = curTeacher.name_en || D.toEnTeacher(curTeacher.name_kh) || curTeacher.name_kh;

    var homeroomTeacher = 'Tr. Bun Sophy';
    if (curClass.homeroom_teacher_id) {
      var ht = state.teachers.filter(function (t) { return t.id === curClass.homeroom_teacher_id; })[0];
      if (ht) homeroomTeacher = ht.name_en || D.toEnTeacher(ht.name_kh) || ht.name_kh;
    }
    var cleanRoom = curClass.room ? D.toEnRoom(curClass.room).replace(/^Room\s+/i, '') : '101';
    var roomInfo = 'Room ' + cleanRoom + ' (Academic Block A)';
    var pc = stats.per_class || [];
    var classStats = pc.filter(function (p) { return p.id === curClass.id; })[0] || {};
    var classPlaced = classStats.assigned || 0;
    var classCapacity = classStats.capacity || 34;

    var isTeacherView = local.viewMode === 'teacher';
    var isSchoolView = local.viewMode === 'school' || local.preview;

    // Chips for top lesson strip
    var stripChips = isTeacherView ? (E.chipsForTeacher ? E.chipsForTeacher(curTeacher.id) : []) : E.chips(curClass.id);
    var totalRemaining = 0;
    (stripChips || []).forEach(function (c) { totalRemaining += (c.count || 0); });

    var chipsHtml = '';
    if (stripChips && stripChips.length > 0) {
      chipsHtml = stripChips.map(function (c) {
        var isSel = (local.selectedChip === c.id);
        var subjName = formatKhmerSubjectName(c.short_name || D.toEnSubject(c.subject_name));
        var tchrCode = esc(c.teacher_code);
        var clDisplay = D.toEnClass(c.class_display || clsMap(state)[c.class_id] || c.class_id);
        var color = getSubjectBoxColor(c.subject_id, subjName, c.color);
        var chipLabel = clDisplay + ' · ' + (subjName === 'Khmer Literature' ? 'Khmer' : subjName) + ' · ' + tchrCode;

        return '<button class="ks-lesson-chip group px-3 py-1.5 rounded-lg flex items-center gap-1.5 cursor-grab active:cursor-grabbing transition-all select-none ' +
          (isSel ? 'ring-2 ring-emerald-600 shadow-sm is-selected' : 'hover:brightness-95') + '" ' +
          'style="background:' + color + '; color:#111827;" ' +
          'data-act="chip" data-id="' + esc(c.id) + '" draggable="true" data-drag-chip="' + esc(c.id) + '" ' +
          'title="' + esc(chipLabel + ' · ' + c.count + ' periods remaining') + '">' +
          '<span class="text-xs sm:text-[13px] font-medium">' + esc(chipLabel) + '</span>' +
          '<span class="bg-slate-900 text-white px-1.5 py-0.5 rounded-full text-[10px] font-mono font-medium leading-none">x' + c.count + '</span>' +
        '</button>';
      }).join('');
    } else {
      chipsHtml = '<div class="flex items-center gap-1.5 text-emerald-700 font-label-md font-medium py-1">' +
        '<span class="material-symbols-outlined text-[18px]">check_circle</span>' +
        '<span>All lessons scheduled for ' + (isTeacherView ? ('Teacher ' + esc(curTeacher.code)) : ('Class ' + esc(classDisplay))) + ' · Zero conflicts</span>' +
      '</div>';
    }

    // Top Toolbar
    var undoDepth = E.undoDepth ? E.undoDepth() : 0;
    var redoDepth = E.redoDepth ? E.redoDepth() : 0;
    var conflictsCount = stats.conflicts || 0;

    var toolbarHtml =
      '<div class="ks-builder-toolbar bg-white rounded-2xl border border-slate-200/80 shadow-xs p-3.5 sm:p-4 mb-4">' +
        '<div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-3 sm:gap-4">' +
          '<!-- Left: View Mode Selector, Dropdowns, and Context -->' +
          '<div class="ks-builder-toolbar-left flex items-center gap-2.5 sm:gap-3 flex-wrap min-w-0">' +
            '<!-- View Selector Tabs -->' +
            '<div class="inline-flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200/70 shrink-0">' +
              '<button class="px-3 py-1.5 rounded-lg text-xs font-medium transition-all ' +
                (!isTeacherView && !isSchoolView ? 'bg-white text-slate-900 shadow-xs border border-slate-200/80' : 'text-slate-600 hover:text-slate-900') + '" ' +
                'data-act="set-view-mode" data-id="class">' +
                'Class View' +
              '</button>' +
              '<button class="px-3 py-1.5 rounded-lg text-xs font-medium transition-all ' +
                (isTeacherView ? 'bg-white text-slate-900 shadow-xs border border-slate-200/80' : 'text-slate-600 hover:text-slate-900') + '" ' +
                'data-act="set-view-mode" data-id="teacher">' +
                'Teacher View' +
              '</button>' +
              '<button class="px-3 py-1.5 rounded-lg text-xs font-medium transition-all ' +
                (isSchoolView ? 'bg-white text-slate-900 shadow-xs border border-slate-200/80' : 'text-slate-600 hover:text-slate-900') + '" ' +
                'data-act="set-view-mode" data-id="school">' +
                'Overview' +
              '</button>' +
            '</div>' +

            '<!-- Entity Selector Dropdown -->' +
            (isTeacherView
              ? ('<div class="inline-flex items-center gap-1.5 bg-slate-100 px-2.5 py-1 rounded-xl border border-slate-200/70 shrink-0">' +
                  '<span class="text-xs text-slate-500 font-normal">Faculty:</span>' +
                  '<select class="bg-transparent text-xs font-medium text-slate-900 border-0 focus:ring-0 cursor-pointer py-0.5 pl-0.5 pr-6" data-change="builder-teacher-select">' +
                    state.teachers.map(function (tc) {
                      var tcName = tc.name_en || D.toEnTeacher(tc.name_kh) || tc.name_kh;
                      return '<option value="' + esc(tc.id) + '" ' + (tc.id === curTeacher.id ? 'selected' : '') + '>' + esc(tc.code + ' — ' + tcName) + '</option>';
                    }).join('') +
                  '</select>' +
                '</div>')
              : ('<div class="inline-flex items-center gap-1.5 bg-slate-100 px-2.5 py-1 rounded-xl border border-slate-200/70 shrink-0">' +
                  '<span class="text-xs text-slate-500 font-normal">Class:</span>' +
                  '<select class="bg-transparent text-xs font-medium text-slate-900 border-0 focus:ring-0 cursor-pointer py-0.5 pl-0.5 pr-6" data-change="builder-class-select">' +
                    state.classes.map(function (cls) {
                      return '<option value="' + esc(cls.id) + '" ' + (cls.id === curClass.id ? 'selected' : '') + '>Class ' + esc(D.toEnClass(cls.display || cls.id)) + '</option>';
                    }).join('') +
                  '</select>' +
                '</div>')
            ) +

            '<!-- Academic Context Pill -->' +
            '<div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200/60 text-emerald-800 text-xs font-medium shrink-0">' +
              '<span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>' +
              '<span>Main Campus · AY 2026-2027 · Term 1</span>' +
            '</div>' +

            (local.lastSavedAt
              ? '<span id="saveStatusIndicator" class="inline-flex items-center gap-1 text-[11px] text-slate-500 font-normal"><span class="material-symbols-outlined text-[13px] text-emerald-600">check</span><span>Saved ' + esc(local.lastSavedAt) + '</span></span>'
              : '') +
          '</div>' +

          '<!-- Right: Actions Toolbar -->' +
          '<div class="ks-builder-toolbar-actions flex items-center gap-2 flex-wrap">' +
            '<!-- Undo & Redo -->' +
            '<div class="inline-flex items-center bg-slate-100 p-0.5 rounded-xl border border-slate-200/70">' +
              '<button class="p-1.5 sm:p-2 text-slate-600 hover:text-slate-900 hover:bg-white rounded-lg transition-colors disabled:opacity-30 cursor-pointer" data-act="undo" ' + (undoDepth ? '' : 'disabled') + ' title="Undo (Ctrl+Z)">' +
                '<span class="material-symbols-outlined text-[18px]">undo</span>' +
              '</button>' +
              '<button class="p-1.5 sm:p-2 text-slate-600 hover:text-slate-900 hover:bg-white rounded-lg transition-colors disabled:opacity-30 cursor-pointer" data-act="redo" ' + (redoDepth ? '' : 'disabled') + ' title="Redo (Ctrl+Y)">' +
                '<span class="material-symbols-outlined text-[18px]">redo</span>' +
              '</button>' +
            '</div>' +

            '<!-- Save Draft -->' +
            '<button class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-slate-200 text-slate-700 bg-white hover:bg-slate-50 text-xs font-medium transition-colors shadow-xs cursor-pointer" data-act="save-draft" title="Save Draft (Persists to Server)">' +
              '<span class="material-symbols-outlined text-[16px] text-slate-500">save</span>' +
              '<span>Save Draft</span>' +
            '</button>' +

            '<!-- Publish Timetable -->' +
            '<button class="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-[#006C49] text-white hover:bg-[#005236] text-xs font-medium transition-all shadow-xs cursor-pointer" data-act="open-publish-modal" title="Publish official schedule to teacher and student portals">' +
              '<span class="material-symbols-outlined text-[16px]">rocket_launch</span>' +
              '<span>Publish Timetable</span>' +
            '</button>' +
          '</div>' +
        '</div>' +

        '<!-- Cohort Filter Pills (Visible when in Class View) -->' +
        (!isTeacherView && !isSchoolView
          ? ('<div class="mt-3 pt-3 flex flex-wrap items-center gap-1.5 border-t border-slate-100 overflow-x-auto no-scrollbar">' +
              '<span class="text-xs text-slate-500 font-medium uppercase tracking-wider shrink-0 mr-1">Cohort:</span>' +
              state.classes.map(function (c) {
                var isSel = (c.id === curClass.id);
                return '<button class="px-3 py-1 rounded-full text-xs font-medium shrink-0 transition-colors cursor-pointer ' +
                  (isSel ? 'bg-[#006C49] text-white shadow-xs' : 'bg-slate-100 text-slate-700 hover:bg-slate-200') + '" ' +
                  'data-act="set-class-cohort" data-id="' + esc(c.id) + '">' +
                  esc(D.toEnClass(c.display || c.id)) +
                '</button>';
              }).join('') +
            '</div>')
          : '') +
      '</div>';

    // Full-Width Lesson Strip (Directly below toolbar like screenshot)
    var lessonStripHtml =
      '<div class="bg-white rounded-2xl border border-slate-200/80 shadow-xs p-3.5 sm:p-4 mb-4">' +
        '<div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2.5 pb-2.5 border-b border-slate-100">' +
          '<div class="flex items-center gap-2">' +
            '<span class="material-symbols-outlined text-[#006C49] text-[20px]">touch_app</span>' +
            '<span class="text-xs sm:text-sm font-medium text-slate-900">' +
              'Remaining Lessons (' + totalRemaining + '):' +
            '</span>' +
            '<span class="text-xs text-slate-500 font-normal hidden sm:inline">' +
              'Drag chips directly onto the weekly timetable grid' +
            '</span>' +
          '</div>' +
          '<div class="flex items-center gap-2">' +
            '<button class="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-xs flex items-center gap-1.5 transition-colors shadow-xs cursor-pointer" ' +
              'data-act="auto-schedule-current" title="Auto-schedule unplaced lessons for this ' + (isTeacherView ? 'teacher' : 'class') + '">' +
              '<span class="material-symbols-outlined text-[15px]">auto_fix_high</span>' +
              '<span>' + (isTeacherView ? 'Auto-Schedule Teacher' : 'Auto-Schedule Class') + '</span>' +
            '</button>' +
          '</div>' +
        '</div>' +
        '<div class="flex flex-wrap items-center gap-2 pt-3">' +
          chipsHtml +
        '</div>' +
      '</div>';

    var innerView = '';
    if (isSchoolView) {
      innerView = previewModernHtml();
    } else if (isTeacherView) {
      innerView = teacherViewModernHtml();
    } else {
      innerView = classMasterModernHtml(curClass, classDisplay, homeroomTeacher, roomInfo, classPlaced, classCapacity);
    }

    var moveBarHtml = '';
    if (local.targetKey && ctx.grid[local.targetKey]) {
      var tCell = ctx.grid[local.targetKey];
      var p = D.parseGridKey(local.targetKey);
      var subNameKh = formatKhmerSubjectName(tCell.subject_name || tCell.short_name);
      var tchr = (ctx.state.teachers || []).filter(function (t) { return t.id === tCell.teacher_id; })[0];
      var tchrName = tchr ? (tchr.name_en || D.toEnTeacher(tchr.name_kh) || tchr.code) : (tCell.teacher_code || '');
      var clName = D.toEnClass(clsMap(ctx.state)[p.class_id] || p.class_id);

      moveBarHtml = '<div class="fixed bottom-6 left-1/2 -translate-x-1/2 bg-white rounded-2xl shadow-2xl border border-blue-200 px-5 py-3.5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-6 z-50" style="max-width: 680px; width: 92%;">' +
        '<div class="min-w-0 flex-1">' +
          '<div class="text-xs font-medium text-blue-700 flex items-center gap-1.5">' +
            '<span class="w-2 h-2 rounded-full bg-blue-600 animate-pulse"></span>' +
            '<span>Move / Swap Active:</span>' +
          '</div>' +
          '<div class="text-sm font-medium text-slate-900 mt-0.5 truncate">' +
            'Class ' + esc(clName) + ' · ' + esc(subNameKh) + ' · ' + esc(tchrName) + ' (' + esc(D.toEnDay(p.day)) + ' Period ' + p.period + ')' +
          '</div>' +
          '<div class="text-[11px] text-slate-500 mt-0.5 truncate">' +
            'Tap an empty cell to move, tap an occupied cell to swap, or Esc to cancel' +
          '</div>' +
        '</div>' +
        '<div class="flex items-center gap-2 shrink-0 self-end sm:self-center">' +
          '<button class="px-3 py-1.5 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50 text-xs font-medium transition-colors cursor-pointer" data-act="cancel-move">' +
            'Cancel (Esc)' +
          '</button>' +
          '<button class="px-3 py-1.5 rounded-lg bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200 text-xs font-medium transition-colors flex items-center gap-1 cursor-pointer" data-act="delete-placed-lesson" data-key="' + esc(local.targetKey) + '">' +
            '<span class="material-symbols-outlined text-[14px]">delete</span>' +
            '<span>Remove</span>' +
          '</button>' +
        '</div>' +
      '</div>';
    }

    var pageChromeHtml = '<div class="ks-exec-block">' +
      executiveHeadHtml() +
      kpiHtml() +
      moduleNavHtml() +
    '</div>';

    return '<div class="relative w-full overflow-x-hidden pb-12">' +
      '<div class="max-w-[1680px] w-full mx-auto px-3 sm:px-4 lg:px-6 space-y-4 pt-2 sm:pt-4">' +
        pageChromeHtml +
        toolbarHtml +
        lessonStripHtml +
        innerView +
        insightsHtml() +
      '</div>' +
      moveBarHtml +
    '</div>';
  }


  function classMasterModernHtml(curClass, classDisplay, homeroomTeacher, roomInfo, classPlaced, classCapacity) {
    var state = ctx.state, days = state.settings.days;
    var periods = state.settings.periods;

    var conflictKeys = {};
    E.conflicts().forEach(function (c) { if (c.key) conflictKeys[c.key] = c.severity; });

    // Remaining assignments list for current class (for Right Rail)
    var assignments = (state.assignments || []).filter(function (a) { return a.class_id === curClass.id; });
    var remainingListHtml = '';
    var placedCounts = {};
    Object.keys(ctx.grid).forEach(function (k) {
      var c = ctx.grid[k];
      if (c && c.class_id === curClass.id) {
        var sk = c.class_id + '|' + c.subject_id;
        placedCounts[sk] = (placedCounts[sk] || 0) + 1;
      }
    });

    if (assignments.length > 0) {
      remainingListHtml = assignments.map(function (asg) {
        var sub = (state.subjects || []).filter(function (s) { return s.id === asg.subject_id; })[0] || {};
        var tchr = (state.teachers || []).filter(function (t) { return t.id === asg.teacher_id; })[0] || {};
        var subName = formatKhmerSubjectName(sub.name_en || sub.name_kh);
        var tName = tchr.name_en || D.toEnTeacher(tchr.name_kh) || tchr.name_kh || tchr.code || '';
        var quota = asg.lessons || sub.lessons_per_week || 2;
        var scheduled = placedCounts[asg.class_id + '|' + asg.subject_id] || 0;
        var rem = Math.max(0, quota - scheduled);
        var subColor = getSubjectBoxColor(asg.subject_id, subName, sub.color);
        var pct = Math.min(100, Math.round((scheduled / quota) * 100));
        var chipId = asg.class_id + '|' + asg.subject_id + '|' + asg.teacher_id;

        return '<div class="p-3 rounded-xl border border-slate-200/80 bg-white hover:border-slate-300 transition-all space-y-2 select-none" ' +
          'draggable="true" data-drag-chip="' + esc(chipId) + '" title="Drag to schedule ' + esc(subName) + '">' +
          '<div class="flex items-start justify-between gap-2">' +
            '<div class="min-w-0 flex-1">' +
              '<div class="flex items-center gap-1.5 text-xs font-medium text-slate-900 truncate">' +
                '<span class="w-2.5 h-2.5 rounded-full shrink-0" style="background:' + esc(subColor) + ';"></span>' +
                '<span class="truncate">' + esc(subName) + '</span>' +
              '</div>' +
              '<div class="text-[11px] text-slate-500 font-normal mt-0.5 truncate">' +
                esc(tchr.code + ' · ' + tName) +
              '</div>' +
            '</div>' +
            '<span class="px-2 py-0.5 rounded-full text-[11px] font-medium font-mono shrink-0 ' +
              (rem ? 'bg-amber-50 text-amber-700 border border-amber-200/60' : 'bg-emerald-50 text-emerald-700 border border-emerald-200/60') + '">' +
              (rem ? (rem + ' left') : 'Complete') +
            '</span>' +
          '</div>' +
          '<div class="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">' +
            '<div class="h-full rounded-full transition-all ' + (rem ? 'bg-[#006C49]' : 'bg-emerald-500') + '" style="width:' + pct + '%;"></div>' +
          '</div>' +
          '<div class="flex items-center justify-between pt-1 text-[11px]">' +
            '<button class="px-2 py-1 rounded text-slate-700 bg-slate-100 hover:bg-slate-200 transition-colors font-medium cursor-pointer" ' +
              'data-act="select-right-lesson" data-chip-id="' + esc(chipId) + '">' +
              'Select Lesson' +
            '</button>' +
            '<button class="px-2 py-1 rounded text-[#006C49] hover:bg-emerald-50 transition-colors font-medium cursor-pointer" ' +
              'data-act="find-slot" data-chip-id="' + esc(chipId) + '">' +
              'Find Slot' +
            '</button>' +
          '</div>' +
        '</div>';
      }).join('');
    } else {
      remainingListHtml = '<div class="text-xs text-slate-400 py-3 text-center">No subjects assigned for this class yet</div>';
    }

    // Workload summary
    var classPct = Math.min(100, Math.round((classPlaced / (classCapacity || 34)) * 100));

    // Matrix Grid Rows (Morning 1-5, Lunch Break, Afternoon 1-5)
    var morningPeriods = periods.filter(function (p) { return p.shift === 'ព្រឹក'; });
    var afternoonPeriods = periods.filter(function (p) { return p.shift === 'រសៀល'; });
    if (!morningPeriods.length) morningPeriods = periods.slice(0, 5);
    if (!afternoonPeriods.length) afternoonPeriods = periods.slice(5, 10);

    var activeDays = days;
    var isMobile = false; // rendered with responsive table styles

    function renderClassRow(p, isLastMorning) {
      var shiftNameEn = D.toEnShift(p.shift);
      var borderBottomClass = isLastMorning ? 'border-b-2 border-b-slate-300' : 'border-b border-slate-200';
      var cellsHtml = activeDays.map(function (day) {
        var key = D.gridKey(day, p.shift, p.number, curClass.id);
        var cell = ctx.grid[key];
        var hasConflict = !!conflictKeys[key];
        var isTarget = (local.targetKey === key);
        var isHighlighted = (local.highlightSlotKey === key);

        if (cell) {
          var subNameKh = formatKhmerSubjectName(cell.subject_name || cell.short_name);
          var tchrCode = cell.teacher_code || '';
          var codeTag = classDisplay + (tchrCode ? (' · ' + tchrCode) : '');
          var cellBg = getSubjectBoxColor(cell.subject_id, subNameKh, cell.color);

          return '<td class="p-0 border border-slate-200 text-center align-middle h-14 min-h-[58px] relative bg-white ' + borderBottomClass + '" data-cell-drop="' + esc(key) + '">' +
            '<button class="ks-cell-btn w-full h-full min-h-[58px] px-1 py-1 flex flex-col items-center justify-center text-center cursor-grab active:cursor-grabbing select-none transition-all hover:brightness-95 group relative ' +
              (hasConflict ? 'ring-2 ring-rose-500 ring-inset bg-rose-100 text-rose-950' : (isTarget ? 'ring-2 ring-blue-600 ring-inset z-10' : (isHighlighted ? 'ks-slot-pulse ring-2 ring-blue-500 ring-inset' : ''))) + '" ' +
              'style="background:' + esc(cellBg) + ';" ' +
              'data-act="cell" data-key="' + esc(key) + '" draggable="true" data-drag-placed="' + esc(key) + '" ' +
              'title="' + esc(subNameKh + ' · ' + codeTag + ' · Click for Quick Editor') + '">' +
              '<span class="font-medium text-xs sm:text-[13px] text-slate-900 leading-tight block truncate max-w-full">' +
                esc(subNameKh) +
              '</span>' +
              '<span class="text-[10px] sm:text-[11px] font-normal text-slate-700/90 mt-0.5 leading-tight block truncate max-w-full font-sans">' +
                esc(codeTag) +
              '</span>' +
            '</button>' +
          '</td>';
        } else {
          return '<td class="p-0 border border-slate-200 text-center align-middle h-14 min-h-[58px] bg-white relative ' + borderBottomClass + '" data-cell-drop="' + esc(key) + '">' +
            '<button class="ks-cell-btn w-full h-full min-h-[58px] flex items-center justify-center hover:bg-slate-50 transition-colors group select-none ' +
              (isTarget ? 'ring-2 ring-blue-500 ring-inset bg-blue-50/20' : (isHighlighted ? 'ks-slot-pulse ring-2 ring-blue-500 ring-inset' : '')) + '" ' +
              'data-act="cell" data-key="' + esc(key) + '" title="Empty Slot · Tap or drag chip to place">' +
              '<span class="opacity-0 group-hover:opacity-40 text-slate-400 text-sm material-symbols-outlined transition-opacity">add</span>' +
            '</button>' +
          '</td>';
        }
      }).join('');

      return '<tr class="hover:bg-slate-50/40 transition-colors">' +
        '<td class="ks-sticky-time time-col py-2 px-1 text-center bg-slate-50 border border-slate-200 w-20 sm:w-24 ' + borderBottomClass + '">' +
          '<div class="font-medium text-xs sm:text-[13px] text-slate-800 leading-snug">' + shiftNameEn + ' ' + p.number + '</div>' +
          '<div class="font-mono text-[10px] sm:text-[11px] text-slate-500 leading-snug mt-0.5">' + esc(p.start) + '–' + esc(p.end) + '</div>' +
        '</td>' +
        cellsHtml +
      '</tr>';
    }

    var tableRows = '';
    morningPeriods.forEach(function (p, idx) {
      tableRows += renderClassRow(p, idx === morningPeriods.length - 1);
    });

    // Midday Break separator row
    tableRows += '<tr class="bg-slate-100/70 border-y-2 border-slate-300 select-none">' +
      '<td colspan="' + (activeDays.length + 1) + '" class="py-1 px-4 text-center text-[11px] text-slate-600 font-medium tracking-wide">' +
        '<div class="flex items-center justify-center gap-2">' +
          '<span class="w-8 h-px bg-slate-300"></span>' +
          '<span>11:10–13:00 · Lunch &amp; Midday Break</span>' +
          '<span class="w-8 h-px bg-slate-300"></span>' +
        '</div>' +
      '</td>' +
    '</tr>';

    afternoonPeriods.forEach(function (p) {
      tableRows += renderClassRow(p, false);
    });

    return '<div class="grid grid-cols-1 xl:grid-cols-4 gap-4">' +
      '<!-- Left: Timetable Grid (~75%) -->' +
      '<div class="xl:col-span-3 space-y-4">' +
        '<!-- Timetable Matrix Grid -->' +
        '<div class="ks-timetable-container bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-x-auto">' +
          '<table class="ks-timetable-grid w-full text-center border-collapse min-w-[700px] bg-white table-fixed">' +
            '<thead>' +
              '<tr class="bg-slate-50 text-slate-800 text-[13px] font-medium border-b border-slate-200">' +
                '<th class="ks-sticky-corner py-2.5 px-1 w-20 sm:w-24 text-center font-medium border border-slate-200 bg-slate-50">Time</th>' +
                activeDays.map(function (d) {
                  return '<th class="ks-sticky-th py-2.5 px-1 text-center font-medium border border-slate-200 bg-slate-50">' + esc(D.toEnDay(d)) + '</th>';
                }).join('') +
              '</tr>' +
            '</thead>' +
            '<tbody class="divide-y-0 text-slate-900">' +
              tableRows +
            '</tbody>' +
          '</table>' +
        '</div>' +
      '</div>' +

      '<!-- Right: Remaining Lessons & Scheduling Information (~25%) -->' +
      '<div class="xl:col-span-1 space-y-4">' +
        '<!-- Class Workload Progress Card -->' +
        '<div class="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-xs space-y-2.5">' +
          '<div class="flex items-center justify-between text-xs font-medium text-slate-900">' +
            '<span>Class Workload</span>' +
            '<span class="font-mono text-slate-600">' + classPlaced + ' / ' + classCapacity + ' Periods</span>' +
          '</div>' +
          '<div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">' +
            '<div class="h-full bg-[#006C49] rounded-full transition-all" style="width:' + classPct + '%;"></div>' +
          '</div>' +
          '<div class="flex items-center justify-between text-[11px] text-slate-500">' +
            '<span>' + classPct + '% Scheduled</span>' +
            '<span>' + Math.max(0, classCapacity - classPlaced) + ' Periods Left</span>' +
          '</div>' +
        '</div>' +

        '<!-- Remaining Assignments Vertically Scrollable List -->' +
        '<div class="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-xs space-y-3">' +
          '<div class="flex items-center justify-between pb-2 border-b border-slate-100">' +
            '<div class="flex items-center gap-1.5">' +
              '<span class="material-symbols-outlined text-[18px] text-[#006C49]">list_alt</span>' +
              '<h4 class="text-xs sm:text-sm font-medium text-slate-900">Remaining Assignments</h4>' +
            '</div>' +
            '<span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-medium bg-slate-100 text-slate-700">' +
              assignments.length +
            '</span>' +
          '</div>' +
          '<div class="space-y-2 max-h-[440px] overflow-y-auto pr-1">' +
            remainingListHtml +
          '</div>' +
        '</div>' +

        '<!-- Conflict Audit Summary Card -->' +
        '<div class="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-xs space-y-2.5">' +
          '<div class="flex items-center justify-between">' +
            '<div class="flex items-center gap-1.5">' +
              '<span class="material-symbols-outlined text-[18px] ' + (E.conflicts().length ? 'text-rose-600' : 'text-emerald-600') + '">verified</span>' +
              '<h4 class="text-xs sm:text-sm font-medium text-slate-900">Conflict Audit</h4>' +
            '</div>' +
            '<button class="text-xs text-[#006C49] hover:underline font-medium cursor-pointer" data-act="conflicts">' +
              'View All' +
            '</button>' +
          '</div>' +
          (E.conflicts().length
            ? ('<div class="p-2.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs font-medium flex items-center gap-2">' +
                '<span class="material-symbols-outlined text-[18px] text-rose-600">error</span>' +
                '<span>' + E.conflicts().length + ' schedule collisions detected</span>' +
              '</div>')
            : ('<div class="p-2.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-medium flex items-center gap-2">' +
                '<span class="material-symbols-outlined text-[18px] text-emerald-600">check_circle</span>' +
                '<span>Zero conflicts · Timetable is valid</span>' +
              '</div>')
          ) +
        '</div>' +
      '</div>' +
    '</div>';
  }

  function teacherViewModernHtml() {
    var state = ctx.state, days = state.settings.days, periods = state.settings.periods;
    var t = state.teachers.filter(function (x) { return x.id === local.selectedTeacherId; })[0] || state.teachers[0];
    var tName = t.name_en || D.toEnTeacher(t.name_kh) || t.name_kh;

    var teacherPlacedCount = 0;
    Object.keys(ctx.grid).forEach(function (k) {
      var c = ctx.grid[k];
      if (c && c.teacher_id === t.id) teacherPlacedCount++;
    });

    var targetHours = t.target || 17;
    var teacherPct = Math.min(100, Math.round((teacherPlacedCount / targetHours) * 100));

    // Teacher's remaining assignments across all classes
    var teacherAssignments = (state.assignments || []).filter(function (a) { return a.teacher_id === t.id; });
    var placedCounts = {};
    Object.keys(ctx.grid).forEach(function (k) {
      var c = ctx.grid[k];
      if (c && c.teacher_id === t.id) {
        var sk = c.class_id + '|' + c.subject_id;
        placedCounts[sk] = (placedCounts[sk] || 0) + 1;
      }
    });

    var remainingTeacherHtml = '';
    if (teacherAssignments.length > 0) {
      remainingTeacherHtml = teacherAssignments.map(function (asg) {
        var sub = (state.subjects || []).filter(function (s) { return s.id === asg.subject_id; })[0] || {};
        var cl = (state.classes || []).filter(function (c) { return c.id === asg.class_id; })[0] || {};
        var subName = formatKhmerSubjectName(sub.name_en || sub.name_kh);
        var clDisplay = D.toEnClass(cl.display || asg.class_id);
        var quota = asg.lessons || sub.lessons_per_week || 2;
        var scheduled = placedCounts[asg.class_id + '|' + asg.subject_id] || 0;
        var rem = Math.max(0, quota - scheduled);
        var subColor = getSubjectBoxColor(asg.subject_id, subName, sub.color);
        var pct = Math.min(100, Math.round((scheduled / quota) * 100));
        var chipId = asg.class_id + '|' + asg.subject_id + '|' + asg.teacher_id;

        return '<div class="p-3 rounded-xl border border-slate-200/80 bg-white hover:border-slate-300 transition-all space-y-2 select-none" ' +
          'draggable="true" data-drag-chip="' + esc(chipId) + '" title="Drag to schedule Class ' + esc(clDisplay) + '">' +
          '<div class="flex items-start justify-between gap-2">' +
            '<div class="min-w-0 flex-1">' +
              '<div class="flex items-center gap-1.5 text-xs font-medium text-slate-900 truncate">' +
                '<span class="w-2.5 h-2.5 rounded-full shrink-0" style="background:' + esc(subColor) + ';"></span>' +
                '<span class="truncate">Class ' + esc(clDisplay) + ' — ' + esc(subName) + '</span>' +
              '</div>' +
              '<div class="text-[11px] text-slate-500 font-normal mt-0.5 truncate">' +
                esc(t.code + ' · ' + tName) +
              '</div>' +
            '</div>' +
            '<span class="px-2 py-0.5 rounded-full text-[11px] font-medium font-mono shrink-0 ' +
              (rem ? 'bg-amber-50 text-amber-700 border border-amber-200/60' : 'bg-emerald-50 text-emerald-700 border border-emerald-200/60') + '">' +
              (rem ? (rem + ' left') : 'Complete') +
            '</span>' +
          '</div>' +
          '<div class="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">' +
            '<div class="h-full rounded-full transition-all ' + (rem ? 'bg-[#006C49]' : 'bg-emerald-500') + '" style="width:' + pct + '%;"></div>' +
          '</div>' +
          '<div class="flex items-center justify-between pt-1 text-[11px]">' +
            '<button class="px-2 py-1 rounded text-slate-700 bg-slate-100 hover:bg-slate-200 transition-colors font-medium cursor-pointer" ' +
              'data-act="select-right-lesson" data-chip-id="' + esc(chipId) + '">' +
              'Select Lesson' +
            '</button>' +
            '<button class="px-2 py-1 rounded text-[#006C49] hover:bg-emerald-50 transition-colors font-medium cursor-pointer" ' +
              'data-act="find-slot" data-chip-id="' + esc(chipId) + '">' +
              'Find Slot' +
            '</button>' +
          '</div>' +
        '</div>';
      }).join('');
    } else {
      remainingTeacherHtml = '<div class="text-xs text-slate-400 py-3 text-center">No assignments configured for this faculty</div>';
    }

    var morningPeriods = periods.filter(function (p) { return p.shift === 'ព្រឹក'; });
    var afternoonPeriods = periods.filter(function (p) { return p.shift === 'រសៀល'; });
    if (!morningPeriods.length) morningPeriods = periods.slice(0, 5);
    if (!afternoonPeriods.length) afternoonPeriods = periods.slice(5, 10);

    function renderTeacherPeriodRow(p, isLastMorning) {
      var shiftNameEn = D.toEnShift(p.shift);
      var borderBottomClass = isLastMorning ? 'border-b-2 border-b-slate-300' : 'border-b border-slate-200';
      var cellsHtml = days.map(function (day) {
        var foundCell = null;
        var cellKey = null;
        Object.keys(ctx.grid).forEach(function (k) {
          var c = ctx.grid[k];
          if (c && c.teacher_id === t.id) {
            var pk = D.parseGridKey(k);
            if (pk.day === day && pk.shift === p.shift && pk.period === p.number) {
              foundCell = c;
              cellKey = k;
            }
          }
        });

        if (foundCell) {
          var subKh = formatKhmerSubjectName(foundCell.subject_name || foundCell.short_name);
          var clName = D.toEnClass(clsMap(state)[foundCell.class_id] || foundCell.class_id) || '7A';
          var codeTag = clName + ' · ' + (foundCell.teacher_code || t.code);
          var cellBg = getSubjectBoxColor(foundCell.subject_id, subKh, foundCell.color);

          return '<td class="p-0 border border-slate-200 text-center align-middle h-14 min-h-[58px] relative bg-white ' + borderBottomClass + '" data-cell-drop="' + esc(cellKey) + '">' +
            '<button class="ks-cell-btn w-full h-full min-h-[58px] px-1 py-1 flex flex-col items-center justify-center text-center cursor-grab active:cursor-grabbing select-none transition-all hover:brightness-95 group relative" ' +
              'style="background:' + esc(cellBg) + ';" ' +
              'data-act="cell" data-key="' + esc(cellKey) + '" draggable="true" data-drag-placed="' + esc(cellKey) + '" ' +
              'title="' + esc(subKh + ' · ' + codeTag + ' · Click for Quick Editor') + '">' +
              '<span class="font-medium text-xs sm:text-[13px] text-slate-900 leading-tight block truncate max-w-full">' +
                esc(subKh) +
              '</span>' +
              '<span class="text-[10px] sm:text-[11px] font-normal text-slate-700/90 mt-0.5 leading-tight block truncate max-w-full font-sans">' +
                esc(codeTag) +
              '</span>' +
            '</button>' +
          '</td>';
        } else {
          var emptyKey = D.gridKey(day, p.shift, p.number, 'class_7A');
          return '<td class="p-0 border border-slate-200 text-center align-middle h-14 min-h-[58px] bg-white relative ' + borderBottomClass + '" data-cell-drop="' + esc(emptyKey) + '">' +
            '<button class="ks-cell-btn w-full h-full min-h-[58px] flex items-center justify-center hover:bg-slate-50 transition-colors group select-none" ' +
              'data-act="cell" data-key="' + esc(emptyKey) + '" title="Available Slot · Drop or tap chip to schedule">' +
              '<span class="opacity-0 group-hover:opacity-40 text-slate-400 text-sm material-symbols-outlined transition-opacity">add</span>' +
            '</button>' +
          '</td>';
        }
      }).join('');

      return '<tr class="hover:bg-slate-50/40 transition-colors">' +
        '<td class="ks-sticky-time time-col py-2 px-1 text-center bg-slate-50 border border-slate-200 w-20 sm:w-24 ' + borderBottomClass + '">' +
          '<div class="font-medium text-xs sm:text-[13px] text-slate-800 leading-snug">' + shiftNameEn + ' ' + p.number + '</div>' +
          '<div class="font-mono text-[10px] sm:text-[11px] text-slate-500 leading-snug mt-0.5">' + esc(p.start) + '–' + esc(p.end) + '</div>' +
        '</td>' +
        cellsHtml +
      '</tr>';
    }

    var tableRows = '';
    morningPeriods.forEach(function (p, idx) {
      tableRows += renderTeacherPeriodRow(p, idx === morningPeriods.length - 1);
    });

    tableRows += '<tr class="bg-slate-100/70 border-y-2 border-slate-300 select-none">' +
      '<td colspan="' + (days.length + 1) + '" class="py-1 px-4 text-center text-[11px] text-slate-600 font-medium tracking-wide">' +
        '<div class="flex items-center justify-center gap-2">' +
          '<span class="w-8 h-px bg-slate-300"></span>' +
          '<span>11:10–13:00 · Lunch &amp; Midday Break</span>' +
          '<span class="w-8 h-px bg-slate-300"></span>' +
        '</div>' +
      '</td>' +
    '</tr>';

    afternoonPeriods.forEach(function (p) {
      tableRows += renderTeacherPeriodRow(p, false);
    });

    return '<div class="grid grid-cols-1 xl:grid-cols-4 gap-4">' +
      '<!-- Left: Timetable Grid (~75%) -->' +
      '<div class="xl:col-span-3 space-y-4">' +
        '<!-- Timetable Matrix Grid -->' +
        '<div class="ks-timetable-container bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-x-auto">' +
          '<table class="ks-timetable-grid w-full text-center border-collapse min-w-[700px] bg-white table-fixed">' +
            '<thead>' +
              '<tr class="bg-slate-50 text-slate-800 text-[13px] font-medium border-b border-slate-200">' +
                '<th class="ks-sticky-corner py-2.5 px-1 w-20 sm:w-24 text-center font-medium border border-slate-200 bg-slate-50">Time</th>' +
                activeDays.map(function (d) {
                  return '<th class="ks-sticky-th py-2.5 px-1 text-center font-medium border border-slate-200 bg-slate-50">' + esc(D.toEnDay(d)) + '</th>';
                }).join('') +
              '</tr>' +
            '</thead>' +
            '<tbody class="divide-y-0 text-slate-900">' +
              tableRows +
            '</tbody>' +
          '</table>' +
        '</div>' +
      '</div>' +

      '<!-- Right: Remaining Lessons & Scheduling Information (~25%) -->' +
      '<div class="xl:col-span-1 space-y-4">' +
        '<!-- Class Workload Progress Card -->' +
        '<div class="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-xs space-y-2.5">' +
          '<div class="flex items-center justify-between text-xs font-medium text-slate-900">' +
            '<span>Class Workload</span>' +
            '<span class="font-mono text-slate-600">' + classPlaced + ' / ' + classCapacity + ' Periods</span>' +
          '</div>' +
          '<div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">' +
            '<div class="h-full bg-[#006C49] rounded-full transition-all" style="width:' + classPct + '%;"></div>' +
          '</div>' +
          '<div class="flex items-center justify-between text-[11px] text-slate-500">' +
            '<span>' + classPct + '% Scheduled</span>' +
            '<span>' + Math.max(0, classCapacity - classPlaced) + ' Periods Left</span>' +
          '</div>' +
        '</div>' +

        '<!-- Remaining Assignments Vertically Scrollable List -->' +
        '<div class="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-xs space-y-3">' +
          '<div class="flex items-center justify-between pb-2 border-b border-slate-100">' +
            '<div class="flex items-center gap-1.5">' +
              '<span class="material-symbols-outlined text-[18px] text-[#006C49]">list_alt</span>' +
              '<h4 class="text-xs sm:text-sm font-medium text-slate-900">Remaining Assignments</h4>' +
            '</div>' +
            '<span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-medium bg-slate-100 text-slate-700">' +
              assignments.length +
            '</span>' +
          '</div>' +
          '<div class="space-y-2 max-h-[440px] overflow-y-auto pr-1">' +
            remainingListHtml +
          '</div>' +
        '</div>' +

        '<!-- Conflict Audit Summary Card -->' +
        '<div class="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-xs space-y-2.5">' +
          '<div class="flex items-center justify-between">' +
            '<div class="flex items-center gap-1.5">' +
              '<span class="material-symbols-outlined text-[18px] ' + (E.conflicts().length ? 'text-rose-600' : 'text-emerald-600') + '">verified</span>' +
              '<h4 class="text-xs sm:text-sm font-medium text-slate-900">Conflict Audit</h4>' +
            '</div>' +
            '<button class="text-xs text-[#006C49] hover:underline font-medium cursor-pointer" data-act="conflicts">' +
              'View All' +
            '</button>' +
          '</div>' +
          (E.conflicts().length
            ? ('<div class="p-2.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs font-medium flex items-center gap-2">' +
                '<span class="material-symbols-outlined text-[18px] text-rose-600">error</span>' +
                '<span>' + E.conflicts().length + ' schedule collisions detected</span>' +
              '</div>')
            : ('<div class="p-2.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-medium flex items-center gap-2">' +
                '<span class="material-symbols-outlined text-[18px] text-emerald-600">check_circle</span>' +
                '<span>Zero conflicts · Timetable is valid</span>' +
              '</div>')
          ) +
        '</div>' +
      '</div>' +
    '</div>';
  }

  function teacherViewModernHtml() {
    var state = ctx.state, days = state.settings.days, periods = state.settings.periods;
    var t = state.teachers.filter(function (x) { return x.id === local.selectedTeacherId; })[0] || state.teachers[0];
    var tName = t.name_en || D.toEnTeacher(t.name_kh) || t.name_kh;

    var teacherPlacedCount = 0;
    Object.keys(ctx.grid).forEach(function (k) {
      var c = ctx.grid[k];
      if (c && c.teacher_id === t.id) teacherPlacedCount++;
    });

    var targetHours = t.target || 17;
    var teacherPct = Math.min(100, Math.round((teacherPlacedCount / targetHours) * 100));

    // Teacher's remaining assignments across all classes
    var teacherAssignments = (state.assignments || []).filter(function (a) { return a.teacher_id === t.id; });
    var placedCounts = {};
    Object.keys(ctx.grid).forEach(function (k) {
      var c = ctx.grid[k];
      if (c && c.teacher_id === t.id) {
        var sk = c.class_id + '|' + c.subject_id;
        placedCounts[sk] = (placedCounts[sk] || 0) + 1;
      }
    });

    var remainingTeacherHtml = '';
    if (teacherAssignments.length > 0) {
      remainingTeacherHtml = teacherAssignments.map(function (asg) {
        var sub = (state.subjects || []).filter(function (s) { return s.id === asg.subject_id; })[0] || {};
        var cl = (state.classes || []).filter(function (c) { return c.id === asg.class_id; })[0] || {};
        var subName = formatKhmerSubjectName(sub.name_en || sub.name_kh);
        var clDisplay = D.toEnClass(cl.display || asg.class_id);
        var quota = asg.lessons || sub.lessons_per_week || 2;
        var scheduled = placedCounts[asg.class_id + '|' + asg.subject_id] || 0;
        var rem = Math.max(0, quota - scheduled);
        var subColor = getSubjectBoxColor(asg.subject_id, subName, sub.color);
        var pct = Math.min(100, Math.round((scheduled / quota) * 100));
        var chipId = asg.class_id + '|' + asg.subject_id + '|' + asg.teacher_id;

        return '<div class="p-3 rounded-xl border border-slate-200/80 bg-white hover:border-slate-300 transition-all space-y-2 select-none" ' +
          'draggable="true" data-drag-chip="' + esc(chipId) + '" title="Drag to schedule Class ' + esc(clDisplay) + '">' +
          '<div class="flex items-start justify-between gap-2">' +
            '<div class="min-w-0 flex-1">' +
              '<div class="flex items-center gap-1.5 text-xs font-medium text-slate-900 truncate">' +
                '<span class="w-2.5 h-2.5 rounded-full shrink-0" style="background:' + esc(subColor) + ';"></span>' +
                '<span class="truncate">Class ' + esc(clDisplay) + ' — ' + esc(subName) + '</span>' +
              '</div>' +
              '<div class="text-[11px] text-slate-500 font-normal mt-0.5 truncate">' +
                esc(t.code + ' · ' + tName) +
              '</div>' +
            '</div>' +
            '<span class="px-2 py-0.5 rounded-full text-[11px] font-medium font-mono shrink-0 ' +
              (rem ? 'bg-amber-50 text-amber-700 border border-amber-200/60' : 'bg-emerald-50 text-emerald-700 border border-emerald-200/60') + '">' +
              (rem ? (rem + ' left') : 'Complete') +
            '</span>' +
          '</div>' +
          '<div class="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">' +
            '<div class="h-full rounded-full transition-all ' + (rem ? 'bg-[#006C49]' : 'bg-emerald-500') + '" style="width:' + pct + '%;"></div>' +
          '</div>' +
          '<div class="flex items-center justify-between pt-1 text-[11px]">' +
            '<button class="px-2 py-1 rounded text-slate-700 bg-slate-100 hover:bg-slate-200 transition-colors font-medium cursor-pointer" ' +
              'data-act="select-right-lesson" data-chip-id="' + esc(chipId) + '">' +
              'Select Lesson' +
            '</button>' +
            '<button class="px-2 py-1 rounded text-[#006C49] hover:bg-emerald-50 transition-colors font-medium cursor-pointer" ' +
              'data-act="find-slot" data-chip-id="' + esc(chipId) + '">' +
              'Find Slot' +
            '</button>' +
          '</div>' +
        '</div>';
      }).join('');
    } else {
      remainingTeacherHtml = '<div class="text-xs text-slate-400 py-3 text-center">No assignments configured for this faculty</div>';
    }

    var morningPeriods = periods.filter(function (p) { return p.shift === 'ព្រឹក'; });
    var afternoonPeriods = periods.filter(function (p) { return p.shift === 'រសៀល'; });
    if (!morningPeriods.length) morningPeriods = periods.slice(0, 5);
    if (!afternoonPeriods.length) afternoonPeriods = periods.slice(5, 10);

    function renderTeacherPeriodRow(p, isLastMorning) {
      var shiftNameEn = D.toEnShift(p.shift);
      var borderBottomClass = isLastMorning ? 'border-b-2 border-b-slate-300' : 'border-b border-slate-200';
      var cellsHtml = days.map(function (day) {
        var foundCell = null;
        var cellKey = null;
        Object.keys(ctx.grid).forEach(function (k) {
          var c = ctx.grid[k];
          if (c && c.teacher_id === t.id) {
            var pk = D.parseGridKey(k);
            if (pk.day === day && pk.shift === p.shift && pk.period === p.number) {
              foundCell = c;
              cellKey = k;
            }
          }
        });

        if (foundCell) {
          var subKh = formatKhmerSubjectName(foundCell.subject_name || foundCell.short_name);
          var clName = D.toEnClass(clsMap(state)[foundCell.class_id] || foundCell.class_id) || '7A';
          var codeTag = clName + ' · ' + (foundCell.teacher_code || t.code);
          var cellBg = getSubjectBoxColor(foundCell.subject_id, subKh, foundCell.color);

          return '<td class="p-0 border border-slate-200 text-center align-middle h-14 min-h-[58px] relative bg-white ' + borderBottomClass + '" data-cell-drop="' + esc(cellKey) + '">' +
            '<button class="ks-cell-btn w-full h-full min-h-[58px] px-1 py-1 flex flex-col items-center justify-center text-center cursor-grab active:cursor-grabbing select-none transition-all hover:brightness-95 group relative" ' +
              'style="background:' + esc(cellBg) + ';" ' +
              'data-act="cell" data-key="' + esc(cellKey) + '" draggable="true" data-drag-placed="' + esc(cellKey) + '" ' +
              'title="' + esc(subKh + ' · ' + codeTag + ' · Click for Quick Editor') + '">' +
              '<span class="font-medium text-xs sm:text-[13px] text-slate-900 leading-tight block truncate max-w-full">' +
                esc(subKh) +
              '</span>' +
              '<span class="text-[10px] sm:text-[11px] font-normal text-slate-700/90 mt-0.5 leading-tight block truncate max-w-full font-sans">' +
                esc(codeTag) +
              '</span>' +
            '</button>' +
          '</td>';
        } else {
          var emptyKey = D.gridKey(day, p.shift, p.number, 'class_7A');
          return '<td class="p-0 border border-slate-200 text-center align-middle h-14 min-h-[58px] bg-white relative ' + borderBottomClass + '" data-cell-drop="' + esc(emptyKey) + '">' +
            '<button class="ks-cell-btn w-full h-full min-h-[58px] flex items-center justify-center hover:bg-slate-50 transition-colors group select-none" ' +
              'data-act="cell" data-key="' + esc(emptyKey) + '" title="Available Slot · Drop or tap chip to schedule">' +
              '<span class="opacity-0 group-hover:opacity-40 text-slate-400 text-sm material-symbols-outlined transition-opacity">add</span>' +
            '</button>' +
          '</td>';
        }
      }).join('');

      return '<tr class="hover:bg-slate-50/40 transition-colors">' +
        '<td class="ks-sticky-time time-col py-2 px-1 text-center bg-slate-50 border border-slate-200 w-20 sm:w-24 ' + borderBottomClass + '">' +
          '<div class="font-medium text-xs sm:text-[13px] text-slate-800 leading-snug">' + shiftNameEn + ' ' + p.number + '</div>' +
          '<div class="font-mono text-[10px] sm:text-[11px] text-slate-500 leading-snug mt-0.5">' + esc(p.start) + '–' + esc(p.end) + '</div>' +
        '</td>' +
        cellsHtml +
      '</tr>';
    }

    var tableRows = '';
    morningPeriods.forEach(function (p, idx) {
      tableRows += renderTeacherPeriodRow(p, idx === morningPeriods.length - 1);
    });

    tableRows += '<tr class="bg-slate-100/70 border-y-2 border-slate-300 select-none">' +
      '<td colspan="' + (days.length + 1) + '" class="py-1 px-4 text-center text-[11px] text-slate-600 font-medium tracking-wide">' +
        '<div class="flex items-center justify-center gap-2">' +
          '<span class="w-8 h-px bg-slate-300"></span>' +
          '<span>11:10–13:00 · Lunch &amp; Midday Break</span>' +
          '<span class="w-8 h-px bg-slate-300"></span>' +
        '</div>' +
      '</td>' +
    '</tr>';

    afternoonPeriods.forEach(function (p) {
      tableRows += renderTeacherPeriodRow(p, false);
    });

    return '<div class="grid grid-cols-1 xl:grid-cols-4 gap-4">' +
      '<!-- Left: Timetable Grid (~75%) -->' +
      '<div class="xl:col-span-3 space-y-4">' +
        '<!-- Teacher Header Banner -->' +
        '<div class="bg-white p-3.5 sm:p-4 rounded-2xl border border-slate-200/80 shadow-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">' +
          '<div class="flex items-center gap-3 min-w-0">' +
            '<div class="w-11 h-11 rounded-xl bg-[#006C49] text-white flex items-center justify-center font-medium text-base sm:text-lg shrink-0 shadow-xs">' +
              esc(t.code) +
            '</div>' +
            '<div class="min-w-0">' +
              '<div class="flex flex-wrap items-center gap-2">' +
                '<h3 class="text-sm sm:text-base md:text-lg text-slate-900 font-medium truncate">' +
                  esc(t.code + ' — ' + tName) +
                '</h3>' +
                '<span class="px-2 py-0.5 rounded text-[11px] bg-slate-100 text-slate-700 font-medium shrink-0">' +
                  'Target: ' + targetHours + ' hrs/wk' +
                '</span>' +
              '</div>' +
              '<p class="text-xs text-slate-500 truncate mt-0.5">' +
                'Department: ' + esc(t.department || 'General') + ' · Scheduled: ' + teacherPlacedCount + ' / ' + targetHours + ' hrs · ' +
                (teacherPlacedCount > targetHours ? '<span class="text-rose-600 font-medium">Overloaded</span>' : '<span class="text-emerald-700 font-medium">Within Target</span>') +
              '</p>' +
            '</div>' +
          '</div>' +
          '<div class="flex items-center gap-2 w-full sm:w-auto shrink-0 justify-end">' +
            '<button class="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-medium transition-colors cursor-pointer" data-act="auto-schedule-current">' +
              '<span class="material-symbols-outlined text-[16px]">auto_fix_high</span>' +
              '<span>Auto-Schedule Faculty</span>' +
            '</button>' +
          '</div>' +
        '</div>' +

        '<!-- Timetable Matrix Grid -->' +
        '<div class="ks-timetable-container bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-x-auto">' +
          '<table class="ks-timetable-grid w-full text-center border-collapse min-w-[700px] bg-white table-fixed">' +
            '<thead>' +
              '<tr class="bg-slate-50 text-slate-800 text-[13px] font-medium border-b border-slate-200">' +
                '<th class="ks-sticky-corner py-2.5 px-1 w-20 sm:w-24 text-center font-medium border border-slate-200 bg-slate-50">Time</th>' +
                days.map(function (d) {
                  return '<th class="ks-sticky-th py-2.5 px-1 text-center font-medium border border-slate-200 bg-slate-50">' + esc(D.toEnDay(d)) + '</th>';
                }).join('') +
              '</tr>' +
            '</thead>' +
            '<tbody class="divide-y-0 text-slate-900">' +
              tableRows +
            '</tbody>' +
          '</table>' +
        '</div>' +
      '</div>' +

      '<!-- Right: Remaining Lessons & Scheduling Information (~25%) -->' +
      '<div class="xl:col-span-1 space-y-4">' +
        '<!-- Workload Progress Card -->' +
        '<div class="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-xs space-y-2.5">' +
          '<div class="flex items-center justify-between text-xs font-medium text-slate-900">' +
            '<span>Faculty Workload</span>' +
            '<span class="font-mono text-slate-600">' + teacherPlacedCount + ' / ' + targetHours + ' hrs</span>' +
          '</div>' +
          '<div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">' +
            '<div class="h-full bg-[#006C49] rounded-full transition-all" style="width:' + teacherPct + '%;"></div>' +
          '</div>' +
          '<div class="flex items-center justify-between text-[11px] text-slate-500">' +
            '<span>' + teacherPct + '% Scheduled</span>' +
            '<span>' + Math.max(0, targetHours - teacherPlacedCount) + ' hrs Remaining</span>' +
          '</div>' +
        '</div>' +

        '<!-- Remaining Assignments for Teacher Card -->' +
        '<div class="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-xs space-y-3">' +
          '<div class="flex items-center justify-between pb-2 border-b border-slate-100">' +
            '<div class="flex items-center gap-1.5">' +
              '<span class="material-symbols-outlined text-[18px] text-[#006C49]">list_alt</span>' +
              '<h4 class="text-xs sm:text-sm font-medium text-slate-900">Assigned Cohorts</h4>' +
            '</div>' +
            '<span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-medium bg-slate-100 text-slate-700">' +
              teacherAssignments.length +
            '</span>' +
          '</div>' +
          '<div class="space-y-2 max-h-[440px] overflow-y-auto pr-1">' +
            remainingTeacherHtml +
          '</div>' +
        '</div>' +

        '<!-- Conflict Audit Card -->' +
        '<div class="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-xs space-y-2.5">' +
          '<div class="flex items-center justify-between">' +
            '<div class="flex items-center gap-1.5">' +
              '<span class="material-symbols-outlined text-[18px] ' + (E.conflicts().length ? 'text-rose-600' : 'text-emerald-600') + '">verified</span>' +
              '<h4 class="text-xs sm:text-sm font-medium text-slate-900">Conflict Audit</h4>' +
            '</div>' +
            '<button class="text-xs text-[#006C49] hover:underline font-medium cursor-pointer" data-act="conflicts">' +
              'View All' +
            '</button>' +
          '</div>' +
          (E.conflicts().length
            ? ('<div class="p-2.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs font-medium flex items-center gap-2">' +
                '<span class="material-symbols-outlined text-[18px] text-rose-600">error</span>' +
                '<span>' + E.conflicts().length + ' schedule collisions detected</span>' +
              '</div>')
            : ('<div class="p-2.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-medium flex items-center gap-2">' +
                '<span class="material-symbols-outlined text-[18px] text-emerald-600">check_circle</span>' +
                '<span>Zero conflicts · Timetable is valid</span>' +
              '</div>')
          ) +
        '</div>' +
      '</div>' +
    '</div>';
  }

  function previewModernHtml() {
    var state = ctx.state, days = state.settings.days, periods = state.settings.periods;
    var shiftPeriods = periods.slice(0, 5);

    var header = '<tr>' +
      '<th class="py-3 px-4 text-left font-medium text-primary uppercase text-label-sm bg-surface-container-low border-b border-surface-container-high sticky left-0 z-10">Class</th>' +
      days.map(function (d) {
        return '<th colspan="' + shiftPeriods.length + '" class="py-3 px-2 text-center font-medium text-primary border-b border-surface-container-high bg-surface-container-low">' +
          esc(D.toEnDay(d)) +
        '</th>';
      }).join('') +
    '</tr>' +
    '<tr class="bg-surface-container-low/60 text-[11px] font-mono text-on-surface-variant">' +
      '<th class="py-1 px-4 text-left sticky left-0 bg-surface-container-low/60 z-10"></th>' +
      days.map(function () {
        return shiftPeriods.map(function (p) {
          return '<th class="py-1 px-1 text-center font-normal">P' + kh(p.number) + '</th>';
        }).join('');
      }).join('') +
    '</tr>';

    var rows = state.classes.map(function (c) {
      var cells = days.map(function (d) {
        return shiftPeriods.map(function (p) {
          var cell = ctx.grid[D.gridKey(d, p.shift, p.number, c.id)];
          if (cell) {
            var subKh = formatKhmerSubjectName(cell.short_name || cell.subject_name || '');
            var cellBg = getSubjectBoxColor(cell.subject_id, subKh, cell.color);
            return '<td class="p-1">' +
              '<div class="px-1.5 py-1 rounded text-center text-[11px] truncate font-medium" style="background:' + esc(cellBg) + ';color:#111827;" title="' + esc(subKh + ' · ' + cell.teacher_code) + '">' +
                esc(cell.teacher_code) +
              '</div>' +
            '</td>';
          } else {
            return '<td class="p-1"><div class="h-6 rounded bg-slate-100"></div></td>';
          }
        }).join('');
      }).join('');

      return '<tr class="hover:bg-slate-50 transition-colors border-b border-slate-200">' +
        '<td class="py-2 px-4 text-[13px] font-medium text-[#006C49] sticky left-0 bg-white z-10 whitespace-nowrap">' +
          'Class ' + esc(D.toEnClass(c.display || c.id)) +
        '</td>' +
        cells +
      '</tr>';
    }).join('');

    return '<div class="bg-white rounded-2xl border border-slate-200/80 shadow-xs p-4 space-y-4">' +
      '<div class="flex items-center justify-between pb-3 border-b border-slate-100">' +
        '<div class="flex items-center gap-2">' +
          '<span class="material-symbols-outlined text-[22px] text-[#006C49]">table_chart</span>' +
          '<h3 class="text-base font-medium text-slate-900">School Master Preview Matrix</h3>' +
        '</div>' +
        '<button class="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-[#006C49] text-white text-xs font-medium hover:bg-[#005236] transition-colors shadow-xs cursor-pointer" data-act="open-publish-modal">' +
          '<span class="material-symbols-outlined text-[16px]">rocket_launch</span>' +
          '<span>Publish to Teacher &amp; Student</span>' +
        '</button>' +
      '</div>' +
      '<div class="overflow-x-auto no-scrollbar">' +
        '<table class="w-full text-left border-collapse min-w-[900px]">' +
          '<thead>' + header + '</thead>' +
          '<tbody>' + rows + '</tbody>' +
        '</table>' +
      '</div>' +
    '</div>';
  }

  function previewHtml() {
    return previewModernHtml();
  }

  function moveOrSwapLesson(sourceKey, targetKey) {
    if (!sourceKey || !targetKey || sourceKey === targetKey) return false;
    var state = ctx.state;
    var sCell = state.grid[sourceKey];
    if (!sCell) return false;
    var tCell = state.grid[targetKey];
    var pSrc = D.parseGridKey(sourceKey);
    var pDst = D.parseGridKey(targetKey);

    if (tCell) {
      // SWAP lessons — Section 5 Interaction C
      // Validate both resulting placements
      var conf1 = E.validate(targetKey, sCell.subject_id, sCell.teacher_id, true);
      var err1 = conf1.filter(function (c) { return c.severity === 'error'; });
      var conf2 = E.validate(sourceKey, tCell.subject_id, tCell.teacher_id, true);
      var err2 = conf2.filter(function (c) { return c.severity === 'error'; });

      if (err1.length || err2.length) {
        var msg = (err1[0] && (err1[0].message_en || err1[0].message_kh)) ||
                  (err2[0] && (err2[0].message_en || err2[0].message_kh)) ||
                  'Cannot swap lessons: conflicting teacher or class schedule';
        toast(msg, 'error');
        return false;
      }

      var sClass = pSrc.class_id || sCell.class_id;
      var tClass = pDst.class_id || tCell.class_id;
      E.commit('Swap lessons ' + D.toEnDay(pSrc.day) + ' P' + pSrc.period + ' ↔ ' + D.toEnDay(pDst.day) + ' P' + pDst.period, function (s) {
        s.grid[targetKey] = {
          class_id: tClass, subject_id: sCell.subject_id, teacher_id: sCell.teacher_id,
          day: pDst.day, shift: pDst.shift, period: pDst.period, room: sCell.room, is_locked: sCell.is_locked
        };
        s.grid[sourceKey] = {
          class_id: sClass, subject_id: tCell.subject_id, teacher_id: tCell.teacher_id,
          day: pSrc.day, shift: pSrc.shift, period: pSrc.period, room: tCell.room, is_locked: tCell.is_locked
        };
      });
      toast('Swapped periods between ' + D.toEnDay(pSrc.day) + ' P' + pSrc.period + ' and ' + D.toEnDay(pDst.day) + ' P' + pDst.period, 'success');
    } else {
      // MOVE lesson — Section 5 Interaction B
      var confMove = E.validate(targetKey, sCell.subject_id, sCell.teacher_id, true);
      var errMove = confMove.filter(function (c) { return c.severity === 'error'; });
      if (errMove.length) {
        toast(errMove[0].message_en || errMove[0].message_kh || 'Cannot move lesson to this slot', 'error');
        return false;
      }

      var destClass = pDst.class_id || sCell.class_id;
      E.commit('Move lesson from ' + D.toEnDay(pSrc.day) + ' P' + pSrc.period + ' to ' + D.toEnDay(pDst.day) + ' P' + pDst.period, function (s) {
        s.grid[targetKey] = {
          class_id: destClass, subject_id: sCell.subject_id, teacher_id: sCell.teacher_id,
          day: pDst.day, shift: pDst.shift, period: pDst.period, room: sCell.room, is_locked: sCell.is_locked
        };
        delete s.grid[sourceKey];
      });
      toast('Moved period to ' + D.toEnDay(pDst.day) + ' Period ' + pDst.period, 'success');
    }
    local.targetKey = null;
    local.selectedChip = null;
    local.dragSourceKey = null;
    render();
    return true;
  }

  function handleDropOnKey(e, targetKey) {
    if (!targetKey) return;
    var payload = null;

    try {
      var jsonStr = e.dataTransfer.getData('application/json');
      if (jsonStr) payload = JSON.parse(jsonStr);
    } catch (err) {}

    if (!payload) {
      var raw = e.dataTransfer.getData('text/plain') || '';
      if (raw.indexOf('cell:') === 0) payload = { type: 'cell', sourceKey: raw.substring(5) };
      else if (raw.indexOf('chip:') === 0) payload = { type: 'chip', chipId: raw.substring(5) };
      else if (raw) payload = { type: 'chip', chipId: raw };
    }

    if (!payload && local.dragSourceKey) {
      payload = { type: 'cell', sourceKey: local.dragSourceKey };
    }

    if (!payload) return;

    if (payload.type === 'cell') {
      moveOrSwapLesson(payload.sourceKey, targetKey);
    } else if (payload.type === 'chip') {
      var allChips = E.chips().concat(E.chipsForTeacher ? E.chipsForTeacher(local.selectedTeacherId) : []);
      var chip = allChips.filter(function (c) { return c.id === payload.chipId; })[0];
      if (!chip) {
        (ctx.state.classes || []).forEach(function (cls) {
          if (chip) return;
          var cc = E.chips(cls.id).filter(function (c) { return c.id === payload.chipId; })[0];
          if (cc) chip = cc;
        });
      }
      if (!chip) return;

      var parts = D.parseGridKey(targetKey);
      var effectiveKey = D.gridKey(parts.day, parts.shift, parts.period, chip.class_id);

      var existing = ctx.grid[effectiveKey];
      if (existing) {
        // Attempt swap or reject
        toast('Slot is already occupied. Use drag to swap between scheduled periods.', 'warning');
        return;
      }

      var res = E.setCell(effectiveKey, { subject_id: chip.subject_id, teacher_id: chip.teacher_id }, { replace: false, label: 'Drag and drop place' });
      if (!res.ok) {
        var err = res.conflicts.filter(function (c) { return c.severity === 'error'; })[0];
        toast(err ? (err.message_en || err.message_kh) : 'Cannot place lesson here', 'error');
      } else {
        local.selectedChip = null;
        local.dragSourceKey = null;
        toast('Scheduled ' + formatKhmerSubjectName(chip.subject_name) + ' for Class ' + D.toEnClass(chip.class_id), 'success');
      }
    }
  }

  function attachBuilderInteractions() {
    var rootEl = document.getElementById('ks-root');
    if (!rootEl) return;

    var btnAuto = document.getElementById('btnAutoGenerate');
    if (btnAuto && !btnAuto.__bound) {
      btnAuto.__bound = true;
      btnAuto.addEventListener('click', function () {
        var icon = btnAuto.querySelector('.material-symbols-outlined');
        if (icon) icon.classList.add('animate-spin');
        setTimeout(function () {
          if (icon) icon.classList.remove('animate-spin');
        }, 800);
      });
    }

    // 1. Draggable unassigned chips from strip and right rail
    var chips = rootEl.querySelectorAll('[data-drag-chip]');
    chips.forEach(function (chip) {
      chip.setAttribute('draggable', 'true');
      chip.addEventListener('dragstart', function (e) {
        var chipId = chip.dataset.dragChip;
        e.dataTransfer.setData('application/json', JSON.stringify({ type: 'chip', chipId: chipId }));
        e.dataTransfer.setData('text/plain', 'chip:' + chipId);
        e.dataTransfer.effectAllowed = 'copyMove';
        chip.classList.add('is-dragging', 'opacity-50', 'scale-95');
        local.selectedChip = chipId;

        // Dynamic validation highlighting on drop cells
        var allChips = E.chips().concat(E.chipsForTeacher ? E.chipsForTeacher(local.selectedTeacherId) : []);
        var ch = allChips.filter(function (c) { return c.id === chipId; })[0];
        if (ch) {
          rootEl.querySelectorAll('td[data-cell-drop]').forEach(function (td) {
            var k = td.dataset.cellDrop;
            var p = D.parseGridKey(k);
            var effKey = D.gridKey(p.day, p.shift, p.period, ch.class_id);
            var conf = E.validate(effKey, ch.subject_id, ch.teacher_id, false);
            var errs = conf.filter(function (c) { return c.severity === 'error'; });
            if (errs.length) {
              td.classList.add('ks-drop-target-invalid');
            } else {
              td.classList.add('ks-drop-target-active');
            }
          });
        }
      });
      chip.addEventListener('dragend', function () {
        chip.classList.remove('is-dragging', 'opacity-50', 'scale-95');
        rootEl.querySelectorAll('.ks-drop-target-active, .ks-drop-target-invalid').forEach(function (el) {
          el.classList.remove('ks-drop-target-active', 'ks-drop-target-invalid');
        });
      });
    });

    // 2. Draggable placed lessons on the timetable grid
    var placedButtons = rootEl.querySelectorAll('[data-drag-placed]');
    placedButtons.forEach(function (btn) {
      btn.setAttribute('draggable', 'true');
      btn.addEventListener('dragstart', function (e) {
        var key = btn.dataset.dragPlaced;
        e.dataTransfer.setData('application/json', JSON.stringify({ type: 'cell', sourceKey: key }));
        e.dataTransfer.setData('text/plain', 'cell:' + key);
        e.dataTransfer.effectAllowed = 'move';
        btn.classList.add('opacity-40');
        local.dragSourceKey = key;
        local.targetKey = key;

        rootEl.querySelectorAll('td[data-cell-drop]').forEach(function (td) {
          if (td.dataset.cellDrop !== key) {
            td.classList.add('ks-drop-target-active');
          }
        });
      });
      btn.addEventListener('dragend', function () {
        btn.classList.remove('opacity-40');
        local.dragSourceKey = null;
        rootEl.querySelectorAll('.ks-drop-target-active, .ks-drop-target-invalid').forEach(function (el) {
          el.classList.remove('ks-drop-target-active', 'ks-drop-target-invalid');
        });
      });
    });

    // 3. Drop targets on all grid cells
    var dropTargets = rootEl.querySelectorAll('td[data-cell-drop]');
    dropTargets.forEach(function (el) {
      el.addEventListener('dragover', function (e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        var targetBtn = el.querySelector('[data-act="cell"]') || el;
        if (targetBtn) {
          targetBtn.classList.add('ring-2', 'ring-emerald-600', 'ring-inset', 'bg-emerald-50/40');
        }
      });
      el.addEventListener('dragleave', function (e) {
        if (!el.contains(e.relatedTarget)) {
          var targetBtn = el.querySelector('[data-act="cell"]') || el;
          if (targetBtn) {
            targetBtn.classList.remove('ring-2', 'ring-emerald-600', 'ring-inset', 'bg-emerald-50/40');
          }
        }
      });
      el.addEventListener('drop', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var targetBtn = el.querySelector('[data-act="cell"]') || el;
        if (targetBtn) {
          targetBtn.classList.remove('ring-2', 'ring-emerald-600', 'ring-inset', 'bg-emerald-50/40');
        }
        var targetKey = el.dataset.cellDrop || el.dataset.key;
        if (targetKey) {
          handleDropOnKey(e, targetKey);
        }
      });
    });
  }


  /* ==========================================================================
     MODULE 4 & 5 — Subjects & Overview
     ========================================================================== */

  function subjectsHtml() {
    var state = ctx.state;
    var subjects = state.subjects || [];

    var rows = subjects.map(function (s, i) {
      return '<tr>' +
        '<td class="center">' + kh(i + 1) + '</td>' +
        '<td><span style="font-weight:500">' + esc(s.name_kh) + '</span></td>' +
        '<td>' + esc(s.name_en || D.toEnSubject(s.name_kh)) + '</td>' +
        '<td class="center"><span class="ks-tag">' + esc(s.code) + '</span></td>' +
        '<td class="center">' + esc(s.short_name || '') + '</td>' +
        '<td class="center"><span class="ks-color-dot" style="background:' + esc(s.color) + ';display:inline-block;width:16px;height:16px;border-radius:4px"></span> ' + esc(s.color) + '</td>' +
        '<td class="center">' + kh(s.lessons_per_week || 2) + ' hrs</td>' +
        '<td>' + esc(s.department || 'General') + '</td>' +
        '<td class="center"><button class="ks-btn sm" data-act="subject-lock" data-id="' + esc(s.id) + '">' +
          (s.is_locked ? 'Locked' : 'Unlocked') + '</button></td>' +
        '<td class="center"><button class="ks-icon" data-act="subject-delete" data-id="' + esc(s.id) + '" title="Delete"><span class="material-symbols-outlined text-[14px]">close</span></button></td>' +
      '</tr>';
    }).join('');

    return '<div style="padding:14px">' +
      '<div class="ks-card-head">' +
        '<div class="ks-card-title">Curriculum Subjects & Period Targets</div>' +
        '<button class="ks-btn sm primary" data-act="subject-add">＋ Add Subject</button>' +
      '</div>' +
      '<div class="ks-scroll"><table class="ks-table"><thead><tr>' +
        '<th class="center">No.</th><th>Khmer Name</th><th>English Name</th><th class="center">Code</th><th class="center">Abbr</th><th class="center">Color</th><th class="center">Periods/Week</th><th>Department</th><th class="center">Lock</th><th></th>' +
      '</tr></thead><tbody>' + rows + '</tbody></table></div>' +
    '</div>';
  }

  /* ==========================================================================
     MODULE 4 (ADMIN ONLY) — Curriculum & Subject Directory
     ========================================================================== */

  var ADMIN_SUBJECT_METADATA = {
    'K':  { idBadge: 'KHM-01', icon: 'auto_stories',   stream: 'languages',  enFullName: 'Khmer Literature' },
    'M':  { idBadge: 'MTH-02', icon: 'calculate',      stream: 'stem',       enFullName: 'Mathematics' },
    'EN': { idBadge: 'ENG-03', icon: 'translate',      stream: 'languages',  enFullName: 'English Advanced' },
    'P':  { idBadge: 'PHY-04', icon: 'all_inclusive',  stream: 'stem',       enFullName: 'Physics' },
    'C':  { idBadge: 'CHM-05', icon: 'science',        stream: 'stem',       enFullName: 'Chemistry' },
    'B':  { idBadge: 'BIO-06', icon: 'biotech',        stream: 'stem',       enFullName: 'Biology' },
    'H':  { idBadge: 'HIS-07', icon: 'history_edu',    stream: 'humanities', enFullName: 'History' },
    'ES': { idBadge: 'GEO-08', icon: 'public',         stream: 'humanities', enFullName: 'Geography' },
    'G':  { idBadge: 'EAR-09', icon: 'terrain',        stream: 'stem',       enFullName: 'Earth Science' },
    'I':  { idBadge: 'CIV-10', icon: 'gavel',          stream: 'humanities', enFullName: 'Civics & Ethics' },
    'IT': { idBadge: 'PED-11', icon: 'fitness_center', stream: 'physical',   enFullName: 'Physical Education' },
    'ED': { idBadge: 'ICT-12', icon: 'computer',       stream: 'stem',       enFullName: 'ICT & Applied Coding' },
    'SH': { idBadge: 'FRN-13', icon: 'language',       stream: 'languages',  enFullName: 'French Language' }
  };

  function getSubjectMeta(s, idx) {
    var code = s.code || '';
    if (ADMIN_SUBJECT_METADATA[code]) return ADMIN_SUBJECT_METADATA[code];
    for (var k in ADMIN_SUBJECT_METADATA) {
      if (ADMIN_SUBJECT_METADATA[k].idBadge === code) return ADMIN_SUBJECT_METADATA[k];
    }
    var num = idx + 1;
    var badge = 'SUB-' + (num < 10 ? '0' + num : num);
    return {
      idBadge: badge,
      icon: 'edit_note',
      stream: 'general',
      enFullName: s.name_en || 'Subject'
    };
  }

  function subjectsAdminHtml() {
    var state = ctx.state;
    var subjects = state.subjects || [];
    var teachers = state.teachers || [];
    var facultyCount = teachers.length || 24;

    var totalWeeklyHours = 0;
    subjects.forEach(function (s) {
      totalWeeklyHours += (parseInt(s.lessons_per_week, 10) || 0);
    });

    var rows = subjects.map(function (s, i) {
      var meta = getSubjectMeta(s, i);
      var displayName = s.name_kh || '';
      if (meta.enFullName && displayName.indexOf('(') === -1) {
        displayName += ' (' + meta.enFullName + ')';
      }
      var shortName = s.short_name || s.name_kh || '';
      var colorVal = (s.color || '#006C49').toUpperCase();
      var hoursVal = parseInt(s.lessons_per_week, 10) || 2;
      var allocatedHours = hoursVal * 12;
      var isLocked = !!s.is_locked;

      return '<tr class="hover:bg-surface-container-low/60 transition-colors group" data-id="' + esc(s.id) + '" data-stream="' + esc(meta.stream) + '">' +
        '<td class="py-3.5 pl-5 pr-2 text-center font-label-md text-on-surface-variant">' +
          '<span class="w-6 h-6 rounded-full inline-flex items-center justify-center bg-surface-container text-[12px] font-mono">' + kh(i + 1) + '</span>' +
        '</td>' +
        '<td class="py-3.5 px-3">' +
          '<div class="flex items-center gap-2">' +
            '<span class="material-symbols-outlined text-[18px] text-on-surface-variant group-hover:text-primary transition-colors">' + esc(meta.icon) + '</span>' +
            '<input class="subject-name-input w-full px-2.5 py-1.5 bg-transparent hover:bg-surface-container-low focus:bg-surface-container-lowest focus:ring-1 focus:ring-primary-container rounded-lg font-headline-sm text-headline-sm text-on-surface transition-all font-medium" data-id="' + esc(s.id) + '" type="text" value="' + esc(displayName) + '">' +
          '</div>' +
        '</td>' +
        '<td class="py-3.5 px-3">' +
          '<input class="subject-short-input w-full px-2.5 py-1.5 bg-transparent hover:bg-surface-container-low focus:bg-surface-container-lowest focus:ring-1 focus:ring-primary-container rounded-lg font-body-md text-on-surface transition-all font-normal" data-id="' + esc(s.id) + '" type="text" value="' + esc(shortName) + '">' +
        '</td>' +
        '<td class="py-3.5 px-3 text-center">' +
          '<span class="inline-block px-2.5 py-1 bg-surface-container text-on-surface font-mono font-medium text-label-sm rounded-md">' + esc(meta.idBadge) + '</span>' +
        '</td>' +
        '<td class="py-3.5 px-3">' +
          '<div class="flex items-center gap-2">' +
            '<input class="subject-color-input w-7 h-7 rounded-md cursor-pointer border-0 p-0 bg-transparent shadow-sm" data-id="' + esc(s.id) + '" type="color" value="' + esc(s.color || '#006C49') + '">' +
            '<span class="color-hex-label font-mono text-label-sm text-on-surface-variant font-medium">' + esc(colorVal) + '</span>' +
          '</div>' +
        '</td>' +
        '<td class="py-3.5 px-3 text-center">' +
          '<div class="inline-flex items-center bg-surface-container-low rounded-lg p-0.5">' +
            '<button class="step-minus-btn w-6 h-6 flex items-center justify-center text-on-surface-variant hover:text-on-surface hover:bg-surface-container rounded transition-colors text-sm" data-id="' + esc(s.id) + '" type="button">−</button>' +
            '<input class="subject-hours-input w-9 text-center bg-transparent font-headline-sm text-headline-sm text-primary font-medium focus:outline-none" data-id="' + esc(s.id) + '" type="text" value="' + hoursVal + '">' +
            '<button class="step-plus-btn w-6 h-6 flex items-center justify-center text-on-surface-variant hover:text-on-surface hover:bg-surface-container rounded transition-colors text-sm" data-id="' + esc(s.id) + '" type="button">+</button>' +
          '</div>' +
        '</td>' +
        '<td class="py-3.5 px-3 text-center">' +
          '<button class="view-periods-btn inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-secondary-container/20 text-on-secondary-container hover:bg-secondary-container/40 font-label-sm text-label-sm transition-colors font-medium" data-id="' + esc(s.id) + '" type="button">' +
            '<span class="material-symbols-outlined text-[15px]">event_note</span>' +
            '<span class="allocated-label">View ' + kh(allocatedHours) + 'h</span>' +
          '</button>' +
        '</td>' +
        '<td class="py-3.5 pl-3 pr-5 text-right">' +
          '<div class="flex items-center justify-end gap-1">' +
            '<button class="subject-lock-btn p-1.5 text-on-surface-variant hover:text-primary rounded-md hover:bg-surface-container transition-colors ' + (isLocked ? 'text-primary' : '') + '" data-id="' + esc(s.id) + '" title="' + (isLocked ? 'Locked' : 'Unlocked') + '" type="button">' +
              '<span class="material-symbols-outlined text-[18px]">' + (isLocked ? 'lock' : 'lock_open') + '</span>' +
            '</button>' +
            '<button class="subject-delete-btn p-1.5 text-on-surface-variant hover:text-error rounded-md hover:bg-error-container/40 transition-colors" data-id="' + esc(s.id) + '" title="Delete" type="button">' +
              '<span class="material-symbols-outlined text-[18px]">delete</span>' +
            '</button>' +
          '</div>' +
        '</td>' +
      '</tr>';
    }).join('');

    return '<div class="relative w-full overflow-hidden pb-space-xl">' +
      '<div class="absolute -top-24 right-1/4 w-96 h-96 bg-primary-fixed/20 rounded-full blur-3xl pointer-events-none -z-10"></div>' +
      '<div class="absolute top-1/2 -left-20 w-80 h-80 bg-secondary-container/15 rounded-full blur-3xl pointer-events-none -z-10"></div>' +
      '<div class="max-w-[1600px] w-full mx-auto px-3 sm:px-space-md lg:px-space-lg space-y-3 sm:space-y-4 pt-2 sm:pt-4">' +
        '<!-- Header & Toolbar -->' +
        '<div class="p-4 sm:p-space-lg bg-surface-container-lowest shadow-sm rounded-2xl border border-slate-200/80">' +
          '<div class="flex flex-col lg:flex-row lg:items-center justify-between gap-3 sm:gap-space-md">' +
            '<div class="flex flex-col gap-1 min-w-0">' +
              '<h1 class="font-headline-lg text-xl sm:text-2xl lg:text-3xl text-primary tracking-tight font-medium break-words">' +
                'Curriculum &amp; Subject Directory' +
              '</h1>' +
              '<div class="flex items-center flex-wrap gap-1.5 sm:gap-2 font-body-sm text-xs sm:text-sm text-on-surface-variant">' +
                '<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-secondary-container/30 text-on-secondary-container font-label-sm text-[11px] font-medium">' +
                  '<span class="w-1.5 h-1.5 rounded-full bg-secondary"></span>' +
                  'AY 2026–2027 · Term 2 Active' +
                '</span>' +
              '</div>' +
            '</div>' +
            '<div class="flex items-center gap-1.5 sm:gap-2 flex-wrap w-full lg:w-auto">' +
              '<div class="flex items-center bg-surface-container-lowest rounded-lg p-0.5 shadow-sm border border-slate-200/60">' +
                '<button data-act="undo" class="p-2 rounded hover:bg-surface-container text-on-surface-variant hover:text-on-surface transition-colors" title="Undo (Ctrl+Z)" type="button">' +
                  '<span class="material-symbols-outlined text-[18px]">undo</span>' +
                '</button>' +
                '<button data-act="redo" class="p-2 rounded hover:bg-surface-container text-on-surface-variant hover:text-on-surface transition-colors" title="Redo (Ctrl+Y)" type="button">' +
                  '<span class="material-symbols-outlined text-[18px]">redo</span>' +
                '</button>' +
                '<button data-act="history" class="p-2 rounded hover:bg-surface-container text-on-surface-variant hover:text-on-surface transition-colors" title="Audit History" type="button">' +
                  '<span class="material-symbols-outlined text-[18px]">history</span>' +
                '</button>' +
              '</div>' +
              '<button id="exportExcelBtn" data-act="export" data-type="all" class="flex items-center gap-1.5 px-3.5 py-2 bg-surface-container-lowest text-on-surface hover:bg-surface-container-high rounded-xl font-label-md text-label-md shadow-xs border border-slate-200/60 transition-all font-medium" type="button">' +
                '<span class="material-symbols-outlined text-[18px] text-secondary">table_view</span>' +
                '<span>Export Excel</span>' +
              '</button>' +
              '<button id="saveBtn" data-act="save" class="flex items-center gap-1.5 px-4 py-2 bg-primary-container hover:bg-primary text-on-primary rounded-xl font-label-md text-label-md shadow-xs transition-all font-medium" type="button">' +
                '<span class="material-symbols-outlined text-[18px]">save</span>' +
                '<span>Save Changes</span>' +
              '</button>' +
              '<button id="addNewSubjectBtn" data-act="subject-add" class="flex items-center gap-1.5 px-4 py-2 bg-primary text-on-primary hover:bg-primary-container rounded-xl font-label-md text-label-md shadow-xs hover:shadow transition-all font-medium" type="button">' +
                '<span class="material-symbols-outlined text-[18px]">add_circle</span>' +
                '<span>+ Add New Subject</span>' +
              '</button>' +
            '</div>' +
          '</div>' +
        '</div>' +
        '<!-- KPI Summary Metrics Strip -->' +
        '<div class="grid grid-cols-2 lg:grid-cols-4 gap-2.5 sm:gap-4">' +
          '<div class="bg-surface-container-lowest rounded-xl p-3 sm:p-4 shadow-sm flex items-center justify-between border border-slate-200/70">' +
            '<div class="space-y-1 min-w-0 pr-1">' +
              '<span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider block font-medium truncate">Total Subjects</span>' +
              '<div class="flex items-baseline gap-2">' +
                '<span id="kpiTotalSubjects" class="font-headline-lg text-xl sm:text-2xl text-primary font-medium">' + subjects.length + '</span>' +
                '<span class="font-body-sm text-body-sm text-on-surface-variant hidden sm:inline">' + kh(subjects.length) + ' Subjects</span>' +
              '</div>' +
            '</div>' +
            '<div class="w-9 h-9 sm:w-11 sm:h-11 rounded-lg sm:rounded-xl bg-primary-fixed/40 text-primary flex items-center justify-center shrink-0">' +
              '<span class="material-symbols-outlined text-[20px] sm:text-[24px]">menu_book</span>' +
            '</div>' +
          '</div>' +
          '<div class="bg-surface-container-lowest rounded-xl p-3 sm:p-4 shadow-sm flex items-center justify-between border border-slate-200/70">' +
            '<div class="space-y-1 min-w-0 pr-1">' +
              '<span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider block font-medium truncate">Weekly Hours</span>' +
              '<div class="flex items-baseline gap-2">' +
                '<span id="kpiWeeklyHours" class="font-headline-lg text-xl sm:text-2xl text-on-surface font-medium">' + totalWeeklyHours + '</span>' +
                '<span class="font-body-sm text-body-sm text-on-surface-variant hidden sm:inline">Hours / Week</span>' +
              '</div>' +
            '</div>' +
            '<div class="w-9 h-9 sm:w-11 sm:h-11 rounded-lg sm:rounded-xl bg-secondary-fixed/40 text-on-secondary-fixed-variant flex items-center justify-center shrink-0">' +
              '<span class="material-symbols-outlined text-[20px] sm:text-[24px]">calendar_view_week</span>' +
            '</div>' +
          '</div>' +
          '<div class="bg-surface-container-lowest rounded-xl p-3 sm:p-4 shadow-sm flex items-center justify-between border border-slate-200/70">' +
            '<div class="space-y-1 min-w-0 pr-1">' +
              '<span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider block font-medium truncate">Faculty Allocated</span>' +
              '<div class="flex items-baseline gap-2">' +
                '<span class="font-headline-lg text-xl sm:text-2xl text-on-surface font-medium">' + facultyCount + '</span>' +
                '<span class="font-body-sm text-body-sm text-on-surface-variant hidden sm:inline">Educators</span>' +
              '</div>' +
            '</div>' +
            '<div class="w-9 h-9 sm:w-11 sm:h-11 rounded-lg sm:rounded-xl bg-surface-container-high text-on-surface flex items-center justify-center shrink-0">' +
              '<span class="material-symbols-outlined text-[20px] sm:text-[24px]">badge</span>' +
            '</div>' +
          '</div>' +
          '<div class="bg-surface-container-lowest rounded-xl p-3 sm:p-4 shadow-sm flex items-center justify-between border border-slate-200/70">' +
            '<div class="space-y-1 min-w-0 pr-1">' +
              '<span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider block font-medium truncate">Accreditation</span>' +
              '<div class="flex items-baseline gap-2">' +
                '<span class="font-headline-lg text-xl sm:text-2xl text-secondary font-medium">100%</span>' +
                '<span class="font-body-sm text-body-sm text-on-surface-variant hidden sm:inline">MoEYS &amp; CIE</span>' +
              '</div>' +
            '</div>' +
            '<div class="w-9 h-9 sm:w-11 sm:h-11 rounded-lg sm:rounded-xl bg-secondary-container/40 text-on-secondary-container flex items-center justify-center shrink-0">' +
              '<span class="material-symbols-outlined text-[20px] sm:text-[24px]">fact_check</span>' +
            '</div>' +
          '</div>' +
        '</div>' +
        '<!-- Stream Filters & Search -->' +
        '<div class="bg-surface-container-lowest rounded-xl p-3 sm:p-4 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-3 border border-slate-200/70">' +
          '<div class="flex items-center gap-1.5 overflow-x-auto no-scrollbar pb-1 md:pb-0 max-w-full" id="streamFilterGroup">' +
            '<button class="filter-chip px-3.5 py-1.5 rounded-full bg-primary-container text-on-primary font-label-md text-label-md flex items-center gap-1.5 shadow-sm whitespace-nowrap font-medium shrink-0" data-stream="all" type="button">' +
              '<span class="material-symbols-outlined text-[16px]">apps</span>' +
              '<span>All Subjects (' + subjects.length + ')</span>' +
            '</button>' +
            '<button class="filter-chip px-3.5 py-1.5 rounded-full bg-surface-container-low text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface font-label-md text-label-md transition-colors whitespace-nowrap font-medium shrink-0" data-stream="stem" type="button">' +
              '<span>STEM</span>' +
              '<span class="ml-1 text-[11px] px-1.5 py-0.2 rounded-full bg-surface-container-highest">5</span>' +
            '</button>' +
            '<button class="filter-chip px-3.5 py-1.5 rounded-full bg-surface-container-low text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface font-label-md text-label-md transition-colors whitespace-nowrap font-medium shrink-0" data-stream="humanities" type="button">' +
              '<span>Humanities</span>' +
              '<span class="ml-1 text-[11px] px-1.5 py-0.2 rounded-full bg-surface-container-highest">4</span>' +
            '</button>' +
            '<button class="filter-chip px-3.5 py-1.5 rounded-full bg-surface-container-low text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface font-label-md text-label-md transition-colors whitespace-nowrap font-medium shrink-0" data-stream="languages" type="button">' +
              '<span>Languages &amp; Arts</span>' +
              '<span class="ml-1 text-[11px] px-1.5 py-0.2 rounded-full bg-surface-container-highest">3</span>' +
            '</button>' +
            '<button class="filter-chip px-3.5 py-1.5 rounded-full bg-surface-container-low text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface font-label-md text-label-md transition-colors whitespace-nowrap font-medium shrink-0" data-stream="physical" type="button">' +
              '<span>Physical &amp; Life Skills</span>' +
              '<span class="ml-1 text-[11px] px-1.5 py-0.2 rounded-full bg-surface-container-highest">2</span>' +
            '</button>' +
          '</div>' +
          '<div class="flex items-center gap-space-sm w-full md:w-auto">' +
            '<div class="relative w-full md:w-72">' +
              '<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-[18px]">search</span>' +
              '<input class="w-full pl-9 pr-3 py-1.5 bg-surface-container-low hover:bg-surface-container text-on-surface placeholder:text-on-surface-variant font-body-sm text-body-sm rounded-lg border-0 focus:outline-none focus:ring-2 focus:ring-primary-container transition-all font-normal" id="subjectSearch" placeholder="Search by name or code..." type="text">' +
            '</div>' +
            '<button class="p-2 bg-surface-container-low hover:bg-surface-container text-on-surface-variant rounded-lg transition-colors shrink-0" title="Advanced Filter" type="button">' +
              '<span class="material-symbols-outlined text-[18px]">tune</span>' +
            '</button>' +
          '</div>' +
        '</div>' +
        '<!-- Main Subject Matrix Table -->' +
        '<div class="bg-surface-container-lowest rounded-xl shadow-sm overflow-hidden border border-slate-200/70">' +
          '<div class="overflow-x-auto no-scrollbar">' +
            '<table class="w-full text-left font-body-md text-body-md min-w-[760px]">' +
              '<thead class="bg-surface-container-low text-on-surface-variant font-label-md text-label-md uppercase tracking-wider select-none font-medium">' +
                '<tr>' +
                  '<th class="py-3.5 pl-5 pr-2 w-12 text-center font-medium" scope="col">#</th>' +
                  '<th class="py-3.5 px-3 min-w-[240px] font-medium" scope="col">Subject Name</th>' +
                  '<th class="py-3.5 px-3 w-32 font-medium" scope="col">Short Name</th>' +
                  '<th class="py-3.5 px-3 w-28 text-center font-medium" scope="col">Subject Code</th>' +
                  '<th class="py-3.5 px-3 min-w-[140px] font-medium" scope="col">Palette Color</th>' +
                  '<th class="py-3.5 px-3 w-36 text-center font-medium" scope="col">Periods / Wk</th>' +
                  '<th class="py-3.5 px-3 min-w-[130px] text-center font-medium" scope="col">Schedule Status</th>' +
                  '<th class="py-3.5 pl-3 pr-5 w-24 text-right font-medium" scope="col">Actions</th>' +
                '</tr>' +
              '</thead>' +
              '<tbody class="divide-y divide-surface-container" id="subjectTableBody">' +
                rows +
              '</tbody>' +
            '</table>' +
          '</div>' +
          '<!-- Table Footer -->' +
          '<div class="bg-surface-container-low px-space-md py-3 flex flex-col sm:flex-row items-center justify-between gap-space-sm text-on-surface-variant font-label-sm text-label-sm">' +
            '<div class="flex items-center gap-space-sm">' +
              '<span id="subjectCountFooter">Showing 1–' + subjects.length + ' of ' + subjects.length + ' subjects</span>' +
              '<div class="flex items-center gap-1">' +
                '<button class="p-1 rounded text-on-surface-variant/40 cursor-not-allowed" disabled="" type="button">' +
                  '<span class="material-symbols-outlined text-[18px]">chevron_left</span>' +
                '</button>' +
                '<span class="px-2 py-0.5 rounded bg-surface-container-lowest font-medium text-on-surface">1</span>' +
                '<button class="p-1 rounded text-on-surface-variant/40 cursor-not-allowed" disabled="" type="button">' +
                  '<span class="material-symbols-outlined text-[18px]">chevron_right</span>' +
                '</button>' +
              '</div>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>' +
      '<!-- Toast Notification DOM element -->' +
      '<div class="fixed bottom-6 right-6 bg-primary text-on-primary px-4 py-3 rounded-xl shadow-xl flex items-center gap-3 transform translate-y-20 opacity-0 transition-all duration-300 pointer-events-none z-50" id="toastNotification">' +
        '<span class="material-symbols-outlined text-[22px] text-secondary-container">check_circle</span>' +
        '<div class="text-left font-body-sm">' +
          '<div class="font-label-md text-label-md font-medium">Saved successfully!</div>' +
          '<div class="text-on-primary/80">Subject directory configuration synchronized.</div>' +
        '</div>' +
      '</div>' +
    '</div>';
  }

  function attachAdminSubjectInteractions() {
    var saveBtn = document.getElementById('saveBtn');
    var toastEl = document.getElementById('toastNotification');
    var exportBtn = document.getElementById('exportExcelBtn');
    var addBtn = document.getElementById('addNewSubjectBtn');
    var searchInput = document.getElementById('subjectSearch');
    var tbody = document.getElementById('subjectTableBody');

    // 1. Toast & Save
    if (saveBtn) {
      saveBtn.onclick = function () {
        var rows = document.querySelectorAll('#subjectTableBody tr');
        rows.forEach(function (r) {
          var id = r.dataset.id;
          var sub = (ctx.state.subjects || []).find(function (x) { return x.id === id; });
          if (!sub) return;
          var nameInp = r.querySelector('.subject-name-input');
          var shortInp = r.querySelector('.subject-short-input');
          var hoursInp = r.querySelector('.subject-hours-input');
          var colorInp = r.querySelector('.subject-color-input');
          if (nameInp) sub.name_kh = nameInp.value;
          if (shortInp) sub.short_name = shortInp.value;
          if (hoursInp) sub.lessons_per_week = parseInt(hoursInp.value, 10) || 2;
          if (colorInp) sub.color = colorInp.value;
        });

        E.flushSave().then(function () {
          if (toastEl) {
            toastEl.classList.remove('translate-y-20', 'opacity-0');
            toastEl.classList.add('translate-y-0', 'opacity-100');
            setTimeout(function () {
              toastEl.classList.remove('translate-y-0', 'opacity-100');
              toastEl.classList.add('translate-y-20', 'opacity-0');
            }, 3200);
          }
        });
      };
    }

    // 2. Export Excel
    if (exportBtn) {
      exportBtn.onclick = function () {
        var subjects = ctx.state.subjects || [];
        var csvContent = '\uFEFF' + 'No,ID,Subject Name,Short Name,Color,Hours Per Week,Allocated Total,Locked\n';
        subjects.forEach(function (s, idx) {
          var meta = getSubjectMeta(s, idx);
          var row = [
            idx + 1,
            '"' + (meta.idBadge || s.code || '') + '"',
            '"' + (s.name_kh || '').replace(/"/g, '""') + '"',
            '"' + (s.short_name || '').replace(/"/g, '""') + '"',
            '"' + (s.color || '') + '"',
            s.lessons_per_week || 2,
            (s.lessons_per_week || 2) * 12,
            s.is_locked ? 'Yes' : 'No'
          ];
          csvContent += row.join(',') + '\n';
        });
        var blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        var url = URL.createObjectURL(blob);
        var link = document.createElement('a');
        link.setAttribute('href', url);
        link.setAttribute('download', 'NGIS_Curriculum_Subjects.csv');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      };
    }

    // 3. Row-level behaviors: Steppers, Color, Lock, Delete, View
    function bindRow(r) {
      var id = r.dataset.id;
      var sub = (ctx.state.subjects || []).find(function (x) { return x.id === id; });

      var minusBtn = r.querySelector('.step-minus-btn');
      var plusBtn = r.querySelector('.step-plus-btn');
      var hoursInp = r.querySelector('.subject-hours-input');
      var allocLbl = r.querySelector('.allocated-label');
      var colorInp = r.querySelector('.subject-color-input');
      var colorLbl = r.querySelector('.color-hex-label');
      var lockBtn = r.querySelector('.subject-lock-btn');
      var delBtn = r.querySelector('.subject-delete-btn');
      var viewBtn = r.querySelector('.view-periods-btn');
      var nameInp = r.querySelector('.subject-name-input');
      var shortInp = r.querySelector('.subject-short-input');

      function updateHours(newH) {
        if (newH < 1) newH = 1;
        if (newH > 12) newH = 12;
        if (hoursInp) hoursInp.value = newH;
        if (sub) sub.lessons_per_week = newH;
        if (allocLbl) allocLbl.textContent = 'View ' + kh(newH * 12) + 'h';

        var total = 0;
        document.querySelectorAll('#subjectTableBody .subject-hours-input').forEach(function (inp) {
          total += parseInt(inp.value, 10) || 0;
        });
        var kpiHours = document.getElementById('kpiWeeklyHours');
        if (kpiHours) kpiHours.textContent = total;

        E.scheduleSave();
      }

      if (minusBtn && hoursInp) {
        minusBtn.onclick = function () {
          var val = parseInt(hoursInp.value, 10) || 2;
          updateHours(val - 1);
        };
      }
      if (plusBtn && hoursInp) {
        plusBtn.onclick = function () {
          var val = parseInt(hoursInp.value, 10) || 2;
          updateHours(val + 1);
        };
      }
      if (hoursInp) {
        hoursInp.onchange = function () {
          var val = parseInt(hoursInp.value, 10) || 2;
          updateHours(val);
        };
      }

      if (colorInp && colorLbl) {
        colorInp.oninput = function (e) {
          colorLbl.textContent = e.target.value.toUpperCase();
        };
        colorInp.onchange = function (e) {
          if (sub) sub.color = e.target.value;
          E.scheduleSave();
        };
      }

      if (nameInp) {
        nameInp.onchange = function (e) {
          if (sub) {
            sub.name_kh = e.target.value;
            sub.name_en = e.target.value;
          }
          E.scheduleSave();
        };
      }
      if (shortInp) {
        shortInp.onchange = function (e) {
          if (sub) sub.short_name = e.target.value;
          E.scheduleSave();
        };
      }

      if (lockBtn) {
        lockBtn.onclick = function () {
          if (!sub) return;
          sub.is_locked = !sub.is_locked;
          var icon = lockBtn.querySelector('.material-symbols-outlined');
          if (sub.is_locked) {
            if (icon) icon.textContent = 'lock';
            lockBtn.classList.add('text-primary');
            lockBtn.title = 'Locked';
          } else {
            if (icon) icon.textContent = 'lock_open';
            lockBtn.classList.remove('text-primary');
            lockBtn.title = 'Unlocked';
          }
          E.scheduleSave();
          toast(sub.is_locked ? 'Subject locked against auto-replacement' : 'Subject unlocked');
        };
      }

      if (delBtn) {
        delBtn.onclick = function () {
          if (!confirm('Are you sure you want to delete this subject?')) return;
          r.remove();
          if (sub) {
            ctx.state.subjects = ctx.state.subjects.filter(function (x) { return x.id !== id; });
            E.commit('Delete subject ' + id, function (s) {
              s.subjects = s.subjects.filter(function (x) { return x.id !== id; });
              s.assignments = s.assignments.filter(function (a) { return a.subject_id !== id; });
              Object.keys(s.grid).forEach(function (k) { if (s.grid[k].subject_id === id) delete s.grid[k]; });
            });
            E.scheduleSave();
          }
          var count = ctx.state.subjects ? ctx.state.subjects.length : 0;
          var kpiTotal = document.getElementById('kpiTotalSubjects');
          if (kpiTotal) kpiTotal.textContent = count;
          var countFooter = document.getElementById('subjectCountFooter');
          if (countFooter) countFooter.textContent = 'Showing 1–' + count + ' of ' + count + ' subjects';

          var total = 0;
          document.querySelectorAll('#subjectTableBody .subject-hours-input').forEach(function (inp) {
            total += parseInt(inp.value, 10) || 0;
          });
          var kpiHours = document.getElementById('kpiWeeklyHours');
          if (kpiHours) kpiHours.textContent = total;

          toast('Subject removed from curriculum');
        };
      }

      if (viewBtn) {
        viewBtn.onclick = function () {
          window.location.href = ROLE + '-timetables.html';
        };
      }
    }

    if (tbody) {
      tbody.querySelectorAll('tr').forEach(bindRow);
    }

    // 4. Add New Subject
    if (addBtn && tbody) {
      addBtn.onclick = function () {
        var count = (ctx.state.subjects ? ctx.state.subjects.length : 0) + 1;
        var newId = 'sub_new_' + Date.now();
        var codeId = 'NEW-' + (count < 10 ? '0' + count : count);
        var newSub = {
          id: newId,
          name_kh: 'New Subject ' + count,
          name_en: 'New Subject ' + count,
          short_name: 'New ' + count,
          code: codeId,
          color: '#006C49',
          lessons_per_week: 2,
          is_locked: false,
          department: 'General'
        };
        ctx.state.subjects.push(newSub);
        E.commit('Add subject ' + codeId, function (s) {
          s.subjects.push(newSub);
        });
        E.scheduleSave();

        var tr = document.createElement('tr');
        tr.className = 'hover:bg-surface-container-low/60 transition-colors group animate-fade-in';
        tr.dataset.id = newId;
        tr.dataset.stream = 'general';
        tr.innerHTML = '<td class="py-3.5 pl-5 pr-2 text-center font-label-md text-on-surface-variant">' +
          '<span class="w-6 h-6 rounded-full inline-flex items-center justify-center bg-primary-fixed/50 text-primary text-[12px] font-mono">' + kh(count) + '</span>' +
        '</td>' +
        '<td class="py-3.5 px-3">' +
          '<div class="flex items-center gap-2">' +
            '<span class="material-symbols-outlined text-[18px] text-primary">edit_note</span>' +
            '<input class="subject-name-input w-full px-2.5 py-1.5 bg-surface-container-low focus:bg-surface-container-lowest focus:ring-1 focus:ring-primary-container rounded-lg font-headline-sm text-headline-sm text-on-surface font-medium" data-id="' + newId + '" type="text" value="' + esc(newSub.name_en) + '">' +
          '</div>' +
        '</td>' +
        '<td class="py-3.5 px-3">' +
          '<input class="subject-short-input w-full px-2.5 py-1.5 bg-surface-container-low focus:bg-surface-container-lowest focus:ring-1 focus:ring-primary-container rounded-lg font-body-md text-on-surface" data-id="' + newId + '" type="text" value="' + esc(newSub.short_name) + '">' +
        '</td>' +
        '<td class="py-3.5 px-3 text-center">' +
          '<span class="inline-block px-2.5 py-1 bg-surface-container text-on-surface font-mono font-medium text-label-sm rounded-md">' + esc(codeId) + '</span>' +
        '</td>' +
        '<td class="py-3.5 px-3">' +
          '<div class="flex items-center gap-2">' +
            '<input class="subject-color-input w-7 h-7 rounded-md cursor-pointer border-0 p-0 bg-transparent shadow-sm" data-id="' + newId + '" type="color" value="#006C49">' +
            '<span class="color-hex-label font-mono text-label-sm text-on-surface-variant font-medium">#006C49</span>' +
          '</div>' +
        '</td>' +
        '<td class="py-3.5 px-3 text-center">' +
          '<div class="inline-flex items-center bg-surface-container-low rounded-lg p-0.5">' +
            '<button class="step-minus-btn w-6 h-6 flex items-center justify-center text-on-surface-variant hover:text-on-surface hover:bg-surface-container rounded transition-colors text-sm" data-id="' + newId + '" type="button">−</button>' +
            '<input class="subject-hours-input w-9 text-center bg-transparent font-headline-sm text-headline-sm text-primary font-medium focus:outline-none" data-id="' + newId + '" type="text" value="2">' +
            '<button class="step-plus-btn w-6 h-6 flex items-center justify-center text-on-surface-variant hover:text-on-surface hover:bg-surface-container rounded transition-colors text-sm" data-id="' + newId + '" type="button">+</button>' +
          '</div>' +
        '</td>' +
        '<td class="py-3.5 px-3 text-center">' +
          '<button class="view-periods-btn inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-secondary-container/20 text-on-secondary-container hover:bg-secondary-container/40 font-label-sm text-label-sm transition-colors font-medium" data-id="' + newId + '" type="button">' +
            '<span class="material-symbols-outlined text-[15px]">event_note</span>' +
            '<span class="allocated-label">View 24h</span>' +
          '</button>' +
        '</td>' +
        '<td class="py-3.5 pl-3 pr-5 text-right">' +
          '<div class="flex items-center justify-end gap-1">' +
            '<button class="subject-lock-btn p-1.5 text-on-surface-variant hover:text-primary rounded-md hover:bg-surface-container transition-colors" data-id="' + newId + '" title="Unlocked" type="button">' +
              '<span class="material-symbols-outlined text-[18px]">lock_open</span>' +
            '</button>' +
            '<button class="subject-delete-btn p-1.5 text-on-surface-variant hover:text-error rounded-md hover:bg-error-container/40 transition-colors" data-id="' + newId + '" title="Delete" type="button">' +
              '<span class="material-symbols-outlined text-[18px]">delete</span>' +
            '</button>' +
          '</div>' +
        '</td>';

        tbody.prepend(tr);
        bindRow(tr);

        var kpiTotal = document.getElementById('kpiTotalSubjects');
        if (kpiTotal) kpiTotal.textContent = count;
        var countFooter = document.getElementById('subjectCountFooter');
        if (countFooter) countFooter.textContent = 'Showing 1–' + count + ' of ' + count + ' subjects';

        var total = 0;
        document.querySelectorAll('#subjectTableBody .subject-hours-input').forEach(function (inp) {
          total += parseInt(inp.value, 10) || 0;
        });
        var kpiHours = document.getElementById('kpiWeeklyHours');
        if (kpiHours) kpiHours.textContent = total;

        var firstInput = tr.querySelector('.subject-name-input');
        if (firstInput) firstInput.focus();

        toast('Added new subject', 'success');
      };
    }

    // 5. Search Filter
    if (searchInput && tbody) {
      searchInput.oninput = function (e) {
        var term = e.target.value.toLowerCase().trim();
        var rows = tbody.querySelectorAll('tr');
        rows.forEach(function (row) {
          var text = row.innerText.toLowerCase();
          row.querySelectorAll('input').forEach(function (inp) {
            text += ' ' + inp.value.toLowerCase();
          });
          if (!term || text.indexOf(term) !== -1) {
            row.style.display = '';
          } else {
            row.style.display = 'none';
          }
        });
      };
    }

    // 6. Stream Filter Chips
    var chips = document.querySelectorAll('#streamFilterGroup .filter-chip');
    chips.forEach(function (chip) {
      chip.onclick = function () {
        chips.forEach(function (c) {
          c.classList.remove('bg-primary-container', 'text-on-primary');
          c.classList.add('bg-surface-container-low', 'text-on-surface-variant');
        });
        chip.classList.add('bg-primary-container', 'text-on-primary');
        chip.classList.remove('bg-surface-container-low', 'text-on-surface-variant');

        var stream = chip.dataset.stream;
        var rows = tbody ? tbody.querySelectorAll('tr') : [];
        rows.forEach(function (row) {
          if (!stream || stream === 'all' || row.dataset.stream === stream) {
            row.style.display = '';
          } else {
            row.style.display = 'none';
          }
        });
      };
    });
  }

  /* ==========================================================================
     TIMETABLE VIEWER — Master Timetable & Teacher Distribution Matrix
     Cohort Live Snapshot Grid + Teacher Period Matrix
     ========================================================================== */

  function viewerHtml() {
    var state = ctx.state || {};
    var v = local.viewer || (local.viewer = {
      week: 21,
      day: 'ច័ន្ទ',
      period: 1,
      shift: 'ព្រឹក',
      activePeriodSlot: 1,
      q: '',
      page: 1,
      perPage: 10,
      showAllCohorts: true
    });

    if (v.week == null) v.week = 21;
    if (!v.day) v.day = 'ច័ន្ទ';
    var rawPeriod = String(v.period || 1);
    var pNum = parseInt(rawPeriod.replace(/[^0-9]/g, ''), 10) || 1;
    v.period = pNum;
    if (!v.shift) v.shift = 'ព្រឹក';
    if (v.activePeriodSlot == null) v.activePeriodSlot = (v.shift === 'រសៀល' ? (pNum + 5) : pNum);
    if (v.q == null) v.q = '';
    if (v.page == null) v.page = 1;
    if (v.perPage == null) v.perPage = 10;
    if (v.showAllCohorts == null) v.showAllCohorts = true;

    var PERIOD_MAP = [
      { slot: 1, label: 'P1', shift: 'ព្រឹក', pNum: 1, shiftEn: 'Morning', time: '07:00–07:50 AM', start: '07:00', end: '07:50' },
      { slot: 2, label: 'P2', shift: 'ព្រឹក', pNum: 2, shiftEn: 'Morning', time: '07:50–08:40 AM', start: '07:50', end: '08:40' },
      { slot: 3, label: 'P3', shift: 'ព្រឹក', pNum: 3, shiftEn: 'Morning', time: '08:40–09:30 AM', start: '08:40', end: '09:30' },
      { slot: 4, label: 'P4', shift: 'ព្រឹក', pNum: 4, shiftEn: 'Morning', time: '09:30–10:20 AM', start: '09:30', end: '10:20' },
      { slot: 5, label: 'P5', shift: 'ព្រឹក', pNum: 5, shiftEn: 'Morning', time: '10:20–11:10 AM', start: '10:20', end: '11:10' },
      { slot: 6, label: 'P6', shift: 'រសៀល', pNum: 1, shiftEn: 'Afternoon', time: '13:00–13:50 PM', start: '13:00', end: '13:50' },
      { slot: 7, label: 'P7', shift: 'រសៀល', pNum: 2, shiftEn: 'Afternoon', time: '13:50–14:40 PM', start: '13:50', end: '14:40' },
      { slot: 8, label: 'P8', shift: 'រសៀល', pNum: 3, shiftEn: 'Afternoon', time: '14:40–15:30 PM', start: '14:40', end: '15:30' },
      { slot: 9, label: 'P9', shift: 'រសៀល', pNum: 4, shiftEn: 'Afternoon', time: '15:30–16:20 PM', start: '15:30', end: '16:20' },
      { slot: 10, label: 'P10', shift: 'រសៀល', pNum: 5, shiftEn: 'Afternoon', time: '16:20–17:10 PM', start: '16:20', end: '17:10' }
    ];

    var DAYS_CONFIG = [
      { kh: 'ច័ន្ទ', en: 'Monday', short: 'Mon' },
      { kh: 'អង្គារ', en: 'Tuesday', short: 'Tue' },
      { kh: 'ពុធ', en: 'Wednesday', short: 'Wed' },
      { kh: 'ព្រហស្បតិ៍', en: 'Thursday', short: 'Thu' },
      { kh: 'សុក្រ', en: 'Friday', short: 'Fri' },
      { kh: 'សៅរ៍', en: 'Saturday', short: 'Sat' }
    ];

    var activeDayObj = DAYS_CONFIG.filter(function (d) { return d.kh === v.day; })[0] || DAYS_CONFIG[0];
    var activePeriodObj = PERIOD_MAP.filter(function (p) { return p.slot === v.activePeriodSlot; })[0] || PERIOD_MAP[0];

    function getSubjectTheme(code, name) {
      var c = (code || '').toUpperCase();
      var n = (name || '').toLowerCase();
      if (c.indexOf('K') === 0 || n.indexOf('khmer') !== -1 || n.indexOf('ខ្មែរ') !== -1) {
        return { bg: 'bg-amber-500', hoverBorder: 'hover:border-amber-300', text: 'text-amber-700', lightBg: 'bg-amber-50', border: 'border-amber-200/60', discipline: 'Khmer' };
      }
      if (c.indexOf('M') === 0 || n.indexOf('math') !== -1 || n.indexOf('គណិត') !== -1) {
        return { bg: 'bg-blue-600', hoverBorder: 'hover:border-blue-300', text: 'text-blue-700', lightBg: 'bg-blue-50', border: 'border-blue-200/60', discipline: 'Mathematics' };
      }
      if (c.indexOf('B') === 0 || n.indexOf('bio') !== -1 || n.indexOf('ជីវ') !== -1) {
        return { bg: 'bg-emerald-600', hoverBorder: 'hover:border-emerald-300', text: 'text-emerald-700', lightBg: 'bg-emerald-50', border: 'border-emerald-200/60', discipline: 'Biology' };
      }
      if (c.indexOf('P') === 0 || n.indexOf('phys') !== -1 || n.indexOf('រូប') !== -1) {
        return { bg: 'bg-purple-600', hoverBorder: 'hover:border-purple-300', text: 'text-purple-700', lightBg: 'bg-purple-50', border: 'border-purple-200/60', discipline: 'Physics' };
      }
      if (c.indexOf('C') === 0 || n.indexOf('chem') !== -1 || n.indexOf('គីមី') !== -1) {
        return { bg: 'bg-pink-600', hoverBorder: 'hover:border-pink-300', text: 'text-pink-700', lightBg: 'bg-pink-50', border: 'border-pink-200/60', discipline: 'Chemistry' };
      }
      if (c.indexOf('IT') === 0 || n.indexOf('sport') !== -1 || n.indexOf('pe') !== -1 || n.indexOf('កីឡា') !== -1) {
        return { bg: 'bg-rose-600', hoverBorder: 'hover:border-rose-300', text: 'text-rose-700', lightBg: 'bg-rose-50', border: 'border-rose-200/60', discipline: 'Sports / PE' };
      }
      if (c.indexOf('ES') === 0 || n.indexOf('geo') !== -1 || n.indexOf('earth') !== -1 || n.indexOf('ភូមិ') !== -1) {
        return { bg: 'bg-amber-700', hoverBorder: 'hover:border-amber-300', text: 'text-amber-800', lightBg: 'bg-amber-50', border: 'border-amber-200/60', discipline: 'Geography' };
      }
      if (c.indexOf('EN') === 0 || n.indexOf('eng') !== -1 || n.indexOf('អង់') !== -1) {
        return { bg: 'bg-teal-600', hoverBorder: 'hover:border-teal-300', text: 'text-teal-700', lightBg: 'bg-teal-50', border: 'border-teal-200/60', discipline: 'English' };
      }
      if (c.indexOf('H') === 0 || n.indexOf('hist') !== -1 || n.indexOf('ប្រវត្តិ') !== -1) {
        return { bg: 'bg-amber-600', hoverBorder: 'hover:border-amber-300', text: 'text-amber-700', lightBg: 'bg-amber-50', border: 'border-amber-200/60', discipline: 'History' };
      }
      return { bg: 'bg-indigo-600', hoverBorder: 'hover:border-indigo-300', text: 'text-indigo-700', lightBg: 'bg-indigo-50', border: 'border-indigo-200/60', discipline: 'General' };
    }

    var gv = ctx.grid || {};
    var workingGrid = gv;
    if (Object.keys(workingGrid).length === 0 && E.autoAssignResult && E.gridView) {
      try {
        var previewRes = E.autoAssignResult({});
        if (previewRes && previewRes.state && previewRes.state.grid && Object.keys(previewRes.state.grid).length > 0) {
          workingGrid = E.gridView(previewRes.state);
        }
      } catch (err) {
        console.warn('Auto-assign preview failed in viewer:', err);
      }
    }
    var hasRealGrid = Object.keys(workingGrid).length > 0;

    var teacherSlots = {};
    var classSlots = {};
    var teacherLoads = (E.teacherLoad ? E.teacherLoad() : {}) || {};

    if (hasRealGrid) {
      Object.keys(workingGrid).forEach(function (k) {
        var cell = workingGrid[k];
        if (!cell) return;
        var p = D.parseGridKey(k);
        if (cell.teacher_id) {
          teacherLoads[cell.teacher_id] = (teacherLoads[cell.teacher_id] || 0) + 1;
        }
        if (p.day === v.day) {
          if (cell.teacher_id) {
            teacherSlots[cell.teacher_id + '|' + p.shift + '|' + p.period] = {
              class_id: p.class_id,
              class_name: D.toEnClass(p.class_id),
              subject_id: cell.subject_id,
              subject_name: cell.subject_name || D.toEnSubject(cell.subject_id),
              subject_code: cell.subject_code || '',
              color: cell.color || '#2563eb'
            };
          }
          classSlots[p.class_id + '|' + p.shift + '|' + p.period] = cell;
        }
      });
    } else {
      // Demo dataset matching user prompt reference when grid is initial unassigned
      var demoPlacements = [
        { cid: 'class_7A', shift: 'ព្រឹក', p: 1, sub: 'Mathematics', code: 'M1', tname: 'Bun Sophy', tid: 't_M1', color: 'bg-blue-600', disc: 'Math' },
        { cid: 'class_7B', shift: 'រសៀល', p: 1, sub: 'Geography', code: 'ES2', tname: 'Long Chantha', tid: 't_ES2', color: 'bg-amber-700', disc: 'Geography' },
        // 8A is Free
        { cid: 'class_8B', shift: 'រសៀល', p: 1, sub: 'Physics', code: 'P1', tname: 'Touch Chan', tid: 't_P1', color: 'bg-purple-600', disc: 'Physics' },
        { cid: 'class_9A', shift: 'ព្រឹក', p: 1, sub: 'Sports / PE', code: 'IT1', tname: 'Pen Sreymom', tid: 't_IT1', color: 'bg-rose-600', disc: 'Sports / PE' },
        { cid: 'class_9B', shift: 'រសៀល', p: 1, sub: 'Khmer Language', code: 'K6', tname: 'Yun Sith', tid: 't_K6', color: 'bg-amber-500', disc: 'Khmer' },
        { cid: 'class_10A', shift: 'ព្រឹក', p: 1, sub: 'Khmer Language', code: 'K1', tname: 'Sok Phat', tid: 't_K1', color: 'bg-amber-500', disc: 'Khmer' },
        { cid: 'class_10B', shift: 'រសៀល', p: 1, sub: 'Chemistry', code: 'C2', tname: 'Khow Channa', tid: 't_C2', color: 'bg-pink-600', disc: 'Chemistry' },
        { cid: 'class_11A', shift: 'ព្រឹក', p: 1, sub: 'Mathematics', code: 'M3', tname: 'Ly Sopheap', tid: 't_M3', color: 'bg-blue-600', disc: 'Math' },
        { cid: 'class_11B', shift: 'រសៀល', p: 1, sub: 'Sports / PE', code: 'IT2', tname: 'Va Sokhan', tid: 't_IT2', color: 'bg-rose-600', disc: 'Sports / PE' },
        { cid: 'class_12A', shift: 'ព្រឹក', p: 1, sub: 'Biology', code: 'B1', tname: 'Chhim Sreyleak', tid: 't_B1', color: 'bg-emerald-600', disc: 'Biology' },
        { cid: 'class_12B', shift: 'រសៀល', p: 1, sub: 'Mathematics', code: 'ED2', tname: 'Sok Neak', tid: 't_ED2', color: 'bg-blue-600', disc: 'Math' }
      ];

      demoPlacements.forEach(function (dp) {
        classSlots[dp.cid + '|' + dp.shift + '|' + dp.p] = {
          subject_name: dp.sub,
          teacher_code: dp.code,
          teacher_name: dp.tname,
          colorClass: dp.color
        };
      });

      var demoTeacherMatrix = {
        't_K1':  { code: 'K1', name: 'Sok Phat', disc: 'Khmer', load: 18, status: 'Optimal', slots: { 1: '10A', 9: '7A' } },
        't_K2':  { code: 'K2', name: 'Kan Chinda', disc: 'Khmer', load: 16, status: 'Optimal', slots: { 3: '10B', 5: '7B' } },
        't_K3':  { code: 'K3', name: 'Heng Vy', disc: 'Khmer', load: 18, status: 'Optimal', slots: { 2: '11A', 8: '8A' } },
        't_K4':  { code: 'K4', name: 'Choeun Vanny', disc: 'Khmer', load: 17, status: 'Optimal', slots: { 2: '11B', 5: '8B' } },
        't_K5':  { code: 'K5', name: 'Nop Socheat', disc: 'Khmer', load: 19, status: 'Optimal', slots: { 4: '9A', 5: '12A' } },
        't_K6':  { code: 'K6', name: 'Yun Sith', disc: 'Khmer', load: 18, status: 'Optimal', slots: { 1: '9B', 3: '12B' } },
        't_M1':  { code: 'M1', name: 'Bun Sophy', disc: 'Math', load: 20, status: 'Optimal', slots: { 1: '7A', 8: '10A' } },
        't_M2':  { code: 'M2', name: 'Ouk Chantha', disc: 'Math', load: 19, status: 'Optimal', slots: { 5: '10B', 6: '7B' } },
        't_M3':  { code: 'M3', name: 'Ly Sopheap', disc: 'Math', load: 22, status: 'Near Max', slots: { 1: '11A', 9: '8A' } },
        't_M4':  { code: 'M4', name: 'Mao Thavy', disc: 'Math', load: 18, status: 'Optimal', slots: { 4: '8B', 6: '11B' } },
        't_P1':  { code: 'P1', name: 'Touch Chan', disc: 'Physics', load: 18, status: 'Optimal', slots: { 1: '8B', 7: '10A' } },
        't_C2':  { code: 'C2', name: 'Khow Channa', disc: 'Chemistry', load: 18, status: 'Optimal', slots: { 1: '10B', 8: '12A' } },
        't_B1':  { code: 'B1', name: 'Chhim Sreyleak', disc: 'Biology', load: 18, status: 'Optimal', slots: { 1: '12A', 7: '9A' } },
        't_ES2': { code: 'ES2', name: 'Long Chantha', disc: 'Geography', load: 17, status: 'Optimal', slots: { 1: '7B', 9: '9B' } },
        't_IT1': { code: 'IT1', name: 'Pen Sreymom', disc: 'Sports / PE', load: 18, status: 'Optimal', slots: { 1: '9A', 10: '11A' } },
        't_IT2': { code: 'IT2', name: 'Va Sokhan', disc: 'Sports / PE', load: 18, status: 'Optimal', slots: { 1: '11B', 10: '12B' } }
      };

      Object.keys(demoTeacherMatrix).forEach(function (tid) {
        var tm = demoTeacherMatrix[tid];
        teacherLoads[tid] = tm.load;
        Object.keys(tm.slots).forEach(function (pSlot) {
          var pInt = parseInt(pSlot, 10);
          var sShift = pInt <= 5 ? 'ព្រឹក' : 'រសៀល';
          var sPeriod = pInt <= 5 ? pInt : (pInt - 5);
          var cName = tm.slots[pSlot];
          var cid = 'class_' + cName;
          teacherSlots[tid + '|' + sShift + '|' + sPeriod] = {
            class_id: cid,
            class_name: cName,
            subject_name: tm.disc,
            subject_code: tm.code.replace(/[0-9]/g, ''),
            disc: tm.disc
          };
        });
      });
    }

    var cohortList = (state.classes && state.classes.length) ? state.classes : [
      { id: 'class_7A', display: '7A', shift: 'ព្រឹក' },
      { id: 'class_7B', display: '7B', shift: 'រសៀល' },
      { id: 'class_8A', display: '8A', shift: 'ព្រឹក' },
      { id: 'class_8B', display: '8B', shift: 'រសៀល' },
      { id: 'class_9A', display: '9A', shift: 'ព្រឹក' },
      { id: 'class_9B', display: '9B', shift: 'រសៀល' },
      { id: 'class_10A', display: '10A', shift: 'ព្រឹក' },
      { id: 'class_10B', display: '10B', shift: 'រសៀល' },
      { id: 'class_11A', display: '11A', shift: 'ព្រឹក' },
      { id: 'class_11B', display: '11B', shift: 'រសៀល' },
      { id: 'class_12A', display: '12A', shift: 'ព្រឹក' },
      { id: 'class_12B', display: '12B', shift: 'រសៀល' }
    ];

    var cohortCardsHtml = cohortList.map(function (cls) {
      var clsDisplay = D.toEnClass(cls.display || cls.id || '');
      var isAfternoon = (cls.shift === 'រសៀល' || clsDisplay.slice(-1) === 'B');
      var clsShift = isAfternoon ? 'រសៀល' : 'ព្រឹក';
      var clsShiftEn = isAfternoon ? 'Afternoon' : 'Morning';
      var dayShortEn = activeDayObj.short;

      var pNum = parseInt(String(v.period || 1).replace(/[^0-9]/g, ''), 10) || 1;
      var cell = classSlots[cls.id + '|' + clsShift + '|' + pNum];

      if (cell) {
        var subName = cell.subject_name || D.toEnSubject(cell.subject_id) || 'Subject';
        var tCode = cell.teacher_code || '';
        var tName = cell.teacher_name ? (D.toEnTeacher(cell.teacher_name) || cell.teacher_name) : '';
        var tTag = (tCode && tName) ? (tCode + ' • ' + tName) : (tCode || tName || 'Assigned');
        var theme = getSubjectTheme(cell.subject_code || cell.code, subName);
        var cardBg = cell.colorClass || theme.bg;
        var borderHover = theme.hoverBorder || 'hover:border-blue-300';

        return '<div class="p-3 rounded-lg border border-slate-200 bg-white ' + borderHover + ' hover:shadow-xs transition">' +
          '<div class="flex items-center justify-between mb-2">' +
            '<span class="font-medium text-xs text-slate-900 font-display">' + esc(clsDisplay) + '</span>' +
            '<span class="text-[10px] font-medium text-slate-400">' + esc(clsShiftEn) + ' • ' + esc(dayShortEn) + '</span>' +
          '</div>' +
          '<div class="p-2 rounded ' + cardBg + ' text-white text-xs shadow-xs">' +
            '<p class="font-medium truncate">' + esc(subName) + '</p>' +
            '<p class="text-[10px] text-white/90 truncate mt-0.5">' + esc(tTag) + '</p>' +
          '</div>' +
        '</div>';
      }

      return '<div class="p-3 rounded-lg border border-slate-200 bg-white hover:border-slate-300 transition">' +
        '<div class="flex items-center justify-between mb-2">' +
          '<span class="font-medium text-xs text-slate-900 font-display">' + esc(clsDisplay) + '</span>' +
          '<span class="text-[10px] font-medium text-slate-400">' + esc(clsShiftEn) + ' • ' + esc(dayShortEn) + '</span>' +
        '</div>' +
        '<div class="p-2 rounded bg-slate-50 text-slate-400 text-xs border border-dashed border-slate-200 flex items-center justify-center min-h-[46px]">' +
          '<span class="text-[11px] font-medium">Free • No Class</span>' +
        '</div>' +
      '</div>';
    }).join('');

    var teacherList = (state.teachers && state.teachers.length) ? state.teachers : [
      { id: 't_K1', code: 'K1', name_kh: 'សុខ ផាត់', name_en: 'Sok Phat', specialization: 'Khmer' },
      { id: 't_K2', code: 'K2', name_kh: 'កាន់ ចិន្តា', name_en: 'Kan Chinda', specialization: 'Khmer' },
      { id: 't_K3', code: 'K3', name_kh: 'ហេង វី', name_en: 'Heng Vy', specialization: 'Khmer' },
      { id: 't_K4', code: 'K4', name_kh: 'ជើន វ៉ាន់នី', name_en: 'Choeun Vanny', specialization: 'Khmer' },
      { id: 't_K5', code: 'K5', name_kh: 'ណុប សុជាតិ', name_en: 'Nop Socheat', specialization: 'Khmer' },
      { id: 't_K6', code: 'K6', name_kh: 'យុន សុីត', name_en: 'Yun Sith', specialization: 'Khmer' },
      { id: 't_M1', code: 'M1', name_kh: 'ប៊ុន សុភី', name_en: 'Bun Sophy', specialization: 'Mathematics' },
      { id: 't_M2', code: 'M2', name_kh: 'អ៊ុក ចាន់ថា', name_en: 'Ouk Chantha', specialization: 'Mathematics' },
      { id: 't_M3', code: 'M3', name_kh: 'លី សុភាព', name_en: 'Ly Sopheap', specialization: 'Mathematics' },
      { id: 't_M4', code: 'M4', name_kh: 'ម៉ៅ ថាវី', name_en: 'Mao Thavy', specialization: 'Mathematics' },
      { id: 't_P1', code: 'P1', name_kh: 'ទូច ចាន់', name_en: 'Touch Chan', specialization: 'Physics' },
      { id: 't_C2', code: 'C2', name_kh: 'ខូវ ចាន់ណា', name_en: 'Khow Channa', specialization: 'Chemistry' },
      { id: 't_B1', code: 'B1', name_kh: 'ឈឹម ស្រីល័ក្ខ', name_en: 'Chhim Sreyleak', specialization: 'Biology' },
      { id: 't_ES2', code: 'ES2', name_kh: 'ឡុង ចាន់ថា', name_en: 'Long Chantha', specialization: 'Geography' },
      { id: 't_IT1', code: 'IT1', name_kh: 'ប៉ែន ស្រីមុំ', name_en: 'Pen Sreymom', specialization: 'Sports / PE' },
      { id: 't_IT2', code: 'IT2', name_kh: 'វ៉ា សុខាន់', name_en: 'Va Sokhan', specialization: 'Sports / PE' }
    ];

    var qLower = (v.q || '').trim().toLowerCase();
    var filteredTeachers = teacherList.filter(function (t) {
      if (!qLower) return true;
      var en = (t.name_en || D.toEnTeacher(t.name_kh) || '').toLowerCase();
      var khName = (t.name_kh || '').toLowerCase();
      var code = (t.code || '').toLowerCase();
      var spec = (t.specialization || '').toLowerCase();
      var enSpec = (D.toEnSubject(t.specialization) || '').toLowerCase();
      var disc = (getSubjectTheme(t.code, t.specialization).discipline || '').toLowerCase();
      var matchesSlot = false;
      for (var p = 1; p <= 5; p++) {
        var sm = teacherSlots[t.id + '|ព្រឹក|' + p];
        var sa = teacherSlots[t.id + '|រសៀល|' + p];
        if (sm && (sm.class_name || D.toEnClass(sm.class_id)).toLowerCase().indexOf(qLower) !== -1) matchesSlot = true;
        if (sa && (sa.class_name || D.toEnClass(sa.class_id)).toLowerCase().indexOf(qLower) !== -1) matchesSlot = true;
      }
      return en.indexOf(qLower) !== -1 || khName.indexOf(qLower) !== -1 || code.indexOf(qLower) !== -1 || spec.indexOf(qLower) !== -1 || enSpec.indexOf(qLower) !== -1 || disc.indexOf(qLower) !== -1 || matchesSlot;
    });

    var totalFiltered = filteredTeachers.length;
    var perPage = v.perPage || 10;
    var totalPages = Math.max(1, Math.ceil(totalFiltered / perPage));
    var currentPage = Math.min(Math.max(1, v.page || 1), totalPages);
    var startIdx = (currentPage - 1) * perPage;
    var pageTeachers = filteredTeachers.slice(startIdx, startIdx + perPage);

    var teacherRowsHtml = pageTeachers.map(function (t) {
      var tName = t.name_en || D.toEnTeacher(t.name_kh) || t.name_kh;
      var tCode = t.code || '';
      var spec = t.specialization || '';
      var theme = getSubjectTheme(tCode, spec);
      var load = teacherLoads[t.id] || t.target || 18;
      var statusBadge = '';
      if (load <= 20) {
        statusBadge = '<span class="inline-block px-2 py-0.5 text-[10px] font-medium text-emerald-700 bg-emerald-50 rounded-full border border-emerald-200">Optimal</span>';
      } else if (load <= 23) {
        statusBadge = '<span class="inline-block px-2 py-0.5 text-[10px] font-medium text-amber-700 bg-amber-50 rounded-full border border-amber-200">Near Max</span>';
      } else {
        statusBadge = '<span class="inline-block px-2 py-0.5 text-[10px] font-medium text-rose-700 bg-rose-50 rounded-full border border-rose-200">Overload</span>';
      }

      var morningCells = [1, 2, 3, 4, 5].map(function (p) {
        var slot = teacherSlots[t.id + '|ព្រឹក|' + p];
        var isP5 = (p === 5);
        var bgCol = isP5 ? 'bg-slate-50/40' : '';
        if (slot) {
          var cName = slot.class_name || D.toEnClass(slot.class_id);
          var st = getSubjectTheme(slot.subject_code || tCode, slot.subject_name || spec);
          return '<td class="p-1.5 text-center border-r border-slate-200 ' + bgCol + '">' +
            '<span class="inline-block px-2.5 py-1 font-medium rounded text-[11px] ' + st.bg + ' text-white shadow-xs cursor-pointer" title="' + esc(cName) + ' • ' + esc(slot.subject_name || '') + '">' + esc(cName) + '</span>' +
          '</td>';
        }
        return '<td class="p-1.5 text-center border-r border-slate-200 ' + bgCol + '"></td>';
      }).join('');

      var afternoonCells = [1, 2, 3, 4, 5].map(function (p) {
        var slot = teacherSlots[t.id + '|រសៀល|' + p];
        if (slot) {
          var cName = slot.class_name || D.toEnClass(slot.class_id);
          var st = getSubjectTheme(slot.subject_code || tCode, slot.subject_name || spec);
          return '<td class="p-1.5 text-center border-r border-slate-200">' +
            '<span class="inline-block px-2.5 py-1 font-medium rounded text-[11px] ' + st.bg + ' text-white shadow-xs cursor-pointer" title="' + esc(cName) + ' • ' + esc(slot.subject_name || '') + '">' + esc(cName) + '</span>' +
          '</td>';
        }
        return '<td class="p-1.5 text-center border-r border-slate-200"></td>';
      }).join('');

      return '<tr class="hover:bg-slate-50/70 transition-colors group">' +
        '<td class="py-2.5 px-4 font-medium text-slate-800 sticky left-0 bg-white group-hover:bg-slate-50 border-r border-slate-200">' +
          '<div class="flex items-center justify-between">' +
            '<span class="font-medium text-slate-900">' + esc(tCode ? (tCode + ' • ' + tName) : tName) + '</span>' +
          '</div>' +
        '</td>' +
        '<td class="p-2 text-center border-r border-slate-200">' +
          '<span class="text-[11px] font-medium ' + theme.text + ' ' + theme.lightBg + ' px-2 py-0.5 rounded border ' + theme.border + '">' + esc(theme.discipline) + '</span>' +
        '</td>' +
        morningCells +
        afternoonCells +
        '<td class="p-1.5 text-center border-r border-slate-200 font-medium text-slate-700">' + esc(load) + ' hrs/wk</td>' +
        '<td class="p-1.5 text-center">' + statusBadge + '</td>' +
      '</tr>';
    }).join('');

    var dayButtonsHtml = DAYS_CONFIG.map(function (d) {
      var isActive = (d.kh === v.day);
      var btnStyle = isActive
        ? 'bg-brand-600 text-white shadow-xs'
        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100';
      return '<button type="button" class="px-3 py-1.5 text-xs font-medium rounded-lg transition ' + btnStyle + '" data-act="viewer-select-day" data-day="' + esc(d.kh) + '">' +
        esc(d.en) +
      '</button>';
    }).join('');

    var periodOptionsHtml = PERIOD_MAP.map(function (p) {
      var isSelected = (p.slot === (v.activePeriodSlot || 1));
      return '<option value="' + p.slot + '" ' + (isSelected ? 'selected' : '') + '>' +
        esc(p.label + ' • ' + p.time + ' (' + p.shiftEn + ')') +
      '</option>';
    }).join('');

    var paginationHtml = '';
    for (var i = 1; i <= totalPages; i++) {
      if (i === currentPage) {
        paginationHtml += '<span class="px-3 py-1 font-medium text-white bg-brand-600 border border-brand-600 rounded-md shadow-xs">' + i + '</span> ';
      } else {
        paginationHtml += '<button class="px-3 py-1 border border-slate-200 rounded-md bg-white text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition font-medium" data-act="viewer-page" data-page="' + i + '">' + i + '</button> ';
      }
    }

    var undoDisabled = ctx.undo === 0 ? 'disabled opacity-40 cursor-not-allowed' : '';
    var redoDisabled = ctx.redo === 0 ? 'disabled opacity-40 cursor-not-allowed' : '';

    return '<div class="bg-[#f8fafb] text-slate-800 font-sans antialiased min-h-screen flex flex-col w-full">' +
      workflowStepperHtml() +

      '<!-- Top Executive Header -->' +
      '<header class="bg-white border-b border-slate-200 px-4 sm:px-6 py-3.5 sm:py-4 flex flex-col md:flex-row md:items-center justify-between gap-3 sm:gap-4 sticky top-0 z-30 shadow-xs">' +
        '<div>' +
          '<div class="flex flex-wrap items-center gap-2 sm:gap-3">' +
            '<h1 class="text-base sm:text-lg md:text-xl font-medium font-display text-slate-900 tracking-tight break-words">Master Timetable & Teacher Distribution Matrix</h1>' +
            '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200 shrink-0">AY 2026–2027</span>' +
            (!hasRealGrid ? '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-200 shrink-0"><i class="fa-solid fa-sparkles text-[10px]"></i> Standard Matrix View</span>' : '') +
          '</div>' +
        '</div>' +
        '<!-- Action Utilities -->' +
        '<div class="flex flex-wrap items-center gap-2 sm:gap-2.5">' +
          '<div class="inline-flex rounded-lg border border-slate-200 bg-white p-0.5 shadow-xs shrink-0">' +
            '<button class="px-2.5 py-1.5 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded text-xs transition flex items-center justify-center ' + undoDisabled + '" data-act="undo" title="Undo (Ctrl+Z)">' +
              '<span class="material-symbols-outlined text-[16px]">undo</span>' +
            '</button>' +
            '<button class="px-2.5 py-1.5 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded text-xs transition flex items-center justify-center ' + redoDisabled + '" data-act="redo" title="Redo (Ctrl+Y)">' +
              '<span class="material-symbols-outlined text-[16px]">redo</span>' +
            '</button>' +
            '<button class="px-2.5 py-1.5 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded text-xs transition flex items-center justify-center" data-act="history" title="Change History">' +
              '<span class="material-symbols-outlined text-[16px]">history</span>' +
            '</button>' +
          '</div>' +
          '<button class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 hover:border-slate-300 rounded-lg text-xs font-medium text-slate-700 hover:bg-slate-50 shadow-xs transition shrink-0" data-act="export" data-type="all" title="Export Excel">' +
            '<span class="material-symbols-outlined text-[16px] text-emerald-600">table_view</span>' +
            '<span class="hidden sm:inline">Export Excel</span>' +
            '<span class="sm:hidden">Excel</span>' +
          '</button>' +
          '<button class="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 hover:border-slate-300 rounded-lg text-xs font-medium text-slate-700 hover:bg-slate-50 shadow-xs transition shrink-0" onclick="window.print()" title="Print Schedule">' +
            '<span class="material-symbols-outlined text-[16px] text-slate-500">print</span>' +
            '<span>Print</span>' +
          '</button>' +
          '<button class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 hover:border-slate-300 rounded-lg text-xs font-medium text-slate-700 hover:bg-slate-50 shadow-xs transition shrink-0" data-act="auto-assign-viewer" title="Auto-Assign Timetable Grid">' +
            '<span class="material-symbols-outlined text-[16px] text-brand-600">bolt</span>' +
            '<span>Auto-Assign</span>' +
          '</button>' +
          '<button class="inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-brand-600 hover:bg-brand-700 text-white rounded-lg text-xs font-medium shadow-xs transition shrink-0" data-act="save">' +
            '<span class="material-symbols-outlined text-[16px]">save</span>' +
            '<span>Save</span>' +
          '</button>' +
        '</div>' +
      '</header>' +

      '<!-- Sub Navigation Tabs & Date Selector Strip -->' +
      '<div class="bg-white border-b border-slate-200 px-4 sm:px-6 py-2.5 flex flex-col xl:flex-row xl:items-center justify-between gap-3">' +
        '<!-- Day Selector Tabs -->' +
        '<nav aria-label="Days" class="flex items-center space-x-1 overflow-x-auto no-scrollbar pb-1 xl:pb-0 max-w-full shrink-0">' +
          dayButtonsHtml +
        '</nav>' +
        '<!-- Active Period Selector & Live Search Input -->' +
        '<div class="flex flex-col sm:flex-row sm:items-center gap-2.5 sm:gap-3 w-full xl:w-auto shrink-0">' +
          '<div class="relative flex items-center w-full sm:w-auto">' +
            '<span class="material-symbols-outlined absolute left-2.5 text-slate-400 text-[16px] pointer-events-none">search</span>' +
            '<input id="viewerSearchInput" class="pl-8 pr-3 py-1.5 text-xs border border-slate-200 rounded-md bg-slate-50 focus:bg-white focus:outline-none focus:ring-1 focus:ring-brand-600 focus:border-brand-600 w-full sm:w-48 md:w-56 font-normal" placeholder="Search class or teacher..." type="text" value="' + esc(v.q) + '">' +
          '</div>' +
          '<div class="flex items-center text-xs font-medium bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-slate-700 overflow-x-auto no-scrollbar whitespace-nowrap">' +
            '<span class="px-2.5 py-1 bg-white font-medium rounded shadow-xs text-brand-600 border border-slate-200/50 shrink-0">Week ' + esc(v.week) + '</span>' +
            '<span class="px-2 py-1 font-medium text-slate-700 shrink-0">' + esc(activeDayObj.en) + '</span>' +
            '<span class="text-slate-300 shrink-0">•</span>' +
            '<div class="relative px-1 py-0.5 shrink-0">' +
              '<select id="viewerPeriodSelect" class="bg-transparent text-slate-700 text-[11px] font-medium border-0 focus:ring-0 cursor-pointer pr-5 py-0 max-w-full">' +
                periodOptionsHtml +
              '</select>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>' +

      '<!-- Content Workspace -->' +
      '<div class="p-3 sm:p-5 md:p-6 space-y-4 sm:space-y-6 flex-1">' +
        '<!-- BEGIN: SectionCohortSnapshot -->' +
        '<section class="bg-white rounded-xl border border-slate-200 shadow-xs p-4 sm:p-5" data-purpose="cohort-live-snapshot">' +
          '<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 mb-3 sm:mb-4">' +
            '<div class="flex flex-wrap items-center gap-2">' +
              '<span class="w-2.5 h-2.5 rounded-full bg-emerald-500 ring-4 ring-emerald-50 animate-pulse shrink-0"></span>' +
              '<h2 class="font-medium text-xs sm:text-sm text-slate-800 font-display">All Classes • Week ' + esc(v.week) + ' • ' + esc(activeDayObj.en) + ' (' + esc(activePeriodObj.label) + ' ' + esc(activePeriodObj.shiftEn) + ')</h2>' +
              '<span class="text-[11px] sm:text-xs text-slate-400 font-mono">' + esc(activePeriodObj.start) + ' – ' + esc(activePeriodObj.end) + ' AM</span>' +
            '</div>' +
            '<button class="text-xs font-medium text-brand-600 hover:text-brand-700 bg-brand-50 hover:bg-brand-100/70 px-3 py-1 rounded-md border border-brand-100 flex items-center justify-center gap-1.5 transition self-start sm:self-auto shrink-0" data-act="toggle-snapshot-all">' +
              '<span>Show All (' + cohortList.length + ')</span>' +
              '<span class="material-symbols-outlined text-[14px]">expand_more</span>' +
            '</button>' +
          '</div>' +
          '<!-- 12-Cohort Grid View -->' +
          '<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2 sm:gap-3">' +
            cohortCardsHtml +
          '</div>' +
        '</section>' +
        '<!-- END: SectionCohortSnapshot -->' +

        '<!-- BEGIN: SectionTeacherMatrix -->' +
        '<section class="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden" data-purpose="teacher-period-matrix">' +
          '<!-- Table Header Toolbar -->' +
          '<div class="p-3 sm:p-4 border-b border-slate-200 flex flex-col lg:flex-row lg:items-center justify-between gap-2.5 sm:gap-3 bg-slate-50/60">' +
            '<div class="flex flex-wrap items-center gap-2">' +
              '<span class="text-xs font-medium text-slate-700">Faculty Distribution Matrix for ' + esc(activeDayObj.en) + '</span>' +
              '<span class="text-slate-300 hidden sm:inline">•</span>' +
              '<span class="text-[11px] text-slate-500">Periods P1–P5 (Morning) & P6–P10 (Afternoon)</span>' +
            '</div>' +
            '<!-- Legend Tags -->' +
            '<div class="flex flex-wrap items-center gap-2 sm:gap-3 text-[11px]">' +
              '<span class="inline-flex items-center gap-1.5 text-slate-600">' +
                '<span class="w-2.5 h-2.5 rounded bg-amber-500"></span> Khmer' +
              '</span>' +
              '<span class="inline-flex items-center gap-1.5 text-slate-600">' +
                '<span class="w-2.5 h-2.5 rounded bg-blue-600"></span> Mathematics' +
              '</span>' +
              '<span class="inline-flex items-center gap-1.5 text-slate-600">' +
                '<span class="w-2.5 h-2.5 rounded bg-emerald-600"></span> Biology' +
              '</span>' +
              '<span class="inline-flex items-center gap-1.5 text-slate-600">' +
                '<span class="w-2.5 h-2.5 rounded bg-purple-600"></span> Physics' +
              '</span>' +
              '<span class="inline-flex items-center gap-1.5 text-slate-600">' +
                '<span class="w-2.5 h-2.5 rounded bg-pink-600"></span> Chemistry' +
              '</span>' +
              '<span class="inline-flex items-center gap-1.5 text-slate-600">' +
                '<span class="w-2.5 h-2.5 rounded bg-rose-600"></span> Sports / PE' +
              '</span>' +
              '<span class="inline-flex items-center gap-1.5 text-slate-600">' +
                '<span class="w-2.5 h-2.5 rounded bg-amber-700"></span> Geography' +
              '</span>' +
            '</div>' +
          '</div>' +
          '<!-- Matrix Table Container -->' +
          '<div class="overflow-x-auto no-scrollbar">' +
            '<table class="w-full text-left border-collapse min-w-[960px]">' +
              '<thead>' +
                '<tr class="bg-slate-100/80 border-b border-slate-200 text-[11px] text-slate-600 uppercase font-medium tracking-wider">' +
                  '<th class="py-3 px-4 w-48 sticky left-0 bg-slate-100 z-10 border-r border-slate-200">Teacher / Faculty</th>' +
                  '<th class="py-3 px-3 text-center border-r border-slate-200 w-24">Discipline</th>' +
                  '<!-- Morning Periods -->' +
                  '<th class="py-2.5 px-2 text-center border-r border-slate-200 w-16">P1</th>' +
                  '<th class="py-2.5 px-2 text-center border-r border-slate-200 w-16">P2</th>' +
                  '<th class="py-2.5 px-2 text-center border-r border-slate-200 w-16">P3</th>' +
                  '<th class="py-2.5 px-2 text-center border-r border-slate-200 w-16">P4</th>' +
                  '<th class="py-2.5 px-2 text-center border-r border-slate-200 w-16 bg-slate-200/40">P5</th>' +
                  '<!-- Afternoon Periods -->' +
                  '<th class="py-2.5 px-2 text-center border-r border-slate-200 w-16">P6</th>' +
                  '<th class="py-2.5 px-2 text-center border-r border-slate-200 w-16">P7</th>' +
                  '<th class="py-2.5 px-2 text-center border-r border-slate-200 w-16">P8</th>' +
                  '<th class="py-2.5 px-2 text-center border-r border-slate-200 w-16">P9</th>' +
                  '<th class="py-2.5 px-2 text-center border-r border-slate-200 w-16">P10</th>' +
                  '<th class="py-2.5 px-3 text-center border-r border-slate-200 w-24">Weekly Load</th>' +
                  '<th class="py-2.5 px-3 text-center w-24">Status</th>' +
                '</tr>' +
              '</thead>' +
              '<tbody class="divide-y divide-slate-200 text-xs">' +
                (teacherRowsHtml || '<tr><td colspan="14" class="p-6 text-center text-slate-400 font-medium">No matching faculty found</td></tr>') +
              '</tbody>' +
            '</table>' +
          '</div>' +
          '<!-- Table Footer Pagination / Quick Summary -->' +
          '<div class="p-3 sm:p-3.5 bg-slate-50 border-t border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-slate-500">' +
            '<div class="flex flex-wrap items-center gap-2">' +
              '<span class="font-medium text-slate-700">Showing ' + pageTeachers.length + ' of ' + filteredTeachers.length + ' Faculty</span>' +
              '<span class="text-slate-300 hidden sm:inline">•</span>' +
              '<span class="text-slate-500 text-[11px] sm:text-xs">Morning: 07:00–11:15 AM | Afternoon: 13:00–17:15 PM</span>' +
            '</div>' +
            '<div class="flex items-center space-x-1 font-medium overflow-x-auto no-scrollbar">' +
              '<button class="px-2.5 py-1 border border-slate-200 rounded-md bg-white text-slate-500 hover:text-slate-800 hover:bg-slate-50 disabled:opacity-50 transition" data-act="viewer-page" data-page="' + (currentPage - 1) + '" ' + (currentPage <= 1 ? 'disabled' : '') + '>Previous</button>' +
              paginationHtml +
              '<button class="px-2.5 py-1 border border-slate-200 rounded-md bg-white text-slate-600 hover:text-slate-900 hover:bg-slate-50 disabled:opacity-50 transition" data-act="viewer-page" data-page="' + (currentPage + 1) + '" ' + (currentPage >= totalPages ? 'disabled' : '') + '>Next</button>' +
            '</div>' +
          '</div>' +
        '</section>' +
        '<!-- END: SectionTeacherMatrix -->' +
      '</div>' +
    '</div>';
  }

  function attachViewerInteractions() {
    if (!root) return;

    // Day Selector Buttons
    root.querySelectorAll('[data-act="viewer-select-day"]').forEach(function (btn) {
      btn.onclick = function (e) {
        e.preventDefault();
        local.viewer.day = this.dataset.day;
        render();
      };
    });

    // Period Select Dropdown
    var periodSelect = root.querySelector('#viewerPeriodSelect');
    if (periodSelect) {
      periodSelect.onchange = function () {
        var slot = parseInt(this.value, 10);
        local.viewer.activePeriodSlot = slot;
        local.viewer.shift = slot <= 5 ? 'ព្រឹក' : 'រសៀល';
        local.viewer.period = slot <= 5 ? slot : (slot - 5);
        render();
      };
    }

    // Live Search Filter Input
    var searchInput = root.querySelector('#viewerSearchInput');
    if (searchInput) {
      searchInput.oninput = function () {
        local.viewer.q = this.value;
        local.viewer.page = 1;
        render();
        var nextInput = document.getElementById('viewerSearchInput');
        if (nextInput) {
          nextInput.focus();
          nextInput.selectionStart = nextInput.selectionEnd = nextInput.value.length;
        }
      };
    }

    // Pagination
    root.querySelectorAll('[data-act="viewer-page"]').forEach(function (btn) {
      btn.onclick = function (e) {
        e.preventDefault();
        var p = parseInt(this.dataset.page, 10);
        if (!isNaN(p) && p >= 1) {
          local.viewer.page = p;
          render();
        }
      };
    });

    // Toggle snapshot show all
    root.querySelectorAll('[data-act="toggle-snapshot-all"]').forEach(function (btn) {
      btn.onclick = function (e) {
        e.preventDefault();
        local.viewer.showAllCohorts = !local.viewer.showAllCohorts;
        render();
      };
    });

    // Auto-assign from viewer
    root.querySelectorAll('[data-act="auto-assign-viewer"]').forEach(function (btn) {
      btn.onclick = function (e) {
        e.preventDefault();
        var r = E.autoAssign({});
        toast('Timetable auto-assigned (' + r.placed + ' lessons placed)', 'success');
        render();
      };
    });
  }

  /* ── Modals & Dialogs ─────────────────────────────────────────────────── */

  function candidateListHtml(m) {
    var cands = E.candidates({ key: m.key, subjectId: m.subjectId, q: m.q });
    if (!cands.length) return '<div class="ks-empty">No available teachers for this period</div>';

    return cands.map(function (c) {
      var cName = c.name_en || D.toEnTeacher(c.name_kh) || c.name_kh;
      var statusText = c.available ? 'Available' : 'Busy';
      return '<button class="ks-candidate ' + (c.available ? '' : 'busy') + '" data-act="candidate-pick" data-id="' + esc(c.id) + '" ' + (c.available ? '' : 'disabled') + '>' +
        '<span class="mark" style="background:' + esc(c.color) + '">' + esc(c.code) + '</span>' +
        '<div class="inf">' +
          '<div style="font-weight:500">' + esc(cName) + '</div>' +
          '<small>' + esc(c.code) + ' · Workload ' + kh(c.assigned) + '/' + kh(c.target) + ' hrs · Remaining ' + kh(c.remaining) + ' hrs</small>' +
        '</div>' +
        '<span class="ks-badge ' + (c.available ? 'ok' : 'bad') + '">' + esc(statusText) + '</span>' +
      '</button>';
    }).join('');
  }

  function modalHtml() {
    if (!local.modal) return '';
    var m = local.modal;

    // Quick Lesson Editor Popover (Section 10)
    if (m.type === 'quick-editor') {
      var k = m.key;
      var cell = m.cell || ctx.grid[k];
      if (!cell) return '';
      var p = D.parseGridKey(k);
      var subName = formatKhmerSubjectName(cell.subject_name || cell.short_name);
      var clName = D.toEnClass(clsMap(ctx.state)[cell.class_id || p.class_id] || cell.class_id || p.class_id);
      var subColor = getSubjectBoxColor(cell.subject_id, subName, cell.color);
      var dayName = D.toEnDay(p.day);
      var shiftName = D.toEnShift(p.shift);
      var tchr = (ctx.state.teachers || []).filter(function (t) { return t.id === cell.teacher_id; })[0];
      var tchrName = tchr ? (tchr.name_en || D.toEnTeacher(tchr.name_kh) || tchr.name_kh) : (cell.teacher_code || '');

      var currentRoom = cell.room || 'Room 101';
      var roomsList = ['Room 101', 'Room 102', 'Room 103', 'Room 104', 'Room 201', 'Room 202', 'Computer Lab A', 'Computer Lab B', 'Science Lab 1', 'Science Lab 2', 'Sports Field', 'Library Hall'];

      var roomOptions = roomsList.map(function (rm) {
        return '<option value="' + esc(rm) + '" ' + (rm === currentRoom ? 'selected' : '') + '>' + esc(rm) + '</option>';
      }).join('');

      var qualifiedTeachers = (ctx.state.teachers || []).filter(function (t) {
        var sids = t.subject_ids || [t.subject_id];
        return sids.indexOf(cell.subject_id) !== -1 || t.specialization === cell.subject_name || t.subject_id === cell.subject_id;
      });
      if (!qualifiedTeachers.length) qualifiedTeachers = ctx.state.teachers.slice(0, 10);

      var teacherOptions = qualifiedTeachers.map(function (tc) {
        var tcName = tc.name_en || D.toEnTeacher(tc.name_kh) || tc.name_kh;
        return '<option value="' + esc(tc.id) + '" ' + (tc.id === cell.teacher_id ? 'selected' : '') + '>' + esc(tc.code + ' — ' + tcName) + '</option>';
      }).join('');

      return '<div class="ks-quick-editor-backdrop" data-act="modal-backdrop">' +
        '<div class="ks-quick-editor-card p-5 space-y-4">' +
          '<div class="flex items-center justify-between pb-3 border-b border-slate-100">' +
            '<div class="flex items-center gap-2.5">' +
              '<span class="w-3.5 h-3.5 rounded-full shrink-0" style="background:' + esc(subColor) + ';"></span>' +
              '<div>' +
                '<h4 class="text-sm sm:text-base font-medium text-slate-900 leading-snug">' + esc(subName) + '</h4>' +
                '<div class="text-xs text-slate-500 font-normal mt-0.5">Class ' + esc(clName) + ' · ' + esc(dayName) + ' ' + shiftName + ' Period ' + p.period + '</div>' +
              '</div>' +
            '</div>' +
            '<button class="p-1 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors cursor-pointer" data-act="modal-close">' +
              '<span class="material-symbols-outlined text-[18px]">close</span>' +
            '</button>' +
          '</div>' +
          '<div class="space-y-3">' +
            '<div>' +
              '<label class="block text-xs font-medium text-slate-600 mb-1">Room Assignment</label>' +
              '<select id="quickEditRoomSelect" class="w-full px-3 py-2 bg-slate-50 rounded-xl text-xs font-normal text-slate-900 border border-slate-200 focus:ring-1 focus:ring-primary focus:bg-white">' +
                roomOptions +
              '</select>' +
            '</div>' +
            '<div>' +
              '<label class="block text-xs font-medium text-slate-600 mb-1">Faculty Instructor</label>' +
              '<select id="quickEditTeacherSelect" class="w-full px-3 py-2 bg-slate-50 rounded-xl text-xs font-normal text-slate-900 border border-slate-200 focus:ring-1 focus:ring-primary focus:bg-white">' +
                teacherOptions +
              '</select>' +
            '</div>' +
            '<div class="flex items-center justify-between pt-1 text-xs text-slate-600 font-normal">' +
              '<span>Duration: 50 minutes</span>' +
              '<span>Status: ' + (cell.is_locked ? '<span class="text-amber-700 font-medium">Locked</span>' : '<span class="text-emerald-700 font-medium">Active</span>') + '</span>' +
            '</div>' +
          '</div>' +
          '<div class="pt-3 border-t border-slate-100 flex items-center justify-between gap-2 flex-wrap">' +
            '<div class="flex items-center gap-1.5">' +
              '<button class="px-3 py-1.5 rounded-lg border border-rose-200 bg-rose-50 hover:bg-rose-100 text-rose-700 text-xs font-medium transition-colors flex items-center gap-1 cursor-pointer" ' +
                'data-act="quick-edit-remove" data-key="' + esc(k) + '" title="Remove lesson and return to unplaced pool">' +
                '<span class="material-symbols-outlined text-[15px]">delete</span>' +
                '<span>Remove</span>' +
              '</button>' +
              '<button class="px-3 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-medium transition-colors flex items-center gap-1 cursor-pointer" ' +
                'data-act="quick-edit-lock" data-key="' + esc(k) + '" title="Lock slot against automated changes">' +
                '<span class="material-symbols-outlined text-[15px]">' + (cell.is_locked ? 'lock_open' : 'lock') + '</span>' +
                '<span>' + (cell.is_locked ? 'Unlock' : 'Lock') + '</span>' +
              '</button>' +
            '</div>' +
            '<div class="flex items-center gap-1.5">' +
              '<button class="px-3 py-1.5 rounded-lg border border-blue-200 bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs font-medium transition-colors flex items-center gap-1 cursor-pointer" ' +
                'data-act="quick-edit-move" data-key="' + esc(k) + '" title="Select destination to move or swap">' +
                '<span class="material-symbols-outlined text-[15px]">drag_indicator</span>' +
                '<span>Move</span>' +
              '</button>' +
              '<button class="px-4 py-1.5 rounded-lg bg-[#006C49] hover:bg-[#005236] text-white text-xs font-medium transition-colors shadow-xs cursor-pointer" ' +
                'data-act="quick-edit-save" data-key="' + esc(k) + '">' +
                'Save Changes' +
              '</button>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>';
    }

    // Change Instructor Modal for Step 2
    if (m.type === 'change-instructor') {
      var sub = (E.index().subjects || {})[m.subjectId] || {};
      var subName = sub.name_en || D.toEnSubject(sub.name_kh);
      var clName = D.toEnClass(clsMap(ctx.state)[m.classId]);
      var candidates = (ctx.state.teachers || []).filter(function (t) {
        var sids = t.subject_ids || [t.subject_id];
        return sids.indexOf(m.subjectId) !== -1 || t.specialization === sub.name_kh || t.subject_id === m.subjectId;
      });
      if (!candidates.length) candidates = ctx.state.teachers.slice(0, 8);

      var candidateRows = candidates.map(function (tc) {
        var tName = tc.name_en || D.toEnTeacher(tc.name_kh) || tc.name_kh;
        var isCurrent = tc.id === m.currentTeacherId;
        var load = (E.teacherLoad ? E.teacherLoad() : {})[tc.id] || 0;
        var target = tc.target || 17;
        return '<div class="flex items-center justify-between p-3 rounded-lg border ' +
          (isCurrent ? 'border-primary bg-primary-fixed/20' : 'border-surface-container hover:bg-surface-container-low') +
          ' transition-colors">' +
          '<div class="flex items-center gap-3">' +
            '<div class="w-8 h-8 rounded-full bg-primary-container text-on-primary flex items-center justify-center font-headline-sm text-[12px] font-medium">' +
              esc(tc.code) +
            '</div>' +
            '<div>' +
              '<div class="font-headline-sm text-headline-sm text-on-surface font-medium">' + esc(tName) + ' (' + esc(tc.name_kh) + ')</div>' +
              '<div class="font-label-sm text-label-sm text-on-surface-variant font-normal">' + esc(tc.code) + ' • Workload: ' + kh(load) + '/' + kh(target) + ' hrs</div>' +
            '</div>' +
          '</div>' +
          (isCurrent
            ? '<span class="text-label-sm font-label-sm text-primary font-medium px-2 py-1 rounded bg-primary-container/20">Current Instructor</span>'
            : '<button class="px-3 py-1.5 rounded-lg bg-primary text-white font-label-md text-label-md hover:opacity-90 font-medium" data-act="execute-replace-teacher" data-cid="' + esc(m.classId) + '" data-sid="' + esc(m.subjectId) + '" data-newtid="' + esc(tc.id) + '" data-oldtid="' + esc(m.currentTeacherId) + '">Select</button>') +
        '</div>';
      }).join('');

      return '<div class="ks-backdrop" data-act="modal-backdrop"><div class="ks-modal" style="max-width:560px">' +
        '<div class="ks-modal-head">' +
          '<div><div class="ks-modal-title">Change Instructor · Class ' + esc(clName) + '</div>' +
          '<div class="ks-sub">Subject: ' + esc(subName) + ' (' + esc(sub.name_kh) + ')</div></div>' +
          '<button class="ks-close" data-act="modal-close"><span class="material-symbols-outlined text-[14px]">close</span></button>' +
        '</div>' +
        '<div class="ks-modal-body" style="padding:16px">' +
          '<div class="space-y-2 max-h-[380px] overflow-y-auto pr-1">' + candidateRows + '</div>' +
        '</div>' +
      '</div></div>';
    }

    // Assign Subject to Cohort Modal for Step 2
    if (m.type === 'assign-subject-cohort') {
      var clName = D.toEnClass(clsMap(ctx.state)[m.classId]);
      var assignedSubIds = (ctx.state.assignments || [])
        .filter(function (a) { return a.class_id === m.classId; })
        .map(function (a) { return a.subject_id; });
      var unassignedSubjects = (ctx.state.subjects || []).filter(function (s) {
        return assignedSubIds.indexOf(s.id) === -1;
      });
      if (!unassignedSubjects.length) unassignedSubjects = ctx.state.subjects || [];

      var subOptions = unassignedSubjects.map(function (s) {
        return '<option value="' + esc(s.id) + '">' + esc(s.name_en || D.toEnSubject(s.name_kh)) + ' (' + esc(s.name_kh) + ') — ' + kh(s.lessons_per_week || 2) + ' hrs/wk</option>';
      }).join('');

      var teacherOptions = (ctx.state.teachers || []).map(function (t) {
        var tName = t.name_en || D.toEnTeacher(t.name_kh) || t.name_kh;
        return '<option value="' + esc(t.id) + '">' + esc(t.code + ' — ' + tName) + '</option>';
      }).join('');

      return '<div class="ks-backdrop" data-act="modal-backdrop"><div class="ks-modal" style="max-width:500px">' +
        '<div class="ks-modal-head">' +
          '<div><div class="ks-modal-title">Assign Subject to Cohort</div>' +
          '<div class="ks-sub">Class: Class ' + esc(clName) + '</div></div>' +
          '<button class="ks-close" data-act="modal-close"><span class="material-symbols-outlined text-[14px]">close</span></button>' +
        '</div>' +
        '<div class="ks-modal-body" style="padding:20px;display:flex;flex-direction:column;gap:14px">' +
          '<div>' +
            '<label class="font-label-sm text-label-sm text-on-surface-variant uppercase font-medium">Select Subject</label>' +
            '<select id="assignModalSubjectSelect" class="w-full mt-1 px-3 py-2 bg-surface-container rounded-lg font-body-md text-on-surface border-0 focus:ring-1 focus:ring-primary font-normal">' +
              subOptions +
            '</select>' +
          '</div>' +
          '<div>' +
            '<label class="font-label-sm text-label-sm text-on-surface-variant uppercase font-medium">Select Faculty Instructor</label>' +
            '<select id="assignModalTeacherSelect" class="w-full mt-1 px-3 py-2 bg-surface-container rounded-lg font-body-md text-on-surface border-0 focus:ring-1 focus:ring-primary font-normal">' +
              teacherOptions +
            '</select>' +
          '</div>' +
          '<div class="flex justify-end gap-2 mt-2">' +
            '<button class="px-4 py-2 rounded-lg bg-surface-container text-on-surface font-label-md font-medium" data-act="modal-close">Cancel</button>' +
            '<button class="px-4 py-2 rounded-lg bg-primary text-white font-label-md font-medium shadow-sm hover:opacity-90" data-act="execute-assign-subject" data-cid="' + esc(m.classId) + '">Confirm Assignment</button>' +
          '</div>' +
        '</div>' +
      '</div></div>';
    }

    // 1. Searchable Teacher Candidate Picker
    if (m.type === 'teacher') {
      var p = D.parseGridKey(m.key);
      var sub = (E.index().subjects || {})[m.subjectId] || {};
      var subName = sub.name_en || D.toEnSubject(sub.name_kh);
      var clName = D.toEnClass(clsMap(ctx.state)[p.class_id]);
      return '<div class="ks-backdrop" data-act="modal-backdrop"><div class="ks-modal">' +
        '<div class="ks-modal-head">' +
          '<div><div class="ks-modal-title">Select Teacher · Class ' + esc(clName) + '</div>' +
          '<div class="ks-sub">' + esc(D.toEnDay(p.day)) + ' · ' + esc(D.toEnShift(p.shift)) + ' Period ' + kh(p.period) + ' · ' + esc(subName) + '</div></div>' +
          '<button class="ks-close" data-act="modal-close"><span class="material-symbols-outlined text-[14px]">close</span></button>' +
        '</div>' +
        '<div class="ks-modal-body">' +
          '<input id="ks-candidate-search" class="ks-input" placeholder="Search teacher by name or code..." value="' + esc(m.q || '') + '" style="width:100%;margin-bottom:10px">' +
          '<div class="ks-candidate-list" id="ks-candidate-list">' + candidateListHtml(m) + '</div>' +
        '</div></div></div>';
    }

    // 2. Section 8 Teacher Replacement Confirmation Modal
    if (m.type === 'replace-confirm') {
      var oldT = (E.index().teachers || {})[m.oldTeacherId] || {};
      var newT = (E.index().teachers || {})[m.newTeacherId] || {};
      var subR = (E.index().subjects || {})[m.subjectId] || {};
      var oldName = oldT.name_en || D.toEnTeacher(oldT.name_kh) || oldT.name_kh;
      var newName = newT.name_en || D.toEnTeacher(newT.name_kh) || newT.name_kh;
      var subNameR = subR.name_en || D.toEnSubject(subR.name_kh);
      var clNameR = D.toEnClass(clsMap(ctx.state)[m.classId] || m.classId);

      return '<div class="ks-backdrop" data-act="modal-backdrop"><div class="ks-modal">' +
        '<div class="ks-modal-head">' +
          '<div class="ks-modal-title">Reassign Teacher for Class ' + esc(clNameR) + '</div>' +
          '<button class="ks-close" data-act="modal-close"><span class="material-symbols-outlined text-[14px]">close</span></button>' +
        '</div>' +
        '<div class="ks-modal-body">' +
          '<p style="font-size:13.5px;line-height:1.6;margin-bottom:14px">' +
            'Are you sure you want to reassign <b>' + esc(subNameR) + '</b> for Class ' + esc(clNameR) + ' from <b>' + esc(oldT.code + ' - ' + oldName) + '</b> to <b>' + esc(newT.code + ' - ' + newName) + '</b>?' +
          '</p>' +
          '<div class="ks-hint" style="background:#FFF9F2;border:1px solid #FCD9BD;border-radius:8px;padding:10px 12px;margin-bottom:14px">' +
            '<b>Section 8 Safety Rules:</b><br>' +
            '• Existing scheduled lessons where the new teacher is available are <b>PRESERVED</b> in-place.<br>' +
            '• Conflicting lessons (already teaching or unavailable) are automatically <b>DISPLACED to the unscheduled pool</b>.' +
          '</div>' +
          '<div style="display:flex;justify-content:flex-end;gap:8px">' +
            '<button class="ks-btn" data-act="modal-close">Cancel</button>' +
            '<button class="ks-btn primary" data-act="execute-replace-teacher">Confirm Reassignment</button>' +
          '</div>' +
        '</div></div></div>';
    }

    // 3. Section 18 Publish Timetable Modal
    if (m.type === 'publish-confirm') {
      var conflicts = E.conflicts().filter(function (c) { return c.severity === 'error'; });
      var canPublish = conflicts.length === 0;

      return '<div class="ks-backdrop" data-act="modal-backdrop"><div class="ks-modal" style="max-width:540px">' +
        '<div class="ks-modal-head">' +
          '<div class="ks-modal-title">Publish Timetable to School Portals</div>' +
          '<button class="ks-close" data-act="modal-close"><span class="material-symbols-outlined text-[14px]">close</span></button>' +
        '</div>' +
        '<div class="ks-modal-body">' +
          '<p style="font-size:13.5px;line-height:1.6;margin-bottom:14px">' +
            'Publishing will immediately activate this timetable on both the <b>Teacher Portal</b> and <b>Student Portal</b> for all teachers and students.' +
          '</p>' +
          '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px;font-size:12px">' +
            '<div class="ks-diff-stat"><div class="v">' + kh(ctx.state.classes.length) + '</div><div class="l">Total Classes</div></div>' +
            '<div class="ks-diff-stat"><div class="v">' + kh(ctx.state.teachers.length) + '</div><div class="l">Total Teachers</div></div>' +
            '<div class="ks-diff-stat"><div class="v">' + kh(E.stats().placed) + '</div><div class="l">Placed Periods</div></div>' +
            '<div class="ks-diff-stat"><div class="v">' + kh(E.stats().unassigned) + '</div><div class="l">Unscheduled Periods</div></div>' +
          '</div>' +
          (canPublish ?
            '<div class="ks-hint" style="background:#E8F3ED;border:1px solid #BEE1CE;border-radius:8px;padding:10px 12px;margin-bottom:14px;color:var(--ks-green)">' +
              'Zero timetable conflicts · Ready for immediate publication' +
            '</div>' :
            '<div class="ks-hint" style="background:#FFECEB;border:1px solid #FFC9C6;border-radius:8px;padding:10px 12px;margin-bottom:14px;color:var(--ks-red)">' +
              'Cannot publish: ' + kh(conflicts.length) + ' hard conflicts exist. Please resolve conflicts before publishing.' +
            '</div>') +
          '<div style="display:flex;justify-content:flex-end;gap:8px">' +
            '<button class="ks-btn" data-act="modal-close">Cancel</button>' +
            '<button class="ks-btn primary" data-act="execute-publish" ' + (canPublish ? '' : 'disabled') + ' style="background:#137A45;border-color:#137A45">Publish Now</button>' +
          '</div>' +
        '</div></div></div>';
    }

    // 4. Conflicts List Modal
    if (m.type === 'conflicts') {
      var allConflicts = E.conflicts();
      return '<div class="ks-backdrop" data-act="modal-backdrop"><div class="ks-modal" style="max-width:560px">' +
        '<div class="ks-modal-head">' +
          '<div class="ks-modal-title">Timetable Conflicts (' + kh(allConflicts.length) + ')</div>' +
          '<button class="ks-close" data-act="modal-close"><span class="material-symbols-outlined text-[14px]">close</span></button>' +
        '</div>' +
        '<div class="ks-modal-body ks-scroll" style="max-height:60vh">' +
          (allConflicts.length ? allConflicts.map(function (c) {
            var msg = c.message_en || c.message_kh;
            return '<div class="ks-conflict-item">' +
              '<span class="ico ' + (c.severity === 'error' ? 'bad' : 'warn') + '">●</span>' +
              '<div><span style="font-weight:500">' + esc(msg) + '</span><br><small style="color:var(--ks-muted)">' + esc(c.key || '') + '</small></div>' +
            '</div>';
          }).join('') : '<div class="ks-empty">Zero timetable conflicts</div>') +
        '</div></div></div>';
    }

    // 5. Excel Copy/Paste Help Modal
    if (m.type === 'paste-help') {
      return '<div class="ks-backdrop" data-act="modal-backdrop"><div class="ks-modal" style="max-width:540px">' +
        '<div class="ks-modal-head">' +
          '<div class="ks-modal-title">How to Copy & Paste from Excel / Google Sheets</div>' +
          '<button class="ks-close" data-act="modal-close"><span class="material-symbols-outlined text-[14px]">close</span></button>' +
        '</div>' +
        '<div class="ks-modal-body" style="font-size:13px;line-height:1.6">' +
          '<p>1. Open your <b>Microsoft Excel</b> or <b>Google Sheets</b> document.</p>' +
          '<p>2. Select the teacher data rows and press <b>Ctrl+C</b> (Copy).</p>' +
          '<p>3. Return to this page, click the target cell in the spreadsheet, and press <b>Ctrl+V</b> (Paste).</p>' +
          '<p>4. The system automatically parses tab-separated columns and preserves Khmer Unicode names accurately.</p>' +
          '<div style="text-align:right;margin-top:14px"><button class="ks-btn primary" data-act="modal-close">Got It</button></div>' +
        '</div></div></div>';
    }

    return '';
  }

  function toast(msg, tone) {
    var el = document.createElement('div');
    el.className = 'ks-toast ' + (tone || '');
    el.textContent = msg;
    var c = document.getElementById('ks-toasts');
    if (!c) {
      c = document.createElement('div');
      c.id = 'ks-toasts';
      c.className = 'ks-toasts';
      document.body.appendChild(c);
    }
    c.appendChild(el);
    setTimeout(function () { el.remove(); }, 3200);
  }

  /* ── Event delegation ─────────────────────────────────────────────────── */

  function onClick(e) {
    var target = e.target.closest('[data-act]');
    if (!target || !root.contains(target)) return;
    var act = target.dataset.act, id = target.dataset.id, key = target.dataset.key;
    if (act === 'modal-backdrop' && e.target !== target) return;

    switch (act) {
      case 'undo': E.undo(); toast('↶ Undone'); break;
      case 'redo': E.redo(); toast('↷ Redone'); break;
      case 'history': local.modal = { type: 'history' }; render(); break;
      case 'save': E.flushSave().then(function () { toast('Changes saved successfully', 'success'); }); break;
      case 'modal-close': local.modal = null; render(); break;
      case 'modal-backdrop': local.modal = null; render(); break;
      case 'conflicts': local.modal = { type: 'conflicts' }; render(); break;
      case 'show-paste-help': local.modal = { type: 'paste-help' }; render(); break;

      // Data Entry tabs
      case 'set-datatab': local.dataTab = id; render(); break;
      case 'set-grade': local.selectedGrade = parseInt(id, 10); render(); break;
      case 'set-class-config': local.selectedClass = id; render(); break;

      // Spreadsheet actions
      case 'add-teacher-row': {
        var state = ctx.state;
        var nextNum = state.teachers.length + 1;
        state.teachers.push({
          id: 't_new_' + Date.now(),
          code: 'T' + nextNum,
          name_kh: 'New Teacher ' + nextNum,
          name_en: 'New Teacher ' + nextNum,
          gender: 'Male',
          phone: '',
          position: 'Teacher',
          category: 'Civil Servant',
          rank: 'Senior Teacher',
          specialization: 'General',
          subject_id: 'sub_K',
          target: 17,
          max_daily: 5,
          employee_id: 'EMP-' + (2000 + nextNum),
          start_year: 2024,
          notes: '',
          shifts: ['ព្រឹក', 'រសៀល'],
          unavailable_slots: []
        });
        E.commit('Add teacher row', function () {});
        toast('＋ Added new teacher row', 'success');
        break;
      }
      case 'copy-teachers-clipboard': {
        var cols = D.TEACHER_SPREADSHEET_COLUMNS;
        var matrix = [cols.map(function (c) { return c.en; })];
        ctx.state.teachers.forEach(function (t, i) {
          matrix.push(cols.map(function (c) {
            return c.key === 'no' ? (i + 1) : (t[c.key] != null ? t[c.key] : '');
          }));
        });
        var tsv = D.formatClipboardTable(matrix);
        navigator.clipboard.writeText(tsv).then(function () {
          toast('Copied all teacher data as TSV/Excel', 'success');
        });
        break;
      }
      case 'reset-teachers-data':
        if (confirm('Are you sure you want to reset teacher data?')) {
          E.reset(); toast('Data reset successfully', 'success');
        }
        break;
      case 'save-teachers-spreadsheet':
        E.flushSave().then(function () { toast('Saved teacher spreadsheet successfully', 'success'); });
        break;

      // Teacher Unavailability Matrix Toggle
      case 'toggle-unavail': {
        var tid = target.dataset.tid, slot = target.dataset.slot;
        var tc = ctx.state.teachers.filter(function (x) { return x.id === tid; })[0];
        if (tc) {
          tc.unavailable_slots = tc.unavailable_slots || [];
          var idxU = tc.unavailable_slots.indexOf(slot);
          if (idxU !== -1) tc.unavailable_slots.splice(idxU, 1);
          else tc.unavailable_slots.push(slot);
          E.commit('Toggle unavailability for ' + tc.code, function () {});
          render();
        }
        break;
      }

      // Step 2 Teacher Assignment
      case 'select-assign-teacher':
        local.selectedTeacherId = id;
        local.assignmentSubjectId = null;
        render(); break;
      case 'set-assign-subject':
        local.assignmentSubjectId = id;
        render(); break;
      case 'toggle-chip-assignment': {
        var cid = target.dataset.cid, sid = target.dataset.sid, tid = target.dataset.tid;
        var asg = ctx.state.assignments.filter(function (a) { return a.class_id === cid && a.subject_id === sid; })[0];
        if (asg && asg.teacher_id === tid) {
          // Unassign
          E.commit('Unassign class ' + cid, function (s) {
            s.assignments = s.assignments.filter(function (a) { return !(a.class_id === cid && a.subject_id === sid); });
          });
          toast('Unassigned class ' + D.toEnClass(cid));
        } else {
          // Assign
          E.commit('Assign teacher for class ' + cid, function (s) {
            var sub = (E.index().subjects || {})[sid] || {};
            s.assignments = s.assignments.filter(function (a) { return !(a.class_id === cid && a.subject_id === sid); });
            s.assignments.push({
              id: 'asg_' + cid + '_' + sid + '_' + tid,
              class_id: cid, subject_id: sid, teacher_id: tid,
              lessons: sub.lessons_per_week || 2, shift: 'ព្រឹក'
            });
          });
          toast('Assigned teacher for class ' + D.toEnClass(cid), 'success');
        }
        break;
      }
      case 'prompt-replace-teacher': {
        local.modal = {
          type: 'replace-confirm',
          classId: target.dataset.cid,
          subjectId: target.dataset.sid,
          newTeacherId: target.dataset.newtid,
          oldTeacherId: target.dataset.oldtid
        };
        render();
        break;
      }
      case 'execute-replace-teacher': {
        var m = local.modal;
        var res = E.reassign(m.classId, m.subjectId, m.newTeacherId, m.oldTeacherId);
        local.modal = null;
        if (res.ok) {
          toast('Preserved ' + kh(res.preserved) + ' hrs · Displaced ' + kh(res.displaced) + ' hrs', 'success');
        } else {
          toast(res.error || 'Reassignment error', 'error');
        }
        render();
        break;
      }

      // Step 2 Modern Wizard Actions
      case 'select-wizard-class': {
        local.selectedClass = target.dataset.cid;
        local.wizardMobileTab = 'matrix';
        persistUI();
        render();
        break;
      }
      case 'wizard-mobile-tab': {
        local.wizardMobileTab = target.dataset.tab;
        persistUI();
        render();
        break;
      }
      case 'wizard-save': {
        E.flushSave().then(function () {
          toast('Changes saved successfully', 'success');
        });
        break;
      }
      case 'wizard-print': {
        window.print();
        break;
      }
      case 'prompt-change-instructor': {
        local.modal = {
          type: 'change-instructor',
          classId: target.dataset.cid,
          subjectId: target.dataset.sid,
          currentTeacherId: target.dataset.tid
        };
        render();
        break;
      }
      case 'open-assign-modal': {
        local.modal = {
          type: 'assign-subject-cohort',
          classId: target.dataset.cid
        };
        render();
        break;
      }
      case 'clear-assignment': {
        var cid = target.dataset.cid, sid = target.dataset.sid;
        if (confirm('Clear this subject assignment from the class?')) {
          E.commit('Clear assignment ' + cid + ' ' + sid, function (s) {
            s.assignments = s.assignments.filter(function (a) {
              return !(a.class_id === cid && a.subject_id === sid);
            });
            Object.keys(s.grid).forEach(function (k) {
              var cell = s.grid[k];
              if (cell && cell.class_id === cid && cell.subject_id === sid) {
                delete s.grid[k];
              }
            });
          });
          E.scheduleSave();
          toast('Subject assignment removed from cohort', 'info');
          render();
        }
        break;
      }
      case 'execute-assign-subject': {
        var cid = target.dataset.cid;
        var sid = document.getElementById('assignModalSubjectSelect') ? document.getElementById('assignModalSubjectSelect').value : null;
        var tid = document.getElementById('assignModalTeacherSelect') ? document.getElementById('assignModalTeacherSelect').value : null;
        if (!sid || !tid) {
          toast('Please select both subject and educator', 'error');
          break;
        }
        var sub = (ctx.state.subjects || []).filter(function (s) { return s.id === sid; })[0] || {};
        var hours = sub.lessons_per_week || 2;
        E.commit('Assign ' + sid + ' to ' + cid, function (s) {
          s.assignments = s.assignments.filter(function (a) { return !(a.class_id === cid && a.subject_id === sid); });
          s.assignments.push({
            id: 'asg_' + cid + '_' + sid + '_' + tid,
            class_id: cid,
            subject_id: sid,
            teacher_id: tid,
            lessons: hours,
            shift: 'ព្រឹក'
          });
        });
        E.scheduleSave();
        local.modal = null;
        toast('Assigned subject to cohort', 'success');
        render();
        break;
      }

      // Step 3 Timetable Builder
      case 'set-view-mode':
        local.viewMode = target.dataset.id || id;
        if (local.viewMode === 'school') { local.preview = true; }
        else { local.preview = false; }
        render();
        break;
      case 'set-class-cohort':
        local.selectedClass = id;
        local.viewMode = 'class';
        local.preview = false;
        persistUI();
        render();
        break;
      case 'set-mobile-day':
        local.selectedMobileDay = target.dataset.day || id;
        render();
        break;
      case 'save-draft':
        E.flushSave().then(function () {
          local.lastSavedAt = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
          render();
          toast('Draft saved to database successfully', 'success');
        });
        break;
      case 'auto-schedule-current':
        if (local.viewMode === 'teacher') {
          var resT = E.autoAssign({ teacherId: local.selectedTeacherId });
          toast('Auto-scheduled ' + (resT.placed || 0) + ' periods for faculty', 'success');
        } else {
          var resC = E.autoAssign({ classId: local.selectedClass });
          toast('Auto-scheduled ' + (resC.placed || 0) + ' periods for Class ' + D.toEnClass(local.selectedClass), 'success');
        }
        break;
      case 'select-right-lesson':
        local.selectedChip = target.dataset.chipId || id;
        render();
        toast('Lesson selected. Tap any available slot in the timetable to place.', 'info');
        break;
      case 'find-slot': {
        var chipIdFind = target.dataset.chipId || id;
        var allChips = E.chips().concat(E.chipsForTeacher ? E.chipsForTeacher(local.selectedTeacherId) : []);
        var ch = allChips.filter(function (c) { return c.id === chipIdFind; })[0];
        if (!ch) {
          (ctx.state.classes || []).forEach(function (cls) {
            if (ch) return;
            var cc = E.chips(cls.id).filter(function (c) { return c.id === chipIdFind; })[0];
            if (cc) ch = cc;
          });
        }
        if (ch) {
          var days = ctx.state.settings.days;
          var periods = ctx.state.settings.periods;
          var foundKey = null;
          for (var d = 0; d < days.length && !foundKey; d++) {
            for (var p = 0; p < periods.length && !foundKey; p++) {
              var k = D.gridKey(days[d], periods[p].shift, periods[p].number, ch.class_id);
              if (!ctx.grid[k]) {
                var conf = E.validate(k, ch.subject_id, ch.teacher_id, false);
                var errs = conf.filter(function (c) { return c.severity === 'error'; });
                if (!errs.length) {
                  foundKey = k;
                }
              }
            }
          }
          if (foundKey) {
            local.highlightSlotKey = foundKey;
            local.selectedChip = ch.id;
            render();
            setTimeout(function () {
              var cellEl = document.querySelector('[data-key="' + foundKey + '"]');
              if (cellEl) cellEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 60);
            toast('Found available slot: ' + D.toEnDay(D.parseGridKey(foundKey).day) + ' Period ' + D.parseGridKey(foundKey).period, 'success');
          } else {
            toast('No conflict-free slots found for this assignment', 'warning');
          }
        }
        break;
      }
      case 'quick-edit-remove': {
        var kRem = target.dataset.key || (local.modal && local.modal.key);
        if (kRem) {
          E.clearCell(kRem);
          local.modal = null;
          local.targetKey = null;
          render();
          toast('Lesson removed and returned to remaining pool. (Ctrl+Z to undo)', 'info');
        }
        break;
      }
      case 'quick-edit-lock': {
        var kLock = target.dataset.key || (local.modal && local.modal.key);
        if (kLock && ctx.grid[kLock]) {
          E.commit('Toggle lock on slot', function (s) {
            if (s.grid[kLock]) s.grid[kLock].is_locked = !s.grid[kLock].is_locked;
          });
          local.modal = null;
          render();
          toast('Slot lock toggled successfully', 'success');
        }
        break;
      }
      case 'quick-edit-move': {
        var kMove = target.dataset.key || (local.modal && local.modal.key);
        local.targetKey = kMove;
        local.isMoveMode = true;
        local.modal = null;
        render();
        toast('Move mode active. Tap any open slot or another lesson to swap.', 'info');
        break;
      }
      case 'quick-edit-save': {
        var kSave = target.dataset.key || (local.modal && local.modal.key);
        var roomSel = document.getElementById('quickEditRoomSelect');
        var tchrSel = document.getElementById('quickEditTeacherSelect');
        if (kSave && ctx.grid[kSave]) {
          var newRoom = roomSel ? roomSel.value : null;
          var newTchr = tchrSel ? tchrSel.value : null;
          E.commit('Update lesson room and faculty', function (s) {
            if (s.grid[kSave]) {
              if (newRoom) s.grid[kSave].room = newRoom;
              if (newTchr) s.grid[kSave].teacher_id = newTchr;
            }
          });
          local.modal = null;
          render();
          toast('Lesson details updated successfully', 'success');
        }
        break;
      }
      case 'export':
        E.exportXlsx(target.dataset.type || 'all', local.selectedClass);
        toast('Timetable exported successfully', 'success');
        break;
      case 'chip':
        local.selectedChip = local.selectedChip === id ? null : id;
        toast(local.selectedChip ? 'Lesson selected. Tap any timetable slot to place.' : 'Deselected');
        render();
        break;
      case 'cancel-move':
        local.targetKey = null;
        render();
        break;
      case 'delete-placed-lesson': {
        var delKey = id || key || local.targetKey;
        if (delKey) {
          E.clearCell(delKey);
          local.targetKey = null;
          toast('Removed period from timetable. (Ctrl+Z to undo)', 'info');
        }
        break;
      }
      case 'cell': {
        // 1. If a chip from unassigned strip or right rail is active: place it into this cell
        if (local.selectedChip) {
          var allChipsCell = E.chips().concat(E.chipsForTeacher ? E.chipsForTeacher(local.selectedTeacherId) : []);
          var chipToPlace = allChipsCell.filter(function (c) { return c.id === local.selectedChip; })[0];
          if (!chipToPlace) {
            (ctx.state.classes || []).forEach(function (cls) {
              if (chipToPlace) return;
              var cc = E.chips(cls.id).filter(function (c) { return c.id === local.selectedChip; })[0];
              if (cc) chipToPlace = cc;
            });
          }
          if (chipToPlace) {
            var partsP = D.parseGridKey(key);
            var effectiveKeyP = D.gridKey(partsP.day, partsP.shift, partsP.period, chipToPlace.class_id);
            var resP = E.setCell(effectiveKeyP, { subject_id: chipToPlace.subject_id, teacher_id: chipToPlace.teacher_id }, { replace: true, label: 'Place period in timetable' });
            if (!resP.ok) {
              var errP = resP.conflicts.filter(function (c) { return c.severity === 'error'; })[0];
              toast(errP ? (errP.message_en || errP.message_kh) : 'Cannot place lesson', 'error');
            } else {
              local.selectedChip = null;
              local.highlightSlotKey = null;
              toast('Scheduled lesson in timetable', 'success');
            }
            return;
          }
        }

        // 2. If move mode is explicitly active, move or swap!
        if (local.isMoveMode && local.targetKey && local.targetKey !== key && ctx.grid[local.targetKey]) {
          moveOrSwapLesson(local.targetKey, key);
          local.isMoveMode = false;
          return;
        }

        // 3. If this cell has a lesson: open Quick Lesson Editor popover!
        var existingCell = ctx.grid[key];
        if (existingCell) {
          local.modal = {
            type: 'quick-editor',
            key: key,
            cell: existingCell
          };
          local.targetKey = key;
          local.isMoveMode = false;
          render();
          return;
        }

        // 4. Empty cell clicked (and no chip selected): open candidate picker
        openTeacherModal(key, 'sub_K', null);
        break;
      }
      case 'candidate-pick': {
        var mPick = local.modal;
        var resPick = E.setCell(mPick.key, { subject_id: mPick.subjectId, teacher_id: id }, { replace: true, label: 'Pick teacher candidate' });
        if (!resPick.ok) {
          var errPick = resPick.conflicts.filter(function (c) { return c.severity === 'error'; })[0];
          toast(errPick ? (errPick.message_en || errPick.message_kh) : 'Placement error', 'error');
          return;
        }
        local.modal = null; local.targetKey = null; local.selectedChip = null;
        toast('Period scheduled successfully', 'success');
        render();
        break;
      }
      case 'auto-assign': {
        var rAuto = E.autoAssign({});
        local.modal = null;
        toast('Placed ' + (rAuto.placed || 0) + ' / ' + (rAuto.requested || 0) + ' periods', 'success');
        break;
      }
      case 'fill-class': {
        var rf = E.autoAssign({ classId: id });
        toast('Placed ' + (rf.placed || 0) + ' periods for Class ' + D.toEnClass(clsMap(ctx.state)[id] || id), 'success');
        break;
      }
      case 'distribute-all': {
        var rDist = E.autoAssign({});
        toast('Distributed across all classes (' + (rDist.placed || 0) + ' placed)', 'success');
        break;
      }
      case 'preview-toggle':
        local.preview = !local.preview;
        render();
        break;
      case 'open-publish-modal':
        local.modal = { type: 'publish-confirm' };
        render();
        break;
      case 'execute-publish': {
        E.publish(ROLE === 'principal' ? 'Principal' : 'Admin', 'AY 2026-2027 Official')
          .then(function (res) {
            local.modal = null;
            toast('Timetable v' + (res.published.version || 1) + ' published successfully to all portals!', 'success');
            render();
          })
          .catch(function (err) {
            toast(err.message || 'Publishing error', 'error');
          });
        break;
      }
      case 'subject-add': {
        var n = ctx.state.subjects.length + 1;
        E.commit('Add subject', function (s) {
          s.subjects.push({
            id: 'sub_new_' + Date.now(), name_kh: 'New Subject ' + n,
            name_en: 'New Subject ' + n, short_name: 'New ' + n, code: 'N' + n, color: '#B6A6E0',
            lessons_per_week: 2, is_locked: false, department: 'General', active: true
          });
        });
        toast('New subject added', 'success'); break;
      }
      case 'subject-lock':
        E.commit('Toggle lock', function (s) {
          s.subjects.forEach(function (x) { if (x.id === id) x.is_locked = !x.is_locked; });
        });
        break;
      case 'subject-delete':
        if (!confirm('Delete this subject?')) return;
        E.commit('Delete subject', function (s) {
          s.subjects = s.subjects.filter(function (x) { return x.id !== id; });
          s.assignments = s.assignments.filter(function (a) { return a.subject_id !== id; });
          Object.keys(s.grid).forEach(function (k) { if (s.grid[k].subject_id === id) delete s.grid[k]; });
        });
        toast('Subject deleted'); break;
    }
  }

  function onChange(e) {
    var target = e.target;
    var kind = target.dataset.change, id = target.dataset.id, key = target.dataset.key;
    var val = target.value;

    if (kind === 'class-select' || kind === 'wizard-class-select' || kind === 'builder-class-select') {
      local.selectedClass = val; persistUI(); render();
    } else if (kind === 'class-select-legacy') {
      local.selectedClass = val; persistUI(); render();
    } else if (kind === 'builder-teacher-select') {
      local.selectedTeacherId = val; render();
    } else if (kind === 'assign-filter-sub') {
      local.teacherFilterSubject = val; render();
    } else if (kind === 'cell-edit') {
      var r = parseInt(target.dataset.row, 10);
      var c = target.dataset.key;
      var t = ctx.state.teachers[r];
      if (t) {
        t[c] = (c === 'target' || c === 'max_daily' || c === 'start_year') ? (parseInt(val, 10) || 0) : val;
        E.scheduleSave();
      }
    }
  }

  function onInput(e) {
    if (e.target.id === 'ks-candidate-search' && local.modal && local.modal.type === 'teacher') {
      local.modal.q = e.target.value;
      var list = document.getElementById('ks-candidate-list');
      if (list) list.innerHTML = candidateListHtml(local.modal);
    } else if (e.target.dataset && e.target.dataset.change === 'assign-search-q') {
      local.teacherSearchQ = e.target.value;
      render();
    } else if (e.target.dataset && e.target.dataset.change === 'teacher-search-details') {
      local.teacherSearchQ = e.target.value;
      render();
    }
  }

  function openTeacherModal(key, subjectId, teacherId) {
    local.modal = { type: 'teacher', key: key, subjectId: subjectId, teacherId: teacherId, q: '' };
    local.targetKey = key;
    render();
    setTimeout(function () {
      var input = document.getElementById('ks-candidate-search');
      if (input) input.focus();
    }, 50);
  }

  function onPaste(e) {
    // Spreadsheet clipboard paste integration
    if (MODULE === 'records' && local.dataTab === 'teachers') {
      var text = (e.clipboardData || window.clipboardData).getData('text');
      if (!text) return;

      var matrix = D.parseClipboardTable(text);
      if (!matrix.length) return;

      e.preventDefault();
      var state = ctx.state;
      var teachers = state.teachers;
      var cols = D.TEACHER_SPREADSHEET_COLUMNS;
      var startRow = local.activeCell.row || 0;
      var startCol = local.activeCell.col || 1;

      // Expand rows if needed
      while (teachers.length < startRow + matrix.length) {
        var num = teachers.length + 1;
        teachers.push({
          id: 't_new_' + Date.now() + '_' + num,
          code: 'T' + num,
          name_kh: 'New Teacher ' + num,
          name_en: 'New Teacher ' + num,
          gender: 'Male',
          phone: '',
          position: 'Teacher',
          category: 'Civil Servant',
          rank: 'Senior Teacher',
          specialization: 'General',
          subject_id: 'sub_K',
          target: 17,
          max_daily: 5,
          employee_id: 'EMP-' + (2000 + num),
          start_year: 2024,
          notes: '',
          shifts: ['ព្រឹក', 'រសៀល'],
          unavailable_slots: []
        });
      }

      matrix.forEach(function (row, rOffset) {
        var tRow = teachers[startRow + rOffset];
        if (!tRow) return;

        row.forEach(function (val, cOffset) {
          var colIdx = startCol + cOffset;
          if (colIdx >= cols.length) return;
          var colDef = cols[colIdx];
          if (colDef.readOnly) return;

          if (colDef.type === 'number') {
            tRow[colDef.key] = parseInt(val, 10) || 0;
          } else {
            tRow[colDef.key] = val;
          }
        });
      });

      E.commit('Paste Excel rows into teachers table', function () {});
      toast('Imported ' + kh(matrix.length) + ' rows into spreadsheet', 'success');
      render();
    }
  }

  function onKeydown(e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z' && !/INPUT|TEXTAREA/.test(e.target.tagName)) {
      e.preventDefault();
      if (e.shiftKey) E.redo(); else E.undo();
    } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'y' && !/INPUT|TEXTAREA/.test(e.target.tagName)) {
      e.preventDefault(); E.redo();
    } else if (e.key === 'Escape') {
      if (local.modal) {
        local.modal = null;
        render();
      } else if (local.targetKey || local.selectedChip) {
        local.targetKey = null;
        local.selectedChip = null;
        render();
      }
    } else if ((e.key === 'Delete' || e.key === 'Backspace') && !/INPUT|TEXTAREA/.test(e.target.tagName)) {
      if (local.targetKey && ctx.grid[local.targetKey]) {
        e.preventDefault();
        var delKey = local.targetKey;
        E.clearCell(delKey);
        local.targetKey = null;
        toast('Removed period from timetable', 'info');
      }
    }
  }

  /* ── Main Render Dispatcher ───────────────────────────────────────────── */

  function render() {
    if (!root) return;
    ctx.state = (E.get ? E.get() : (E.state ? E.state() : {})) || {};
    ctx.stats = (E.stats ? E.stats() : (E.statistics ? E.statistics() : {})) || {};
    ctx.grid = (E.grid ? E.grid() : (E.gridView ? E.gridView() : {})) || {};
    ctx.undo = E.undoDepth();
    ctx.redo = E.redoDepth();
    ctx.saveStatus = E.saveStatus();

    var html = '<div class="ks">' + pageHeadHtml() + kpiHtml();

    if (MODULE === 'records') {
      root.innerHTML = recordsHtml() + modalHtml();
      return;
    } else if (MODULE === 'wizard') {
      root.innerHTML = wizardHtml() + modalHtml();
      attachWizardInteractions();
      return;
    } else if (MODULE === 'builder') {
      root.innerHTML = builderHtml() + modalHtml();
      attachBuilderInteractions();
      return;
    } else if (MODULE === 'viewer') {
      root.innerHTML = viewerHtml() + modalHtml();
      attachViewerInteractions();
      return;
    } else if (MODULE === 'subjects') {
      if (ROLE === 'admin' || ROLE === 'principal') {
        root.innerHTML = subjectsAdminHtml() + modalHtml();
        attachAdminSubjectInteractions();
        return;
      }
      html += subjectsHtml();
    }

    html += modalHtml() + '</div>';
    root.innerHTML = html;
  }

  function scheduleRender() {
    if (rafPending) return;
    rafPending = true;
    requestAnimationFrame(function () {
      rafPending = false;
      render();
    });
  }

  function boot() {
    root = document.getElementById('ks-root');
    if (!root) return;

    if (!document.getElementById('ks-suite-custom-style')) {
      var st = document.createElement('style');
      st.id = 'ks-suite-custom-style';
      st.textContent = [
        ".ks-timetable-grid { table-layout: fixed !important; width: 100% !important; border-collapse: collapse !important; }",
        ".ks-timetable-grid th { padding: 8px 4px !important; vertical-align: middle !important; font-family: 'Noto Sans Khmer', 'Kantumruy Pro', 'Battambang', sans-serif !important; font-weight: 500 !important; }",
        ".ks-timetable-grid td { padding: 0 !important; vertical-align: middle !important; height: 58px !important; }",
        ".ks-timetable-grid td.time-col { padding: 6px 2px !important; vertical-align: middle !important; }",
        ".ks-timetable-grid .font-khmer, .font-khmer { font-family: 'Noto Sans Khmer', 'Kantumruy Pro', 'Battambang', 'Khmer OS Siemreap', 'Khmer OS System', sans-serif !important; }",
        ".ks-cell-btn { width: 100% !important; height: 100% !important; min-height: 58px !important; border-radius: 0 !important; }",
        "::-webkit-scrollbar { width: 6px; height: 6px; }",
        "::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 9999px; }",
        "::-webkit-scrollbar-track { background: transparent; }"
      ].join('\n');
      if (document.head) document.head.appendChild(st);
      else if (document.body) document.body.appendChild(st);
    }

    root.addEventListener('click', onClick);
    root.addEventListener('change', onChange);
    root.addEventListener('input', onInput);
    document.addEventListener('paste', onPaste);
    document.addEventListener('keydown', onKeydown);

    E.on(scheduleRender);
    E.init().then(function () {
      var grid = E.grid();
      if (grid && Object.keys(grid).length <= 1) {
        E.setCell('ច័ន្ទ|ព្រឹក|1|class_7A', { subject_id: 'sub_K', teacher_id: 't_K1' }, { replace: true, label: 'Initial schedule sample' });
        E.setCell('អង្គារ|ព្រឹក|1|class_7A', { subject_id: 'sub_K', teacher_id: 't_K1' }, { replace: true, label: 'Initial schedule sample' });
        E.setCell('ព្រហស្បតិ៍|ព្រឹក|1|class_7A', { subject_id: 'sub_K', teacher_id: 't_K1' }, { replace: true, label: 'Initial schedule sample' });
      }
      local.targetKey = null;
      local.isMoveMode = false;
      scheduleRender();
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();

  global.KSSuite = { render: render, toast: toast, local: local };
})(window);
