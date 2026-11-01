/* ══════════════════════════════════════
   HERO BANNER — Teacher Dashboard
   Builds and injects the hero section,
   wires up the profile dropdown.
   ══════════════════════════════════════ */

(function () {

  /* ── Teacher data ── */
  var TEACHER = {
    name:      'Dr. Sarah Jenkins',
    id:        'TCH-2026-088',
    dept:      'Mathematics & Science Department',
    classes:   'Grade 11-A, 10-C, 12-B',
    email:     'sarah.jenkins@ngis.edu.kh',
    room:      'Room 302 · Academic Wing B',
    joined:    'Aug 2019',
    roleTitle: 'Senior Faculty · Mathematics Lead',
    avatar:    'https://images.pexels.com/photos/3769021/pexels-photo-3769021.jpeg?auto=compress&cs=tinysrgb&w=160',
    avatarSm:  'https://images.pexels.com/photos/3769021/pexels-photo-3769021.jpeg?auto=compress&cs=tinysrgb&w=80',
  };

  /* ── Live date ── */
  var DAYS   = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  var MONTHS = ['January','February','March','April','May','June',
                'July','August','September','October','November','December'];
  var now    = new Date();
  var dateStr = DAYS[now.getDay()] + ', ' + MONTHS[now.getMonth()] + ' ' + now.getDate() + ', ' + now.getFullYear();

  var C = window.HERO_CONFIG || {};

  var heroTitle = C.title || 'Welcome to your dashboard';
  var heroGreeting = C.greeting || C.subtitle || 'Hello, Dr. Sarah! Ready to inspire your students today?';
  var heroDate = C.date || dateStr;

  /* ── Build HTML ── */
  var html =
    '<div class="hero hero-main">' +

      '<!-- ── Tier 1: Main Header Bar ── -->' +
      '<div class="hero-topbar">' +

        '<!-- Left: Brand Logo Image -->' +
        '<a href="teacher.html" class="htb-brand-wrap" aria-label="New Gateway International School">' +
          '<img class="htb-brand-logo-img" src="../student/LOGO NGIS (2).png" alt="New Gateway International School" onerror="this.onerror=null;this.src=\'../../assets/images/logo.png\'">' +
        '</a>' +

        '<!-- Center: Global Search Capsule -->' +
        '<div class="htb-search-wrap" role="search">' +
          '<span class="mi htb-search-icon">search</span>' +
          '<input type="search" class="htb-search-input" id="htbSearchInput" placeholder="Search classes, students, tasks, curricula…" aria-label="Search classes, students, tasks, curricula">' +
          '<kbd class="htb-search-kbd">⌘ K</kbd>' +
        '</div>' +

        '<!-- Right: Controls & User Profile -->' +
        '<div class="htb-right-controls">' +
          '<a href="teacher-calendar.html" class="htb-ctrl-btn" id="htbCalBtn" title="Timetable & Calendar" aria-label="Calendar">' +
            '<span class="mi">calendar_today</span>' +
          '</a>' +
          '<a href="teacher-notifications.html" id="htbNotifBtn" class="htb-ctrl-btn" title="Notifications" aria-label="Notifications">' +
            '<span class="mi">notifications</span>' +
            '<span class="htb-ctrl-badge">3</span>' +
          '</a>' +
          '<a href="teacher-announcements.html" class="htb-ctrl-btn" id="htbMsgBtn" title="Announcements & Communications" aria-label="Communications">' +
            '<span class="mi">mail</span>' +
            '<span class="htb-ctrl-badge" style="background:#e11d48">8</span>' +
          '</a>' +

          '<div class="htb-ctrl-divider" aria-hidden="true"></div>' +

          '<div class="htb-profile-chip" id="htbProfile" role="button" tabindex="0" aria-label="Account menu" aria-haspopup="true" aria-expanded="false">' +
            '<div class="htb-chip-avatar-wrap">' +
              '<img class="htb-chip-avatar" src="' + TEACHER.avatarSm + '" alt="' + TEACHER.name + '">' +
              '<span class="htb-online-pip" title="Active"></span>' +
            '</div>' +
            '<div class="htb-chip-text">' +
              '<div class="htb-chip-name-row">' +
                '<span class="htb-chip-name">' + TEACHER.name + '</span>' +
              '</div>' +
              '<span class="htb-chip-meta">Senior Faculty</span>' +
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

    '</div>';

  /* ── Inject into placeholder ── */
  var placeholder = document.getElementById('heroBanner');
  if (placeholder) placeholder.outerHTML = html;

  /* ── Profile dropdown HTML ── */
  var ddHtml =
    '<div class="htb-dropdown" id="htbDropdown">' +
      '<div class="htb-dd-header">' +
        '<img class="htb-dd-avatar" src="' + TEACHER.avatar + '" alt="' + TEACHER.name + '">' +
        '<div>' +
          '<div class="htb-dd-name">' + TEACHER.name + '</div>' +
          '<div class="htb-dd-id">Faculty ID: ' + TEACHER.id + '</div>' +
        '</div>' +
      '</div>' +
      '<div class="htb-dd-divider"></div>' +
      '<div class="htb-dd-info">' +
        '<div class="htb-dd-row"><span class="mi">school</span><span>' + TEACHER.dept + '</span></div>' +
        '<div class="htb-dd-row"><span class="mi">class</span><span>' + TEACHER.classes + '</span></div>' +
        '<div class="htb-dd-row"><span class="mi">email</span><span>' + TEACHER.email + '</span></div>' +
        '<div class="htb-dd-row"><span class="mi">location_on</span><span>' + TEACHER.room + '</span></div>' +
        '<div class="htb-dd-row"><span class="mi">calendar_today</span><span>Joined: ' + TEACHER.joined + '</span></div>' +
        '<div class="htb-dd-row"><span class="mi">star</span><span>' + TEACHER.roleTitle + '</span></div>' +
      '</div>' +
      '<div class="htb-dd-divider"></div>' +
      '<div class="htb-dd-actions">' +
        '<a href="teacher-profile.html" class="htb-dd-btn"><span class="mi">manage_accounts</span>My Profile</a>' +
        '<a href="../../index.html" class="htb-dd-btn htb-dd-btn-danger"><span class="mi">logout</span>Sign Out</a>' +
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

  function openDD() {
    positionDropdown();
    dropdown.classList.add('open');
    var profileTrigger = document.getElementById('htbProfile');
    if (profileTrigger) profileTrigger.setAttribute('aria-expanded', 'true');
    var bd = document.getElementById('htbBackdrop');
    if (bd) bd.classList.add('open');
  }

  function closeDD() {
    dropdown.classList.remove('open');
    var profileTrigger = document.getElementById('htbProfile');
    if (profileTrigger) profileTrigger.setAttribute('aria-expanded', 'false');
    var bd = document.getElementById('htbBackdrop');
    if (bd) bd.classList.remove('open');
  }

  document.addEventListener('DOMContentLoaded', function () {
    var profile = document.getElementById('htbProfile');
    var bd = document.getElementById('htbBackdrop');
    if (profile) {
      profile.addEventListener('click', function (e) {
        e.stopPropagation();
        if (dropdown.classList.contains('open')) closeDD();
        else openDD();
      });
      profile.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          if (dropdown.classList.contains('open')) closeDD();
          else openDD();
        }
      });
    }

    if (bd) bd.addEventListener('click', closeDD);

    document.addEventListener('click', function (e) {
      if (dropdown.classList.contains('open') && !dropdown.contains(e.target) && e.target !== profile) {
        closeDD();
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && dropdown.classList.contains('open')) closeDD();
    });

    window.addEventListener('resize', function () {
      if (dropdown.classList.contains('open')) positionDropdown();
    });

    // Global Search focus shortcut ⌘K / Ctrl+K
    var searchInput = document.getElementById('htbSearchInput');
    window.addEventListener('keydown', function (e) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (searchInput) {
          searchInput.focus();
          searchInput.select();
        }
      }
    });
  });

})();

