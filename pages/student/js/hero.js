/* ══════════════════════════════════════
   HERO BANNER — Student Dashboard
   Builds and injects the hero section,
   wires up the profile dropdown.
   ══════════════════════════════════════ */

(function () {

  /* ── Student data ── */
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
          '<img class="htb-brand-logo-img" src="LOGO NGIS (2).png" alt="New Gateway International School" onerror="this.onerror=null;this.src=\'../../assets/images/logo.png\'">' +
        '</a>' +

        '<!-- Center: Global Search Capsule -->' +
        '<div class="htb-search-wrap" role="search">' +
          '<span class="mi htb-search-icon">search</span>' +
          '<input type="search" class="htb-search-input" id="htbSearchInput" placeholder="Search courses," aria-label="Search courses">' +
        '</div>' +

        '<!-- Right: Controls & User Profile -->' +
        '<div class="htb-right-controls">' +
          '<button type="button" class="htb-hamburger hamburger-btn mobile-hamburger-btn" id="htbHamburger" data-action="toggle-sidebar" aria-label="Open menu" aria-expanded="false" title="Open navigation">' +
            '<span class="mi">menu</span>' +
          '</button>' +

          '<button type="button" id="htbNotifBtn" class="htb-ctrl-btn" title="Notifications" aria-label="Notifications">' +
            '<span class="mi">notifications</span>' +
            '<span class="htb-ctrl-badge">3</span>' +
          '</button>' +

          '<a href="student-notifications.html" class="htb-ctrl-btn" id="htbMsgBtn" title="Messages" aria-label="Messages">' +
            '<span class="mi">mail</span>' +
            '<span class="htb-ctrl-badge">11</span>' +
          '</a>' +

          '<div class="htb-profile-chip" id="htbProfile" role="button" tabindex="0" aria-label="Account menu" aria-haspopup="true" aria-expanded="false">' +
            '<div class="htb-chip-avatar-wrap">' +
              '<img class="htb-chip-avatar" src="' + STUDENT.avatarSm + '" alt="' + STUDENT.name + '">' +
            '</div>' +
            '<div class="htb-chip-text">' +
              '<div class="htb-chip-name-row">' +
                '<span class="htb-chip-name">' + STUDENT.name + '</span>' +
              '</div>' +
            '</div>' +
          '</div>' +
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

    '</div>';

  /* ── Inject into placeholder ── */
  var placeholder = document.getElementById('heroBanner');
  if (placeholder) placeholder.outerHTML = html;

  /* ── Profile dropdown HTML ── */
  var ddHtml =
    '<div class="htb-dropdown" id="htbDropdown">' +
      '<div class="htb-dd-header">' +
        '<img class="htb-dd-avatar" src="' + STUDENT.avatar + '" alt="' + STUDENT.name + '">' +
        '<div>' +
          '<div class="htb-dd-name">' + STUDENT.name + '</div>' +
          '<div class="htb-dd-id">Student ID: ' + STUDENT.id + '</div>' +
        '</div>' +
      '</div>' +
      '<div class="htb-dd-divider"></div>' +
      '<div class="htb-dd-info">' +
        '<div class="htb-dd-row"><span class="mi">school</span><span>' + STUDENT.stream + '</span></div>' +
        '<div class="htb-dd-row"><span class="mi">class</span><span>' + STUDENT.class + '</span></div>' +
        '<div class="htb-dd-row"><span class="mi">email</span><span>' + STUDENT.email + '</span></div>' +
        '<div class="htb-dd-row"><span class="mi">calendar_today</span><span>Enrolled: ' + STUDENT.enrolled + '</span></div>' +
        '<div class="htb-dd-row"><span class="mi">emoji_events</span><span>GPA: ' + STUDENT.gpa + '</span></div>' +
      '</div>' +
      '<div class="htb-dd-divider"></div>' +
      '<div class="htb-dd-actions">' +
        '<a href="student-profile.html" class="htb-dd-btn"><span class="mi">manage_accounts</span>My Profile</a>' +
        '<a href="/" class="htb-dd-btn htb-dd-btn-danger"><span class="mi">logout</span>Sign Out</a>' +
      '</div>' +
    '</div>';

  var ddEl = document.createElement('div');
  ddEl.innerHTML = ddHtml;
  var dropdown = ddEl.firstChild;
  document.body.appendChild(dropdown);

  /* ── Profile dropdown logic ── */
  function positionDropdown() {
    var profile = document.getElementById('htbProfile');
    if (!profile) return;
    var rect = profile.getBoundingClientRect();
    if (window.innerWidth <= 600) {
      dropdown.style.top   = (rect.bottom + 8) + 'px';
      dropdown.style.right = '12px';
      dropdown.style.left  = 'auto';
      return;
    }
    dropdown.style.top   = (rect.bottom + 10) + 'px';
    dropdown.style.right = (window.innerWidth - rect.right) + 'px';
    dropdown.style.left  = 'auto';
  }

  function closePanels() {
    if (notifPanel) notifPanel.classList.remove('open');
    var nb = document.getElementById('htbNotifBtn');
    if (nb) nb.classList.remove('active');
  }

  function openDD() {
    closePanels();
    positionDropdown();
    dropdown.classList.add('open');
    var profileTrigger = document.getElementById('htbProfile');
    if (profileTrigger) profileTrigger.setAttribute('aria-expanded', 'true');
    var arr = document.getElementById('htbParr');
    if (arr) arr.classList.add('open');
    var bd = document.getElementById('htbBackdrop');
    if (bd) bd.classList.add('open');
    document.body.style.overflow = window.innerWidth <= 600 ? 'hidden' : '';
  }

  function closeDD() {
    dropdown.classList.remove('open');
    var profileTrigger = document.getElementById('htbProfile');
    if (profileTrigger) profileTrigger.setAttribute('aria-expanded', 'false');
    var arr = document.getElementById('htbParr');
    if (arr) arr.classList.remove('open');
    var bd = document.getElementById('htbBackdrop');
    if (bd) bd.classList.remove('open');
    document.body.style.overflow = '';
  }

  var profileTrigger = document.getElementById('htbProfile');
  if (profileTrigger) {
    profileTrigger.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        dropdown.classList.contains('open') ? closeDD() : openDD();
      }
    });
  }

  document.addEventListener('click', function (e) {
    var profile = document.getElementById('htbProfile');
    if (profile && profile.contains(e.target)) {
      e.stopPropagation();
      dropdown.classList.contains('open') ? closeDD() : openDD();
      return;
    }
    var bd = document.getElementById('htbBackdrop');
    if ((bd && bd.contains(e.target)) || !dropdown.contains(e.target)) closeDD();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeDD(); closePanels(); }
    if ((e.metaKey || e.ctrlKey) && (e.key === 'k' || e.key === 'K')) {
      e.preventDefault();
      var sInp = document.getElementById('htbSearchInput');
      if (sInp) sInp.focus();
    }
  });
  window.addEventListener('resize', function () { if (dropdown.classList.contains('open')) positionDropdown(); });
  window.addEventListener('scroll', function () { if (dropdown.classList.contains('open')) positionDropdown(); }, true);

  /* ── Hamburger ── */
  var hamburger = document.getElementById('htbHamburger');
  if (hamburger) {
    hamburger.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      e.stopImmediatePropagation();
      if (typeof window.toggleSidebar === 'function') {
        window.toggleSidebar();
        return;
      }
      var sidebar = document.getElementById('sidebar');
      var scrim   = document.getElementById('scrim');
      if (!sidebar) return;
      var isOpen = sidebar.classList.contains('open');
      if (isOpen) {
        sidebar.classList.remove('open');
        if (scrim) scrim.classList.remove('show');
        hamburger.setAttribute('aria-expanded', 'false');
      } else {
        sidebar.classList.add('open');
        if (scrim) scrim.classList.add('show');
        hamburger.setAttribute('aria-expanded', 'true');
      }
    });
  }

  /* ══════════════════════════════════════
     NOTIFICATION & MAIL DROPDOWNS
     ══════════════════════════════════════ */

  /* ── Notification dropdown ── */
  var notifData = [
    { icon: 'assignment', color: '#2563eb', bg: '#eff6ff', title: 'Physics Essay Draft posted',    meta: 'Mr. Sophea · 12m ago',   unread: true  },
    { icon: 'grade',      color: '#16a34a', bg: '#f0fdf4', title: 'Chemistry graded: 88%',          meta: 'Ms. Kiry · 2h ago',      unread: true  },
    { icon: 'campaign',   color: '#2455D6', bg: 'rgba(36,85,214,0.1)', title: 'Science Fair registration open', meta: 'School · Yesterday', unread: false }
  ];

  var notifItemsHtml = '';
  for (var n = 0; n < notifData.length; n++) {
    var nd = notifData[n];
    notifItemsHtml +=
      '<a href="' + notifLink + '" class="hpd-item">' +
        '<div class="hpd-notif-ico" style="background:' + nd.bg + '">' +
          '<span class="mi" style="color:' + nd.color + '">' + nd.icon + '</span>' +
        '</div>' +
        '<div class="hpd-notif-body">' +
          '<div class="hpd-notif-title">' + nd.title + '</div>' +
          '<div class="hpd-notif-meta">' + nd.meta + '</div>' +
        '</div>' +
        (nd.unread ? '<div class="hpd-unread-dot"></div>' : '') +
      '</a>';
  }

  var notifPanelEl = document.createElement('div');
  notifPanelEl.innerHTML =
    '<div class="hpd" id="htbNotifPanel">' +
      '<div class="hpd-head">' +
        '<span class="hpd-head-title">Notifications</span>' +
        '<button type="button" class="hpd-head-action" id="htbMarkAllRead">Mark all read</button>' +
      '</div>' +
      '<div class="hpd-list">' +
        notifItemsHtml +
      '</div>' +
      '<div class="hpd-footer">' +
        '<a href="' + notifLink + '" class="hpd-footer-btn">' +
          '<span class="mi">notifications</span>View all' +
        '</a>' +
      '</div>' +
    '</div>';
  var notifPanel = notifPanelEl.firstChild;
  document.body.appendChild(notifPanel);

  /* Wire Mark all read */
  var markAllBtn = notifPanel.querySelector('#htbMarkAllRead');
  if (markAllBtn) {
    markAllBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      var dots = notifPanel.querySelectorAll('.hpd-unread-dot');
      dots.forEach(function (dot) { dot.style.display = 'none'; });
      var nb = document.getElementById('htbNotifBtn');
      if (nb) {
        var badge = nb.querySelector('.htb-ctrl-badge');
        if (badge) badge.style.display = 'none';
      }
      markAllBtn.textContent = 'All read';
      markAllBtn.style.opacity = '0.6';
      markAllBtn.style.cursor = 'default';
      markAllBtn.disabled = true;
    });
  }

  /* Wire individual item click dismiss dot */
  var notifItems = notifPanel.querySelectorAll('.hpd-item');
  notifItems.forEach(function (item) {
    item.addEventListener('click', function () {
      var dot = item.querySelector('.hpd-unread-dot');
      if (dot && dot.style.display !== 'none') {
        dot.style.display = 'none';
        var nb = document.getElementById('htbNotifBtn');
        if (nb) {
          var badge = nb.querySelector('.htb-ctrl-badge');
          if (badge) {
            var count = parseInt(badge.textContent, 10) || 0;
            if (count > 1) {
              badge.textContent = count - 1;
            } else {
              badge.style.display = 'none';
            }
          }
        }
      }
    });
  });

  /* ── Notif button ── */
  var notifBtn = document.getElementById('htbNotifBtn');
  if (notifBtn) {
    notifBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      var wasOpen = notifPanel.classList.contains('open');
      closePanels();
      closeDD();
      if (!wasOpen) {
        posBelow(notifBtn, notifPanel);
        notifPanel.classList.add('open');
        notifBtn.classList.add('active');
      }
    });
  }

  /* ── Close panels on outside click ── */
  document.addEventListener('click', function (e) {
    var nb = document.getElementById('htbNotifBtn');
    if (notifPanel && notifPanel.classList.contains('open')) {
      if (!notifPanel.contains(e.target) && !(nb && nb.contains(e.target))) {
        notifPanel.classList.remove('open');
        if (nb) nb.classList.remove('active');
      }
    }
  });

  /* ── Reposition on scroll/resize ── */
  function reposOpen() {
    var nb = document.getElementById('htbNotifBtn');
    if (nb && notifPanel && notifPanel.classList.contains('open')) posBelow(nb, notifPanel);
  }
  window.addEventListener('resize', reposOpen);
  window.addEventListener('scroll', reposOpen, true);

})();
