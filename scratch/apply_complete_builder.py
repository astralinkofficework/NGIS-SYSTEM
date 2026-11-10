import re

with open(r"assets/js/khmer-suite-ui.js", "r", encoding="utf-8") as f:
    text = f.read()

with open(r"scratch/builder_chunk.js", "r", encoding="utf-8") as f:
    builder_chunk = f.read()

with open(r"scratch/views_chunk.js", "r", encoding="utf-8") as f:
    views_chunk = f.read()

# 1. Replace the entire builder chunk (from STEP 3 to MODULE 4 & 5)
idx_start = text.find('/* ==========================================================================\n     STEP 3 — Modern Timetable Builder & Period Distribution')
idx_subjects = text.find('/* ==========================================================================\n     MODULE 4 & 5 — Subjects & Overview')

assert idx_start != -1 and idx_subjects != -1, "Cannot find builder boundaries"

new_builder_code = builder_chunk + "\n\n" + views_chunk + "\n\n  "

text_part1 = text[:idx_start]
text_part2 = text[idx_subjects:]

text = text_part1 + new_builder_code + text_part2

# 2. Add quick-editor modal to modalHtml()
modal_target = "function modalHtml() {\n    if (!local.modal) return '';\n    var m = local.modal;"

quick_editor_modal_code = r'''function modalHtml() {
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
    }'''

assert modal_target in text, "Cannot find modalHtml target"
text = text.replace(modal_target, quick_editor_modal_code, 1)

# 3. Update onClick handlers for builder actions
onclick_target = "case 'set-view-mode':"
idx_click_start = text.find(onclick_target)
idx_click_end = text.find("case 'subject-add':")

new_onclick_code = r'''case 'set-view-mode':
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

        // 2. If a placed lesson was already selected, and user clicks another cell: MOVE OR SWAP!
        if (local.targetKey && local.targetKey !== key && ctx.grid[local.targetKey]) {
          moveOrSwapLesson(local.targetKey, key);
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
      '''

assert idx_click_start != -1 and idx_click_end != -1, "Cannot find onClick boundaries"
text = text[:idx_click_start] + new_onclick_code + text[idx_click_end:]

# 4. Update onChange for builder-class-select and builder-teacher-select
change_target = "if (kind === 'class-select' || kind === 'wizard-class-select') {"
new_change_code = "if (kind === 'class-select' || kind === 'wizard-class-select' || kind === 'builder-class-select') {"
text = text.replace(change_target, new_change_code, 1)

with open(r"assets/js/khmer-suite-ui.js", "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully replaced and updated assets/js/khmer-suite-ui.js")
print("New file length:", len(text))

