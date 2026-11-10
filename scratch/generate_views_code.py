import sys

code_views = r'''  function classMasterModernHtml(curClass, classDisplay, homeroomTeacher, roomInfo, classPlaced, classCapacity) {
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
        '<!-- Class Identity Header Banner -->' +
        '<div class="bg-white p-3.5 sm:p-4 rounded-2xl border border-slate-200/80 shadow-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">' +
          '<div class="flex items-center gap-3 min-w-0">' +
            '<div class="w-11 h-11 rounded-xl bg-[#006C49] text-white flex items-center justify-center font-medium text-base sm:text-lg shrink-0 shadow-xs">' +
              esc(classDisplay) +
            '</div>' +
            '<div class="min-w-0">' +
              '<div class="flex flex-wrap items-center gap-2">' +
                '<h3 class="text-sm sm:text-base md:text-lg text-slate-900 font-medium truncate">' +
                  'Class ' + esc(classDisplay) + ' Timetable' +
                '</h3>' +
                '<span class="px-2 py-0.5 rounded text-[11px] bg-slate-100 text-slate-700 font-medium shrink-0">' +
                  'Homeroom: ' + esc(homeroomTeacher) +
                '</span>' +
              '</div>' +
              '<p class="text-xs text-slate-500 truncate mt-0.5">' +
                esc(roomInfo) + ' · Scheduled: ' + classPlaced + ' / ' + classCapacity + ' Periods · ' +
                (E.conflicts().length ? '<span class="text-rose-600 font-medium">' + E.conflicts().length + ' Conflicts</span>' : '<span class="text-emerald-700 font-medium">Zero Conflicts</span>') +
              '</p>' +
            '</div>' +
          '</div>' +
          '<div class="flex items-center gap-2 w-full sm:w-auto shrink-0 justify-end">' +
            '<button class="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-medium transition-colors cursor-pointer" data-act="fill-class" data-id="' + esc(curClass.id) + '">' +
              '<span class="material-symbols-outlined text-[16px]">auto_fix_high</span>' +
              '<span>Auto-Schedule Class</span>' +
            '</button>' +
          '</div>' +
        '</div>' +

        '<!-- Timetable Matrix Grid -->' +
        '<div class="ks-timetable-container bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden">' +
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
        '<div class="ks-timetable-container bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden">' +
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
'''

with open('scratch/views_chunk.js', 'w', encoding='utf-8') as f:
    f.write(code_views)
print('Successfully generated views_chunk.js')

