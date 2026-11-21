/* ══════════════════════════════════════════════════════════════
   NGIS STUDENT PORTAL — MASTER ACADEMIC WORKSPACE ENGINE
   ManageBac-Inspired Architecture · Production-Ready Student Hub
   ══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* ── 1. Student Identity Data ── */
  var STUDENT = {
    name: 'Seila Hok',
    fullName: 'Nrinphouneta Seila Hok',
    id: '2026-STD-0142',
    grade: 'Grade 12',
    school: 'NGIS International School',
    section: '12A',
    email: 'seila.hok@ngis.edu.kh',
    gpa: '3.88 / 4.00',
    avatar: '../../assets/images/dashboard-student-portrait.jpg',
    initials: 'SO'
  };

  /* ── 2. Today's Classes Data (7 Periods) ── */
  var TODAY_CLASSES = [
    {
      id: 'cls-today-1',
      time: '07:00 – 07:50',
      subject: 'Khmer Literature',
      gradeRoom: '12A · Room A302',
      teacher: 'Mr. Chhem Sokha',
      dept: 'Khmer Studies Department',
      active: true,
      room: 'Room A302'
    },
    {
      id: 'cls-today-2',
      time: '07:50 – 08:40',
      subject: 'English',
      gradeRoom: '12A · Room A302',
      teacher: 'Mr. James Miller',
      dept: 'English Department',
      active: false,
      room: 'Room A302'
    },
    {
      id: 'cls-today-3',
      time: '08:40 – 09:30',
      subject: 'Mathematics',
      gradeRoom: '12A · Room A203',
      teacher: 'Mr. David Wilson',
      dept: 'Mathematics Department',
      active: false,
      room: 'Room A203'
    },
    {
      id: 'cls-today-4',
      time: '09:50 – 10:40',
      subject: 'Physics',
      gradeRoom: '12A · Science Lab 1',
      teacher: 'Dr. Elizabeth Chen',
      dept: 'Science & STEM Department',
      active: false,
      room: 'Science Lab 1'
    },
    {
      id: 'cls-today-5',
      time: '10:40 – 11:30',
      subject: 'Chemistry',
      gradeRoom: '12A · Science Lab 2',
      teacher: 'Mr. Robert Taylor',
      dept: 'Science & STEM Department',
      active: false,
      room: 'Science Lab 2'
    },
    {
      id: 'cls-today-6',
      time: '13:00 – 13:50',
      subject: 'History & Civics',
      gradeRoom: '12A · Room B104',
      teacher: 'Mrs. Emily Watson',
      dept: 'Social Studies Department',
      active: false,
      room: 'Room B104'
    },
    {
      id: 'cls-today-7',
      time: '13:50 – 14:40',
      subject: 'Computer Science & ICT',
      gradeRoom: '12A · ICT Lab 2',
      teacher: 'Mr. Alex Turner',
      dept: 'Computer Science Department',
      active: false,
      room: 'ICT Lab 2'
    }
  ];

  /* ── 3. Tasks & Deadlines Data (ManageBac-inspired) ── */
  var currentTaskTab = 'upcoming';

  var UPCOMING_TASKS = [
    {
      id: 'task-1',
      title: '8.1 & 8.2 ENG LL - Creative summative',
      due: 'May 29, 11:00 AM',
      dueFull: 'Thursday, May 29, 2026 at 11:00 AM',
      course: 'IB MYP Language and Literature - English 8.2:2425 (Grade 8) 2',
      subject: 'English Language & Literature',
      tags: ['Summative'],
      status: 'Pending',
      points: '100 points',
      teacher: 'Ms. Sarah Collins',
      description: 'Produce a 750-word creative prose piece demonstrating character development and sensory imagery according to Criterion A & C.'
    },
    {
      id: 'task-2',
      title: '8.3 ENG LL - Creative task due',
      due: 'May 28, 12:30 PM',
      dueFull: 'Wednesday, May 28, 2026 at 12:30 PM',
      course: 'IB MYP Language and Literature - English 8.2:2425 (Grade 8) 2',
      subject: 'English Language & Literature',
      tags: ['Summative'],
      status: 'Pending',
      points: '80 points',
      teacher: 'Ms. Sarah Collins',
      description: 'Submit final edited manuscript draft with peer evaluation annotation notes.'
    },
    {
      id: 'task-3',
      title: '8.2 Summative Opening Speeches',
      due: 'Apr 29, 7:30 AM',
      dueFull: 'Wednesday, Apr 29, 2026 at 7:30 AM',
      course: 'IB MYP Individuals and Societies 8.2:2425 (Grade 8) 2',
      subject: 'Individuals & Societies',
      tags: ['Summative'],
      status: 'Pending',
      points: '50 points',
      teacher: 'Dr. Pichdara Pen',
      description: 'Prepare and deliver a 3-minute opening statement arguing an environmental policy case.'
    },
    {
      id: 'task-4',
      title: 'Khmer Grade 8-9 Summative Assessment Crit. C & D',
      due: 'Mar 14, 2:10 PM',
      dueFull: 'Saturday, Mar 14, 2026 at 2:10 PM',
      course: 'IB MYP Language and Literature - Khmer 8/9 BC:2425 (Grade 8) 1',
      subject: 'Khmer Language & Literature',
      tags: ['Summative'],
      status: 'Pending',
      points: '100 points',
      teacher: 'Lokru Sokha Mean',
      description: 'Analyze stylistic devices and classical syntax in the selected Tum Teav excerpt.'
    },
    {
      id: 'task-5',
      title: 'Khmer Grade 8-9 Summative Assessment Crit. A & B',
      due: 'Feb 14, 2:10 PM',
      dueFull: 'Saturday, Feb 14, 2026 at 2:10 PM',
      course: 'IB MYP Language and Literature - Khmer 8/9 BC:2425 (Grade 8) 1',
      subject: 'Khmer Language & Literature',
      tags: ['Summative'],
      status: 'Pending',
      points: '100 points',
      teacher: 'Lokru Sokha Mean',
      description: 'Compose a structured comparative critique exploring thematic character traits.'
    },
    {
      id: 'task-6',
      title: 'Khmer Grade 8-9 Formative Assessment',
      due: 'Feb 6, 2:00 PM',
      dueFull: 'Friday, Feb 6, 2026 at 2:00 PM',
      course: 'IB MYP Language and Literature - Khmer 8/9 BC:2425 (Grade 8) 1',
      subject: 'Khmer Language & Literature',
      tags: ['Formative'],
      status: 'Pending',
      points: '40 points',
      teacher: 'Lokru Sokha Mean',
      description: 'Grammar syntax drill and paragraph construction practice worksheet.'
    }
  ];

  var PAST_TASKS = [
    {
      id: 'past-1',
      title: 'Essay – Criminal Justice',
      due: 'Submitted Nov 20, 2026',
      dueFull: 'Friday, Nov 20, 2026 at 4:30 PM',
      course: 'Law 12A · Dr. Pichdara Pen',
      subject: 'Constitutional Law',
      tags: ['Summative'],
      status: 'Graded',
      points: '92 / 100 pts',
      teacher: 'Dr. Pichdara Pen',
      description: 'Analyze procedural protections under Article 38 of the Constitutional Law.'
    },
    {
      id: 'past-2',
      title: 'Case Study Analysis',
      due: 'Submitted Nov 15, 2026',
      dueFull: 'Sunday, Nov 15, 2026 at 11:59 PM',
      course: 'Criminology 12A · Ms. Sreynich',
      subject: 'Criminology',
      tags: ['Summative'],
      status: 'Graded',
      points: '48 / 50 pts',
      teacher: 'Ms. Sreynich',
      description: 'Evaluate the juvenile rehabilitation frameworks in urban secondary environments.'
    },
    {
      id: 'past-3',
      title: 'Calculus Problem Set 03 — Derivative Theorems',
      due: 'Submitted Nov 10, 2026',
      dueFull: 'Tuesday, Nov 10, 2026 at 10:00 AM',
      course: 'Mathematics 12A · Mr. Chea Sophea',
      subject: 'Advanced Mathematics',
      tags: ['Formative'],
      status: 'Graded',
      points: '100 / 100 pts',
      teacher: 'Mr. Chea Sophea',
      description: 'Differential calculus foundational rules and limit optimization theorems.'
    }
  ];

  var OVERDUE_TASKS = [
    {
      id: 'overdue-1',
      title: 'Research Proposal – Constitutional Precedent',
      due: 'Nov 12, 11:59 PM (9d overdue)',
      dueFull: 'Thursday, Nov 12, 2026 at 11:59 PM',
      course: 'Law 12A · Dr. Pichdara Pen',
      subject: 'Constitutional Law',
      tags: ['Summative'],
      status: 'Overdue',
      points: '75 points',
      teacher: 'Dr. Pichdara Pen',
      description: 'Draft a 3-page research prospectus on statutory interpretation frameworks.'
    },
    {
      id: 'overdue-2',
      title: 'Literature Comparative Critique Draft',
      due: 'Nov 08, 05:00 PM (13d overdue)',
      dueFull: 'Sunday, Nov 08, 2026 at 5:00 PM',
      course: 'IB MYP Language and Literature - English 8.2',
      subject: 'English Language & Literature',
      tags: ['Summative'],
      status: 'Overdue',
      points: '100 points',
      teacher: 'Ms. Sarah Collins',
      description: 'Comparative critique draft on post-war modernist poetry.'
    },
    {
      id: 'overdue-3',
      title: 'Physics Thermodynamics Lab Report',
      due: 'Nov 05, 04:00 PM (16d overdue)',
      dueFull: 'Thursday, Nov 05, 2026 at 4:00 PM',
      course: 'Science 12A · Dr. Sarah Jenkins',
      subject: 'Physics',
      tags: ['Summative'],
      status: 'Overdue',
      points: '60 points',
      teacher: 'Dr. Sarah Jenkins',
      description: 'Calorimetry experimental calculations and error bounds synthesis.'
    },
    {
      id: 'overdue-4',
      title: 'Criminology Urban Juvenile Field Report',
      due: 'Nov 01, 11:59 PM (20d overdue)',
      dueFull: 'Sunday, Nov 01, 2026 at 11:59 PM',
      course: 'Criminology 12A · Ms. Sreynich',
      subject: 'Criminology',
      tags: ['Formative'],
      status: 'Overdue',
      points: '50 points',
      teacher: 'Ms. Sreynich',
      description: 'Field observation notes summary on urban secondary community outreach.'
    }
  ];

  var ASSIGNMENTS = UPCOMING_TASKS;

  /* ── 4. Announcements Data ── */
  var ANNOUNCEMENTS = [
    {
      id: 'ann-1',
      title: 'Graduation & Prom 2026',
      meta: 'Event · Nov 20, 2026',
      category: 'Event',
      date: 'Nov 20, 2026',
      author: 'Office of Student Affairs',
      image: '../../assets/images/news-graduation.jpg',
      icon3d: 'confetti.png',
      summary: 'Commencement rehearsal schedules, venue seating allocations, and prom ticket reservations are officially available for Grade 12 cohorts starting this week.',
      body: 'Commencement rehearsal schedules, venue seating allocations, and prom ticket reservations are officially available for Grade 12 cohorts starting this week. Please visit the student affairs counter in Building A to confirm your guest headcount.'
    },
    {
      id: 'ann-2',
      title: 'University Application Workshop',
      meta: 'Academic · Nov 18, 2026',
      category: 'Academic',
      date: 'Nov 18, 2026',
      author: 'Academic Counseling Department',
      image: '../../assets/images/news-workshop.jpg',
      icon3d: 'graduation-cap.png',
      summary: 'Interactive guidance session on personal essays, Common App submissions, scholarship essays, and counselor recommendation letters in Hall A.',
      body: 'Interactive guidance session on personal essays, Common App submissions, scholarship essays, and counselor recommendation letters in Hall A. All Grade 11 and 12 students are strongly encouraged to bring their preliminary CV drafts.'
    },
    {
      id: 'ann-3',
      title: 'KNY 2026 – School Event',
      meta: 'Event · Nov 15, 2026',
      category: 'Event',
      date: 'Nov 15, 2026',
      author: 'Campus Activities Council',
      image: '../../assets/images/news-festival.jpg',
      icon3d: 'confetti.png',
      summary: 'Annual campus-wide cultural festivities, student exhibitions, and traditional sports games schedule now published on the main campus bulletin.',
      body: 'Annual school-wide cultural festivities, student exhibitions, and traditional sports schedules have been posted on the main campus board. Volunteer sign-ups for food stalls and stage management close this Friday.'
    }
  ];

  /* ── 5. My Classes Data ── */
  var MY_CLASSES = [
    {
      id: 'cls-1',
      name: 'Law',
      code: 'LAW-1201',
      meta: '12A · Dr. Pichdara Pen',
      dept: 'Social Sciences & Jurisprudence',
      teacher: 'Dr. Pichdara Pen',
      room: 'Room B101',
      icon3d: 'open-book.png',
      lessons: 14,
      assignments: 4,
      overview: 'Introduction to legal methodologies, jurisprudence fundamentals, and comparative institutional frameworks.'
    },
    {
      id: 'cls-2',
      name: 'Criminology',
      code: 'CRIM-1202',
      meta: '12A · Ms. Sreynich',
      dept: 'Social Sciences Department',
      teacher: 'Ms. Sreynich',
      room: 'Room B104',
      icon3d: 'business-report.png',
      lessons: 12,
      assignments: 3,
      overview: 'Sociological theories of crime, behavioral analytics, deterrence mechanisms, and modern juvenile justice systems.'
    },
    {
      id: 'cls-3',
      name: 'English',
      code: 'ENG-1201',
      meta: '12A · Mr. James Miller',
      dept: 'English Language & Literature',
      teacher: 'Mr. James Miller',
      room: 'Room A302',
      icon3d: 'books.png',
      lessons: 18,
      assignments: 5,
      overview: 'Advanced rhetoric, critical analysis of 20th-century literature, composition, and academic research synthesis.'
    },
    {
      id: 'cls-4',
      name: 'Mathematics',
      code: 'MATH-1201',
      meta: '12A · Mr. David Wilson',
      dept: 'Mathematics Department',
      teacher: 'Mr. David Wilson',
      room: 'Room A203',
      icon3d: 'calculator.png',
      lessons: 20,
      assignments: 6,
      overview: 'Calculus, discrete probability distributions, matrix algebra, and vector calculus applications.'
    },
    {
      id: 'cls-5',
      name: 'Khmer Literature',
      code: 'KHM-1201',
      meta: '12A · Mr. Chhem Sokha',
      dept: 'Khmer Studies Department',
      teacher: 'Mr. Chhem Sokha',
      room: 'Room A302',
      icon3d: 'open-book.png',
      lessons: 16,
      assignments: 4,
      overview: 'Classical Khmer prose, poetry analysis, cultural heritage studies, and advanced literary composition.'
    },
    {
      id: 'cls-6',
      name: 'Mandarin Chinese',
      code: 'CHN-1201',
      meta: '12A · Ms. Li Wei',
      dept: 'Chinese Language Department',
      teacher: 'Ms. Li Wei',
      room: 'Room C105',
      icon3d: 'compass.png',
      lessons: 15,
      assignments: 3,
      overview: 'HSK Level 4 curriculum, conversational syntax, reading comprehension, and character stroke mastery.'
    }
  ];

  /* ── 6. Weekly Calendar State & Events ── */
  // Base date anchor: Nov 16 to Nov 22, 2026
  var currentWeekOffset = 0;
  var ANCHOR_DATE = new Date(2026, 10, 21); // Saturday Nov 21, 2026

  var WEEK_EVENTS_DB = {
    '2026-11-16': [{ title: 'Law Project', time: 'Due', type: 'due' }],
    '2026-11-18': [{ title: 'Workshop', time: '14:00', type: 'event' }],
    '2026-11-20': [{ title: 'Career Talk', time: '10:00', type: 'event' }],
    '2026-11-21': [{ title: 'Library Study', time: '09:00', type: 'event' }]
  };

  /* Helper to format Date */
  function formatDate(d) {
    var year = d.getFullYear();
    var month = String(d.getMonth() + 1).padStart(2, '0');
    var day = String(d.getDate()).padStart(2, '0');
    return year + '-' + month + '-' + day;
  }

  var MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var FULL_MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var DAY_NAMES = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  /* ── 7. Render Today's Classes ── */
  function renderTodayClasses() {
    var container = document.getElementById('todayClassesList');
    if (!container) return;

    if (!TODAY_CLASSES.length) {
      container.innerHTML =
        '<div class="workspace-empty-state">' +
          '<img src="../../assets/images/icons-3d/empty-box.png" width="48" height="48" class="ngis-3d-icon" alt="No classes">' +
          '<span>No scheduled classes for today.</span>' +
        '</div>';
      return;
    }

    container.innerHTML = TODAY_CLASSES.map(function (cls) {
      return (
        '<div class="workspace-row workspace-row-preview is-preview" data-class-id="' + cls.id + '">' +
          '<div class="workspace-row-left">' +
            '<span class="workspace-row-time">' + cls.time + '</span>' +
            '<span class="workspace-status-dot" aria-hidden="true"></span>' +
            '<div class="workspace-row-info">' +
              '<div class="workspace-row-heading">' + cls.subject + '</div>' +
              '<div class="workspace-row-sub">' + cls.gradeRoom + '</div>' +
            '</div>' +
          '</div>' +
          '<span data-ngis-icon="chevronRight" class="workspace-row-chevron" aria-hidden="true"></span>' +
        '</div>'
      );
    }).join('');

    if (window.NGIS && typeof window.NGIS.hydrateIcons === 'function') {
      window.NGIS.hydrateIcons(container);
    }
  }

  /* ── 8. Render Tasks & Deadlines (ManageBac-inspired) ── */
  function renderUpcomingAssignments() {
    var container = document.getElementById('upcomingAssignmentsList');
    if (!container) return;

    var currentList = currentTaskTab === 'past'
      ? PAST_TASKS
      : currentTaskTab === 'overdue'
        ? OVERDUE_TASKS
        : UPCOMING_TASKS;

    if (!currentList.length) {
      container.innerHTML =
        '<div class="workspace-empty-state" style="padding: 36px 16px; text-align: center;">' +
          '<img src="../../assets/images/icons-3d/ok.png" width="48" height="48" class="ngis-3d-icon" alt="No Tasks" style="margin-bottom:8px;">' +
          '<div style="font-size: 14px; font-weight: 500; color: #29352E;">No Tasks</div>' +
          '<p style="font-size: 12px; color: #64746A; margin: 4px 0 0;">There are no ' + currentTaskTab + ' tasks at this time.</p>' +
        '</div>';
      return;
    }

    container.innerHTML = currentList.map(function (task) {
      // Deduplicate tags defensively (Phase 5 rule)
      var uniqueTags = [];
      (task.tags || []).forEach(function (t) {
        if (uniqueTags.indexOf(t) === -1) uniqueTags.push(t);
      });

      var tagsHtml = uniqueTags.map(function (tg) {
        var cls = tg === 'Formative' ? 'workspace-task-tag-formative' : 'workspace-task-tag-summative';
        return '<span class="workspace-task-tag ' + cls + '">' + tg + '</span>';
      }).join(' ');

      var statusCls = task.status === 'Graded'
        ? 'workspace-task-status-graded'
        : task.status === 'Overdue'
          ? 'workspace-task-status-overdue'
          : 'workspace-task-status-pending';

      var statusText = task.status === 'Graded'
        ? (task.points || 'Graded')
        : task.status === 'Overdue'
          ? 'Overdue'
          : 'Pending';

      var btnClass = task.status === 'Overdue'
        ? 'workspace-task-submit-btn btn-overdue'
        : task.status === 'Graded'
          ? 'workspace-task-submit-btn btn-graded'
          : 'workspace-task-submit-btn';

      var btnLabel = task.status === 'Graded' ? 'View Evaluation' : 'Submit Coursework';
      var btnIcon = task.status === 'Graded' ? 'view' : 'upload';
      var courseName = task.course || task.subject || '';

      return (
        '<article class="workspace-task-card-row" data-task-id="' + task.id + '" title="View ' + task.title + '">' +
          '<div class="workspace-task-header">' +
            '<div class="workspace-task-icon-wrap">' +
              '<img src="../../assets/images/icons-3d/notepad.png" width="20" height="20" class="ngis-3d-icon" alt="" style="background:transparent!important;">' +
            '</div>' +
            '<div class="workspace-task-title-wrap">' +
              '<span class="workspace-task-title-text" onclick="event.stopPropagation(); window.NGISWorkspace.openTaskDetail(\'' + task.id + '\')">' + task.title + '</span>' +
              '<button type="button" class="workspace-task-info-trigger" onclick="event.stopPropagation(); window.NGISWorkspace.openTaskDetail(\'' + task.id + '\')" title="Task details &amp; rubric" aria-label="Details">ⓘ</button>' +
            '</div>' +
          '</div>' +
          '<div class="workspace-task-course-line">' +
            '<span class="workspace-task-course" title="' + courseName + '">' + courseName + '</span>' +
          '</div>' +
          '<div class="workspace-task-meta-action-row">' +
            '<div class="workspace-task-meta-group">' +
              '<span class="workspace-task-time"><span data-ngis-icon="alarmClock"></span> ' + task.due + '</span>' +
              '<span class="workspace-task-status ' + statusCls + '">' + statusText + '</span>' +
            '</div>' +
          '<div class="workspace-task-action-wrap">' +
            '<button type="button" class="' + btnClass + '" onclick="event.stopPropagation(); window.NGISWorkspace.openTaskDetail(\'' + task.id + '\')">' +
              '<span data-ngis-icon="' + btnIcon + '"></span>' +
              '<span>' + btnLabel + '</span>' +
            '</button>' +
            '</div>' +
          '</div>' +
        '</article>'
      );
    }).join('');

    // Hydrate action icons
    if (window.NGIS && typeof window.NGIS.hydrate === 'function') {
      window.NGIS.hydrate(container);
    }
  }

  /* ── 9. Render Announcements (News Style with Picture + Text) ── */
  function renderAnnouncements() {
    var container = document.getElementById('announcementsList');
    if (!container) return;

    if (!ANNOUNCEMENTS.length) {
      container.innerHTML =
        '<div class="workspace-empty-state">' +
          '<img src="../../assets/images/icons-3d/megaphone.png" width="48" height="48" class="ngis-3d-icon" alt="Announcements">' +
          '<span>No school announcements at this time.</span>' +
        '</div>';
      return;
    }

    container.innerHTML = ANNOUNCEMENTS.map(function (ann) {
      var imgHtml = ann.image
        ? '<div class="workspace-news-thumb-wrap">' +
            '<img src="' + ann.image + '" class="workspace-news-thumb" alt="' + ann.title + '" loading="lazy">' +
          '</div>'
        : '';

      return (
        '<article class="workspace-news-row" data-ann-id="' + ann.id + '" role="button" tabindex="0" title="Read ' + ann.title + '">' +
          imgHtml +
          '<div class="workspace-news-content">' +
            '<div class="workspace-news-meta">' +
              '<span class="workspace-news-cat">' + (ann.category || 'News') + '</span>' +
              '<span class="workspace-news-dot">·</span>' +
              '<span class="workspace-news-date">' + ann.date + '</span>' +
            '</div>' +
            '<h4 class="workspace-news-title">' + ann.title + '</h4>' +
            '<p class="workspace-news-snippet">' + (ann.summary || ann.body) + '</p>' +
          '</div>' +
          '<span data-ngis-icon="chevronRight" class="workspace-news-chevron" aria-hidden="true"></span>' +
        '</article>'
      );
    }).join('');

    container.querySelectorAll('.workspace-news-row').forEach(function (row) {
      row.addEventListener('click', function () {
        var id = row.getAttribute('data-ann-id');
        var found = ANNOUNCEMENTS.find(function (a) { return a.id === id; });
        if (found) openAnnouncementModal(found);
      });
      row.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          var id = row.getAttribute('data-ann-id');
          var found = ANNOUNCEMENTS.find(function (a) { return a.id === id; });
          if (found) openAnnouncementModal(found);
        }
      });
    });
  }

  /* ── 10. Render My Classes (ManageBac Image 2 Full-Width Style) ── */
  function renderMyClasses() {
    var container = document.getElementById('myClassesList');
    if (!container) return;

    var countEl = document.getElementById('myClassesCount');
    if (countEl) countEl.textContent = MY_CLASSES.length;

    if (!MY_CLASSES.length) {
      container.innerHTML =
        '<div class="workspace-empty-state">' +
          '<img src="../../assets/images/icons-3d/books.png" width="48" height="48" class="ngis-3d-icon" alt="No classes">' +
          '<span>No enrolled classes found for this semester.</span>' +
        '</div>';
      return;
    }

    container.innerHTML = MY_CLASSES.map(function (cls) {
      var iconHtml = cls.icon3d
        ? '<img src="../../assets/images/icons-3d/' + cls.icon3d + '" width="24" height="24" class="ngis-3d-icon" alt="' + cls.name + '" loading="lazy">'
        : '<span data-ngis-icon="book" style="font-size:20px;color:#176B45;"></span>';

      var initials = (cls.teacher || 'T').split(' ').map(function(w){return w[0];}).filter(Boolean).slice(-2).join('').toUpperCase();

      return (
        '<div class="workspace-class-row" data-class-code="' + cls.code + '">' +
          '<div class="workspace-class-left">' +
            '<div class="workspace-class-icon">' + iconHtml + '</div>' +
            '<div class="workspace-class-info">' +
              '<h4 class="workspace-class-title" data-action="open-detail" role="button" tabindex="0">' + cls.name + ' · 12A (Grade 12)</h4>' +
              '<div class="workspace-class-sub">' + cls.code + ' · ' + (cls.dept || 'Academic Core') + ' · ' + (cls.room || 'Hall A') + '</div>' +
            '</div>' +
          '</div>' +
          '<div class="workspace-class-right">' +
            '<div class="workspace-class-teacher" title="' + cls.teacher + '">' +
              '<div class="workspace-teacher-avatar">' + initials + '</div>' +
              '<span class="workspace-teacher-name">' + cls.teacher + '</span>' +
            '</div>' +
            '<div class="workspace-class-actions">' +
              '<a href="student-notifications.html" class="workspace-class-icon-btn" title="Message ' + cls.teacher + '" aria-label="Message ' + cls.teacher + '">' +
                '<span data-ngis-icon="mail"></span>' +
              '</a>' +
              '<a href="student-lessons.html?class=' + encodeURIComponent(cls.code) + '" class="workspace-class-pill-btn" title="View Units & Lessons">' +
                '<span>Units</span> <span data-ngis-icon="chevronDown" style="font-size:12px;"></span>' +
              '</a>' +
              '<a href="student-assignments.html?class=' + encodeURIComponent(cls.code) + '" class="workspace-class-pill-btn" title="View Class Tasks">' +
                '<span>Tasks</span> <span data-ngis-icon="chevronDown" style="font-size:12px;"></span>' +
              '</a>' +
              '<button type="button" class="workspace-class-icon-btn" data-action="open-detail" title="Class Overview" aria-label="Class Overview">' +
                '<span data-ngis-icon="more"></span>' +
              '</button>' +
            '</div>' +
          '</div>' +
        '</div>'
      );
    }).join('');

    container.querySelectorAll('[data-action="open-detail"]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var row = btn.closest('.workspace-class-row');
        if (!row) return;
        var code = row.getAttribute('data-class-code');
        var found = MY_CLASSES.find(function (c) { return c.code === code; });
        if (found) openClassDetailModal(found);
      });
    });
  }

  /* ── 11. Render Weekly Calendar & Navigation ── */
  function getStartOfWeek(date, offsetWeeks) {
    var d = new Date(date);
    d.setDate(d.getDate() + (offsetWeeks * 7));
    var day = d.getDay();
    var diff = d.getDate() - day + (day === 0 ? -6 : 1); // Adjust when day is Sunday
    return new Date(d.setDate(diff));
  }

  function renderWeeklyCalendar() {
    var startOfWeek = getStartOfWeek(ANCHOR_DATE, currentWeekOffset);
    var endOfWeek = new Date(startOfWeek);
    endOfWeek.setDate(endOfWeek.getDate() + 6);

    // Update label range
    var rangeLabel = document.getElementById('calRangeLabel');
    if (rangeLabel) {
      var sMonth = MONTH_NAMES[startOfWeek.getMonth()];
      var eMonth = MONTH_NAMES[endOfWeek.getMonth()];
      var sYear = startOfWeek.getFullYear();
      var eYear = endOfWeek.getFullYear();

      var labelStr = sMonth + ' ' + startOfWeek.getDate() + ', ' + sYear + ' – ' +
                     eMonth + ' ' + endOfWeek.getDate() + ', ' + eYear;
      if (sMonth === eMonth && sYear === eYear) {
        labelStr = sMonth + ' ' + startOfWeek.getDate() + ' – ' + endOfWeek.getDate() + ', ' + sYear;
      }
      rangeLabel.textContent = labelStr;
    }

    var weekGrid = document.getElementById('weekGrid');
    var mobileAgenda = document.getElementById('mobileAgendaList');

    var daysHtml = '';
    var agendaHtml = '';

    var todayStr = formatDate(ANCHOR_DATE);

    for (var i = 0; i < 7; i++) {
      var curDay = new Date(startOfWeek);
      curDay.setDate(curDay.getDate() + i);

      var curDayStr = formatDate(curDay);
      var dayName = DAY_NAMES[curDay.getDay()];
      var dayNum = curDay.getDate();
      var isToday = (curDayStr === todayStr);

      var evList = WEEK_EVENTS_DB[curDayStr] || [];

      // Desktop Column
      var eventsHtml = evList.map(function (ev) {
        var isDue = (ev.type === 'due');
        return (
          '<div class="workspace-event-block' + (isDue ? ' is-due' : '') + '" title="' + ev.title + '">' +
            '<div class="workspace-event-title">' + ev.title + '</div>' +
            '<div class="workspace-event-time">' + ev.time + '</div>' +
          '</div>'
        );
      }).join('');

      daysHtml +=
        '<div class="workspace-day-col' + (isToday ? ' is-today' : '') + '">' +
          '<div class="workspace-day-header">' +
            '<div class="workspace-day-name">' + dayName + '</div>' +
            '<span class="workspace-day-num">' + dayNum + '</span>' +
          '</div>' +
          '<div class="workspace-day-events">' +
            eventsHtml +
          '</div>' +
        '</div>';

      // Mobile Agenda Item (only if has events or is today)
      if (isToday || evList.length > 0) {
        var mobileEvents = evList.map(function (ev) {
          return (
            '<div style="font-size:12px;font-weight:500;color:#166534;background:#F0FDF4;padding:4px 8px;border-radius:4px;border-left:2px solid #16A34A;display:flex;align-items:center;justify-content:space-between;">' +
              '<span>' + ev.title + '</span>' +
              '<span style="font-size:11px;color:#15803D;">' + ev.time + '</span>' +
            '</div>'
          );
        }).join('');

        agendaHtml +=
          '<div class="workspace-agenda-day-item' + (isToday ? ' is-today' : '') + '">' +
            '<div class="workspace-agenda-day-title">' +
              '<span>' + dayName + ', ' + MONTH_NAMES[curDay.getMonth()] + ' ' + dayNum + '</span>' +
              (isToday ? '<span style="font-size:10px;background:#DCFCE7;color:#166534;padding:2px 6px;border-radius:4px;">Today</span>' : '') +
            '</div>' +
            (mobileEvents || '<div style="font-size:11px;color:#94A3B8;">No scheduled events.</div>') +
          '</div>';
      }
    }

    if (weekGrid) weekGrid.innerHTML = daysHtml;
    if (mobileAgenda) mobileAgenda.innerHTML = agendaHtml || '<div style="padding:12px;text-align:center;color:#94A3B8;font-size:12px;">No scheduled events this week.</div>';

    // Hydrate icons
    if (window.NGIS && typeof window.NGIS.hydrateIcons === 'function') {
      window.NGIS.hydrateIcons();
    }
  }

  /* ── 12. Modals & Dialog Handling ── */
  function ensureModalContainer() {
    var overlay = document.getElementById('wsModalOverlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = 'wsModalOverlay';
      overlay.className = 'workspace-modal-overlay';
      overlay.innerHTML =
        '<div class="workspace-modal-card" id="wsModalCard" role="dialog" aria-modal="true">' +
          '<div class="workspace-modal-head">' +
            '<div class="workspace-modal-title" id="wsModalTitle"></div>' +
            '<button type="button" class="workspace-modal-close" id="wsModalCloseBtn" aria-label="Close dialog">' +
              '<span data-ngis-icon="close"></span>' +
            '</button>' +
          '</div>' +
          '<div class="workspace-modal-body" id="wsModalBody"></div>' +
          '<div class="workspace-modal-foot" id="wsModalFoot"></div>' +
        '</div>';
      document.body.appendChild(overlay);

      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) closeModal();
      });

      var closeBtn = overlay.querySelector('#wsModalCloseBtn');
      if (closeBtn) closeBtn.addEventListener('click', closeModal);

      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && overlay.classList.contains('is-open')) closeModal();
      });
    }
    return overlay;
  }

  function openModal(title, bodyHtml, footHtml) {
    var overlay = ensureModalContainer();
    var titleEl = overlay.querySelector('#wsModalTitle');
    var bodyEl = overlay.querySelector('#wsModalBody');
    var footEl = overlay.querySelector('#wsModalFoot');

    if (titleEl) titleEl.innerHTML = title;
    if (bodyEl) bodyEl.innerHTML = bodyHtml;
    if (footEl) footEl.innerHTML = footHtml || '<button type="button" class="workspace-btn-secondary" onclick="document.getElementById(\'wsModalOverlay\').classList.remove(\'is-open\');">Close</button>';

    overlay.classList.add('is-open');
    document.body.style.overflow = 'hidden';

    if (window.NGIS && typeof window.NGIS.hydrateIcons === 'function') {
      window.NGIS.hydrateIcons(overlay);
    }
  }

  function closeModal() {
    var overlay = document.getElementById('wsModalOverlay');
    if (overlay) overlay.classList.remove('is-open');
    document.body.style.overflow = '';
  }

  /* Specialized Modals */
  function openClassDetailModal(cls) {
    var title = '<img src="../../assets/images/icons-3d/open-book.png" width="22" height="22" class="ngis-3d-icon" style="margin-right:8px;" alt="Class"> ' + cls.name + ' · Class Overview';
    var body =
      '<div style="display:flex;flex-direction:column;gap:14px;">' +
        '<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:14px;display:grid;grid-template-columns:1fr 1fr;gap:10px;">' +
          '<div><div style="font-size:11px;color:#64748B;">Department</div><div style="font-size:13px;font-weight:500;color:#0F172A;">' + (cls.dept || 'Academic Core') + '</div></div>' +
          '<div><div style="font-size:11px;color:#64748B;">Instructor</div><div style="font-size:13px;font-weight:500;color:#0F172A;">' + (cls.teacher || 'Assigned Faculty') + '</div></div>' +
          '<div><div style="font-size:11px;color:#64748B;">Location / Hall</div><div style="font-size:13px;font-weight:500;color:#0F172A;">' + (cls.room || 'Classroom 12A') + '</div></div>' +
          '<div><div style="font-size:11px;color:#64748B;">Current Standing</div><div style="font-size:13px;font-weight:500;color:#16A34A;">In Good Standing (92%)</div></div>' +
        '</div>' +
        '<div>' +
          '<div style="font-weight:500;margin-bottom:4px;color:#0F172A;">Syllabus &amp; Course Scope</div>' +
          '<p style="color:#475569;font-size:13px;margin:0 0 10px 0;">' + (cls.overview || 'Comprehensive course framework emphasizing critical inquiry and academic mastery.') + '</p>' +
        '</div>' +
        '<div style="border-top:1px solid #E2E8F0;padding-top:12px;display:flex;flex-direction:column;gap:8px;">' +
          '<div style="font-size:12px;font-weight:500;color:#0F172A;">Active Modules</div>' +
          '<div style="font-size:12px;color:#475569;display:flex;align-items:center;justify-content:space-between;background:#FAFBFB;padding:8px 10px;border-radius:6px;border:1px solid #E2E8F0;">' +
            '<span>Unit 1: Foundations &amp; Research</span>' +
            '<span style="color:#16A34A;font-weight:500;">Complete</span>' +
          '</div>' +
          '<div style="font-size:12px;color:#475569;display:flex;align-items:center;justify-content:space-between;background:#FAFBFB;padding:8px 10px;border-radius:6px;border:1px solid #E2E8F0;">' +
            '<span>Unit 2: Critical Case Applications</span>' +
            '<span style="color:#D97706;font-weight:500;">In Progress</span>' +
          '</div>' +
        '</div>' +
      '</div>';

    var foot =
      '<a href="student-assignments.html" class="workspace-btn-primary"><span data-ngis-icon="documents"></span>View Class Tasks</a>' +
      '<button type="button" class="workspace-btn-secondary" onclick="document.getElementById(\'wsModalOverlay\').classList.remove(\'is-open\');">Close</button>';

    openModal(title, body, foot);
  }

  function openAssignmentModal(asg) {
    var title = '<img src="../../assets/images/icons-3d/notepad.png" width="22" height="22" class="ngis-3d-icon" style="margin-right:8px;background:transparent!important;" alt="Assignment"> ' + asg.title;
    var body =
      '<div style="display:flex;flex-direction:column;gap:14px;">' +
        '<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:12px;display:grid;grid-template-columns:1fr 1fr;gap:10px;">' +
          '<div><div style="font-size:11px;color:#64748B;">Subject / Course</div><div style="font-size:13px;font-weight:500;color:#0F172A;">' + (asg.course || asg.subject) + '</div></div>' +
          '<div><div style="font-size:11px;color:#64748B;">Due Date</div><div style="font-size:13px;font-weight:500;color:#DC2626;">' + (asg.dueFull || asg.due) + '</div></div>' +
          '<div><div style="font-size:11px;color:#64748B;">Instructor</div><div style="font-size:13px;font-weight:500;color:#0F172A;">' + (asg.teacher || 'Department Faculty') + '</div></div>' +
          '<div><div style="font-size:11px;color:#64748B;">Maximum Points</div><div style="font-size:13px;font-weight:500;color:#0F172A;">' + (asg.points || '100 points') + '</div></div>' +
        '</div>' +
        '<div>' +
          '<div style="font-weight:500;margin-bottom:6px;color:#0F172A;">Task Brief</div>' +
          '<p style="color:#475569;font-size:13px;margin:0;line-height:1.5;">' + asg.description + '</p>' +
        '</div>' +
        '<div style="border:2px dashed #CBD5E1;border-radius:10px;padding:20px;text-align:center;background:#F8FAFC;">' +
          '<span data-ngis-icon="download" style="font-size:24px;color:#176B45;display:inline-block;margin-bottom:6px;"></span>' +
          '<div style="font-size:13px;font-weight:500;color:#0F172A;">Upload submission file (PDF, DOCX)</div>' +
          '<div style="font-size:11px;color:#64748B;margin-top:2px;">Maximum upload size: 25MB</div>' +
          '<input type="file" id="asgFileInput" style="display:none;" onchange="alert(\'File selected: \' + this.files[0].name);">' +
          '<button type="button" class="workspace-btn-secondary" style="margin-top:10px;" onclick="document.getElementById(\'asgFileInput\').click();">Select File</button>' +
        '</div>' +
      '</div>';

    var foot =
      '<button type="button" class="workspace-btn-primary" onclick="alert(\'Assignment submitted successfully!\'); document.getElementById(\'wsModalOverlay\').classList.remove(\'is-open\');"><span data-ngis-icon="checkCircle"></span>Submit Coursework</button>' +
      '<button type="button" class="workspace-btn-secondary" onclick="document.getElementById(\'wsModalOverlay\').classList.remove(\'is-open\');">Cancel</button>';

    openModal(title, body, foot);
  }

  function openAnnouncementModal(ann) {
    var title = '<img src="../../assets/images/icons-3d/megaphone.png" width="22" height="22" class="ngis-3d-icon" style="margin-right:8px;" alt="Announcement"> ' + ann.title;
    var bannerHtml = ann.image
      ? '<div style="width:100%;height:180px;border-radius:8px;overflow:hidden;margin-bottom:8px;background:#F1F5F9;">' +
          '<img src="' + ann.image + '" alt="' + ann.title + '" style="width:100%;height:100%;object-fit:cover;">' +
        '</div>'
      : '';

    var body =
      '<div style="display:flex;flex-direction:column;gap:12px;">' +
        bannerHtml +
        '<div style="display:flex;align-items:center;justify-content:space-between;padding-bottom:10px;border-bottom:1px solid #E2E8F0;flex-wrap:wrap;gap:8px;">' +
          '<span style="font-size:12px;color:#64748B;">Posted by: <span style="font-weight:500;color:#29352E;">' + ann.author + '</span></span>' +
          '<span style="font-size:12px;color:#176B45;font-weight:500;">' + (ann.category || 'News') + ' · ' + ann.date + '</span>' +
        '</div>' +
        '<div style="font-size:13.5px;line-height:1.6;color:#1E293B;">' +
          ann.body +
        '</div>' +
      '</div>';

    openModal(title, body);
  }

  function openAddEventModal() {
    var title = '<img src="../../assets/images/icons-3d/calendar.png" width="22" height="22" class="ngis-3d-icon" style="margin-right:8px;" alt="Calendar"> Add Personal Event';
    var todayStr = formatDate(new Date());
    var body =
      '<form id="addEventForm" style="display:flex;flex-direction:column;gap:12px;" onsubmit="return false;">' +
        '<div>' +
          '<label style="display:block;font-size:12px;font-weight:500;color:#29352E;margin-bottom:4px;">Event Title</label>' +
          '<input type="text" id="evTitleInput" required placeholder="e.g. Physics Revision, Group Study" style="width:100%;padding:8px 12px;border:1px solid #CBD5E1;border-radius:6px;font-size:13px;box-sizing:border-box;">' +
        '</div>' +
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">' +
          '<div>' +
            '<label style="display:block;font-size:12px;font-weight:500;color:#29352E;margin-bottom:4px;">Date</label>' +
            '<input type="date" id="evDateInput" value="' + todayStr + '" style="width:100%;padding:8px 10px;border:1px solid #CBD5E1;border-radius:6px;font-size:13px;box-sizing:border-box;">' +
          '</div>' +
          '<div>' +
            '<label style="display:block;font-size:12px;font-weight:500;color:#29352E;margin-bottom:4px;">Time</label>' +
            '<input type="text" id="evTimeInput" value="15:00" placeholder="e.g. 15:00, Due" style="width:100%;padding:8px 10px;border:1px solid #CBD5E1;border-radius:6px;font-size:13px;box-sizing:border-box;">' +
          '</div>' +
        '</div>' +
        '<div>' +
          '<label style="display:block;font-size:12px;font-weight:500;color:#29352E;margin-bottom:4px;">Category</label>' +
          '<select id="evTypeInput" style="width:100%;padding:8px 10px;border:1px solid #CBD5E1;border-radius:6px;font-size:13px;box-sizing:border-box;background:#fff;">' +
            '<option value="event">Personal Study / Activity</option>' +
            '<option value="due">Assignment Deadline / Due</option>' +
          '</select>' +
        '</div>' +
      '</form>';

    var foot =
      '<button type="button" class="workspace-btn-primary" id="btnSaveEventSubmit"><span data-ngis-icon="checkCircle"></span>Save Event</button>' +
      '<button type="button" class="workspace-btn-secondary" onclick="document.getElementById(\'wsModalOverlay\').classList.remove(\'is-open\');">Cancel</button>';

    openModal(title, body, foot);

    var saveBtn = document.getElementById('btnSaveEventSubmit');
    if (saveBtn) {
      saveBtn.addEventListener('click', function () {
        var tInput = document.getElementById('evTitleInput');
        var dInput = document.getElementById('evDateInput');
        var timeInput = document.getElementById('evTimeInput');
        var typeInput = document.getElementById('evTypeInput');

        if (!tInput || !tInput.value.trim()) {
          alert('Please enter an event title.');
          return;
        }

        var dVal = dInput ? dInput.value : todayStr;
        if (!WEEK_EVENTS_DB[dVal]) {
          WEEK_EVENTS_DB[dVal] = [];
        }
        WEEK_EVENTS_DB[dVal].push({
          title: tInput.value.trim(),
          time: timeInput ? timeInput.value.trim() : '15:00',
          type: typeInput ? typeInput.value : 'event'
        });

        renderWeeklyCalendar();
        closeModal();
      });
    }
  }

  /* ── 13. Event Listeners & Wire-up ── */
  function setupTaskTabsControls() {
    var tabBtns = document.querySelectorAll('.workspace-task-tab');
    tabBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var selected = this.getAttribute('data-task-tab');
        if (!selected || selected === currentTaskTab) return;
        currentTaskTab = selected;

        tabBtns.forEach(function (b) {
          var isCur = b.getAttribute('data-task-tab') === selected;
          b.classList.toggle('active', isCur);
          b.setAttribute('aria-selected', isCur ? 'true' : 'false');
        });

        renderUpcomingAssignments();
      });
    });
  }

  function setupCalendarControls() {
    var prevBtn = document.getElementById('calPrevBtn');
    var nextBtn = document.getElementById('calNextBtn');
    var todayBtn = document.getElementById('calTodayBtn');
    var addBtn = document.getElementById('btnAddPersonalEvent');

    if (prevBtn) {
      prevBtn.addEventListener('click', function () {
        currentWeekOffset--;
        renderWeeklyCalendar();
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        currentWeekOffset++;
        renderWeeklyCalendar();
      });
    }

    if (todayBtn) {
      todayBtn.addEventListener('click', function () {
        currentWeekOffset = 0;
        renderWeeklyCalendar();
      });
    }

    if (addBtn) {
      addBtn.addEventListener('click', openAddEventModal);
    }
  }

  /* Keyboard shortcut Ctrl+K */
  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) {
      e.preventDefault();
      var inp = document.getElementById('workspaceSearchInput');
      if (inp) inp.focus();
    }
  });

  /* ── 14. Initialize Workspace ── */
  function initWorkspace() {
    renderTodayClasses();
    renderUpcomingAssignments();
    setupTaskTabsControls();
    renderAnnouncements();
    renderMyClasses();
    renderWeeklyCalendar();
    setupCalendarControls();

    // Hydrate icons
    if (window.NGIS && typeof window.NGIS.hydrateIcons === 'function') {
      window.NGIS.hydrateIcons();
    }
  }

  // Self-execute when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWorkspace);
  } else {
    initWorkspace();
  }

  // Export for external trigger
  window.NGISWorkspace = {
    init: initWorkspace,
    openClassModal: openClassDetailModal,
    openAssignmentModal: openAssignmentModal,
    openAnnouncementModal: openAnnouncementModal,
    openTaskDetail: function (taskId) {
      var all = UPCOMING_TASKS.concat(PAST_TASKS).concat(OVERDUE_TASKS);
      var found = all.find(function (t) { return t.id === taskId; });
      if (found) {
        openAssignmentModal(found);
      }
    },
    closeModal: closeModal
  };

})();
