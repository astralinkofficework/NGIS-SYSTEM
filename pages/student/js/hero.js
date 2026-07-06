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
  var chatLink      = '../shared/chat.html';
  var groupChatLink = '../shared/group-chat.html';

  /* ── Live date ── */
  var DAYS   = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  var MONTHS = ['January','February','March','April','May','June',
                'July','August','September','October','November','December'];
  var now    = new Date();
  var dateStr = DAYS[now.getDay()] + ', ' + MONTHS[now.getMonth()] + ' ' + now.getDate() + ', ' + now.getFullYear();
  var firstName = STUDENT.name.split(' ')[0];

  /* ── Build HTML ── */
  var html =
    '<div class="hero">' +

      '<div class="hero-topbar">' +

        '<div class="htb-left">' +
          '<button class="htb-hamburger" id="htbHamburger" aria-label="Open menu" aria-expanded="false">' +
            '<span class="mi">menu</span>' +
          '</button>' +
            '<a href="../../index.html" class="htb-home-btn">' +
              '<span class="mi">home</span>' +
              '<span>Home</span>' +
            '</a>' +
          '</nav>' +
        '</div>' +

        '<div class="htb-right">' +
          '<a href="#" class="htb-icon htb-icon-search" title="Search" aria-label="Search"><span class="mi">search</span></a>' +
          '<button id="htbNotifBtn" class="htb-icon htb-notif-btn" title="Notifications" aria-label="Notifications" style="position:relative">' +
            '<span class="mi">notifications</span>' +
            '<span class="htb-badge">3</span>' +
          '</button>' +
          '<button id="htbMailBtn" class="htb-icon htb-notif-btn htb-icon-mail" title="Messages" aria-label="Messages" style="position:relative">' +
            '<span class="mi">mail</span>' +
            '<span class="htb-badge" style="background:#e11d48">11</span>' +
          '</button>' +

          '<div class="htb-profile" id="htbProfile">' +
            '<img class="htb-avatar" src="' + STUDENT.avatarSm + '" alt="' + STUDENT.name + '">' +
            '<div class="htb-pinfo">' +
              '<div class="htb-pname-row">' +
                '<span class="htb-pname">' + STUDENT.name + '</span>' +
                '<span class="mi htb-parr" id="htbParr">keyboard_arrow_down</span>' +
              '</div>' +
              '<div class="htb-pgrade">' + STUDENT.grade + '</div>' +
            '</div>' +
          '</div>' +

        '</div>' +
      '</div>' +

      '<div class="hero-rule"></div>' +
      '<div class="htb-dd-backdrop" id="htbBackdrop"></div>' +

      '<div class="hero-body">' +
        '<div class="hero-text">' +
          '<div class="hero-date">' + dateStr + '</div>' +
          '<h1 class="hero-title">Welcome to your dashboard</h1>' +
          '<p class="hero-greeting">Hello, ' + firstName + '! Ready to learn today?</p>' +
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
        '<a href="../../index.html" class="htb-dd-btn htb-dd-btn-danger"><span class="mi">logout</span>Sign Out</a>' +
      '</div>' +
    '</div>';

  var ddEl = document.createElement('div');
  ddEl.innerHTML = ddHtml;
  var dropdown = ddEl.firstChild;
  document.body.appendChild(dropdown);

  /* ── Profile dropdown logic ── */
  function positionDropdown() {
    if (window.innerWidth <= 600) return;
    var profile = document.getElementById('htbProfile');
    if (!profile) return;
    var rect = profile.getBoundingClientRect();
    dropdown.style.top   = (rect.bottom + 10) + 'px';
    dropdown.style.right = (window.innerWidth - rect.right) + 'px';
    dropdown.style.left  = 'auto';
  }

  function closePanels() {
    if (notifPanel) notifPanel.classList.remove('open');
    if (mailPanel)  mailPanel.classList.remove('open');
  }

  function openDD() {
    closePanels();
    positionDropdown();
    dropdown.classList.add('open');
    document.getElementById('htbParr').classList.add('open');
    var bd = document.getElementById('htbBackdrop');
    if (bd) bd.classList.add('open');
    document.body.style.overflow = window.innerWidth <= 600 ? 'hidden' : '';
  }

  function closeDD() {
    dropdown.classList.remove('open');
    var arr = document.getElementById('htbParr');
    if (arr) arr.classList.remove('open');
    var bd = document.getElementById('htbBackdrop');
    if (bd) bd.classList.remove('open');
    document.body.style.overflow = '';
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

  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeDD(); closePanels(); } });
  window.addEventListener('resize', function () { if (dropdown.classList.contains('open')) positionDropdown(); });
  window.addEventListener('scroll', function () { if (dropdown.classList.contains('open')) positionDropdown(); }, true);

  /* ── Hamburger ── */
  var hamburger = document.getElementById('htbHamburger');
  if (hamburger) {
    hamburger.addEventListener('click', function () {
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

  /* ── Inject CSS ── */
  var s = document.createElement('style');
  s.textContent =
    '.htb-notif-btn{background:none;border:none;padding:0;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;color:rgba(255,255,255,.88);line-height:1;}' +
    '.hpd{position:fixed;z-index:9100;width:320px;max-width:calc(100vw - 20px);background:var(--surface,#fff);border:1px solid var(--border,#e2e8f0);border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,.13);overflow:hidden;opacity:0;pointer-events:none;transform:translateY(6px);transition:opacity .18s,transform .2s cubic-bezier(.22,1,.36,1);}' +
    '.hpd.open{opacity:1;pointer-events:all;transform:translateY(0);}' +
    '.hpd-head{display:flex;align-items:center;justify-content:space-between;padding:12px 14px 10px;border-bottom:1px solid var(--border,#e2e8f0);}' +
    '.hpd-head-title{font-size:13px;font-weight:700;color:var(--text,#0f172a);}' +
    '.hpd-head-action{font-size:11px;color:var(--accent,#1995AD);font-weight:600;cursor:pointer;background:none;border:none;padding:0;}' +
    '.hpd-item{display:flex;align-items:flex-start;gap:10px;padding:10px 14px;text-decoration:none;color:inherit;border-bottom:1px solid var(--surface-2,#f8fafc);transition:background .12s;}' +
    '.hpd-item:hover{background:var(--surface-2,#f8fafc);}' +
    '.hpd-notif-ico{width:34px;height:34px;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}' +
    '.hpd-notif-ico .mi{font-size:17px;}' +
    '.hpd-notif-body{flex:1;min-width:0;}' +
    '.hpd-notif-title{font-size:12px;font-weight:600;color:var(--text,#0f172a);line-height:1.35;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}' +
    '.hpd-notif-meta{font-size:11px;color:var(--muted,#94a3b8);margin-top:2px;}' +
    '.hpd-unread-dot{width:7px;height:7px;border-radius:50%;background:var(--accent,#1995AD);flex-shrink:0;margin-top:5px;}' +
    '.hpd-section{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:var(--muted,#94a3b8);padding:7px 14px 5px;background:var(--surface-2,#f8fafc);border-top:1px solid var(--border,#e2e8f0);}' +
    '.hpd-mail-init{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:12px;font-weight:700;color:#fff;}' +
    '.hpd-mail-group-ico{width:34px;height:34px;border-radius:50%;background:rgba(25,149,173,.1);display:flex;align-items:center;justify-content:center;flex-shrink:0;}' +
    '.hpd-mail-group-ico .mi{font-size:18px;color:#1995AD;}' +
    '.hpd-mail-body{flex:1;min-width:0;}' +
    '.hpd-mail-name{font-size:12px;font-weight:700;color:var(--text,#0f172a);}' +
    '.hpd-mail-msg{font-size:11px;color:#64748b;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;margin-top:1px;}' +
    '.hpd-mail-time{font-size:10px;color:#94a3b8;margin-top:2px;}' +
    '.hpd-mail-badge{min-width:18px;height:18px;border-radius:99px;background:#1995AD;color:#fff;font-size:10px;font-weight:700;display:flex;align-items:center;justify-content:center;padding:0 4px;flex-shrink:0;}' +
    '.hpd-footer{padding:10px 14px;border-top:1px solid var(--border,#e2e8f0);display:flex;gap:8px;}' +
    '.hpd-footer-btn{flex:1;display:flex;align-items:center;justify-content:center;gap:5px;padding:7px 10px;border-radius:7px;font-size:11px;font-weight:700;text-decoration:none;background:#f8fafc;color:#0f172a;border:1px solid #e2e8f0;transition:background .12s;}' +
    '.hpd-footer-btn:hover{background:#e2e8f0;}' +
    '.hpd-footer-btn .mi{font-size:14px;}';
  document.head.appendChild(s);

  /* ── Notification dropdown ── */
  var notifData = [
    { icon: 'assignment', color: '#2563eb', bg: '#eff6ff', title: 'Physics Essay Draft posted',    meta: 'Mr. Sophea \xb7 12m ago',   unread: true  },
    { icon: 'grade',      color: '#16a34a', bg: '#f0fdf4', title: 'Chemistry graded: 88%',          meta: 'Ms. Kiry \xb7 2h ago',      unread: true  },
    { icon: 'campaign',   color: '#1995AD', bg: 'rgba(25,149,173,.08)', title: 'Science Fair registration open', meta: 'School \xb7 Yesterday', unread: false }
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
        '<button class="hpd-head-action">Mark all read</button>' +
      '</div>' +
      notifItemsHtml +
      '<div class="hpd-footer">' +
        '<a href="' + notifLink + '" class="hpd-footer-btn">' +
          '<span class="mi">notifications</span>View all' +
        '</a>' +
      '</div>' +
    '</div>';
  var notifPanel = notifPanelEl.firstChild;
  document.body.appendChild(notifPanel);

  /* ── Mail dropdown ── */
  var directData = [
    { initials: 'PS', color: '#7c3aed', name: 'Dr. Pov Sophea', msg: 'Please review Chapter 7 before tomorrow’s lab…', time: '5m ago',  badge: 2, href: chatLink },
    { initials: 'RL', color: '#0891b2', name: 'Ms. Rin Lina',   msg: 'Your essay submission was received.',                                time: '1h ago', badge: 1, href: chatLink }
  ];
  var groupData = [
    { name: 'Grade 10 Science', msg: 'Tomorrow’s quiz covers chapters 5–7', time: '30m ago', badge: 5, href: groupChatLink },
    { name: 'Study Group 10A', msg: 'Can anyone share notes from today?',                            time: '2h ago',  badge: 3, href: groupChatLink }
  ];

  var mailItemsHtml = '<div class="hpd-section">Direct Messages</div>';
  for (var d = 0; d < directData.length; d++) {
    var dm = directData[d];
    mailItemsHtml +=
      '<a href="' + dm.href + '" class="hpd-item">' +
        '<div class="hpd-mail-init" style="background:' + dm.color + '">' + dm.initials + '</div>' +
        '<div class="hpd-mail-body">' +
          '<div class="hpd-mail-name">' + dm.name + '</div>' +
          '<div class="hpd-mail-msg">' + dm.msg + '</div>' +
          '<div class="hpd-mail-time">' + dm.time + '</div>' +
        '</div>' +
        '<span class="hpd-mail-badge">' + dm.badge + '</span>' +
      '</a>';
  }
  mailItemsHtml += '<div class="hpd-section">Group Chats</div>';
  for (var g = 0; g < groupData.length; g++) {
    var gm = groupData[g];
    mailItemsHtml +=
      '<a href="' + gm.href + '" class="hpd-item">' +
        '<div class="hpd-mail-group-ico"><span class="mi">group</span></div>' +
        '<div class="hpd-mail-body">' +
          '<div class="hpd-mail-name">' + gm.name + '</div>' +
          '<div class="hpd-mail-msg">' + gm.msg + '</div>' +
          '<div class="hpd-mail-time">' + gm.time + '</div>' +
        '</div>' +
        '<span class="hpd-mail-badge">' + gm.badge + '</span>' +
      '</a>';
  }

  var mailPanelEl = document.createElement('div');
  mailPanelEl.innerHTML =
    '<div class="hpd" id="htbMailPanel">' +
      '<div class="hpd-head">' +
        '<span class="hpd-head-title">Messages</span>' +
      '</div>' +
      mailItemsHtml +
      '<div class="hpd-footer">' +
        '<a href="' + chatLink + '" class="hpd-footer-btn">' +
          '<span class="mi">chat</span>Direct Chat' +
        '</a>' +
        '<a href="' + groupChatLink + '" class="hpd-footer-btn">' +
          '<span class="mi">group</span>Group Chat' +
        '</a>' +
      '</div>' +
    '</div>';
  var mailPanel = mailPanelEl.firstChild;
  document.body.appendChild(mailPanel);

  /* ── Panel positioning ── */
  function posBelow(btn, panel) {
    var rect = btn.getBoundingClientRect();
    panel.style.top   = (rect.bottom + 8) + 'px';
    panel.style.right = (window.innerWidth - rect.right) + 'px';
    panel.style.left  = 'auto';
  }

  /* ── Notif button ── */
  var notifBtn = document.getElementById('htbNotifBtn');
  if (notifBtn) {
    notifBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      var wasOpen = notifPanel.classList.contains('open');
      closePanels(); closeDD();
      if (!wasOpen) { posBelow(notifBtn, notifPanel); notifPanel.classList.add('open'); }
    });
  }

  /* ── Mail button ── */
  var mailBtn = document.getElementById('htbMailBtn');
  if (mailBtn) {
    mailBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      var wasOpen = mailPanel.classList.contains('open');
      closePanels(); closeDD();
      if (!wasOpen) { posBelow(mailBtn, mailPanel); mailPanel.classList.add('open'); }
    });
  }

  /* ── Close panels on outside click ── */
  document.addEventListener('click', function (e) {
    var nb = document.getElementById('htbNotifBtn');
    var mb = document.getElementById('htbMailBtn');
    if (!notifPanel.contains(e.target) && !(nb && nb.contains(e.target))) {
      notifPanel.classList.remove('open');
    }
    if (!mailPanel.contains(e.target) && !(mb && mb.contains(e.target))) {
      mailPanel.classList.remove('open');
    }
  });

  /* ── Reposition on scroll/resize ── */
  function reposOpen() {
    var nb = document.getElementById('htbNotifBtn');
    var mb = document.getElementById('htbMailBtn');
    if (nb && notifPanel.classList.contains('open')) posBelow(nb, notifPanel);
    if (mb && mailPanel.classList.contains('open'))  posBelow(mb, mailPanel);
  }
  window.addEventListener('resize', reposOpen);
  window.addEventListener('scroll', reposOpen, true);

})();
