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
      '<div class="bg-white rounded-2xl border border-slate-200/80 shadow-xs p-3.5 sm:p-4 mb-4">' +
        '<div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-3 sm:gap-4">' +
          '<!-- Left: View Mode Selector, Dropdowns, and Context -->' +
          '<div class="flex items-center gap-2.5 sm:gap-3 flex-wrap">' +
            '<!-- View Selector Tabs -->' +
            '<div class="inline-flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200/70">' +
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
              ? ('<div class="inline-flex items-center gap-1.5 bg-slate-100 px-2.5 py-1 rounded-xl border border-slate-200/70">' +
                  '<span class="text-xs text-slate-500 font-normal">Faculty:</span>' +
                  '<select class="bg-transparent text-xs font-medium text-slate-900 border-0 focus:ring-0 cursor-pointer py-0.5 pl-0.5 pr-6" data-change="builder-teacher-select">' +
                    state.teachers.map(function (tc) {
                      var tcName = tc.name_en || D.toEnTeacher(tc.name_kh) || tc.name_kh;
                      return '<option value="' + esc(tc.id) + '" ' + (tc.id === curTeacher.id ? 'selected' : '') + '>' + esc(tc.code + ' — ' + tcName) + '</option>';
                    }).join('') +
                  '</select>' +
                '</div>')
              : ('<div class="inline-flex items-center gap-1.5 bg-slate-100 px-2.5 py-1 rounded-xl border border-slate-200/70">' +
                  '<span class="text-xs text-slate-500 font-normal">Class:</span>' +
                  '<select class="bg-transparent text-xs font-medium text-slate-900 border-0 focus:ring-0 cursor-pointer py-0.5 pl-0.5 pr-6" data-change="builder-class-select">' +
                    state.classes.map(function (cls) {
                      return '<option value="' + esc(cls.id) + '" ' + (cls.id === curClass.id ? 'selected' : '') + '>Class ' + esc(D.toEnClass(cls.display || cls.id)) + '</option>';
                    }).join('') +
                  '</select>' +
                '</div>')
            ) +

            '<!-- Academic Context Pill -->' +
            '<div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200/60 text-emerald-800 text-xs font-medium">' +
              '<span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>' +
              '<span>Main Campus · AY 2026-2027 · Term 1</span>' +
            '</div>' +

            (local.lastSavedAt
              ? '<span class="text-[11px] text-slate-400 font-normal hidden xl:inline">Saved ' + esc(local.lastSavedAt) + '</span>'
              : '') +
          '</div>' +

          '<!-- Right: Actions Toolbar -->' +
          '<div class="flex items-center gap-2 flex-wrap">' +
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

            '<!-- Check Conflicts -->' +
            '<button class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-medium transition-colors shadow-xs cursor-pointer" data-act="conflicts" title="Audit Scheduling Conflicts">' +
              '<span class="material-symbols-outlined text-[16px] ' + (conflictsCount ? 'text-rose-600' : 'text-emerald-600') + '">rule</span>' +
              '<span>Conflicts</span>' +
              '<span class="px-1.5 py-0.5 rounded-full text-[10px] font-mono font-medium ' +
                (conflictsCount ? 'bg-rose-100 text-rose-700' : 'bg-emerald-100 text-emerald-800') + '">' +
                conflictsCount +
              '</span>' +
            '</button>' +

            '<!-- Auto-Schedule -->' +
            '<button id="btnAutoGenerate" class="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-slate-900 text-white hover:bg-slate-800 text-xs font-medium transition-all shadow-xs cursor-pointer" data-act="auto-assign" title="Auto-distribute unscheduled lessons">' +
              '<span class="material-symbols-outlined text-[16px]">bolt</span>' +
              '<span>Auto-Schedule</span>' +
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

    return '<div class="relative w-full overflow-hidden pb-12">' +
      '<div class="max-w-[1680px] w-full mx-auto px-3 sm:px-4 lg:px-6 space-y-4 pt-2 sm:pt-4">' +
        toolbarHtml +
        lessonStripHtml +
        innerView +
      '</div>' +
      moveBarHtml +
    '</div>';
  }
