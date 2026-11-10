/* ============================================================================
   Khmer School Admin Suite — state engine
   Derived counters, conflict engine, undo/redo history, optimistic autosave,
   greedy backtracking auto-assign, AI diff stub and export helpers.
   Publishes window.KSEngine.  Requires khmer-suite-data.js.
   ========================================================================== */
(function (global) {
  'use strict';

  var D = global.KSData;
  var API = '/api/timetable';
  var STORAGE_KEY = 'ngis_khmer_suite_state_v2';
  var UI_KEY = 'ngis_khmer_suite_ui_v2';

  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function sum(arr, fn) { return arr.reduce(function (a, b) { return a + fn(b); }, 0); }

  function index(state) {
    return {
      subjects: state.subjects.reduce(function (m, s) { m[s.id] = s; return m; }, {}),
      teachers: state.teachers.reduce(function (m, t) { m[t.id] = t; return m; }, {}),
      classes: state.classes.reduce(function (m, c) { m[c.id] = c; return m; }, {})
    };
  }

  function teacherLoad(state) {
    var load = {};
    state.teachers.forEach(function (t) { load[t.id] = 0; });
    Object.keys(state.grid).forEach(function (k) {
      var tid = state.grid[k] && state.grid[k].teacher_id;
      if (tid in load) load[tid]++;
    });
    return load;
  }

  function assignedCount(state, classId) {
    var counts = {};
    Object.keys(state.grid).forEach(function (k) {
      var c = state.grid[k];
      if (classId && c.class_id !== classId) return;
      var key = c.class_id + '|' + c.subject_id;
      counts[key] = (counts[key] || 0) + 1;
    });
    return counts;
  }

  function unassignedChips(state, classId) {
    var idx = index(state), placed = assignedCount(state, classId), chips = {};
    state.assignments.forEach(function (asg) {
      if (classId && asg.class_id !== classId) return;
      var key = asg.class_id + '|' + asg.subject_id;
      var remaining = asg.lessons - (placed[key] || 0);
      if (remaining <= 0) return;
      var subject = idx.subjects[asg.subject_id], teacher = idx.teachers[asg.teacher_id];
      if (!subject || !teacher) return;
      var ck = asg.class_id + '|' + asg.subject_id + '|' + asg.teacher_id;
      if (!chips[ck]) chips[ck] = {
        id: ck, class_id: asg.class_id, subject_id: asg.subject_id,
        teacher_id: asg.teacher_id, subject_name: subject.name_kh,
        subject_code: subject.code, color: subject.color,
        teacher_code: teacher.code, teacher_name: teacher.name_kh,
        shift: asg.shift || 'ព្រឹក', count: 0
      };
      chips[ck].count += remaining;
    });
    return Object.keys(chips).map(function (k) { return chips[k]; })
      .sort(function (a, b) { return b.count - a.count || a.subject_code.localeCompare(b.subject_code); });
  }

  function unassignedChipsForTeacher(state, teacherId) {
    var idx = index(state), placed = assignedCount(state), chips = {};
    state.assignments.forEach(function (asg) {
      if (teacherId && asg.teacher_id !== teacherId) return;
      var key = asg.class_id + '|' + asg.subject_id;
      var remaining = asg.lessons - (placed[key] || 0);
      if (remaining <= 0) return;
      var subject = idx.subjects[asg.subject_id], teacher = idx.teachers[asg.teacher_id];
      var cls = idx.classes[asg.class_id];
      if (!subject || !teacher) return;
      var ck = asg.class_id + '|' + asg.subject_id + '|' + asg.teacher_id;
      if (!chips[ck]) chips[ck] = {
        id: ck, class_id: asg.class_id, class_display: cls ? cls.display : asg.class_id,
        subject_id: asg.subject_id,
        teacher_id: asg.teacher_id, subject_name: subject.name_kh,
        subject_code: subject.code, color: subject.color,
        teacher_code: teacher.code, teacher_name: teacher.name_kh,
        shift: asg.shift || 'ព្រឹក', count: 0
      };
      chips[ck].count += remaining;
    });
    return Object.keys(chips).map(function (k) { return chips[k]; })
      .sort(function (a, b) { return b.count - a.count || (a.class_display || '').localeCompare(b.class_display || ''); });
  }

  function scanConflicts(state) {
    var idx = index(state), found = [], slots = {};
    Object.keys(state.grid).forEach(function (key) {
      var cell = state.grid[key], p = D.parseGridKey(key);
      var tk = (cell.teacher_id || '') + '|' + p.day + '|' + p.shift + '|' + p.period;
      if (cell.teacher_id && slots[tk]) {
        found.push({
          type: 'teacher_double_booked', severity: 'error', key: key,
          message_kh: 'គ្រូកំពុងបង្រៀនពីរថ្នាក់ក្នុងម៉ោងតែមួយ',
          message_en: 'Teacher double-booked in this period'
        });
      } else slots[tk] = key;
      var teacher = idx.teachers[cell.teacher_id];
      if (teacher && (teacher.shifts || D.SHIFTS).indexOf(p.shift) === -1) {
        found.push({
          type: 'shift_mismatch', severity: 'error', key: key,
          message_kh: 'គ្រូ ' + teacher.code + ' មិនមានវេន' + p.shift,
          message_en: 'Teacher ' + teacher.code + ' unavailable for ' + p.shift
        });
      }
    });
    var load = teacherLoad(state);
    state.teachers.forEach(function (t) {
      if (load[t.id] > t.target) found.push({
        type: 'workload_exceeded', severity: 'warning', teacher_id: t.id,
        message_kh: 'គ្រូ ' + t.code + ' លើសបន្ទុក (' + load[t.id] + '/' + t.target + ')',
        message_en: 'Teacher ' + t.code + ' overloaded'
      });
    });
    return found;
  }

  function validatePlacement(state, key, subjectId, teacherId, replace) {
    var idx = index(state), p = D.parseGridKey(key), conflicts = [];
    function add(type, severity, kh, en) {
      conflicts.push({ type: type, severity: severity, key: key, teacher_id: teacherId,
        class_id: p.class_id, message_kh: kh, message_en: en });
    }
    var existing = state.grid[key];
    if (existing && !replace) add('class_double_booked', 'error',
      'ថ្នាក់នេះមានមេរៀនរួចហើយក្នុងម៉ោងនេះ', 'This class already has a lesson in this period');
    var doubleBooked = false;
    Object.keys(state.grid).forEach(function (other) {
      if (other === key || doubleBooked) return;
      var cell = state.grid[other], q = D.parseGridKey(other);
      if (cell.teacher_id === teacherId && q.day === p.day && q.shift === p.shift && q.period === p.period) {
        doubleBooked = true;
      }
    });
    if (doubleBooked) add('teacher_double_booked', 'error',
      'គ្រូកំពុងបង្រៀនថ្នាក់ផ្សេងក្នុងម៉ោងនេះ', 'Teacher is already teaching another class this period');
    var teacher = idx.teachers[teacherId], subject = idx.subjects[subjectId];
    if (!teacher) { add('unknown_teacher', 'error', 'រកគ្រូមិនឃើញ', 'Teacher not found'); return conflicts; }
    if ((teacher.shifts || D.SHIFTS).indexOf(p.shift) === -1) add('shift_mismatch', 'error',
      'គ្រូ ' + teacher.code + ' មិនអាចបង្រៀនវេន' + p.shift + ' បានទេ',
      'Teacher ' + teacher.code + ' is not available for the ' + p.shift + ' shift');
    var load = teacherLoad(state);
    if (existing && existing.teacher_id === teacherId) load[teacherId] = Math.max(0, load[teacherId] - 1);
    if ((load[teacherId] || 0) + 1 > teacher.target) add('workload_exceeded', 'warning',
      'គ្រូ ' + teacher.code + ' លើស ' + teacher.target + ' ម៉ោង/សប្តាហ៍',
      'Teacher ' + teacher.code + ' exceeds weekly target');
    if (subject && subject.is_locked) add('subject_locked', 'warning',
      'មុខវិជ្ជា ' + subject.name_kh + ' ត្រូវបានចាក់សោ', 'Subject is locked');
    return conflicts;
  }

  function statistics(state) {
    var chips = unassignedChips(state), load = teacherLoad(state), idx = index(state);
    var totalDemand = sum(state.assignments, function (a) { return a.lessons; });
    var placed = Object.keys(state.grid).length;
    var perClass = state.classes.map(function (cls) {
      var assigned = 0;
      Object.keys(state.grid).forEach(function (k) { if (state.grid[k].class_id === cls.id) assigned++; });
      return {
        id: cls.id, display: cls.display, shift: cls.shift, capacity: cls.capacity,
        assigned: assigned,
        remaining: sum(chips.filter(function (c) { return c.class_id === cls.id; }), function (c) { return c.count; })
      };
    });
    var teachers = state.teachers.map(function (t) {
      var s = idx.subjects[t.subject_id] || {};
      return {
        id: t.id, code: t.code, name_kh: t.name_kh, subject_id: t.subject_id,
        subject_code: s.code || '', color: s.color || '#E5E7EB',
        target: t.target, assigned: load[t.id] || 0,
        remaining: Math.max(0, t.target - (load[t.id] || 0)),
        overloaded: (load[t.id] || 0) > t.target, shifts: t.shifts || D.SHIFTS.slice()
      };
    });
    return {
      total_demand: totalDemand, placed: placed,
      unassigned: sum(chips, function (c) { return c.count; }),
      conflicts: scanConflicts(state).filter(function (c) { return c.severity === 'error'; }).length,
      per_class: perClass, teachers: teachers, chips: chips
    };
  }

  function cellView(state, key, cell) {
    var idx = index(state);
    var s = idx.subjects[cell.subject_id] || {}, t = idx.teachers[cell.teacher_id] || {};
    var color = (s.color && s.color !== '#E5E7EB' && s.color !== '#e5e7eb' && s.color !== '#ffffff') ? s.color : ((D.getSubjectColor) ? D.getSubjectColor(cell.subject_id, s.name_kh || s.name_en) : '#FED766');
    return Object.assign({}, cell, {
      key: key, subject_name: s.name_kh || '', subject_code: s.code || '',
      short_name: s.short_name || '', color: color,
      teacher_code: t.code || '', teacher_name: t.name_kh || ''
    });
  }

  function gridView(state) {
    var out = {}, idx = index(state);
    Object.keys(state.grid).forEach(function (k) {
      var c = state.grid[k], s = idx.subjects[c.subject_id] || {}, t = idx.teachers[c.teacher_id] || {};
      var color = (s.color && s.color !== '#E5E7EB' && s.color !== '#e5e7eb' && s.color !== '#ffffff') ? s.color : ((D.getSubjectColor) ? D.getSubjectColor(c.subject_id, s.name_kh || s.name_en) : '#FED766');
      out[k] = Object.assign({}, c, {
        key: k, subject_name: s.name_kh || '', subject_code: s.code || '',
        short_name: s.short_name || '', color: color,
        teacher_code: t.code || '', teacher_name: t.name_kh || ''
      });
    });
    return out;
  }

  /* ── Auto-assign: greedy + bounded DFS backtracking ───────────────────── */

  function allCells(state, classId) {
    var days = state.settings.days, periods = state.settings.periods;
    var buckets = {};
    days.forEach(function (d) {
      buckets[d] = periods.map(function (p) { return D.gridKey(d, p.shift, p.number, classId); });
    });
    var ordered = [];
    for (var i = 0; i < periods.length; i++) {
      days.forEach(function (d) { ordered.push(buckets[d][i]); });
    }
    return ordered;
  }

  function mulberry32(seed) {
    return function () {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  function autoAssign(state, opts) {
    opts = opts || {};
    var working = clone(state);
    var beforeKeys = Object.keys(working.grid);
    var before = {}; beforeKeys.forEach(function (k) { before[k] = 1; });
    if (opts.clearFirst) {
      Object.keys(working.grid).forEach(function (k) {
        if (!opts.classId || D.parseGridKey(k).class_id === opts.classId) delete working.grid[k];
      });
    }
    var idx = index(working), load = teacherLoad(working), rnd = mulberry32(opts.seed || 7);
    var teacherBusy = {}, subjectDay = {}, classDay = {}, teacherDay = {};
    function inc(map, k) { map[k] = (map[k] || 0) + 1; }
    function dec(map, k) { map[k] = Math.max(0, (map[k] || 0) - 1); }
    Object.keys(working.grid).forEach(function (key) {
      var c = working.grid[key], p = D.parseGridKey(key);
      teacherBusy[[c.teacher_id, p.day, p.shift, p.period].join('|')] = 1;
      inc(subjectDay, [p.class_id, c.subject_id, p.day].join('|'));
      inc(classDay, [p.class_id, p.day].join('|'));
      inc(teacherDay, [c.teacher_id, p.day].join('|'));
    });

    var tasks = [], skipped = [];
    unassignedChips(working, opts.classId).forEach(function (chip) {
      var subject = idx.subjects[chip.subject_id] || {}, teacher = idx.teachers[chip.teacher_id] || {};
      if (subject.is_locked) { skipped.push({ reason: 'subject_locked', chip: chip.id, count: chip.count }); return; }
      for (var i = 0; i < chip.count; i++) tasks.push({
        class_id: chip.class_id, subject_id: chip.subject_id, teacher_id: chip.teacher_id,
        subject_code: chip.subject_code, teacher_code: chip.teacher_code,
        cells: allCells(working, chip.class_id),
        capacity: Math.max(0, (teacher.target || 17) - (load[chip.teacher_id] || 0))
      });
    });
    for (var a = tasks.length - 1; a > 0; a--) {
      var b = Math.floor(rnd() * (a + 1)), tmp = tasks[a]; tasks[a] = tasks[b]; tasks[b] = tmp;
    }
    tasks.sort(function (x, y) {
      return x.capacity - y.capacity ||
        String(x.class_id).localeCompare(String(y.class_id)) ||
        String(x.subject_code).localeCompare(String(y.subject_code));
    });
    var total = tasks.length, nodes = 0, backtracks = 0, maxNodes = 60000;

    function rank(task) {
      var teacher = idx.teachers[task.teacher_id], options = [];
      task.cells.forEach(function (key) {
        if (working.grid[key]) return;
        var p = D.parseGridKey(key);
        if ((teacher.shifts || D.SHIFTS).indexOf(p.shift) === -1) return;
        if (teacherBusy[[task.teacher_id, p.day, p.shift, p.period].join('|')]) return;
        var score = (subjectDay[[task.class_id, task.subject_id, p.day].join('|')] || 0) * 10
          + (classDay[[task.class_id, p.day].join('|')] || 0) * 0.5
          + (teacherDay[[task.teacher_id, p.day].join('|')] || 0) * 0.3
          + (p.shift === 'ព្រឹក' ? 0 : 0.15) + rnd() * 0.2;
        options.push([score, key]);
      });
      options.sort(function (x, y) { return x[0] - y[0]; });
      return options.slice(0, 28).map(function (o) { return o[1]; });
    }

    function place(task, key) {
      var p = D.parseGridKey(key);
      working.grid[key] = {
        class_id: task.class_id, subject_id: task.subject_id, teacher_id: task.teacher_id,
        day: p.day, shift: p.shift, period: p.period
      };
      load[task.teacher_id] = (load[task.teacher_id] || 0) + 1;
      teacherBusy[[task.teacher_id, p.day, p.shift, p.period].join('|')] = 1;
      inc(subjectDay, [task.class_id, task.subject_id, p.day].join('|'));
      inc(classDay, [task.class_id, p.day].join('|'));
      inc(teacherDay, [task.teacher_id, p.day].join('|'));
    }
    function unplace(task, key) {
      var p = D.parseGridKey(key);
      delete working.grid[key];
      load[task.teacher_id] = Math.max(0, (load[task.teacher_id] || 0) - 1);
      delete teacherBusy[[task.teacher_id, p.day, p.shift, p.period].join('|')];
      dec(subjectDay, [task.class_id, task.subject_id, p.day].join('|'));
      dec(classDay, [task.class_id, p.day].join('|'));
      dec(teacherDay, [task.teacher_id, p.day].join('|'));
    }
    function solve(i) {
      if (i >= total) return true;
      if (++nodes > maxNodes) return false;
      var task = tasks[i], teacher = idx.teachers[task.teacher_id];
      if (!teacher || (load[task.teacher_id] || 0) >= teacher.target) return solve(i + 1);
      var cells = rank(task);
      for (var j = 0; j < cells.length; j++) {
        place(task, cells[j]);
        if (solve(i + 1)) return true;
        unplace(task, cells[j]);
        backtracks++;
        if (nodes > maxNodes) return false;
      }
      skipped.push({ reason: 'no_free_cell', teacher_id: task.teacher_id,
        class_id: task.class_id, subject_id: task.subject_id });
      return solve(i + 1);
    }
    solve(0);

    var after = {}, added = [], removed = [];
    Object.keys(working.grid).forEach(function (k) { after[k] = 1; if (!before[k]) added.push(k); });
    beforeKeys.forEach(function (k) { if (!after[k]) removed.push(k); });
    return {
      state: working, placed: added.length, requested: total,
      skipped: skipped.slice(0, 50), backtracks: backtracks, nodes: nodes,
      diff: { added: added, removed: removed, unchanged: beforeKeys.length - removed.length },
      stats: statistics(working)
    };
  }

  function candidates(state, opts) {
    opts = opts || {};
    var parts = opts.key && opts.key.split('|').length === 4 ? D.parseGridKey(opts.key) : {};
    var q = (opts.q || '').trim().toLowerCase(), load = teacherLoad(state), idx = index(state);
    var list = state.teachers.filter(function (t) {
      if (opts.subjectId && t.subject_id !== opts.subjectId) return false;
      if (q && (t.code + ' ' + t.name_kh + ' ' + t.subject_id).toLowerCase().indexOf(q) === -1) return false;
      return true;
    }).map(function (t) {
      var used = load[t.id] || 0, target = t.target;
      var shiftOk = !parts.shift || (t.shifts || D.SHIFTS).indexOf(parts.shift) !== -1;
      var busy = false;
      Object.keys(state.grid).forEach(function (k) {
        if (busy || k === opts.key) return;
        var c = state.grid[k], p = D.parseGridKey(k);
        if (c.teacher_id === t.id && p.day === parts.day && p.shift === parts.shift && p.period === parts.period) busy = true;
      });
      var s = idx.subjects[t.subject_id] || {};
      return {
        id: t.id, code: t.code, name_kh: t.name_kh, subject_id: t.subject_id,
        subject_code: s.code || '', color: s.color || '#E5E7EB',
        assigned: used, target: target, remaining: Math.max(0, target - used),
        shifts: t.shifts || D.SHIFTS.slice(), shift_ok: shiftOk, busy: busy,
        available: !busy && shiftOk && used < target,
        status_kh: busy ? 'កំពុងគូររៀង' : (used < target ? 'សេរី' : 'ពេញបន្ទុក'),
        score: (busy ? 100 : 0) + (shiftOk ? 0 : 60) - Math.max(0, target - used) + (used >= target ? 80 : 0)
      };
    });
    return list.sort(function (a, b) { return a.score - b.score || a.code.localeCompare(b.code); });
  }

  /* ── Engine object ────────────────────────────────────────────────────── */

  var listeners = [];
  var state = null;
  var undoStack = [], redoStack = [], changeLog = [];
  var saveTimer = null, saveStatus = 'saved', online = false;
  var uiState = loadUI();

  function loadUI() {
    try { return JSON.parse(localStorage.getItem(UI_KEY) || '{}') || {}; } catch (e) { return {}; }
  }
  function saveUI(patch) {
    Object.assign(uiState, patch);
    try { localStorage.setItem(UI_KEY, JSON.stringify(uiState)); } catch (e) {}
  }
  var hasLocal = false;
  function loadLocal() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        var s = JSON.parse(raw);
        if (s && s.grid && s.subjects && (s.schema_version >= 2 && s.schema_version <= 4)) {
          hasLocal = true;
          return s;
        }
      }
    } catch (e) {}
    hasLocal = false;
    return D.buildSeedState();
  }
  function persistLocal() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      hasLocal = true;
    } catch (e) {}
  }

  function emit(reason) {
    var payload = {
      state: state, stats: statistics(state), grid: gridView(state),
      history: changeLog.slice().reverse(), undo: undoStack.length,
      redo: redoStack.length, saveStatus: saveStatus, online: online, reason: reason
    };
    listeners.forEach(function (fn) { try { fn(payload); } catch (e) { console.error(e); } });
  }

  function setSaveStatus(s) {
    saveStatus = s;
    emit('save');
  }

  function flushSave() {
    if (saveTimer) { clearTimeout(saveTimer); saveTimer = null; }
    if (typeof navigator !== 'undefined' && navigator.onLine === false) {
      online = false;
      setSaveStatus('offline');
      return Promise.resolve(false);
    }
    online = true;
    setSaveStatus('saving');
    return fetch(API + '/state', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ state: state, label: 'រក្សាទុកដោយស្វ័យប្រវត្តិ' }),
      keepalive: true
    }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (data) {
        if (data && data.revision) state.revision = data.revision;
        setSaveStatus('saved');
        return true;
      }).catch(function () {
        if (typeof navigator !== 'undefined' && navigator.onLine === false) {
          online = false;
          setSaveStatus('offline');
        } else {
          setSaveStatus('dirty');
        }
        return false;
      });
  }

  function scheduleSave() {
    persistLocal();
    setSaveStatus('dirty');
    if (saveTimer) clearTimeout(saveTimer);
    saveTimer = setTimeout(flushSave, 180);
  }

  function commit(label, mutator, options) {
    options = options || {};
    var snapshot = clone(state);
    undoStack.push(snapshot);
    if (undoStack.length > 80) undoStack.shift();
    redoStack = [];
    mutator(state);
    state.revision = (state.revision || 0) + 1;
    state.updated_at = D.nowISO();
    changeLog.push({
      id: 'h' + (changeLog.length + 1), at: D.nowISO(), label: label,
      undoIndex: undoStack.length - 1
    });
    if (changeLog.length > 100) changeLog.shift();
    persistLocal();
    emit(options.reason || 'change');
    if (!options.skipSave) scheduleSave();
    return statistics(state);
  }

  function undo() {
    if (!undoStack.length) return false;
    redoStack.push(clone(state));
    state = undoStack.pop();
    changeLog.push({ id: 'u' + changeLog.length, at: D.nowISO(), label: 'ត្រឡប់ (Undo)' });
    persistLocal(); emit('undo'); scheduleSave();
    return true;
  }
  function redo() {
    if (!redoStack.length) return false;
    undoStack.push(clone(state));
    state = redoStack.pop();
    changeLog.push({ id: 'r' + changeLog.length, at: D.nowISO(), label: 'ធ្វើឡើងវិញ (Redo)' });
    persistLocal(); emit('redo'); scheduleSave();
    return true;
  }
  function restore(snapshotIndex) {
    var snap = undoStack[snapshotIndex];
    if (!snap) return false;
    redoStack.push(clone(state));
    state = clone(snap);
    undoStack.splice(snapshotIndex);
    persistLocal(); emit('restore'); scheduleSave();
    return true;
  }

  function init() {
    state = loadLocal();
    emit('init');
    return fetch(API + '/state', { headers: { 'Accept': 'application/json' } })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (data) {
        online = true;
        if (data && data.state && data.state.grid && (data.state.schema_version >= 2 && data.state.schema_version <= 4)) {
          var serverState = data.state;
          if (!hasLocal) {
            // No prior local storage in this browser session: adopt authoritative server state directly
            state = serverState;
            hasLocal = true;
            persistLocal();
          } else {
            var localRev = (state && typeof state.revision === 'number') ? state.revision : 0;
            var serverRev = (serverState && typeof serverState.revision === 'number') ? serverState.revision : 0;
            
            var localTime = (state && state.updated_at) ? new Date(state.updated_at).getTime() : 0;
            var serverTime = (serverState && serverState.updated_at) ? new Date(serverState.updated_at).getTime() : 0;

            // If local state has newer revision, newer timestamp, or pending unsaved edits, keep local and flush to server
            if (localRev > serverRev || (localRev === serverRev && localTime > serverTime) || saveStatus === 'dirty') {
              flushSave();
            } else {
              state = serverState;
              persistLocal();
            }
          }
        }
        setSaveStatus('saved');
        emit('sync');
        return true;
      })
      .catch(function () {
        online = false; setSaveStatus('offline'); emit('offline');
        return false;
      });
  }

  function api(path, options) {
    return fetch(API + path, Object.assign({ headers: { 'Content-Type': 'application/json' } }, options))
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }); });
  }

  /* ── Export sheet builders (offline fallback + print) ─────────────────── */

  function buildExportSheets(type, classId) {
    var days = state.settings.days, periods = state.settings.periods, gv = gridView(state);
    var title = state.institution.name_kh + ' · ' + state.institution.academic_year;
    var sheets = [];
    var classes = state.classes.filter(function (c) { return !classId || c.id === classId; });
    if (!classes.length) classes = state.classes;

    function headerCell(v) { return { v: v, fill: '#274C77', bold: true, color: 'FFFFFFFF' }; }
    function titleRow(v, span) { return [{ v: v, span: span, fill: '#1E3A5F', bold: true, color: 'FFFFFFFF', size: 15 }]; }
    function subRow(v, span) { return [{ v: v, span: span, fill: '#EAF0F7', align: 'left', color: 'FF334155' }]; }

    if (type === 'timetable' || type === 'all') {
      classes.forEach(function (cls) {
        var rows = [
          titleRow('តារាងម៉ោងថ្នាក់ ' + cls.display + ' · វេន' + cls.shift + ' · ' + cls.days + 'ថ្ងៃ', days.length + 1),
          subRow(title, days.length + 1),
          ['ម៉ោង / ថ្ងៃ'].concat(days).map(headerCell)
        ];
        periods.forEach(function (p) {
          var row = [{ v: p.shift + ' ' + p.number + '  (' + p.start + '–' + p.end + ')', fill: '#F7F9F7' }];
          days.forEach(function (day) {
            var key = D.gridKey(day, p.shift, p.number, cls.id), c = gv[key];
            row.push(c ? { v: c.short_name + ' ' + c.teacher_code, fill: c.color } : { v: '— សេរី —' });
          });
          rows.push(row);
        });
        sheets.push({ name: cls.display, cols: [16].concat(days.map(function () { return 17; })), freeze: 3, rows: rows, landscape: false, rowHeights: [32, 22, 30] });
      });
    }
    if (type === 'master' || type === 'all') {
      var header = ['ថ្នាក់'];
      days.forEach(function (d) { periods.forEach(function (p) { header.push(d + ' · ' + p.shift + ' ' + p.number); }); });
      var mrows = [
        titleRow('ម៉ាទ្រីសកាលវិភាគគ្រប់ថ្នាក់', header.length),
        subRow(state.institution.academic_year + ' · សរុប ' + D.kh(Object.keys(state.grid).length) + ' ម៉ោង', header.length),
        header.map(headerCell)
      ];
      state.classes.forEach(function (cls) {
        var row = [{ v: cls.display, fill: '#F7F9F7', bold: true }];
        days.forEach(function (d) {
          periods.forEach(function (p) {
            var c = gv[D.gridKey(d, p.shift, p.number, cls.id)];
            row.push(c ? { v: c.teacher_code + ' ' + c.short_name, fill: c.color } : { v: '' });
          });
        });
        mrows.push(row);
      });
      sheets.push({ name: 'ម៉ាទ្រីសគ្រប់ថ្នាក់', cols: [11].concat(header.slice(1).map(function () { return 13; })), freeze: 3, rows: mrows, landscape: true, paper: 'A3', rowHeights: [32, 22, 30] });
    }
    if (type === 'records' || type === 'all') {
      var cols = D.RECORD_COLUMNS.concat([{ key: 'type', kh: 'ប្រភេទ', en: 'Type' }]);
      var rrows = [
        titleRow('បញ្ជីព័ត៌មានគ្រូបង្រៀន / សិស្ស', cols.length),
        subRow(title, cols.length),
        cols.map(function (c) { return headerCell(c.kh); })
      ];
      state.records.forEach(function (r) {
        rrows.push(cols.map(function (c) { return { v: r[c.key] == null ? '' : r[c.key] }; }));
      });
      sheets.push({ name: 'ព័ត៌មាន', cols: [7, 26, 8, 20, 8, 12, 20, 24, 14, 14, 20, 24, 16], freeze: 3, rows: rrows, landscape: true, paper: 'A3', rowHeights: [32, 22, 30] });
    }
    if (type === 'subjects' || type === 'all') {
      var sh = ['ល.រ', 'ឈ្មោះមុខវិជ្ជា', 'ឈ្មោះខ្លី', 'កូដ', 'ពណ៌', 'ចំនួន/សប្តាហ៍', 'ចាក់សោ'];
      var srows = [titleRow('បញ្ជីមុខវិជ្ជា', sh.length), subRow('មុខវិជ្ជាដែលចាក់សោ មិនត្រូវបានដាក់ដោយស្វ័យប្រវត្តិទេ', sh.length), sh.map(headerCell)];
      state.subjects.forEach(function (s, i) {
        srows.push([{ v: i + 1 }, { v: s.name_kh }, { v: s.short_name }, { v: s.code },
          { v: s.color, fill: s.color }, { v: s.lessons_per_week }, { v: s.is_locked ? 'បាទ/ចាស' : 'ទេ' }]);
      });
      sheets.push({ name: 'មុខវិជ្ជា', cols: [7, 26, 18, 10, 14, 18, 14], freeze: 3, rows: srows, rowHeights: [32, 22, 30] });
    }
    if (type === 'teachers' || type === 'all') {
      var th = ['ល.រ', 'កូដ', 'គោត្តនាម-នាម', 'មុខវិជ្ជា', 'គោលដៅ', 'បានដាក់', 'វេន'];
      var trows = [titleRow('បញ្ជីគ្រូបង្រៀង និងបន្ទុកម៉ោង', th.length), subRow('បន្ទុក / គោលដៅ ម៉ោងក្នុងមួយសប្តាហ៍', th.length), th.map(headerCell)];
      var st = statistics(state), ix = index(state);
      st.teachers.forEach(function (t, i) {
        trows.push([{ v: i + 1 }, { v: t.code }, { v: t.name_kh },
          { v: (ix.subjects[t.subject_id] || {}).name_kh || '', fill: t.color },
          { v: t.target }, { v: t.assigned, fill: t.overloaded ? '#FCA5A5' : null },
          { v: t.shifts.join(' · ') }]);
      });
      sheets.push({ name: 'គ្រូបង្រៀង', cols: [7, 12, 26, 14, 18, 16, 18], freeze: 3, rows: trows, rowHeights: [32, 22, 30] });
    }
    if (type === 'unassigned') {
      var uh = ['ថ្នាក់', 'មុខវិជ្ជា', 'កូដគ្រូ', 'ឈ្មោះគ្រូ', 'ចំនួន'];
      var urows = [titleRow('មេរៀនដែលមិនទាន់តម្រៀប', uh.length), uh.map(headerCell)];
      var cmap = {}; state.classes.forEach(function (c) { cmap[c.id] = c.display; });
      unassignedChips(state, classId).forEach(function (c) {
        urows.push([{ v: cmap[c.class_id] || c.class_id }, { v: c.subject_name, fill: c.color },
          { v: c.teacher_code }, { v: c.teacher_name }, { v: c.count }]);
      });
      sheets.push({ name: 'មិនទាន់តម្រៀប', cols: [12, 22, 14, 22, 16], freeze: 2, rows: urows, rowHeights: [32, 30] });
    }
    return sheets;
  }

  function exportXlsx(type, classId) {
    type = type || 'all';
    var sheets = buildExportSheets(type, classId);
    var filename = 'ការគ្រប់គ្រងសាលា_' + type + '_' + new Date().toISOString().slice(0, 10).replace(/-/g, '') + '.xlsx';
    if (online) {
      return flushSave().then(function () {
        var qs = '?type=' + encodeURIComponent(type) + (classId ? '&class_id=' + encodeURIComponent(classId) : '');
        window.location.href = API + '/export' + qs;
        return true;
      });
    }
    D.downloadXlsx(filename, sheets);
    return Promise.resolve(true);
  }

  function aiGenerate(constraints) {
    constraints = constraints || {};
    if (online) {
      return api('/generate', {
        method: 'POST',
        body: JSON.stringify({
          preview: true,
          constraints: {
            workload: constraints.workload || 17,
            shifts: constraints.shifts || D.SHIFTS,
            locked_subjects: state.subjects.filter(function (s) { return s.is_locked; }).map(function (s) { return s.id; })
          }
        })
      }).then(function (res) {
        if (!res.ok || !res.data.success) throw new Error('api');
        return {
          token: res.data.token, placed: res.data.placed, requested: res.data.requested,
          diff: res.data.diff, stats: res.data.stats, conflicts: res.data.conflicts,
          proposed_grid: res.data.proposed_grid, summary_kh: res.data.summary_kh,
          local: false
        };
      }).catch(function () {
        var r = autoAssign(state, { seed: Date.now() % 100000 });
        return {
          token: null, placed: r.placed, requested: r.requested, diff: r.diff,
          stats: r.stats, proposed_state: r.state, local: true,
          summary_kh: 'AI ស្នើដាក់ ' + D.kh(r.placed) + ' ម៉ោង · នៅសល់ ' + D.kh(r.stats.unassigned) + ' ម៉ោង'
        };
      });
    }
    var r = autoAssign(state, { seed: Date.now() % 100000 });
    return Promise.resolve({
      token: null, placed: r.placed, requested: r.requested, diff: r.diff,
      stats: r.stats, proposed_state: r.state, local: true,
      summary_kh: 'AI ស្នើដាក់ ' + D.kh(r.placed) + ' ម៉ោង · នៅសល់ ' + D.kh(r.stats.unassigned) + ' ម៉ោង'
    });
  }

  function applyProposal(proposal) {
    if (proposal.token && online) {
      return api('/generate/apply', { method: 'POST', body: JSON.stringify({ token: proposal.token }) })
        .then(function (res) {
          if (!res.ok || !res.data.success) throw new Error('api');
          commit('អនុម័តសំណើ AI', function (s) {
            s.grid = res.data.state.grid; s.subjects = res.data.state.subjects;
            s.teachers = res.data.state.teachers;
          });
          return true;
        }).catch(function () {
          if (!proposal.proposed_state) return false;
          commit('អនុម័តសំណើ AI', function (s) { s.grid = proposal.proposed_state.grid; });
          return true;
        });
    }
    if (!proposal.proposed_state) return Promise.resolve(false);
    commit('អនុម័តសំណើ AI', function (s) { s.grid = proposal.proposed_state.grid; });
    return Promise.resolve(true);
  }

  global.KSEngine = {
    init: init, on: function (fn) { listeners.push(fn); return function () { listeners = listeners.filter(function (f) { return f !== fn; }); }; },
    get: function () { return state; },
    state: function () { return state; },
    stats: function () { return statistics(state); },
    statistics: function () { return statistics(state); },
    grid: function (s) { return gridView(s || state); },
    gridView: function (s) { return gridView(s || state); },
    ui: uiState, setUI: saveUI,
    chips: function (classId) { return unassignedChips(state, classId); },
    chipsForTeacher: function (teacherId) { return unassignedChipsForTeacher(state, teacherId); },
    unassignedChipsForTeacher: function (teacherId) { return unassignedChipsForTeacher(state, teacherId); },
    teacherLoad: function () { return teacherLoad(state); },
    index: function () { return index(state); },
    conflicts: function () { return scanConflicts(state); },
    validate: function (key, sid, tid, replace) { return validatePlacement(state, key, sid, tid, replace); },
    cellView: function (key, cell) { return cellView(state, key, cell); },
    candidates: function (o) { return candidates(state, o); },
    emit: emit, commit: commit, undo: undo, redo: redo, restore: restore,
    undoDepth: function () { return undoStack.length; },
    redoDepth: function () { return redoStack.length; },
    changeLog: function () { return changeLog.slice().reverse(); },
    saveStatus: function () { return saveStatus; },
    isOnline: function () { return online; },
    flushSave: flushSave, scheduleSave: scheduleSave,
    autoAssignResult: function (o) { return autoAssign(state, o); },
    autoAssign: function (o) {
      var result = autoAssign(state, o);
      commit('បង្កើតកាលវិភាគដោយស្វ័យប្រវត្តិ', function (s) { s.grid = result.state.grid; });
      return result;
    },
    setCell: function (key, cell, opts) {
      var conflicts = validatePlacement(state, key, cell.subject_id, cell.teacher_id, opts && opts.replace);
      var errors = conflicts.filter(function (c) { return c.severity === 'error'; });
      if (errors.length && !(opts && opts.force)) return { ok: false, conflicts: conflicts };
      var p = D.parseGridKey(key);
      var full = {
        class_id: p.class_id, subject_id: cell.subject_id, teacher_id: cell.teacher_id,
        day: p.day, shift: p.shift, period: p.period
      };
      commit(opts && opts.label || 'កំណត់ម៉ោង', function (s) { s.grid[key] = full; });
      return { ok: true, conflicts: conflicts };
    },
    clearCell: function (key) {
      if (!state.grid[key]) return false;
      commit('លុបម៉ោង', function (s) { delete s.grid[key]; });
      return true;
    },
    reassign: function (classId, subjectId, newTeacherId, oldTeacherId) {
      var idx = index(state);
      var newTeacher = idx.teachers[newTeacherId];
      if (!newTeacher) return { ok: false, error: 'Teacher not found' };

      var preserved = [], displaced = [], details = [];

      commit('ប្តូរគ្រូបង្រៀន ' + classId, function (s) {
        var asgFound = false;
        s.assignments.forEach(function (a) {
          if (a.class_id === classId && a.subject_id === subjectId) {
            if (!oldTeacherId || a.teacher_id === oldTeacherId) {
              a.teacher_id = newTeacherId;
              asgFound = true;
            }
          }
        });
        if (!asgFound) {
          var sub = idx.subjects[subjectId];
          s.assignments.push({
            id: 'asg_' + classId + '_' + subjectId + '_' + newTeacherId,
            class_id: classId, subject_id: subjectId, teacher_id: newTeacherId,
            lessons: sub ? sub.lessons_per_week : 2, shift: 'ព្រឹក'
          });
        }

        var keys = Object.keys(s.grid);
        keys.forEach(function (key) {
          var cell = s.grid[key];
          if (cell && cell.class_id === classId && cell.subject_id === subjectId) {
            if (oldTeacherId && cell.teacher_id !== oldTeacherId) return;

            var p = D.parseGridKey(key);
            var isBusy = false;
            keys.forEach(function (ok) {
              if (ok !== key && s.grid[ok] && s.grid[ok].teacher_id === newTeacherId) {
                var op = D.parseGridKey(ok);
                if (op.day === p.day && op.shift === p.shift && op.period === p.period) isBusy = true;
              }
            });

            var shiftOk = (newTeacher.shifts || D.SHIFTS).indexOf(p.shift) !== -1;
            var unavail = newTeacher.unavailable_slots || [];
            var isUnavail = unavail.indexOf(key) !== -1 || unavail.indexOf(p.day + '|' + p.shift + '|' + p.period) !== -1;

            if (!isBusy && shiftOk && !isUnavail) {
              cell.teacher_id = newTeacherId;
              preserved.push(key);
              details.push({ key: key, status: 'preserved', day: p.day, period: p.period });
            } else {
              delete s.grid[key];
              displaced.push(key);
              details.push({ key: key, status: 'displaced', day: p.day, period: p.period });
            }
          }
        });
      });

      if (online) {
        api('/reassign', {
          method: 'POST',
          body: JSON.stringify({
            class_id: classId, subject_id: subjectId,
            new_teacher_id: newTeacherId, old_teacher_id: oldTeacherId
          })
        }).catch(function (e) { console.warn('Offline reassign sync deferred', e); });
      }

      return { ok: true, preserved: preserved.length, displaced: displaced.length, details: details };
    },
    publish: function (publishedBy, note) {
      var errors = scanConflicts(state).filter(function (c) { return c.severity === 'error'; });
      if (errors.length) return Promise.reject({ message: 'មានជម្លោះកាលវិភាគ ' + errors.length + ' ករណី', conflicts: errors });

      return api('/publish', {
        method: 'POST',
        body: JSON.stringify({ published_by: publishedBy || 'Admin', note: note || '' })
      }).then(function (res) {
        if (res && res.published) {
          commit('បោះពុម្ពផ្សាយកាលវិភាគ v' + res.published.version, function (s) {
            s.published = res.published;
          });
        }
        return res;
      });
    },
    bulkImportTeachers: function (rows) {
      return api('/teachers/bulk-import', {
        method: 'POST',
        body: JSON.stringify({ teachers: rows })
      }).then(function (res) {
        if (res && res.state) {
          commit('បញ្ចូលទិន្នន័យគ្រូ', function (s) {
            s.teachers = res.state.teachers;
          });
        }
        return res;
      });
    },
    buildExportSheets: buildExportSheets, exportXlsx: exportXlsx,
    aiGenerate: aiGenerate, applyProposal: applyProposal, api: api,
    statistics: statistics, scanConflicts: scanConflicts,
    unassignedChips: unassignedChips, validatePlacement: validatePlacement,
    reset: function () {
      commit('កំណត់ឡើងវិញ', function () {}, { skipSave: false });
      state = D.buildSeedState();
      persistLocal(); emit('reset'); scheduleSave();
    }
  };

  if (typeof window !== 'undefined' && typeof window.addEventListener === 'function') {
    window.addEventListener('beforeunload', function () {
      if (saveTimer || saveStatus === 'dirty') flushSave();
    });
    window.addEventListener('pagehide', function () {
      if (saveTimer || saveStatus === 'dirty') flushSave();
    });
    window.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'hidden' && (saveTimer || saveStatus === 'dirty')) {
        flushSave();
      }
    });
    window.addEventListener('storage', function (e) {
      if (e.key === STORAGE_KEY && e.newValue) {
        try {
          var remote = JSON.parse(e.newValue);
          if (remote && remote.grid && (remote.schema_version >= 2 && remote.schema_version <= 4)) {
            var currRev = (state && state.revision) || 0;
            var newRev = remote.revision || 0;
            if (newRev >= currRev) {
              state = remote;
              emit('storage-sync');
            }
          }
        } catch (err) {}
      }
    });
  }
})(window);
