with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Let's locate from `function renderStudent()` up to `function rowActions(e)`
start_marker = "  function renderStudent() {"
end_marker = "  function rowActions(e) {"

start_pos = js.find(start_marker)
end_pos = js.find(end_marker)

print(f"start: {start_pos}, end: {end_pos}")

clean_render_student = """  function renderStudent() {
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
              '<div class="exw-card-desc" title="' + descStr + '">' + descStr + '</div>' +
              '<a class="exw-card-action" href="#" data-action="view" data-id="' + esc(e.id) + '">' +
                '<span>' + esc(linkText) + '</span>' +
                '<span style="font-size: 14px; font-weight: 500; margin-left: 2px;">&rsaquo;</span>' +
              '</a>' +
            '</div>' +
          '</div>' +
        '</div>';
    });

    html += '</div>';
    box.innerHTML = html;
  }

"""

if start_pos != -1 and end_pos != -1:
    js = js[:start_pos] + clean_render_student + js[end_pos:]
    with open('assets/js/exams-simple.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Fixed renderStudent in assets/js/exams-simple.js!")
else:
    print("Could not find start or end pos!")
