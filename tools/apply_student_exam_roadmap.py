import re

# ==========================================
# 1. UPDATE assets/css/exams-simple.css
# ==========================================
css_path = 'assets/css/exams-simple.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

roadmap_css = """
/* ==========================================================================
   SUBSEQUENT EXAMINATIONS ROADMAP (Student Portal Reference Design)
   ========================================================================== */
.exw-roadmap-card {
  background: #ffffff;
  border-radius: 24px;
  border: 1px solid #eef2f6;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03), 0 1px 2px -1px rgba(0, 0, 0, 0.02);
  padding: 24px 26px;
  margin: 0 auto;
  width: 100%;
}
@media (min-width: 640px) {
  .exw-roadmap-card {
    padding: 30px 36px;
  }
}
.exw-roadmap-head {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding-bottom: 22px;
  margin-bottom: 24px;
  border-bottom: 1px solid #f1f5f9;
}
@media (min-width: 640px) {
  .exw-roadmap-head {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}
.exw-roadmap-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}
.exw-roadmap-dot {
  width: 8px;
  height: 8px;
  border-radius: 9999px;
  background-color: #2563eb;
  flex-shrink: 0;
}
.exw-roadmap-title {
  font-size: 18px;
  font-weight: 500;
  color: #0f172a;
  letter-spacing: -0.01em;
  margin: 0;
}
.exw-roadmap-subtitle {
  font-size: 13px;
  color: #94a3b8;
  font-weight: 400;
  margin: 3px 0 0 0;
}
.exw-roadmap-tools {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.exw-roadmap-search-wrap {
  position: relative;
}
.exw-roadmap-search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  font-size: 16px;
  pointer-events: none;
}
.exw-roadmap-search {
  padding: 6px 14px 6px 34px;
  font-size: 12px;
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 9999px;
  color: #334155;
  width: 175px;
  outline: none;
  transition: all 0.15s ease;
}
.exw-roadmap-search:focus {
  background-color: #ffffff;
  border-color: #3b82f6;
  box-shadow: 0 0 0 1px #3b82f6;
  width: 210px;
}
.exw-roadmap-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 500;
  background-color: #f0f9ff;
  color: #0284c7;
  border: 1px solid #e0f2fe;
}
.exw-roadmap-tabs {
  display: inline-flex;
  padding: 2px;
  background: #f1f5f9;
  border-radius: 9999px;
  font-size: 12px;
  border: 1px solid #e2e8f0;
}
.exw-roadmap-tab {
  padding: 3px 10px;
  border-radius: 9999px;
  border: none;
  background: transparent;
  color: #64748b;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}
.exw-roadmap-tab.active {
  background: #ffffff;
  color: #0f172a;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

/* Timeline Layout */
.exw-timeline-item {
  display: flex;
  align-items: flex-start;
  position: relative;
}
.exw-timeline-spine {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 20px;
  align-self: stretch;
  flex-shrink: 0;
  position: relative;
  width: 32px;
}
@media (max-width: 640px) {
  .exw-timeline-spine {
    margin-right: 12px;
  }
}
.exw-timeline-node {
  width: 32px;
  height: 32px;
  border-radius: 9999px;
  background-color: #0b1527;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 500;
  z-index: 10;
  flex-shrink: 0;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.12);
  outline: 4px solid #ffffff;
}
.exw-timeline-line {
  width: 2px;
  background-color: #3b82f6;
  position: absolute;
  top: 32px;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  z-index: 0;
}
.exw-timeline-card {
  flex: 1;
  margin-bottom: 20px;
  border-radius: 16px;
  background-color: #f8fafc;
  border: 1px solid #f1f5f9;
  padding: 16px 20px;
  transition: all 0.15s ease;
  cursor: pointer;
  text-align: left;
}
.exw-timeline-card:hover {
  background-color: #f1f5f9;
  border-color: #e2e8f0;
}
.exw-card-top {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.exw-pill-time {
  display: inline-flex;
  align-items: center;
  padding: 2.5px 10px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 500;
  background-color: #f0f9ff;
  color: #0284c7;
  border: 1px solid #e0f2fe;
  letter-spacing: 0.02em;
}
.exw-pill-room {
  display: inline-flex;
  align-items: center;
  padding: 2.5px 10px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 400;
  background-color: #f1f5f9;
  color: #475569;
}
.exw-card-format {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 400;
}
.exw-card-title {
  font-size: 15px;
  font-weight: 500;
  color: #0f172a;
  margin: 10px 0 4px 0;
  line-height: 1.35;
}
.exw-timeline-card:hover .exw-card-title {
  color: #2563eb;
}
.exw-card-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 2px;
}
.exw-card-desc {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 400;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.exw-card-action {
  font-size: 12px;
  font-weight: 500;
  color: #2563eb;
  display: inline-flex;
  align-items: center;
  gap: 2px;
  flex-shrink: 0;
  text-decoration: none;
}
.exw-card-action:hover {
  color: #1d4ed8;
}

/* Dark mode adjustments */
[data-theme="dark"] .exw-roadmap-card {
  background: #1e293b;
  border-color: #334155;
}
[data-theme="dark"] .exw-roadmap-head {
  border-color: #334155;
}
[data-theme="dark"] .exw-roadmap-title {
  color: #f8fafc;
}
[data-theme="dark"] .exw-roadmap-search {
  background: #0f172a;
  border-color: #334155;
  color: #e2e8f0;
}
[data-theme="dark"] .exw-roadmap-tabs {
  background: #0f172a;
  border-color: #334155;
}
[data-theme="dark"] .exw-roadmap-tab.active {
  background: #1e293b;
  color: #f8fafc;
}
[data-theme="dark"] .exw-timeline-node {
  outline-color: #1e293b;
}
[data-theme="dark"] .exw-timeline-card {
  background-color: #0f172a;
  border-color: #334155;
}
[data-theme="dark"] .exw-timeline-card:hover {
  background-color: #1e293b;
}
[data-theme="dark"] .exw-card-title {
  color: #f8fafc;
}
[data-theme="dark"] .exw-pill-room {
  background-color: #1e293b;
  color: #cbd5e1;
}
"""

