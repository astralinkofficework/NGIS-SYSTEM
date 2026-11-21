import re

js_path = 'assets/js/exams-simple.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update isUpcoming
old_is_upcoming = """  function isUpcoming(exam) {
    var stamp = String(exam.exam_date || '') + 'T' + String(exam.end_time || '23:59') + ':00';
    var when = new Date(stamp);
    return isNaN(when.getTime()) || when.getTime() >= Date.now();
  }"""

new_is_upcoming = """  function isUpcoming(exam) {
    if (exam && exam.is_demo) return true;
    var stamp = String(exam.exam_date || '') + 'T' + String(exam.end_time || '23:59') + ':00';
    var when = new Date(stamp);
    return isNaN(when.getTime()) || when.getTime() >= Date.now();
  }"""

if old_is_upcoming in js:
    js = js.replace(old_is_upcoming, new_is_upcoming, 1)
    print("Updated isUpcoming")
else:
    print("isUpcoming pattern not exact, checking alternative...")
    js = re.sub(
        r'function isUpcoming\(exam\)\s*\{',
        'function isUpcoming(exam) {\n    if (exam && exam.is_demo) return true;',
        js,
        count=1
    )
    print("Injected is_demo check into isUpcoming")

# 2. Update studentShell to cleanly match the screenshot
# We can find studentShell definition
pattern_shell = r'function studentShell\(\)\s*\{[\s\S]*?^\s*\}'
new_student_shell = """function studentShell() {
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
            '</div>' +
          '</div>' +
          // Timeline Content
          '<div id="exwList"></div>' +
        '</div>' +
      '</div>';
  }"""

js = re.sub(pattern_shell, new_student_shell, js, count=1, flags=re.MULTILINE)
print("Updated studentShell")

# 3. Update renderStudent
pattern_render = r'function renderStudent\(\)\s*\{[\s\S]*?^\s*\}'
new_render_student = """function renderStudent() {
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
  }"""

js = re.sub(pattern_render, new_render_student, js, count=1, flags=re.MULTILINE)
print("Updated renderStudent")

# 4. Update the demo fallback dataset for students in reload()
# Find the demoExams array definition
pattern_demo = r'var demoExams = \[\s*\{[\s\S]*?\}\s*\];'
new_demo = """var demoExams = [
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
          ];"""

js = re.sub(pattern_demo, new_demo, js, count=1)
print("Updated demo fallback dataset")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("Saved assets/js/exams-simple.js successfully!")
