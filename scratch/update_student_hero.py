import os

path = 'pages/student/js/hero.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """  /* ── Student data ── */
  var STUDENT = {
    name:      'Nrinphouneta Hok',
    id:        '2026-STD-0142',
    grade:     'Grade 10',
    stream:    'Grade 10 — Science Stream',
    class:     'Class 10A',
    email:     'nrinphouneta@ngis.edu.kh',
    enrolled:  'Sep 2024',
    gpa:       '3.87 / 4.00',
    avatar:    '../../assets/images/dashboard-student-portrait.jpg',
    avatarSm:  '../../assets/images/dashboard-student-portrait.jpg',
  };

  var notifLink     = 'student-notifications.html';

  /* ── Live date ── */
  var DAYS   = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  var MONTHS = ['January','February','March','April','May','June',
                'July','August','September','October','November','December'];
  var now    = new Date();
  var dateStr = DAYS[now.getDay()] + ', ' + MONTHS[now.getMonth()] + ' ' + now.getDate() + ', ' + now.getFullYear();
  var firstName = STUDENT.name.split(' ')[0];

  /* ── Build HTML ── */
  var html =
    '<div class="hero hero-main">' +

      '<!-- ── Tier 1: Main Header Bar ── -->' +
      '<div class="hero-topbar">' +

        '<!-- Left: Brand Logo Image -->' +
        '<a href="student.html" class="htb-brand-wrap" aria-label="New Gateway International School">' +
          '<img class="htb-brand-logo-img" src="LOGO NGIS (2).png" alt="New Gateway International School" onerror="this.onerror=null;this.src=\\'../../assets/images/logo.png\\'">' +
        '</a>' +

        '<!-- Center: Global Search Capsule -->' +
        '<div class="htb-search-wrap" role="search">' +
          '<span class="mi htb-search-icon">search</span>' +
          '<input type="search" class="htb-search-input" id="htbSearchInput" placeholder="Search courses, syllabi, tutors, grades…" aria-label="Search courses, syllabi, tutors, grades">' +
          '<kbd class="htb-search-kbd">⌘ K</kbd>' +
        '</div>' +

        '<!-- Right: Controls & User Profile -->' +
        '<div class="htb-right-controls">' +
          '<a href="student-calendar.html" class="htb-ctrl-btn" id="htbCalBtn" title="Calendar" aria-label="Calendar">' +
            '<span class="mi">calendar_today</span>' +
          '</a>' +
          '<button type="button" id="htbNotifBtn" class="htb-ctrl-btn" title="Notifications" aria-label="Notifications">' +
            '<span class="mi">notifications</span>' +
            '<span class="htb-ctrl-badge">3</span>' +
          '</button>' +


          '<a href="student-notifications.html" class="htb-ctrl-btn" id="htbMsgBtn" title="Messages" aria-label="Messages">' +
            '<span class="mi">mail</span>' +
            '<span class="htb-ctrl-badge" style="background:#e11d48">11</span>' +
          '</a>' +

          '<div class="htb-ctrl-divider" aria-hidden="true"></div>' +

          '<div class="htb-profile-chip" id="htbProfile" role="button" tabindex="0" aria-label="Account menu" aria-haspopup="true" aria-expanded="false">' +
            '<div class="htb-chip-avatar-wrap">' +
              '<img class="htb-chip-avatar" src="' + STUDENT.avatarSm + '" alt="' + STUDENT.name + '">' +
              '<span class="htb-online-pip" title="Active"></span>' +
            '</div>' +
            '<div class="htb-chip-text">' +
              '<div class="htb-chip-name-row">' +
                '<span class="htb-chip-name">' + STUDENT.name + '</span>' +
              '</div>' +
              '<span class="htb-chip-meta">Grade 10</span>' +
            '</div>' +
          '</div>' +

          '<button type="button" class="htb-hamburger hamburger-btn mobile-hamburger-btn" id="htbHamburger" data-action="toggle-sidebar" aria-label="Open menu" aria-expanded="false" title="Open navigation">' +
            '<span class="mi">menu</span>' +
          '</button>' +
        '</div>' +

      '</div>' +

      '<div class="htb-dd-backdrop" id="htbBackdrop"></div>' +

      '<div class="hero-body">' +
        '<div class="hero-text">' +
          '<div class="hero-date">' + dateStr + '</div>' +
          '<h1 class="hero-title">Welcome to your dashboard</h1>' +
          '<p class="hero-greeting">Hello, ' + firstName + '! Ready to learn today?</p>' +
        '</div>' +
      '</div>' +

    '</div>';"""

replacement = """  /* ── Student data ── */
  var STUDENT = {
    name:      'Nrinphouneta Hok',
    id:        '2026-STD-0142',
    grade:     'Grade 10',
    stream:    'Grade 10 — Science Stream',
    class:     'Class 10A',
    email:     'nrinphouneta@ngis.edu.kh',
    enrolled:  'Sep 2024',
    gpa:       '3.87 / 4.00',
    avatar:    'https://images.pexels.com/photos/3785079/pexels-photo-3785079.jpeg?auto=compress&cs=tinysrgb&w=160',
    avatarSm:  'https://images.pexels.com/photos/3785079/pexels-photo-3785079.jpeg?auto=compress&cs=tinysrgb&w=80',
  };

  var notifLink     = 'student-notifications.html';

  /* ── Live date ── */
  var DAYS   = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  var MONTHS = ['January','February','March','April','May','June',
                'July','August','September','October','November','December'];
  var now    = new Date();
  var dateStr = DAYS[now.getDay()] + ', ' + MONTHS[now.getMonth()] + ' ' + now.getDate() + ', ' + now.getFullYear();
  var firstName = STUDENT.name.split(' ')[0];

  /* ── Page title & subtitle resolution ── */
  var C = window.HERO_CONFIG || {};

  var pageTitles = {
    'student.html': {
      title: 'Welcome to your dashboard',
      greeting: 'Hello, ' + firstName + '! Ready to learn today?'
    },
    'student-attendance.html': {
      title: 'Official Attendance Record',
      greeting: 'Real-time attendance logs, term presence percentage, and session records'
    },
    'student-grades.html': {
      title: 'Academic Performance & Report Cards',
      greeting: 'Official semester records, monthly reviews, and performance evaluations'
    },
    'student-assignments.html': {
      title: 'Assignments & Coursework',
      greeting: 'Track upcoming homework, submitted problem sets, lab reports, and teacher reviews'
    },
    'student-exams.html': {
      title: 'Examinations & Assessments',
      greeting: 'Official exam schedule, hall allocations, seat assignments, and results'
    },
    'student-timetable.html': {
      title: 'Weekly Class Timetable',
      greeting: 'Academic schedule, course periods, classroom locations, and instructors'
    },
    'student-calendar.html': {
      title: 'Academic & Campus Calendar',
      greeting: 'Scheduled school events, examination windows, campus activities, and holidays'
    },
    'student-announcements.html': {
      title: 'Official Announcements & Circulars',
      greeting: 'School notifications, campus news, academic bulletins, and alerts'
    },
    'student-services.html': {
      title: 'Student Services Hub',
      greeting: 'Official document requests, student support, counseling, and campus facilities'
    },
    'student-notifications.html': {
      title: 'Notifications & Communications',
      greeting: 'Campus alerts, instructor communications, and activity notifications'
    },
    'student-profile.html': {
      title: 'Student Profile & Academic Standing',
      greeting: 'Personal information, enrollment credentials, program stream, and records'
    },
    'student-id.html': {
      title: 'Digital Student ID Card',
      greeting: 'Official student credential, library card barcode, and campus access pass'
    },
    'student-clubs.html': {
      title: 'Student Clubs & Co-Curricular',
      greeting: 'Campus clubs, student leadership, extracurricular activities, and events'
    },
    'student-lost-found.html': {
      title: 'Campus Lost & Found Hub',
      greeting: 'Report lost personal items, browse discovered campus articles, and claim belongings'
    }
  };

  var currFile = (window.location.pathname.split('/').pop() || 'student.html').toLowerCase();
  var defaultInfo = pageTitles[currFile] || {
    title: C.title || 'Student Portal',
    greeting: C.greeting || C.subtitle || ('Hello, ' + firstName + '! Ready to learn today?')
  };

  var heroTitle = C.title || defaultInfo.title;
  var heroGreeting = C.greeting || C.subtitle || defaultInfo.greeting;
  var heroDate = C.date || dateStr;

  /* ── Build HTML ── */
  var html =
    '<div class="hero hero-main">' +

      '<!-- ── Tier 1: Main Header Bar ── -->' +
      '<div class="hero-topbar">' +

        '<!-- Left: Brand Logo Image -->' +
        '<a href="student.html" class="htb-brand-wrap" aria-label="New Gateway International School">' +
          '<img class="htb-brand-logo-img" src="LOGO NGIS (2).png" alt="New Gateway International School" onerror="this.onerror=null;this.src=\\'../../assets/images/logo.png\\'">' +
        '</a>' +

        '<!-- Center: Global Search Capsule -->' +
        '<div class="htb-search-wrap" role="search">' +
          '<span class="mi htb-search-icon">search</span>' +
          '<input type="search" class="htb-search-input" id="htbSearchInput" placeholder="Search courses, syllabi, tutors, grades…" aria-label="Search courses, syllabi, tutors, grades">' +
          '<kbd class="htb-search-kbd">⌘ K</kbd>' +
        '</div>' +

        '<!-- Right: Controls & User Profile -->' +
        '<div class="htb-right-controls">' +
          '<a href="student-calendar.html" class="htb-ctrl-btn" id="htbCalBtn" title="Calendar" aria-label="Calendar">' +
            '<span class="mi">calendar_today</span>' +
          '</a>' +
          '<button type="button" id="htbNotifBtn" class="htb-ctrl-btn" title="Notifications" aria-label="Notifications">' +
            '<span class="mi">notifications</span>' +
            '<span class="htb-ctrl-badge">3</span>' +
          '</button>' +


          '<a href="student-notifications.html" class="htb-ctrl-btn" id="htbMsgBtn" title="Messages" aria-label="Messages">' +
            '<span class="mi">mail</span>' +
            '<span class="htb-ctrl-badge" style="background:#e11d48">11</span>' +
          '</a>' +

          '<div class="htb-ctrl-divider" aria-hidden="true"></div>' +

          '<div class="htb-profile-chip" id="htbProfile" role="button" tabindex="0" aria-label="Account menu" aria-haspopup="true" aria-expanded="false">' +
            '<div class="htb-chip-avatar-wrap">' +
              '<img class="htb-chip-avatar" src="' + STUDENT.avatarSm + '" alt="' + STUDENT.name + '">' +
              '<span class="htb-online-pip" title="Active"></span>' +
            '</div>' +
            '<div class="htb-chip-text">' +
              '<div class="htb-chip-name-row">' +
                '<span class="htb-chip-name">' + STUDENT.name + '</span>' +
              '</div>' +
              '<span class="htb-chip-meta">Grade 10</span>' +
            '</div>' +
          '</div>' +

          '<button type="button" class="htb-hamburger hamburger-btn mobile-hamburger-btn" id="htbHamburger" data-action="toggle-sidebar" aria-label="Open menu" aria-expanded="false" title="Open navigation">' +
            '<span class="mi">menu</span>' +
          '</button>' +
        '</div>' +

      '</div>' +

      '<div class="htb-dd-backdrop" id="htbBackdrop"></div>' +

      '<div class="hero-body">' +
        '<div class="hero-text">' +
          '<div class="hero-date">' + heroDate + '</div>' +
          '<h1 class="hero-title">' + heroTitle + '</h1>' +
          '<p class="hero-greeting">' + heroGreeting + '</p>' +
        '</div>' +
      '</div>' +

    '</div>';"""

# Normalize line endings for replacement
norm_content = content.replace('\r\n', '\n')
norm_target = target.replace('\r\n', '\n')
norm_repl = replacement.replace('\r\n', '\n')

if norm_target in norm_content:
    new_content = norm_content.replace(norm_target, norm_repl)
    with open(path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(new_content)
    print("Successfully updated pages/student/js/hero.js")
else:
    print("Target not found in pages/student/js/hero.js")

