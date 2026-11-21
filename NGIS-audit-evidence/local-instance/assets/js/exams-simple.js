/* NGIS Simplified Examination Scheduling Workspace
   One renderer, four portals. All data comes from /api/exams* endpoints. */
(function (window, document) {
  'use strict';

  var root = document.getElementById('examsWorkspace');
  if (!root) return;

  var ROLE = ((window.PAGE && window.PAGE.role) || document.body.getAttribute('data-role') || 'student').toLowerCase();
  if (ROLE === 'editor') ROLE = 'admin';
  if (ROLE === 'super_admin') ROLE = 'superadmin';

  // Department hubs link here with ?dept=<slug>. When present, the calendar is
  // scoped to that department only — it never falls back to other departments.
  var urlParams = new URLSearchParams(window.location.search);
  var deptContext = (urlParams.get('dept') || urlParams.get('subject') || '').trim().toLowerCase();
  var deptLabels = {
    english: 'English Literature', math: 'Mathematics', maths: 'Mathematics',
    science: 'Science', physics: 'Physics', khmer: 'Khmer Literature',
    chinese: 'Chinese Language', history: 'World History', art: 'Fine Arts', ict: 'ICT'
  };
  var deptLabel = deptLabels[deptContext] ||
    (deptContext ? deptContext.charAt(0).toUpperCase() + deptContext.slice(1) : '');

  var state = {
    exams: [],
    stats: {},
    options: null,
    months: [],
    tab: ROLE === 'student' ? 'upcoming' : 'pending',
    type: 'all',
    month: 'all',
    q: '',
    status: 'all',
    campus: 'all',
    dept: 'all',
    classId: 'all',
    editing: null,
    modalMode: ''
  };

  var scrim = null;
  var modal = null;
  var lastFocus = null;
  var toastTimer = null;

  function esc(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function actorHeader() {
    try {
      if (localStorage.getItem('ngis_session_mode') === 'passive') return '';
      var raw = localStorage.getItem('ngis_user') || localStorage.getItem('auth_user') || '';
      var user = raw ? JSON.parse(raw) : null;
      var value = user && (user.email || user.username);
      return value ? String(value).trim().toLowerCase() : '';
    } catch (e) { return ''; }
  }

  async function api(path, options) {
    var opts = options || {};
    var headers = { 'Accept': 'application/json' };
    if (opts.body) headers['Content-Type'] = 'application/json';
    var actor = actorHeader();
    if (actor) headers['X-Actor'] = actor;
    var response = await fetch(path, {
      method: opts.method || 'GET',
      headers: headers,
      body: opts.body ? JSON.stringify(opts.body) : undefined,
      credentials: 'same-origin'
    });
    var json = {};
    try { json = await response.json(); } catch (e) { json = {}; }
    if (!response.ok || json.success === false) {
      throw new Error(json.error || json.message || ('Request failed (' + response.status + ')'));
    }
    return json;
  }

  function toast(__a, __b) {
  /* Shared NGIS operation-feedback engine (ui-states.js) — single
     implementation across all portals; no page-local toast UI anymore. */
  if (!(window.NGISUI && window.NGISUI.toast)) {
    if (window.console) console.warn('toast unavailable:', __a);
    return null;
  }
  var __k = __b;
  if (__b === true || __b === 'error' || __b === 'danger' || __b === 'fail' || __b === 'isError') __k = 'error';
  else if (__b === 'warning' || __b === 'warn') __k = 'warning';
  else if (__b === 'info') __k = 'info';
  else if (__b === 'loading') __k = 'loading';
  else if (__b === false || __b === undefined || __b === null || __b === 'success' || __b === 'ok' || __b === 'done') __k = 'success';
  else __k = 'info';
  return window.NGISUI.toast.show(__k, String(__a));
}

  /* Real async operation lifecycle: loading → actual result → animated
     success/error. Falls back to an instant confirmation when the shared
     feedback engine is unavailable. */
  function op(title, promiseOrFn, successTitle) {
    if (window.NGISUI && window.NGISUI.toast && window.NGISUI.toast.operation) {
      return window.NGISUI.toast.operation(title, promiseOrFn, { successTitle: successTitle });
    }
    return Promise.resolve(typeof promiseOrFn === 'function' ? promiseOrFn() : promiseOrFn)
      .then(function (res) { toast(successTitle); return res; });
  }

  function dateParts(value) {
    var bits = String(value || '').split('-');
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var m = Number(bits[1] || 0);
    return {
      day: bits[2] || '--',
      month: m >= 1 && m <= 12 ? months[m - 1] : '—',
      full: String(value || '')
    };
  }

  function longDate(value) {
    var bits = String(value || '').split('-');
    if (bits.length !== 3) return String(value || '');
    return Number(bits[2]) + ' ' + dateParts(value).month + ' ' + bits[0];
  }

  function monthLabel(value) {
    var bits = String(value || '').split('-');
    var m = Number(bits[1] || 0);
    var names = ['January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'];
    return m >= 1 && m <= 12 ? names[m - 1] + ' ' + bits[0] : String(value || '');
  }

  function statusClass(exam) {
    if (exam.conflict) return 'is-conflict';
    return 'is-' + String(exam.status || '').replace(/_/g, '-');
  }

  function statusText(exam) {
    if (exam.conflict) return 'Conflict — ' + exam.status_label;
    return exam.status_label;
  }

  function isUpcoming(exam) {
    if (exam && exam.is_demo) return true;
    var stamp = String(exam.exam_date || '') + 'T' + String(exam.end_time || '23:59') + ':00';
    var when = new Date(stamp);
    return isNaN(when.getTime()) || when.getTime() >= Date.now();
  }

  function optionsHtml(items, selected, placeholder) {
    var html = '<option value="all">' + esc(placeholder) + '</option>';
    (items || []).forEach(function (item) {
      html += '<option value="' + esc(item.id) + '"' + (String(selected) === String(item.id) ? ' selected' : '') + '>' + esc(item.label || item.name) + '</option>';
    });
    return html;
  }

  function closeModal() {
    if (scrim) scrim.classList.remove('show');
    state.modalMode = '';
    state.editing = null;
    if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
    lastFocus = null;
  }

  function openModal(config) {
    if (!scrim) {
      scrim = document.createElement('div');
      scrim.className = 'exw-modal-scrim';
      scrim.setAttribute('role', 'presentation');
      document.body.appendChild(scrim);
      scrim.addEventListener('mousedown', function (event) {
        if (event.target === scrim) closeModal();
      });
      document.addEventListener('keydown', function (event) {
        if (!scrim || !scrim.classList.contains('show')) return;
        if (event.key === 'Escape') { closeModal(); return; }
        if (event.key !== 'Tab' || !modal) return;
        var focusables = modal.querySelectorAll('button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled])');
        if (!focusables.length) return;
        var first = focusables[0];
        var last = focusables[focusables.length - 1];
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      });
    }
    lastFocus = document.activeElement;
    state.modalMode = config.mode || '';
    scrim.innerHTML =
      '<section class="exw-modal' + (config.wide ? ' exw-modal-wide' : '') + '" role="dialog" aria-modal="true" aria-label="' + esc(config.title) + '">' +
        '<header class="exw-modal-head"><div><div class="exw-modal-title">' + esc(config.title) + '</div>' +
        (config.subtitle ? '<div class="exw-modal-sub">' + esc(config.subtitle) + '</div>' : '') +
        '</div><button type="button" class="exw-modal-close" data-action="close-modal" aria-label="Close dialog">&times;</button></header>' +
        '<div class="exw-modal-body">' + (config.body || '') + '</div>' +
        (config.footer ? '<footer class="exw-modal-foot">' + config.footer + '</footer>' : '') +
      '</section>';
    modal = scrim.querySelector('.exw-modal');
    scrim.classList.add('show');
    var firstInput = modal.querySelector('input:not([type="checkbox"]), select, textarea, button');
    if (firstInput) firstInput.focus();
  }

  function shell(config) {
    root.innerHTML =
      '<div class="exw">' +
        '<div class="exw-head"><div><h1 class="exw-page-title">' + esc(config.title) + '</h1>' +
        '<p class="exw-page-sub">' + esc(config.subtitle) + '</p></div>' +
        '<div class="exw-inline-actions">' + (config.actions || '') + '</div></div>' +
        '<div class="exw-counts" id="exwCounts"></div>' +
        config.body +
      '</div>';
  }

  function renderCounts(items) {
    var box = document.getElementById('exwCounts');
    if (!box) return;
    var pending = items.filter(function (e) { return e.status === 'submitted'; }).length;
    var published = items.filter(function (e) { return e.status === 'published' || e.status === 'results_processing' || e.status === 'results_published'; }).length;
    var upcoming = items.filter(isUpcoming).length;
    var cards = ROLE === 'student'
      ? [['Upcoming', upcoming], ['Completed', items.length - upcoming], ['Total', items.length]]
      : [['All schedules', items.length], ['Pending review', pending], ['Published', published],
         ['Conflicts', items.filter(function (e) { return e.conflict; }).length]];
    box.innerHTML = cards.map(function (c) {
      return '<span class="exw-count"><span class="exw-count-num">' + c[1] + '</span>' + esc(c[0]) + '</span>';
    }).join('');
  }

  function selectFilters(withStatus, extra) {
    var typeTypes = (state.options && state.options.exam_types) || [
      { id: 'monthly', label: 'Monthly Examination' }, { id: 'midterm', label: 'Midterm Examination' },
      { id: 'semester', label: 'Semester Examination' }, { id: 'final', label: 'Final Examination' },
      { id: 'class_test', label: 'Class Test' }
    ];
    var months = (state.months || []).map(function (m) { return { id: m, label: monthLabel(m) }; });
    var html = '';
    if (ROLE !== 'student') {
      html += '<div class="exw-field exw-field-grow"><label class="exw-field-label" for="exwQ">Search</label>' +
        '<input class="exw-input" id="exwQ" type="search" value="' + esc(state.q) + '" placeholder="Subject, class or department">' +
        '<span class="exw-hint" style="margin-top:4px;align-self:flex-start">⌘K</span></div>';
    }
    html += '<div class="exw-field"><label class="exw-field-label" for="exwType">Examination type</label>' +
      '<select class="exw-select" id="exwType">' + optionsHtml(typeTypes, state.type, 'All types') + '</select></div>';
    html += '<div class="exw-field"><label class="exw-field-label" for="exwMonth">Month</label>' +
      '<select class="exw-select" id="exwMonth">' + optionsHtml(months, state.month, 'All months') + '</select></div>';
    if (withStatus) {
      var statuses = [
        { id: 'draft', label: 'Draft' }, { id: 'submitted', label: 'Pending review' },
        { id: 'needs_correction', label: 'Changes requested' }, { id: 'approved', label: 'Approved' },
        { id: 'published', label: 'Published' }, { id: 'rejected', label: 'Rejected' },
        { id: 'cancelled', label: 'Cancelled' }
      ];
      html += '<div class="exw-field"><label class="exw-field-label" for="exwStatus">Status</label>' +
        '<select class="exw-select" id="exwStatus">' + optionsHtml(statuses, state.status, 'All statuses') + '</select></div>';
    }
    if (extra === 'principal') {
      var campuses = ((state.options && state.options.campuses) || []).map(function (c) { return { id: c.id, label: c.name }; });
      var depts = ((state.options && state.options.departments) || []).map(function (d) { return { id: d.id, label: d.name }; });
      var classes = ((state.options && state.options.classes) || []).map(function (c) { return { id: c.id, label: c.name }; });
      html += '<div class="exw-field"><label class="exw-field-label" for="exwCampus">Campus</label>' +
        '<select class="exw-select" id="exwCampus">' + optionsHtml(campuses, state.campus, 'All campuses') + '</select></div>';
      html += '<div class="exw-field"><label class="exw-field-label" for="exwDept">Department</label>' +
        '<select class="exw-select" id="exwDept">' + optionsHtml(depts, state.dept, 'All departments') + '</select></div>';
      html += '<div class="exw-field"><label class="exw-field-label" for="exwClass">Class</label>' +
        '<select class="exw-select" id="exwClass">' + optionsHtml(classes, state.classId, 'All classes') + '</select></div>';
    }
    if (extra === 'admin') {
      var adepts = ((state.options && state.options.departments) || []).map(function (d) { return { id: d.id, label: d.name }; });
      html += '<div class="exw-field"><label class="exw-field-label" for="exwDept">Department</label>' +
        '<select class="exw-select" id="exwDept">' + optionsHtml(adepts, state.dept, 'All departments') + '</select></div>';
    }
    return html;
  }

  function formatTime12(timeStr) {
    if (!timeStr) return '';
    if (timeStr.indexOf('AM') !== -1 || timeStr.indexOf('PM') !== -1) return timeStr;
    var parts = timeStr.split(':');
    if (parts.length < 2) return timeStr;
    var h = parseInt(parts[0], 10);
    var m = parts[1];
    var ampm = h >= 12 ? 'PM' : 'AM';
    h = h % 12;
    if (h === 0) h = 12;
    return (h < 10 ? '0' + h : h) + ':' + m + ' ' + ampm;
  }

  function getContextualLinkText(e) {
    if (e.link_text) return e.link_text;
    var s = (e.subject || e.title || '').toLowerCase();
    if (s.indexOf('math') !== -1 || s.indexOf('calculus') !== -1 || s.indexOf('physics') !== -1) return 'Formulae';
    if (s.indexOf('literature') !== -1 || s.indexOf('reading') !== -1) return 'Texts';
    if (s.indexOf('grammar') !== -1 || s.indexOf('writing') !== -1 || s.indexOf('composition') !== -1) return 'Rubric';
    if (s.indexOf('chinese') !== -1 || s.indexOf('khmer') !== -1 || s.indexOf('language') !== -1) return 'Guide';
    return 'Overview';
  }
  function studentShell() {
    root.innerHTML =
      '<div class="exw max-w-5xl mx-auto py-6 px-4 sm:px-6">' +
        '<div class="exw-roadmap-container">' +
          // Header Bar matching reference screenshot
          '<div class="exw-roadmap-head">' +
            '<div>' +
              '<div class="exw-roadmap-title-row">' +
                '<span class="exw-roadmap-dot"></span>' +
                '<h2 class="exw-roadmap-title" id="roadmapTitle">Subsequent Examinations Roadmap</h2>' +
              '</div>' +
              '<p class="exw-roadmap-subtitle" id="roadmapSubtitle">Chronological progression through July 2026 evaluations</p>' +
            '</div>' +
            '<div class="exw-roadmap-tools">' +
              // Search Filter
              '<div class="exw-roadmap-search-wrap">' +
                '<span class="material-symbols-outlined exw-roadmap-search-icon">search</span>' +
                '<input type="text" id="roadmapFilter" data-ngis-search-skip="true" placeholder="Filter subjects..." value="' + esc(state.q) + '" class="exw-roadmap-search" autocomplete="off">' +
              '</div>' +
              // Queued Badge
              '<span class="exw-roadmap-badge" id="roadmapQueuedBadge">' +
                '<span id="roadmapQueuedCount">5</span>&nbsp;Queued' +
              '</span>' +
            '</div>' +
          '</div>' +
          // Timeline Content
          '<div id="exwList"></div>' +
        '</div>' +
      '</div>';
  }

  function staffShell() {
    var config = {
      teacher: {
        title: 'Examination & Quiz Notices',
        subtitle: 'Publish examination notices, quiz schedules, and revision materials for student cohorts.',
        actions: '<button type="button" class="exw-btn exw-btn-primary" data-action="new"><span class="material-symbols-outlined text-sm align-middle mr-1">add</span>Create Notice</button>',
        tabs: ''
      },
      principal: {
        title: 'Examination Review & Approval',
        subtitle: 'Review teacher schedules, approve or return them, then publish for students.',
        actions: '',
        tabs:
          '<div class="exw-tabs">' +
            ['pending', 'upcoming', 'approved', 'returned', 'published'].map(function (t) {
              var label = { pending: 'Pending approval', upcoming: 'Upcoming', approved: 'Approved', returned: 'Returned', published: 'Published' }[t];
              return '<button type="button" class="exw-tab' + (state.tab === t ? ' active' : '') + '" data-action="tab" data-tab="' + t + '">' + label + '</button>';
            }).join('') +
          '</div>'
      },
      admin: {
        title: 'Examination Schedule Monitor',
        subtitle: 'Search, filter and correct examination schedules across the school.',
        actions: '<button type="button" class="exw-btn" data-action="activity">Activity history</button>',
        tabs: ''
      }
    }[ROLE] || { title: 'Examination Schedules', subtitle: '', actions: '', tabs: '' };

    shell({
      title: config.title,
      subtitle: config.subtitle,
      actions: config.actions,
      body:
        '<section class="exw-card exw-section">' + config.tabs +
        '<div class="exw-toolbar">' + selectFilters(true, ROLE === 'principal' ? 'principal' : (ROLE === 'admin' ? 'admin' : '')) + '</div>' +
        '</section><section class="exw-section"><div id="exwTable"></div></section>'
    });
  }

  function filteredExams() {
    return state.exams.filter(function (e) {
      if (state.type !== 'all' && e.exam_type !== state.type) return false;
      if (state.month !== 'all' && String(e.exam_date || '').slice(0, 7) !== state.month) return false;
      if (ROLE === 'student') {
        if (state.tab === 'upcoming') {
          if (e.completed || !isUpcoming(e)) return false;
        } else if (state.tab === 'completed') {
          if (!e.completed && isUpcoming(e)) return false;
        }
        if (state.q) {
          var hay = (e.subject + ' ' + (e.title || '') + ' ' + (e.department || '') + ' ' + (e.room || '') + ' ' + (e.instructions || '') + ' ' + (e.evaluator_note || '')).toLowerCase();
          if (hay.indexOf(state.q.toLowerCase()) === -1) return false;
        }
        return true;
      }
      if (state.q) {
        var hay = (e.subject + ' ' + e.title + ' ' + e.department + ' ' + e.classes.join(' ')).toLowerCase();
        if (hay.indexOf(state.q.toLowerCase()) === -1) return false;
      }
      if (state.status !== 'all') {
        if (state.status === 'pending' && e.status !== 'submitted' && e.academic_status !== 'pending') return false;
        if (state.status !== 'pending' && e.status !== state.status) return false;
      }
      if (state.dept !== 'all' && e.department_id !== state.dept && e.department.toLowerCase().indexOf(state.dept) === -1) return false;
      if (state.campus !== 'all' && e.campus_id !== state.campus) return false;
      if (state.classId !== 'all' && e.class_ids.indexOf(state.classId) === -1) return false;
      if (ROLE === 'principal' && state.tab === 'pending') return e.status === 'submitted';
      if (ROLE === 'principal' && state.tab === 'approved') return e.status === 'approved';
      if (ROLE === 'principal' && state.tab === 'published') return e.status === 'published';
      if (ROLE === 'principal' && state.tab === 'returned') return e.status === 'needs_correction' || e.status === 'rejected';
      if (ROLE === 'principal' && state.tab === 'upcoming') return isUpcoming(e);
      return true;
    });
  }

  function emptyState(title, note) {
    return '<div class="exw-card exw-empty"><div class="exw-empty-title">' + esc(title) + '</div>' +
      '<div class="exw-empty-note">' + esc(note) + '</div></div>';
  }

  function examCard(e, showDept) {
    var d = dateParts(e.exam_date);
    var meta = [e.exam_type_label];
    if (e.department) meta.push(e.department);
    if (e.classes && e.classes.length) meta.push(e.classes.join(', '));
    return '<li class="exw-exam">' +
      '<div class="exw-date"><span class="exw-date-day">' + esc(d.day) + '</span><span class="exw-date-month">' + esc(d.month) + '</span></div>' +
      '<div class="exw-exam-main">' +
      '<div class="exw-exam-title font-medium text-forest-800 text-[14px] leading-tight">' + esc(e.title || e.subject) + '</div>' +
      '<div class="exw-subject text-xs text-ink-soft mt-0.5">' + esc(e.subject) + '</div>' +
      '<div class="exw-meta mt-1">' + meta.map(function (m) { return '<span>' + esc(m) + '</span>'; }).join('') + '</div></div>' +
      '<div class="exw-right"><div class="exw-time">' + esc(e.start_time) + ' – ' + esc(e.end_time) + '</div>' +
      '<div class="exw-status ' + statusClass(e) + '">' + esc(statusText(e)) + '</div></div>' +
      '</li>';
  }

  function renderStudent() {
    var all = state.exams;
    var items = filteredExams();
    var box = document.getElementById('exwList');
    var badgeCount = document.getElementById('roadmapQueuedCount');
    var badgeWrap = document.getElementById('roadmapQueuedBadge');
    var titleEl = document.getElementById('roadmapTitle');
    var subEl = document.getElementById('roadmapSubtitle');

    if (badgeCount) badgeCount.textContent = items.length;
    if (badgeWrap) {
      badgeWrap.style.display = '';
    }
    if (titleEl) {
      titleEl.textContent = 'Subsequent Examinations Roadmap';
    }
    if (subEl) {
      subEl.textContent = 'Chronological progression through July 2026 evaluations';
    }

    if (!box) return;
    if (!items.length) {
      if (state.q && window.NGIS_EMPTY && typeof window.NGIS_EMPTY.renderNoResults === 'function') {
        window.NGIS_EMPTY.renderNoResults(box, {
          onAction: function () {
            var input = document.getElementById('roadmapFilter');
            if (input) input.value = '';
            state.q = '';
            renderStudent();
          },
          onReset: function () {
            var input = document.getElementById('roadmapFilter');
            if (input) input.value = '';
            state.q = '';
            renderStudent();
          }
        });
        return;
      }
      if (window.NGIS_EMPTY && typeof window.NGIS_EMPTY.render === 'function') {
        window.NGIS_EMPTY.render(box, 'exams');
        return;
      }
      box.innerHTML = emptyState(
        'No examinations found',
        'No upcoming examinations match your filter criteria.'
      );
      return;
    }

    var sorted = items.slice().sort(function (a, b) {
      var da = (a.exam_date || '') + ' ' + (a.start_time || '');
      var db = (b.exam_date || '') + ' ' + (b.start_time || '');
      return da.localeCompare(db);
    });

    var html = '<div class="exw-timeline-wrap">';

    sorted.forEach(function (e, idx) {
      var isFirst = idx === 0;
      var isLast = idx === sorted.length - 1;
      var d = dateParts(e.exam_date);
      var dayStr = String(d.day || '01').padStart(2, '0');
      var monthStr = (d.month || 'JUL').toUpperCase();

      var timeStr = formatTime12(e.start_time) + ' – ' + formatTime12(e.end_time);
      var roomStr = esc(e.room || e.location || (e.classes && e.classes[0] ? e.classes[0] : 'Room 302'));
      var noteStr = esc(e.evaluator_note || e.format || (e.teacher ? e.teacher + ' • ' + (e.exam_type_label || 'Test') : (e.exam_type_label || 'Standard Exam')));
      var descStr = esc(e.instructions || e.topics || e.description || e.notes || (e.subject + ' • ' + (e.exam_type_label || 'Evaluation')));
      var linkText = getContextualLinkText(e);

      var lineClass = isFirst ? 'exw-timeline-line-blue' : 'exw-timeline-line-grey';
      if (isLast) lineClass += ' exw-timeline-line-end';

      var pillClass = isFirst ? 'exw-pill-highlight' : 'exw-pill-neutral';

      html +=
        '<div class="exw-timeline-item">' +
          '<div class="exw-timeline-spine">' +
            '<div class="exw-timeline-node">' + dayStr + '</div>' +
            '<div class="exw-timeline-line ' + lineClass + '"></div>' +
          '</div>' +
          '<div class="exw-roadmap-row" data-action="view" data-id="' + esc(e.id) + '">' +
            '<div class="exw-roadmap-row-top">' +
              '<div class="exw-roadmap-meta">' +
                '<span class="exw-pill-time ' + pillClass + '">' + dayStr + ' ' + monthStr + ' • ' + timeStr + '</span>' +
                '<span class="exw-room-label">' + roomStr + '</span>' +
              '</div>' +
              '<div class="exw-roadmap-evaluator">' + noteStr + '</div>' +
            '</div>' +
            '<div class="exw-roadmap-row-mid">' +
              '<h3 class="exw-roadmap-subject">' + esc(e.title || e.subject) + '</h3>' +
              '<a class="exw-roadmap-action" href="#" data-action="view" data-id="' + esc(e.id) + '">' +
                '<span>' + esc(linkText) + '</span>' +
                '<span class="exw-roadmap-chevron">&rsaquo;</span>' +
              '</a>' +
            '</div>' +
            '<div class="exw-roadmap-row-bot">' +
              '<p class="exw-roadmap-desc" title="' + descStr + '">' + descStr + '</p>' +
            '</div>' +
          '</div>' +
        '</div>';
    });

    html += '</div>';
    box.innerHTML = html;
  }

  function rowActions(e) {
    var actions = '';
    if (ROLE === 'teacher') {
      if (e.status !== 'published' && e.status !== 'cancelled') {
        actions += '<button type="button" class="exw-link" data-action="edit" data-id="' + esc(e.id) + '">Edit</button>';
      }
      if (e.status === 'draft' || e.status === 'needs_correction') {
        actions += '<button type="button" class="exw-link" data-action="submit" data-id="' + esc(e.id) + '">Submit</button>';
      }
      if (e.status !== 'cancelled' && e.status !== 'published') {
        actions += '<button type="button" class="exw-link exw-link-danger" data-action="cancel" data-id="' + esc(e.id) + '">Cancel</button>';
      }
    } else if (ROLE === 'principal') {
      if (e.status === 'submitted') actions += '<button type="button" class="exw-link" data-action="review" data-id="' + esc(e.id) + '">Review</button>';
      if (e.status === 'approved') actions += '<button type="button" class="exw-link" data-action="publish" data-id="' + esc(e.id) + '">Publish</button>';
      if (e.status !== 'cancelled' && e.status !== 'published') {
        actions += '<button type="button" class="exw-link" data-action="edit" data-id="' + esc(e.id) + '">Edit</button>';
      }
      if (e.status === 'published') {
        actions += '<button type="button" class="exw-link" data-action="unpublish" data-id="' + esc(e.id) + '">Withdraw</button>';
      }
      if (e.status !== 'cancelled') {
        actions += '<button type="button" class="exw-link exw-link-danger" data-action="cancel" data-id="' + esc(e.id) + '">Cancel</button>';
      }
    } else {
      actions += '<button type="button" class="exw-link" data-action="view" data-id="' + esc(e.id) + '">View</button>';
      actions += '<button type="button" class="exw-link" data-action="edit" data-id="' + esc(e.id) + '">Correct</button>';
      actions += '<button type="button" class="exw-link" data-action="activity" data-id="' + esc(e.id) + '">History</button>';
      if (e.status !== 'cancelled') {
        actions += '<button type="button" class="exw-link exw-link-danger" data-action="cancel" data-id="' + esc(e.id) + '">Cancel</button>';
      }
    }
    return actions || '<span class="exw-status">—</span>';
  }

  function renderTable() {
    var items = filteredExams();
    renderCounts(state.exams);
    var box = document.getElementById('exwTable');
    if (!box) return;
    var conflictNote = '';
    if (ROLE === 'admin' && state.stats.conflicts) {
      conflictNote = '<div class="exw-note" style="margin-bottom:12px">' + state.stats.conflicts + ' schedule' +
        (state.stats.conflicts === 1 ? '' : 's') + ' currently overlap with another examination for the same class or subject.</div>';
    }
    if (!items.length) {
      box.innerHTML = conflictNote + emptyState('No examinations found', 'Adjust the filters or create a new schedule.');
      return;
    }
    var rows = items.map(function (e) {
      var time = esc(e.start_time) + ' – ' + esc(e.end_time);
      if (e.conflict) time += '<span class="exw-secondary" style="color:#B91C1C">' + esc(e.conflict_message) + '</span>';
      var correction = (ROLE === 'teacher' && e.correction_notes)
        ? '<span class="exw-secondary">Requested: ' + esc(e.correction_notes) + '</span>' : '';
      return '<tr class="transition-colors hover:bg-slate-50 cursor-pointer" data-id="' + esc(e.id) + '" onclick="if(!event.target.closest(\'button, a, input\')) { document.querySelectorAll(\'.exw-table tr\').forEach(function(r) { r.classList.remove(\'selected-row\'); }); this.classList.add(\'selected-row\'); }">' +
        '<td data-label="Subject"><span class="exw-subject-cell">' + esc(e.subject) + '</span>' +
          '<span class="exw-secondary">' + esc(e.exam_type_label) + '</span></td>' +
        '<td data-label="Class">' + esc(e.classes.join(', ')) + '</td>' +
        '<td data-label="Type">' + esc(e.exam_type_label) + '</td>' +
        '<td data-label="Date">' + esc(longDate(e.exam_date)) + '</td>' +
        '<td data-label="Time">' + time + '</td>' +
        '<td data-label="Department">' + esc(e.department) + '</td>' +
        '<td data-label="Status"><span class="exw-status ' + statusClass(e) + '">' + esc(statusText(e)) + '</span>' + correction + '</td>' +
        '<td data-label="Actions"><div class="exw-inline-actions">' + rowActions(e) + '</div></td>' +
        '</tr>';
    }).join('');
    box.innerHTML = conflictNote +
      '<div class="exw-card"><table class="exw-table"><thead><tr>' +
      '<th>Subject</th><th>Class</th><th>Type</th><th>Date</th><th>Time</th><th>Department</th><th>Status</th><th>Actions</th>' +
      '</tr></thead><tbody>' + rows + '</tbody></table></div>';
  }

  function render() {
    if (ROLE === 'student') renderStudent();
    else renderTable();
  }

  function findExam(id) {
    return state.exams.filter(function (e) { return e.id === id; })[0] || null;
  }

  async function reload() {
    try {
      var url = ROLE === 'student'
        ? '/api/exams/student?portal=student' + (deptContext ? '&dept=' + encodeURIComponent(deptContext) : '')
        : '/api/exams/simple?portal=' + encodeURIComponent(ROLE);
      var data = await api(url);
      var fetchedExams = data.exams || data.data || [];

      // Development fallback & demo data for students:
      // Provide realistic records spanning Monthly, Semester, Midterm, Final, Quiz
      if (ROLE === 'student') {
        var hasUpcoming = fetchedExams.some(function (e) { return !e.completed && isUpcoming(e); });
        if (!hasUpcoming) {
          var now = new Date();
          var y = now.getFullYear();
          var m = String(now.getMonth() + 1).padStart(2, '0');
          var d = now.getDate();
          
          var demoExams = [
            {
              id: 'EXM-RDMP-01',
              title: 'Advanced Mathematics',
              subject: 'Advanced Mathematics',
              subject_id: 'subj-math',
              exam_type: 'test',
              exam_type_label: 'Ch. 7-10 Test',
              department: 'Mathematics Department',
              department_id: 'math',
              classes: ['Grade 10A'],
              class_ids: ['cls-10a'],
              room: 'Room 302',
              exam_date: '2026-07-02',
              start_time: '08:30',
              end_time: '10:30',
              evaluator_note: 'Mr. Heng • Ch. 7-10 Test',
              instructions: 'Calculators OK • Integration & Series Theorems',
              link_text: 'Formulae',
              status: 'published',
              status_label: 'Upcoming',
              completed: false,
              teacher: 'Mr. Heng',
              is_demo: true
            },
            {
              id: 'EXM-RDMP-02',
              title: 'English Literature — Mid-Term Examination',
              subject: 'English Literature',
              subject_id: 'subj-eng',
              exam_type: 'midterm',
              exam_type_label: 'Mid-Term Examination',
              department: 'English Department',
              department_id: 'english',
              classes: ['Grade 10A'],
              class_ids: ['cls-10a'],
              room: 'Main Hall • Section A',
              exam_date: '2026-07-14',
              start_time: '10:00',
              end_time: '12:00',
              evaluator_note: 'Essay Format Evaluation',
              instructions: 'Victorian Poetry & Modern Drama Analysis',
              link_text: 'Texts',
              status: 'published',
              status_label: 'Upcoming',
              completed: false,
              teacher: 'Ms. Rathana Chea',
              is_demo: true
            },
            {
              id: 'EXM-RDMP-03',
              title: 'English Grammar & Writing — Assessment',
              subject: 'English Grammar & Writing',
              subject_id: 'subj-eng-gram',
              exam_type: 'assessment',
              exam_type_label: 'Assessment',
              department: 'English Department',
              department_id: 'english',
              classes: ['Grade 10A'],
              class_ids: ['cls-10a'],
              room: 'Room 204',
              exam_date: '2026-07-16',
              start_time: '13:30',
              end_time: '15:00',
              evaluator_note: 'Academic Composition',
              instructions: 'Writing Skills & Rhetorical Devices Rubric',
              link_text: 'Rubric',
              status: 'published',
              status_label: 'Upcoming',
              completed: false,
              teacher: 'Dr. Vance Miller',
              is_demo: true
            },
            {
              id: 'EXM-RDMP-04',
              title: 'Khmer Literature — Mid-Term Examination',
              subject: 'Khmer Literature',
              subject_id: 'subj-khmer',
              exam_type: 'midterm',
              exam_type_label: 'Mid-Term Examination',
              department: 'Khmer Studies',
              department_id: 'khmer',
              classes: ['Grade 10A'],
              class_ids: ['cls-10a'],
              room: 'Hall A • Seat 18',
              exam_date: '2026-07-18',
              start_time: '08:30',
              end_time: '11:00',
              evaluator_note: 'Written Standard Exam',
              instructions: 'Classical Texts, Structure & Khmer Orthography',
              link_text: 'Overview',
              status: 'published',
              status_label: 'Upcoming',
              completed: false,
              teacher: 'Mr. Sokha Chan',
              is_demo: true
            },
            {
              id: 'EXM-RDMP-05',
              title: 'Chinese Language & Writing — Evaluation',
              subject: 'Chinese Language & Writing',
              subject_id: 'subj-chinese',
              exam_type: 'evaluation',
              exam_type_label: 'Evaluation',
              department: 'Foreign Languages',
              department_id: 'chinese',
              classes: ['Grade 10A'],
              class_ids: ['cls-10a'],
              room: 'Room 105',
              exam_date: '2026-07-23',
              start_time: '09:00',
              end_time: '10:30',
              evaluator_note: 'HSK Level 3 Benchmark',
              instructions: 'Character Stroke Dynamics & Conversational Grammar',
              link_text: 'Guide',
              status: 'published',
              status_label: 'Upcoming',
              completed: false,
              teacher: 'Ms. Meiling Chen',
              is_demo: true
            }
          ];

          if (deptContext) {
            demoExams = demoExams.filter(function (e) {
              return e.department_id === deptContext || (e.subject_id && e.subject_id.includes(deptContext));
            });
          }

          fetchedExams = demoExams.concat(fetchedExams);
        }
      }

      state.exams = fetchedExams;
      state.stats = data.stats || {};
      state.months = data.months || [];
      var typeSelect = document.getElementById('exwType');
      if (typeSelect && typeSelect.options.length <= 1 && data.exam_types) {
        data.exam_types.forEach(function (t) {
          var option = document.createElement('option');
          option.value = t.id; option.textContent = t.label;
          typeSelect.appendChild(option);
        });
      }
      render();
    } catch (error) {
      toast(error.message, true);
    }
  }

  async function loadOptions() {
    if (state.options) return state.options;
    var data = await api('/api/exams/options?portal=' + encodeURIComponent(ROLE));
    state.options = data;
    return data;
  }

  function classesFor(subjectId, deptId) {
    var opts = state.options || {};
    var classes = opts.classes || [];
    if (ROLE === 'teacher' && subjectId && opts.assignments) {
      var allowed = opts.assignments.filter(function (a) { return a.subject_id === subjectId; }).map(function (a) { return a.class_id; });
      classes = classes.filter(function (c) { return allowed.indexOf(c.id) !== -1; });
    } else if (deptId) {
      var byDept = classes.filter(function (c) { return c.department_id === deptId; });
      if (byDept.length) classes = byDept;
    }
    return classes;
  }

  function renderClassChecks(selected) {
    var box = document.getElementById('exwClasses');
    if (!box) return;
    var subject = document.getElementById('exwSubject') ? document.getElementById('exwSubject').value : '';
    var dept = document.getElementById('exwDepartment') ? document.getElementById('exwDepartment').value : '';
    var classes = classesFor(subject, dept);
    var chosen = Array.prototype.slice.call(box.querySelectorAll('input:checked')).map(function (i) { return i.value; });
    var merged = (selected && selected.length) ? selected : chosen;
    if (!classes.length) {
      box.innerHTML = '<span class="exw-status">No classes available for this selection.</span>';
      return;
    }
    box.innerHTML = classes.map(function (c) {
      return '<label class="exw-check"><input type="checkbox" name="exwClass" value="' + esc(c.id) + '"' +
        (merged.indexOf(c.id) !== -1 ? ' checked' : '') + '><span>' + esc(c.name) + '</span></label>';
    }).join('');
  }

  async function openForm(exam) {
    try {
      var opts = await loadOptions();
      state.editing = exam || null;
      var departments = opts.departments || [];
      var subjects = opts.subjects || [];
      var types = opts.exam_types || [];
      var currentDept = exam ? exam.department_id : (departments[0] ? departments[0].id : '');
      var currentSubject = exam ? exam.subject_id : (subjects[0] ? subjects[0].id : '');
      var body =
        '<form id="exwForm" class="exw-form">' +
          '<label class="exw-label">Department <span class="exw-label-required">*</span>' +
            '<select class="exw-select" id="exwDepartment">' + departments.map(function (d) {
              return '<option value="' + esc(d.id) + '"' + (d.id === currentDept ? ' selected' : '') + '>' + esc(d.name) + '</option>';
            }).join('') + '</select></label>' +
          '<label class="exw-label">Subject <span class="exw-label-required">*</span>' +
            '<select class="exw-select" id="exwSubject">' + subjects.map(function (s) {
              return '<option value="' + esc(s.id) + '"' + (s.id === currentSubject ? ' selected' : '') + '>' + esc(s.name) + '</option>';
            }).join('') + '</select></label>' +
          '<div class="exw-label">Class or classes <span class="exw-label-required">*</span>' +
            '<div class="exw-checks" id="exwClasses"></div></div>' +
          '<label class="exw-label">Examination type <span class="exw-label-required">*</span>' +
            '<select class="exw-select" id="exwExamType">' + types.map(function (t) {
              return '<option value="' + esc(t.id) + '"' + (exam && exam.exam_type === t.id ? ' selected' : '') + '>' + esc(t.label) + '</option>';
            }).join('') + '</select></label>' +
          '<div class="exw-form-row">' +
            '<label class="exw-label">Examination date <span class="exw-label-required">*</span>' +
              '<input class="exw-input" id="exwDate" type="date" value="' + esc(exam ? exam.exam_date : '') + '"></label>' +
            '<label class="exw-label">Start time <span class="exw-label-required">*</span>' +
              '<input class="exw-input" id="exwStart" type="time" value="' + esc(exam ? exam.start_time : '08:00') + '"></label>' +
          '</div>' +
          '<label class="exw-label">End time <span class="exw-label-required">*</span>' +
            '<input class="exw-input" id="exwEnd" type="time" value="' + esc(exam ? exam.end_time : '09:30') + '"></label>' +
        '</form>';
      var footer = exam
        ? '<button type="button" class="exw-btn" data-action="close-modal">Cancel</button>' +
          '<button type="button" class="exw-btn exw-btn-primary" data-action="save" data-submit="0">Save changes</button>' +
          ((exam.status === 'draft' || exam.status === 'needs_correction')
            ? '<button type="button" class="exw-btn" data-action="save" data-submit="1">Save &amp; submit</button>' : '')
        : '<button type="button" class="exw-btn" data-action="close-modal">Cancel</button>' +
          '<button type="button" class="exw-btn" data-action="save" data-submit="0">Save draft</button>' +
          '<button type="button" class="exw-btn exw-btn-primary" data-action="save" data-submit="1">Submit for approval</button>';
      openModal({
        mode: 'form',
        title: exam ? 'Edit Examination Notice' : 'Create Examination & Quiz Notice',
        subtitle: exam ? exam.subject + ' · ' + exam.exam_type_label : 'Fill in the seven schedule fields below.',
        body: body,
        footer: footer
      });
      renderClassChecks(exam ? exam.class_ids : []);
    } catch (error) { toast(error.message, true); }
  }

  function collectForm() {
    var classes = Array.prototype.slice.call(document.querySelectorAll('input[name="exwClass"]:checked')).map(function (i) { return i.value; });
    return {
      department_id: document.getElementById('exwDepartment').value,
      subject_id: document.getElementById('exwSubject').value,
      class_ids: classes,
      exam_type: document.getElementById('exwExamType').value,
      exam_date: document.getElementById('exwDate').value,
      start_time: document.getElementById('exwStart').value,
      end_time: document.getElementById('exwEnd').value
    };
  }

  async function saveForm(submitNow) {
    var payload = collectForm();
    if (!payload.subject_id || !payload.exam_date || !payload.start_time || !payload.end_time || !payload.class_ids.length) {
      toast('Complete all required fields and select at least one class.', true);
      return;
    }
    payload.submit_for_review = !!submitNow;
    try {
      var exam = state.editing;
      await op(
        exam ? 'Updating schedule…' : (submitNow ? 'Submitting notice…' : 'Saving notice draft…'),
        api(exam ? '/api/exams/simple/' + encodeURIComponent(exam.id) : '/api/exams/simple', {
          method: exam ? 'PUT' : 'POST',
          body: payload
        }),
        exam ? 'Notice updated.' : (submitNow ? 'Notice submitted for Principal review.' : 'Notice draft saved.')
      );
      closeModal();
      await reload();
      if (window.NGIS_showOperationSuccess) {
        window.NGIS_showOperationSuccess({
          title: submitNow ? 'Notice Submitted' : 'Notice Saved',
          message: submitNow
            ? 'Examination notice has been submitted for approval and scheduled for publication.'
            : 'Examination notice draft saved to your workspace.'
        });
      }
    } catch (error) { /* the real error is already rendered by the feedback row */ }
  }

  function openReview(exam) {
    state.editing = exam;
    var body =
      '<div class="exw-review-line"><span>Subject</span><span>' + esc(exam.subject) + '</span></div>' +
      '<div class="exw-review-line"><span>Type</span><span>' + esc(exam.exam_type_label) + '</span></div>' +
      '<div class="exw-review-line"><span>Classes</span><span>' + esc(exam.classes.join(', ')) + '</span></div>' +
      '<div class="exw-review-line"><span>Date</span><span>' + esc(longDate(exam.exam_date)) + '</span></div>' +
      '<div class="exw-review-line"><span>Time</span><span>' + esc(exam.start_time) + ' – ' + esc(exam.end_time) + '</span></div>' +
      '<label class="exw-label" style="margin-top:14px">Reason (required to reject or request changes)' +
        '<textarea class="exw-input" id="exwReviewReason" rows="3" style="height:auto;padding:9px 11px" placeholder="Optional for approval"></textarea></label>';
    var footer =
      '<button type="button" class="exw-btn" data-action="close-modal">Cancel</button>' +
      '<button type="button" class="exw-btn exw-btn-danger" data-action="decision" data-decision="reject">Reject</button>' +
      '<button type="button" class="exw-btn" data-action="decision" data-decision="request_changes">Request changes</button>' +
      '<button type="button" class="exw-btn exw-btn-primary" data-action="decision" data-decision="approve">Approve</button>';
    openModal({ mode: 'review', title: 'Review examination schedule', subtitle: exam.subject + ' · ' + exam.exam_type_label, body: body, footer: footer });
  }

  async function decide(decision) {
    var exam = state.editing;
    if (!exam) return;
    var reason = (document.getElementById('exwReviewReason') || {}).value || '';
    if (decision !== 'approve' && !reason.trim()) { toast('A reason is required for this decision.', true); return; }
    try {
      await op(
        decision === 'approve' ? 'Recording approval…' : 'Recording decision…',
        api('/api/exams/simple/' + encodeURIComponent(exam.id) + '/review', {
          method: 'POST', body: { decision: decision, reason: reason.trim() }
        }),
        decision === 'approve' ? 'Schedule approved.' : 'Decision recorded.'
      );
      closeModal();
      await reload();
    } catch (error) { /* the real error is already rendered by the feedback row */ }
  }

  function openView(exam) {
    var body =
      '<div class="exw-review-line"><span>Subject</span><span>' + esc(exam.subject) + '</span></div>' +
      '<div class="exw-review-line"><span>Department</span><span>' + esc(exam.department) + '</span></div>' +
      '<div class="exw-review-line"><span>Classes</span><span>' + esc(exam.classes.join(', ')) + '</span></div>' +
      '<div class="exw-review-line"><span>Type</span><span>' + esc(exam.exam_type_label) + '</span></div>' +
      '<div class="exw-review-line"><span>Date</span><span>' + esc(longDate(exam.exam_date)) + '</span></div>' +
      '<div class="exw-review-line"><span>Time</span><span>' + esc(exam.start_time) + ' – ' + esc(exam.end_time) + '</span></div>' +
      '<div class="exw-review-line"><span>Status</span><span>' + esc(statusText(exam)) + '</span></div>' +
      (exam.correction_notes ? '<div class="exw-review-line"><span>Notes</span><span>' + esc(exam.correction_notes) + '</span></div>' : '');
    openModal({ mode: 'view', title: 'Examination schedule', subtitle: exam.id, body: body,
      footer: '<button type="button" class="exw-btn" data-action="close-modal">Close</button>' });
  }

  async function openActivity(examId) {
    try {
      var query = examId ? '?exam_id=' + encodeURIComponent(examId) + '&limit=120' : '?limit=120';
      var data = await api('/api/exams/activity' + query);
      var items = data.data || [];
      var body = items.length
        ? '<ul class="exw-activity">' + items.map(function (a) {
            return '<li><time>' + esc(String(a.timestamp || '').replace('T', ' ').replace('Z', '')) + '</time>' +
              '<div><strong>' + esc(a.action.replace(/_/g, ' ')) + '</strong> · ' + esc(a.actor_name) +
              '<p>' + esc(a.notes || (a.previous_state + ' → ' + a.new_state)) + '</p></div></li>';
          }).join('') + '</ul>'
        : '<div class="exw-empty"><div class="exw-empty-title">No activity recorded</div></div>';
      openModal({ mode: 'activity', title: examId ? 'Schedule activity' : 'Examination activity history',
        subtitle: examId || 'All recorded schedule changes', body: body, wide: true,
        footer: '<button type="button" class="exw-btn" data-action="close-modal">Close</button>' });
    } catch (error) { toast(error.message, true); }
  }

  async function simpleAction(action, id) {
    var endpoints = {
      submit: '/submit', publish: '/publish', unpublish: '/unpublish', cancel: '/cancel'
    };
    var labels = { submit: 'submitted', publish: 'published', unpublish: 'withdrawn', cancel: 'cancelled' };
    var verb = { submit: 'Submitting schedule…', publish: 'Publishing schedule…', unpublish: 'Withdrawing schedule…', cancel: 'Cancelling schedule…' };
    try {
      await op(
        verb[action] || 'Updating schedule…',
        api('/api/exams/simple/' + encodeURIComponent(id) + endpoints[action], { method: 'POST', body: {} }),
        'Schedule ' + labels[action] + '.'
      );
      await reload();
    } catch (error) { /* the real error is already rendered by the feedback row */ }
  }

  root.addEventListener('click', function (event) {
    var target = event.target.closest('[data-action]');
    if (!target || !root.contains(target)) return;
    var action = target.getAttribute('data-action');
    var id = target.getAttribute('data-id');
    if (action === 'tab') { state.tab = target.getAttribute('data-tab'); render(); return; }
    if (action === 'new') { openForm(null); return; }
    if (action === 'edit') { openForm(findExam(id)); return; }
    if (action === 'review') { openReview(findExam(id)); return; }
    if (action === 'view') { openView(findExam(id)); return; }
    if (action === 'activity') { openActivity(id || ''); return; }
    if (action === 'decision') { decide(target.getAttribute('data-decision')); return; }
    if (action === 'save') { saveForm(target.getAttribute('data-submit') === '1'); return; }
    if (action === 'submit' || action === 'publish' || action === 'unpublish' || action === 'cancel') {
      simpleAction(action, id); return;
    }
  });

  if (scrim === null) {
    document.addEventListener('click', function (event) {
      var target = event.target.closest('[data-action="close-modal"]');
      if (target && target.closest('.exw-modal-scrim')) closeModal();
      var save = event.target.closest('[data-action="save"]');
      if (save && save.closest('.exw-modal-scrim')) saveForm(save.getAttribute('data-submit') === '1');
      var decision = event.target.closest('[data-action="decision"]');
      if (decision && decision.closest('.exw-modal-scrim')) decide(decision.getAttribute('data-decision'));
    });
  }

  root.addEventListener('change', function (event) {
    var id = event.target.id;
    if (id === 'exwType') { state.type = event.target.value; render(); }
    else if (id === 'exwMonth') { state.month = event.target.value; render(); }
    else if (id === 'exwStatus') { state.status = event.target.value; render(); }
    else if (id === 'exwCampus') { state.campus = event.target.value; render(); }
    else if (id === 'exwDept' && event.target.closest('.exw-toolbar')) { state.dept = event.target.value; render(); }
    else if (id === 'exwClass') { state.classId = event.target.value; render(); }
    else if (id === 'exwDepartment') { renderClassChecks([]); }
    else if (id === 'exwSubject') { renderClassChecks([]); }
  });

  var searchTimer = null;
  root.addEventListener('input', function (event) {
    if (event.target.id !== 'exwQ' && event.target.id !== 'roadmapFilter') return;
    clearTimeout(searchTimer);
    var value = event.target.value;
    searchTimer = setTimeout(function () { state.q = value; render(); }, 180);
  });

  document.addEventListener('keydown', function (event) {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
      var input = document.getElementById('exwQ');
      if (input) { event.preventDefault(); input.focus(); }
    }
  });

  async function init() {
    if (ROLE === 'student') studentShell();
    else staffShell();
    try { await loadOptions(); } catch (error) { /* filters still work without the catalogue */ }
    await reload();
  }

  init();
})(window, document);