if "SUBSEQUENT EXAMINATIONS ROADMAP" not in css:
    css += "\n" + roadmap_css
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("Added roadmap CSS to assets/css/exams-simple.css")
else:
    print("Roadmap CSS already present")

# ==========================================
# 2. UPDATE assets/js/exams-simple.js
# ==========================================
js_path = 'assets/js/exams-simple.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Helper functions to inject before studentShell
helpers_code = """  function formatTime12(timeStr) {
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
"""

# Replace studentShell
old_student_shell = """  function studentShell() {
    shell({
      title: 'My Examination Schedule',
      subtitle: deptContext
        ? 'Published ' + deptLabel + ' examinations for your enrolled classes only.'
        : 'Published examinations for your enrolled classes only.',
      body:
        '<section class="exw-card exw-section">' +
          '<div class="exw-tabs">' +
            '<button type="button" class="exw-tab' + (state.tab === 'upcoming' ? ' active' : '') + '" data-action="tab" data-tab="upcoming">Upcoming</button>' +
            '<button type="button" class="exw-tab' + (state.tab === 'completed' ? ' active' : '') + '" data-action="tab" data-tab="completed">Completed</button>' +
          '</div>' +
          '<div class="exw-toolbar">' + selectFilters(false) + '</div>' +
        '</section>' +
        '<section class="exw-section"><div id="exwList"></div></section>'
    });
  }"""

new_student_shell = helpers_code + """  function studentShell() {
    root.innerHTML =
      '<div class="exw max-w-5xl mx-auto py-6 px-4 sm:px-6">' +
        '<div class="exw-roadmap-card">' +
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
                '<input type="text" id="roadmapFilter" placeholder="Filter subjects..." value="' + esc(state.q) + '" class="exw-roadmap-search">' +
              '</div>' +
              // Queued Badge
              '<span class="exw-roadmap-badge" id="roadmapQueuedBadge">' +
                '<span id="roadmapQueuedCount">5</span>&nbsp;Queued' +
              '</span>' +
              // Tabs Switcher
              '<div class="exw-roadmap-tabs">' +
                '<button type="button" class="exw-roadmap-tab ' + (state.tab === 'upcoming' ? 'active' : '') + '" data-action="tab" data-tab="upcoming">Upcoming</button>' +
                '<button type="button" class="exw-roadmap-tab ' + (state.tab === 'completed' ? 'active' : '') + '" data-action="tab" data-tab="completed">Completed</button>' +
              '</div>' +
            '</div>' +
          '</div>' +
          // Timeline Content
          '<div id="exwList"></div>' +
        '</div>' +
      '</div>';
  }"""

if old_student_shell in js:
    js = js.replace(old_student_shell, new_student_shell, 1)
    print("Replaced studentShell")
else:
    print("Could not find old_student_shell")

# Replace renderStudent
old_render_student = """  function renderStudent() {
    var all = state.exams;
    var items = filteredExams();
    renderCounts(all);
    var box = document.getElementById('exwList');
    if (!box) return;
    if (!items.length) {
      box.innerHTML = emptyState(
        state.tab === 'upcoming' ? 'No upcoming examinations' : 'No completed examinations',
        'Published schedules for your enrolled classes will appear here automatically.'
      );
      return;
    }
    var deptCount = {};
    var subjectCount = {};
    all.forEach(function (e) {
      deptCount[e.department] = (deptCount[e.department] || 0) + 1;
      subjectCount[e.subject] = (subjectCount[e.subject] || 0) + 1;
    });
    var showDept = !deptContext && (Object.keys(deptCount).length > 1 ||
      Object.keys(subjectCount).some(function (s) { return subjectCount[s] > 1; }));
    box.innerHTML = '<ul class="exw-list">' + items.map(function (e) { return examCard(e, showDept); }).join('') + '</ul>';
  }"""

new_render_student = """  function renderStudent() {
    var all = state.exams;
    var items = filteredExams();
    var box = document.getElementById('exwList');
    var badgeCount = document.getElementById('roadmapQueuedCount');
    var badgeWrap = document.getElementById('roadmapQueuedBadge');
    var titleEl = document.getElementById('roadmapTitle');
    var subEl = document.getElementById('roadmapSubtitle');

    if (badgeCount) badgeCount.textContent = items.length;
    if (badgeWrap) {
      badgeWrap.style.display = state.tab === 'upcoming' ? '' : 'none';
    }
    if (titleEl) {
      titleEl.textContent = state.tab === 'upcoming'
        ? 'Subsequent Examinations Roadmap'
        : 'Completed Examinations History';
    }
    if (subEl) {
      subEl.textContent = state.tab === 'upcoming'
        ? 'Chronological progression through July 2026 evaluations'
        : 'Past examination results and performance archive';
    }

    if (!box) return;
    if (!items.length) {
      box.innerHTML = emptyState(
        state.tab === 'upcoming' ? 'No upcoming examinations queued' : 'No completed examinations recorded',
        'Published schedules for your enrolled classes will appear here automatically.'
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
      var isLast = idx === sorted.length - 1;
      var d = dateParts(e.exam_date);
      var dayStr = String(d.day || '01').padStart(2, '0');
      var monthStr = (d.month || 'JUL').toUpperCase();

      var timeStr = formatTime12(e.start_time) + ' – ' + formatTime12(e.end_time);
      var roomStr = esc(e.room || e.location || (e.classes && e.classes[0] ? e.classes[0] : 'Room 302'));
      var noteStr = esc(e.evaluator_note || e.format || (e.teacher ? e.teacher + ' • ' + (e.exam_type_label || 'Test') : (e.exam_type_label || 'Standard Exam')));
      var descStr = esc(e.instructions || e.topics || e.description || e.notes || (e.subject + ' • ' + (e.exam_type_label || 'Evaluation')));
      var linkText = getContextualLinkText(e);

      html +=
        '<div class="exw-timeline-item">' +
          '<div class="exw-timeline-spine">' +
            '<div class="exw-timeline-node">' + dayStr + '</div>' +
            (!isLast ? '<div class="exw-timeline-line"></div>' : '') +
          '</div>' +
          '<div class="exw-timeline-card" data-action="view" data-id="' + esc(e.id) + '">' +
            '<div class="exw-card-top">' +
              '<div class="flex items-center gap-2 flex-wrap">' +
                '<span class="exw-pill-time">' + dayStr + ' ' + monthStr + ' • ' + timeStr + '</span>' +
                '<span class="exw-pill-room">' + roomStr + '</span>' +
              '</div>' +
              '<div class="exw-card-format">' + noteStr + '</div>' +
            '</div>' +
            '<h3 class="exw-card-title">' + esc(e.title || e.subject) + '</h3>' +
            '<div class="exw-card-bottom">' +
              '<div class="exw-card-desc">' + descStr + '</div>' +
              '<a class="exw-card-action" href="#" onclick="event.preventDefault();">' +
                '<span>' + esc(linkText) + '</span>' +
                '<span class="material-symbols-outlined text-[15px]">chevron_right</span>' +
              '</a>' +
            '</div>' +
          '</div>' +
        '</div>';
    });

    html += '</div>';
    box.innerHTML = html;
  }"""

if old_render_student in js:
    js = js.replace(old_render_student, new_render_student, 1)
    print("Replaced renderStudent")
else:
    print("Could not find old_render_student")

# Fix filteredExams search for students
old_filtered = """      if (ROLE === 'student') {
        if (state.tab === 'upcoming') {
          return !e.completed && isUpcoming(e);
        }
        if (state.tab === 'completed') {
          return e.completed || !isUpcoming(e);
        }
        return true;
      }"""

new_filtered = """      if (ROLE === 'student') {
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
      }"""

if old_filtered in js:
    js = js.replace(old_filtered, new_filtered, 1)
    print("Replaced filteredExams for student")
else:
    print("Could not find old_filtered")

# Listen to roadmapFilter in input event
old_input = """  root.addEventListener('input', function (event) {
    if (event.target.id !== 'exwQ') return;
    clearTimeout(searchTimer);
    var value = event.target.value;
    searchTimer = setTimeout(function () { state.q = value; render(); }, 180);
  });"""

new_input = """  root.addEventListener('input', function (event) {
    if (event.target.id !== 'exwQ' && event.target.id !== 'roadmapFilter') return;
    clearTimeout(searchTimer);
    var value = event.target.value;
    searchTimer = setTimeout(function () { state.q = value; render(); }, 180);
  });"""

if old_input in js:
    js = js.replace(old_input, new_input, 1)
    print("Replaced input handler")
else:
    print("Could not find old_input")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("Successfully updated assets/js/exams-simple.js!")
