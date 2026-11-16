/* ══════════════════════════════════════
   NGIS HERO BANNER — Shared builder
   Configure per-page via window.HERO_CONFIG
   before loading this script.
   ══════════════════════════════════════ */

(function () {
  /* ── Shared Bootstrap-icon engine loader (idempotent) ──────────
     The shared top navigation renders icons as data-ngis-icon slots
     with their Material ligature text kept as a no-engine fallback.
     This guarantees the official Bootstrap Icons engine is available
     to hydrate them on every portal page. */
  try {
    if (!window.__NGIS_ICON_ENGINE__) {
      window.__NGIS_ICON_ENGINE__ = true;
      if (!(window.NGIS && window.NGIS.icon) && !document.querySelector('script[src*="action-icons.js"]')) {
        var _root = (window.location.pathname || '').indexOf('/pages/') !== -1 ? '../../' : '';
        if (!document.querySelector('link[href*="action-icons.css"]')) {
          var _l = document.createElement('link');
          _l.rel = 'stylesheet';
          _l.href = _root + 'assets/css/action-icons.css?v=1.13.2';
          document.head.appendChild(_l);
        }
        var _s = document.createElement('script');
        _s.src = _root + 'assets/js/action-icons.js?v=1.13.2';
        _s.defer = true;
        document.head.appendChild(_s);
      }
    }
  } catch (e) { /* icons fall back to ligature glyphs */ }


  var C = window.HERO_CONFIG || {};

  /* Ensure Inter is loaded */
  if (!document.querySelector('link[href*="family=Inter"]')) {
    var fLink = document.createElement("link");
    fLink.rel = "stylesheet";
    fLink.href = "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Kantumruy+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap";
    document.head.appendChild(fLink);
  }

  /* ── Live date ── */
  /* ── Live date ── */
  var DAYS   = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  var MONTHS = ['January','February','March','April','May','June',
                'July','August','September','October','November','December'];
  var now    = new Date();
  var dateStr = DAYS[now.getDay()] + ', ' + MONTHS[now.getMonth()] + ' ' +
                now.getDate() + ', ' + now.getFullYear();

  /* ── Role & Path Resolution ── */
  var VALID_ROLES = ['admin', 'superadmin', 'principal', 'teacher', 'student', 'staff'];
  var STAFF_ALLOWED_FILES = ['admin-services.html', 'principal-lost-found.html', 'admin-campuses.html', 'admin-school-information.html', 'admin-settings.html'];
  var PRINCIPAL_ADMIN_FILES = ['admin-school-information.html', 'admin-dashboard-content.html', 'admin-timetables.html'];
  function normHeroRole(r) {
    if (!r) return '';
    r = String(r).trim().toLowerCase();
    if (r === 'super_admin' || r === 'superadmin') return 'superadmin';
    if (r === 'editor') return 'admin';
    return r;
  }
  function canServeHeroRole(r, seg, file) {
    if (VALID_ROLES.indexOf(r) === -1) return false;
    if (!seg || seg === 'shared') return true;
    if (r === 'staff') return STAFF_ALLOWED_FILES.indexOf(file) !== -1;
    if (r === 'superadmin' || r === 'admin') return seg === 'admin' || seg === 'principal';
    if (r === 'principal') return seg === 'principal' || PRINCIPAL_ADMIN_FILES.indexOf(file) !== -1;
    return seg === r;
  }

  var pathname = (window.location.pathname || '').replace(/\\/g, '/').toLowerCase();
  var fileOnly = (pathname.split('/').pop() || '').toLowerCase();
  var params = new URLSearchParams(window.location.search || '');
  var queryRole = normHeroRole(params.get('portal') || params.get('role') || '');
  var pathMatch = pathname.match(/\/pages\/(admin|teacher|student|principal|shared)\//);
  var pathRole = pathMatch ? pathMatch[1] : '';

  var storedRole = '';
  try { storedRole = normHeroRole(localStorage.getItem('ngis_active_portal') || ''); } catch (e) {}

  var explicitSession = false;
  var sessionRole = '';
  try {
    var mode = localStorage.getItem('ngis_session_mode');
    var rawUser = localStorage.getItem('ngis_user');
    if (rawUser) {
      var u = JSON.parse(rawUser);
      if (u && u.role) {
        sessionRole = normHeroRole(u.portal || u.role);
        explicitSession = (mode !== 'passive');
      }
    }
  } catch (e) {}

  var pageCfgRole = normHeroRole(window.PAGE && window.PAGE.role);
  var activeRole = 'student';
  if (explicitSession && sessionRole && canServeHeroRole(sessionRole, pathRole, fileOnly)) {
    if (queryRole && canServeHeroRole(queryRole, pathRole, fileOnly) && (queryRole === sessionRole || sessionRole === 'superadmin' || (sessionRole === 'admin' && queryRole !== 'student'))) {
      activeRole = queryRole;
    } else {
      activeRole = sessionRole;
    }
  } else if (queryRole && canServeHeroRole(queryRole, pathRole, fileOnly)) {
    activeRole = queryRole;
  } else if ((storedRole === 'staff' || storedRole === 'superadmin') && canServeHeroRole(storedRole, pathRole, fileOnly)) {
    activeRole = storedRole;
  } else if (pathRole && pathRole !== 'shared' && VALID_ROLES.indexOf(pathRole) !== -1) {
    activeRole = pathRole;
  } else if (pageCfgRole && canServeHeroRole(pageCfgRole, pathRole, fileOnly)) {
    activeRole = pageCfgRole;
  } else if (storedRole && canServeHeroRole(storedRole, pathRole, fileOnly)) {
    activeRole = storedRole;
  } else if (sessionRole && canServeHeroRole(sessionRole, pathRole, fileOnly)) {
    activeRole = sessionRole;
  }

  var rootPrefix = pathname.indexOf('/pages/') !== -1 ? '../../' : '';

  function resolveRoleUrl(targetRole, filename) {
    if (!filename) return '#';
    if (filename.indexOf('http') === 0 || filename.indexOf('#') === 0) return filename;
    var dest = filename;
    var folderRole = (targetRole === 'superadmin' || targetRole === 'staff') ? 'admin' : targetRole;
    if (filename.indexOf('/') === -1) {
      if (pathname.indexOf('/pages/' + folderRole + '/') === -1) {
        dest = (pathname.indexOf('/pages/') !== -1 ? '../' + folderRole + '/' : 'pages/' + folderRole + '/') + filename;
      }
    } else if (filename.indexOf('../') !== 0 && pathname.indexOf('/pages/') !== -1) {
      dest = '../../' + filename.replace(/^\/+/, '');
    }
    if ((targetRole === 'staff' || targetRole === 'superadmin') && dest.indexOf('portal=') === -1) {
      dest += (dest.indexOf('?') === -1 ? '?' : '&') + 'portal=' + encodeURIComponent(targetRole);
    } else if (dest.indexOf('/shared/') !== -1 && dest.indexOf('portal=') === -1) {
      dest += (dest.indexOf('?') === -1 ? '?' : '&') + 'portal=' + encodeURIComponent(targetRole);
    }
    return dest;
  }

  var ROLE_DEFAULTS = {
    superadmin: {
      brandSub: 'SUPER ADMIN PORTAL',
      name: 'Sok Panha Heng',
      roleMeta: 'Super Administrator',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=80&fit=crop&crop=face',
      id: 'Super Admin ID: SUP-2024-001',
      calendar: 'admin-calendar.html',
      profile: 'admin-settings.html',
      notif: 'admin-logs.html',
      home: 'admin.html',
      ddRows: [
        { icon: 'badge', text: 'Super Admin ID: SUP-2024-001' },
        { icon: 'verified_user', text: 'Role: Super Administrator' },
        { icon: 'business', text: 'Global Governance Suite' }
      ]
    },
    admin: {
      brandSub: 'ADMINISTRATION PORTAL',
      name: 'Sok Panha Heng',
      roleMeta: 'School Administrator',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=80&fit=crop&crop=face',
      id: 'Admin ID: ADM-2024-001',
      calendar: 'admin-calendar.html',
      profile: 'admin-settings.html',
      notif: '../shared/announcements.html',
      home: 'admin.html',
      ddRows: [
        { icon: 'badge', text: 'Admin ID: ADM-2024-001' },
        { icon: 'verified_user', text: 'Role: School Administrator' },
        { icon: 'business', text: 'Central Administration' }
      ]
    },
    staff: {
      brandSub: 'STAFF PORTAL',
      name: 'Chanthou Meas',
      roleMeta: 'Campus Operations Staff',
      avatar: 'https://images.pexels.com/photos/3184339/pexels-photo-3184339.jpeg?auto=compress&cs=tinysrgb&w=80',
      id: 'Staff ID: STF-2024-018',
      calendar: 'admin-services.html',
      profile: 'admin-settings.html',
      notif: '../shared/announcements.html',
      home: 'admin-services.html',
      ddRows: [
        { icon: 'badge', text: 'Staff ID: STF-2024-018' },
        { icon: 'support_agent', text: 'Role: Campus Operations Staff' },
        { icon: 'location_city', text: 'Campus Operations Desk' }
      ]
    },
    teacher: {
      brandSub: 'TEACHER PORTAL',
      name: 'Dr. Sarah Jenkins',
      roleMeta: 'Mathematics Lead',
      avatar: 'https://images.pexels.com/photos/1181686/pexels-photo-1181686.jpeg?auto=compress&cs=tinysrgb&w=80',
      id: 'Teacher ID: TCH-2024-042',
      calendar: 'teacher-calendar.html',
      profile: 'teacher-profile.html',
      notif: '../shared/announcements.html?portal=teacher',
      home: 'teacher.html',
      ddRows: [
        { icon: 'school', text: 'Faculty of Mathematics' },
        { icon: 'schedule', text: 'Term 2 • AY 2025–26' },
        { icon: 'class', text: 'Assigned: 5 Classes' }
      ]
    },
    principal: {
      brandSub: 'PRINCIPAL PORTAL',
      name: 'Dr. Ly Bunheng',
      roleMeta: 'Executive Principal',
      avatar: 'https://images.pexels.com/photos/2182970/pexels-photo-2182970.jpeg?auto=compress&cs=tinysrgb&w=80',
      id: 'Principal ID: PRN-2024-002',
      calendar: 'principal-reports.html',
      profile: 'principal-profile.html',
      notif: '../shared/announcements.html',
      home: 'principal.html',
      ddRows: [
        { icon: 'verified', text: 'Executive Campus Leadership' },
        { icon: 'domain', text: 'Phnom Penh Main Campus' },
        { icon: 'assessment', text: 'Cambridge & MoEYS' }
      ]
    },
    student: {
      brandSub: 'STUDENT PORTAL',
      name: 'Nrinphouneta Hok',
      roleMeta: 'Grade 10 • Term 2',
      avatar: 'https://images.pexels.com/photos/3785079/pexels-photo-3785079.jpeg?auto=compress&cs=tinysrgb&w=80',
      id: 'Student ID: 2026-STD-0142',
      calendar: 'student-calendar.html',
      profile: 'student-profile.html',
      notif: 'student-notifications.html',
      home: 'student.html',
      ddRows: [
        { icon: 'school', text: 'Grade 10 - Section A' },
        { icon: 'star', text: 'GPA 3.85' },
        { icon: 'badge', text: 'ID: 2026-STD-0142' }
      ]
    }
  };

  var rDef = ROLE_DEFAULTS[activeRole] || ROLE_DEFAULTS.student;
  var firstName = (C.name || rDef.name).split(' ')[0];

  /* ── Breadcrumb HTML ── */
  var crumbs = C.breadcrumbs || [];
  var crumbHtml = '';
  for (var i = 0; i < crumbs.length; i++) {
    crumbHtml += '<span class="mi htb-sep" data-ngis-icon="chevronRight" aria-hidden="true">chevron_right</span>';
    if (crumbs[i].href) {
      crumbHtml += '<a href="' + crumbs[i].href + '" class="htb-crumb-link">' + crumbs[i].label + '</a>';
    } else {
      crumbHtml += '<span class="htb-crumb-cur">' + crumbs[i].label + '</span>';
    }
  }

  /* ── Badges ── */
  var notifBadge = C.notifCount ? '<span class="htb-ctrl-badge">' + C.notifCount + '</span>' : '';

  /* ── Link targets ── */
  var notifLink     = C.notifLink ? resolveRoleUrl(activeRole, C.notifLink) : resolveRoleUrl(activeRole, rDef.notif || '../shared/announcements.html');
  var calendarLink  = C.calendarLink ? resolveRoleUrl(activeRole, C.calendarLink) : resolveRoleUrl(activeRole, rDef.calendar);
  var profileLink   = C.profileLink ? resolveRoleUrl(activeRole, C.profileLink) : resolveRoleUrl(activeRole, rDef.profile);

  /* ── Build hero HTML ── */
  var brandTitle = C.brandTitle || "New Gateway Int'l School";
  var brandSub   = C.brandSub   || C.portalLabel || rDef.brandSub;
  var roleMeta   = C.grade || C.roleMeta || C.role || rDef.roleMeta;
  var userName   = C.name || rDef.name;
  var userId     = C.id || rDef.id;
  var ADMIN_GROUP_PHOTO_RE = /pexels-photo-3184339/i;
  var DEFAULT_ADMIN_PORTRAIT = 'https://images.pexels.com/photos/2182970/pexels-photo-2182970.jpeg?auto=compress&cs=tinysrgb&w=160&h=160&fit=crop&crop=faces,top';
  function normalizeHeroAvatar(rawUrl) {
    var src = String(rawUrl || '').trim();
    if (!src || ADMIN_GROUP_PHOTO_RE.test(src)) {
      src = (activeRole === 'admin' || !rDef.avatar) ? DEFAULT_ADMIN_PORTRAIT : rDef.avatar;
    }
    if (/images\.pexels\.com\/photos\//i.test(src)) {
      try {
        var pu = new URL(src);
        pu.searchParams.set('auto', 'compress');
        pu.searchParams.set('cs', 'tinysrgb');
        pu.searchParams.set('w', '160');
        pu.searchParams.set('h', '160');
        pu.searchParams.set('fit', 'crop');
        pu.searchParams.set('crop', 'faces,top');
        return pu.toString();
      } catch (_) {}
    }
    if (/images\.unsplash\.com\/photo-/i.test(src)) {
      try {
        var uu = new URL(src);
        uu.searchParams.set('w', '160');
        uu.searchParams.set('h', '160');
        uu.searchParams.set('fit', 'crop');
        uu.searchParams.set('crop', 'faces,top');
        return uu.toString();
      } catch (_) {}
    }
    return src;
  }
  function heroInitials(fullName) {
    var parts = String(fullName || 'U').replace(/^(Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.|Coach)\s+/i, '').trim().split(/\s+/).filter(Boolean);
    if (!parts.length) return 'U';
    if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }
  var userAvatar = normalizeHeroAvatar(C.avatarSm || C.avatar || rDef.avatar);
  var userInitials = heroInitials(userName);

  var portalHomeUrl = resolveRoleUrl(activeRole, rDef.home);
  var homeTarget = C.homeLink || portalHomeUrl;

  var breadcrumbsHtml = '';
  if (crumbs.length > 0) {
    breadcrumbsHtml = '<a href="' + homeTarget + '" class="htb-crumb-home"><span class="mi" data-ngis-icon="home" aria-hidden="true">home</span><span>Home</span></a>';
    for (var i = 0; i < crumbs.length; i++) {
      breadcrumbsHtml += '<span class="htb-crumb-sep">/</span>';
      if (crumbs[i].href) {
        breadcrumbsHtml += '<a href="' + crumbs[i].href + '" class="htb-crumb-item">' + crumbs[i].label + '</a>';
      } else {
        breadcrumbsHtml += '<span class="htb-crumb-cur">' + crumbs[i].label + '</span>';
      }
    }
  } else {
    breadcrumbsHtml = '<a href="' + homeTarget + '" class="htb-crumb-home"><span class="mi" data-ngis-icon="home" aria-hidden="true">home</span><span>Home</span></a><span class="htb-crumb-sep">/</span><a href="#" class="htb-crumb-item">Academics</a><span class="htb-crumb-sep">/</span><span class="htb-crumb-cur">' + (C.title || 'Dashboard Overview') + '</span>';
  }

  /* ── Header Color Rule: Main page vs Subpage ── */
  var filename = (pathname.split('/').pop() || '').toLowerCase();
  var isMainFilename = (
    filename === 'student.html' ||
    filename === 'teacher.html' ||
    filename === 'principal.html' ||
    filename === 'index.html' ||
    filename === ''
  );
  var isMainPage = (C.isMainPage === true || C.isMain === true || C.showHeroBody === true) ||
    (isMainFilename && window.PAGE && (window.PAGE.active === 'dashboard' || window.PAGE.active === 'home'));

  // Admin portal pages do not display the large hero-body greeting banner
  if (C.showHeroBody === false || (activeRole === 'admin' && C.showHeroBody !== true) || (filename === 'admin.html' && C.showHeroBody !== true)) {
    isMainPage = false;
  }
  var placeholder = document.getElementById('heroBanner');
  var hasMobileAppbar = Boolean(document.querySelector('.mobile-appbar, div[class*="md:hidden"] [data-action="toggle-sidebar"], header[class*="md:hidden"]'));
  var hasLgMobileHeader = Boolean(
    (placeholder && placeholder.className && placeholder.className.indexOf('lg:block') !== -1) ||
    document.querySelector('header[class*="lg:hidden"], div[class*="lg:hidden"] [data-action="toggle-sidebar"], div[class*="lg:hidden"] .hamburger-btn')
  );
  var heroExtraClass = '';
  if (placeholder && placeholder.className && placeholder.className.indexOf('no-print') !== -1) heroExtraClass += ' no-print';
  if (hasMobileAppbar) heroExtraClass += ' has-mobile-appbar';
  if (hasLgMobileHeader) heroExtraClass += ' has-lg-mobile-appbar';
  var heroClass = (isMainPage ? 'hero hero-main' : 'hero hero-subpage hero-transparent') + heroExtraClass;

  var logoSrc = C.logoSrc || (rootPrefix + 'assets/images/logo.png');

  var html =
    '<header class="' + heroClass + '" role="banner">' +

      '<!-- ── Tier 1: Main Header Bar ── -->' +
      '<div class="hero-topbar">' +

        '<button type="button" class="htb-hamburger hamburger-btn mobile-hamburger-btn" id="htbHamburger" data-action="toggle-sidebar" aria-label="Open menu" aria-expanded="false" title="Open navigation">' +
          '<span class="mi" data-ngis-icon="menu" aria-hidden="true">menu</span>' +
        '</button>' +

        '<!-- Left: Brand Logo Image -->' +
        '<a href="' + homeTarget + '" class="htb-brand-wrap" aria-label="New Gateway International School">' +
          '<img class="htb-brand-logo-img" src="' + logoSrc + '" alt="New Gateway International School" onerror="this.onerror=null;this.src=\'../../assets/images/logo.png\'">' +
        '</a>' +

        '<!-- Center: Global Search Capsule -->' +
        '<div class="htb-search-wrap" role="search">' +
          '<span class="mi htb-search-icon" data-ngis-icon="search" aria-hidden="true">search</span>' +
          '<input type="search" class="htb-search-input" id="htbSearchInput" placeholder="Search courses, syllabi, tutors, grades…" aria-label="Search courses, syllabi, tutors, grades">' +
          '<kbd class="htb-search-kbd">⌘ K</kbd>' +
        '</div>' +

        '<!-- Right: Controls & User Profile -->' +
        '<div class="htb-right-controls">' +
          '<a href="' + calendarLink + '" class="htb-ctrl-btn" id="htbCalBtn" title="Calendar" aria-label="Calendar">' +
            '<span class="mi" data-ngis-icon="calendar" aria-hidden="true">calendar_today</span>' +
          '</a>' +
          '<button type="button" id="htbNotifBtn" class="htb-ctrl-btn" title="Notifications" aria-label="Notifications">' +
            '<span class="mi" data-ngis-icon="bell" aria-hidden="true">notifications</span>' +
            (notifBadge || '<span class="htb-ctrl-badge">3</span>') +
          '</button>' +
          (activeRole === 'student' ?
          '<a href="' + (C.chatLink || resolveRoleUrl('student', 'student-notifications.html')) + '" class="htb-ctrl-btn" title="Messages" aria-label="Messages">' +
            '<span class="mi" data-ngis-icon="mail" aria-hidden="true">mail</span>' +
            '<span class="htb-ctrl-badge" style="background:#92243D">11</span>' +
          '</a>' : '') +


          '<div class="htb-ctrl-divider" aria-hidden="true"></div>' +

          '<div class="htb-profile-chip" id="htbProfile" role="button" tabindex="0" aria-label="Account menu">' +
            '<div class="htb-chip-avatar-wrap">' +
              (userAvatar ?
                '<span class="htb-chip-initials" aria-hidden="true" style="display:none">' + userInitials + '</span>' +
                '<img class="htb-chip-avatar" src="' + userAvatar + '" alt="' + userName + '" onerror="this.style.display=\'none\';var f=this.parentElement.querySelector(\'.htb-chip-initials\');if(f)f.style.display=\'flex\';">' :
                '<span class="htb-chip-initials" aria-hidden="true" style="display:flex">' + userInitials + '</span>'
              ) +
              '<span class="htb-online-pip" title="Active"></span>' +
            '</div>' +
            '<div class="htb-chip-text">' +
              '<div class="htb-chip-name-row">' +
                '<span class="htb-chip-name">' + userName + '</span>' +
              '</div>' +
              '<span class="htb-chip-meta">' + roleMeta + '</span>' +
            '</div>' +
          '</div>' +
        '</div>' +

      '</div>' +

      '<div class="htb-dd-backdrop" id="htbBackdrop"></div>' +

      ((C.showHeroBody !== false && (C.showHeroBody === true || C.isDashboard === true || isMainPage === true)) ?
      '<div class="hero-body">' +
        '<div class="hero-text">' +
          '<div class="hero-date">' + dateStr + '</div>' +
          '<h1 class="hero-title">' + (C.title || 'Welcome to your dashboard') + '</h1>' +
          '<p class="hero-greeting">' + (C.greeting || 'Hello, ' + firstName + '! Ready for today?') + '</p>' +
        '</div>' +
      '</div>' : '') +

    '</header>';

  /* ── Inject hero ── */
  if (placeholder) placeholder.outerHTML = html;

  /* ── Profile dropdown HTML ── */
  var ddRows = C.ddRows || rDef.ddRows || [];
  var rowsHtml = '';
  for (var j = 0; j < ddRows.length; j++) {
    rowsHtml += '<div class="htb-dd-row"><span class="mi" data-ngis-icon="' + ddRows[j].icon + '">' + ddRows[j].icon + '</span><span>' + ddRows[j].text + '</span></div>';
  }

  var ddHtml =
    '<div class="htb-dropdown" id="htbDropdown">' +
      '<div class="htb-dd-header">' +
        '<div class="htb-dd-avatar-wrap">' +
          (userAvatar ?
            '<span class="htb-dd-initials" aria-hidden="true" style="display:none">' + userInitials + '</span>' +
            '<img class="htb-dd-avatar" src="' + userAvatar + '" alt="' + userName + '" onerror="this.style.display=\'none\';var f=this.parentElement.querySelector(\'.htb-dd-initials\');if(f)f.style.display=\'flex\';">' :
            '<span class="htb-dd-initials" aria-hidden="true" style="display:flex">' + userInitials + '</span>'
          ) +
        '</div>' +
        '<div>' +
          '<div class="htb-dd-name">' + userName + '</div>' +
          '<div class="htb-dd-id">' + userId + '</div>' +
        '</div>' +
      '</div>' +
      '<div class="htb-dd-divider"></div>' +
      '<div class="htb-dd-divider"></div>' +
      '<div class="htb-dd-demo-box">' +
        '<div class="htb-dd-demo-title"><span class="mi" style="font-size:15px" data-ngis-icon="sort" aria-hidden="true">swap_horiz</span>Switch Demo Role</div>' +
        '<div class="htb-dd-demo-grid">' +
          '<a href="' + resolveRoleUrl('student', 'student.html') + '" class="htb-dd-demo-item' + (activeRole==='student'?' active':'') + '" onclick="window.NGISAuth&&window.NGISAuth.setDemoUser(\'student\')">Student</a>' +
          '<a href="' + resolveRoleUrl('teacher', 'teacher.html') + '" class="htb-dd-demo-item' + (activeRole==='teacher'?' active':'') + '" onclick="window.NGISAuth&&window.NGISAuth.setDemoUser(\'teacher\')">Teacher</a>' +
          '<a href="' + resolveRoleUrl('admin', 'admin.html') + '" class="htb-dd-demo-item' + (activeRole==='admin'?' active':'') + '" onclick="window.NGISAuth&&window.NGISAuth.setDemoUser(\'admin\')">Admin</a>' +
          '<a href="' + resolveRoleUrl('principal', 'principal.html') + '" class="htb-dd-demo-item' + (activeRole==='principal'?' active':'') + '" onclick="window.NGISAuth&&window.NGISAuth.setDemoUser(\'principal\')">Principal</a>' +
          '<a href="' + resolveRoleUrl('staff', 'admin-services.html') + '" class="htb-dd-demo-item' + (activeRole==='staff'?' active':'') + '" onclick="window.NGISAuth&&window.NGISAuth.setDemoUser(\'staff\')">Staff</a>' +
          '<a href="' + resolveRoleUrl('superadmin', 'admin.html') + '" class="htb-dd-demo-item' + (activeRole==='superadmin'?' active':'') + '" onclick="window.NGISAuth&&window.NGISAuth.setDemoUser(\'superadmin\')">Super Admin</a>' +
        '</div>' +
      '</div>' +
      '<div class="htb-dd-divider"></div>' +
      '<div class="htb-dd-actions">' +
        '<a href="' + profileLink + '" class="htb-dd-btn">' +
          '<span class="mi" data-ngis-icon="user" aria-hidden="true">manage_accounts</span>My Profile' +
        '</a>' +
        '<a href="' + (C.signOutLink || (rootPrefix + 'index.html')) + '" class="htb-dd-btn htb-dd-btn-danger" id="htbSignOutBtn" onclick="window.NGISAuth&&window.NGISAuth.clearSession()">' +
          '<span class="mi" data-ngis-icon="logout" aria-hidden="true">logout</span>Sign Out' +
        '</a>' +
      '</div>' +
    '</div>';

  var ddEl = document.createElement('div');
  ddEl.innerHTML = ddHtml;
  var dropdown = ddEl.firstChild;
  document.body.appendChild(dropdown);

  /* ── Profile dropdown positioning ── */
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
    if (searchPanel) searchPanel.classList.remove('open');
    var nb = document.getElementById('htbNotifBtn');
    if (nb) nb.classList.remove('active');
  }

  function openDD() {
    closePanels();
    positionDropdown();
    dropdown.classList.add('open');
    var arr = document.getElementById('htbParr');
    if (arr) arr.classList.add('open');
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

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeDD(); closePanels(); }
    if ((e.metaKey || e.ctrlKey) && (e.key === 'k' || e.key === 'K')) {
      e.preventDefault();
      var sInp = document.getElementById('htbSearchInput');
      if (sInp) sInp.focus();
    }
  });
  window.addEventListener('resize',   function () { if (dropdown.classList.contains('open')) positionDropdown(); });
  window.addEventListener('scroll',   function () { if (dropdown.classList.contains('open')) positionDropdown(); }, true);

  /* ── Hamburger → layout.js sidebar ── */
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

  /* ── Inject CSS ── */
  var s = document.createElement('style');
  s.textContent =
    '.htb-notif-btn{background:none;border:none;padding:0;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;color:rgba(255,255,255,.88);line-height:1;}' +
    '.hpd{position:fixed;z-index:9100;width:320px;max-width:calc(100vw - 20px);background:var(--surface,#fff);border:1px solid var(--border,#E5E5E8);border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,.13);overflow:hidden;opacity:0;pointer-events:none;transform:translateY(6px);transition:opacity .18s,transform .2s cubic-bezier(.22,1,.36,1);}' +
    '.hpd.open{opacity:1;pointer-events:all;transform:translateY(0);}' +
    '.hpd-head{display:flex;align-items:center;justify-content:space-between;padding:12px 14px 10px;border-bottom:1px solid var(--border,#E5E5E8);}' +
    '.hpd-head-title{font-size:13px;font-weight: 400;color:var(--text,#000000);}' +
    '.hpd-head-action{font-size:11px;color:var(--accent,#202F63);font-weight: 400;cursor:pointer;background:none;border:none;padding:0;}' +
    '.hpd-item{display:flex;align-items:flex-start;gap:10px;padding:10px 14px;text-decoration:none;color:inherit;border-bottom:1px solid var(--surface-2,#F3F3F5);transition:background .12s;}' +
    '.hpd-item:hover{background:var(--surface-2,#F3F3F5);}' +
    '.hpd-notif-ico{width:34px;height:34px;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}' +
    '.hpd-notif-ico .mi{font-size:17px;}' +
    '.hpd-notif-body{flex:1;min-width:0;}' +
    '.hpd-notif-title{font-size:12px;font-weight: 400;color:var(--text,#000000);line-height:1.35;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}' +
    '.hpd-notif-meta{font-size:11px;color:var(--muted,#77777F);margin-top:2px;}' +
    '.hpd-unread-dot{width:7px;height:7px;border-radius:50%;background:var(--accent,#202F63);flex-shrink:0;margin-top:5px;}' +
    '.hpd-section{font-size:10px;font-weight: 400;text-transform:uppercase;letter-spacing:.6px;color:var(--muted,#77777F);padding:7px 14px 5px;background:var(--surface-2,#F3F3F5);border-top:1px solid var(--border,#E5E5E8);}' +
    '.hpd-mail-init{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:12px;font-weight: 400;color:#fff;}' +
    '.hpd-mail-group-ico{width:34px;height:34px;border-radius:50%;background:var(--primary-soft,rgba(25,149,173,.1));display:flex;align-items:center;justify-content:center;flex-shrink:0;}' +
    '.hpd-mail-group-ico .mi{font-size:18px;color:var(--primary,#202F63);}' +
    '.hpd-mail-body{flex:1;min-width:0;}' +
    '.hpd-mail-name{font-size:12px;font-weight: 400;color:var(--text,#000000);}' +
    '.hpd-mail-msg{font-size:11px;color:var(--muted,#555555);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;margin-top:1px;}' +
    '.hpd-mail-time{font-size:10px;color:var(--muted,#77777F);margin-top:2px;}' +
    '.hpd-mail-badge{min-width:18px;height:18px;border-radius:99px;background:var(--accent,#202F63);color:#fff;font-size:10px;font-weight: 400;display:flex;align-items:center;justify-content:center;padding:0 4px;flex-shrink:0;}' +
    '.hpd-footer{padding:10px 14px;border-top:1px solid var(--border,#E5E5E8);display:flex;gap:8px;}' +
    '.hpd-footer-btn{flex:1;display:flex;align-items:center;justify-content:center;gap:5px;padding:7px 10px;border-radius:7px;font-size:11px;font-weight: 400;text-decoration:none;background:var(--surface-2,#F3F3F5);color:var(--text,#000000);border:1px solid var(--border,#E5E5E8);transition:background .12s;}' +
    '.hpd-footer-btn:hover{background:var(--border,#E5E5E8);}' +
    '.hpd-footer-btn .mi{font-size:14px;}' +
    '.hpd-search{width:360px;max-height:70vh;overflow-y:auto;}' +
    '.hpd-search-input-wrap{display:flex;align-items:center;gap:8px;padding:10px 14px;border-bottom:1px solid var(--border,#E5E5E8);position:sticky;top:0;background:var(--surface,#fff);}' +
    '.hpd-search-input{flex:1;border:none;outline:none;background:none;font-size:13px;color:var(--text,#000000);font-family:inherit;}' +
    '.hpd-empty{padding:20px 14px;font-size:12px;color:var(--muted,#77777F);text-align:center;line-height:1.5;}';
  document.head.appendChild(s);

  /* ── Notification dropdown ── */
  var notifData = [
    { icon: 'assignment', color: '#202F63', bg: '#F3F3F5', title: 'Physics Essay Draft posted',    meta: 'Mr. Sophea \xb7 12m ago',   unread: true  },
    { icon: 'grade',      color: '#000000', bg: '#F3F3F5', title: 'Chemistry graded: 88%',          meta: 'Ms. Kiry \xb7 2h ago',      unread: true  },
    { icon: 'campaign',   color: '#202F63', bg: 'rgba(25,149,173,.08)', title: 'Science Fair registration open', meta: 'School \xb7 Yesterday', unread: false }
  ];

  var notifItemsHtml = '';
  for (var n = 0; n < notifData.length; n++) {
    var nd = notifData[n];
    notifItemsHtml +=
      '<a href="' + notifLink + '" class="hpd-item">' +
        '<div class="hpd-notif-ico" style="background:' + nd.bg + '">' +
          '<span class="mi" style="color:' + nd.color + '" data-ngis-icon="' + nd.icon + '">' + nd.icon + '</span>' +
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
          '<span class="mi" data-ngis-icon="bell" aria-hidden="true">notifications</span>View all' +
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
        var badge = nb.querySelector('.htb-ctrl-badge') || nb.querySelector('.htb-badge');
        if (badge) badge.style.display = 'none';
      }
      markAllBtn.innerHTML = 'All read <svg class="inline-block w-3 h-3 ml-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>';
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
          var badge = nb.querySelector('.htb-ctrl-badge') || nb.querySelector('.htb-badge');
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

  /* ── Global search (admin only) ── */
  var searchPanel = null;
  var ROLE = activeRole || normHeroRole(window.PAGE && window.PAGE.role);
  if (ROLE === 'admin' || ROLE === 'superadmin') {
    var SEARCH_INDEX = [
      { type: 'Student',    name: 'Kosal Rith Mony',        sub: 'STU-2241 \xb7 11-A',       icon: 'school',              href: resolveRoleUrl(ROLE, 'admin-users-students.html') },
      { type: 'Student',    name: 'Sreylin Vuth',           sub: 'STU-2242 \xb7 6-B',        icon: 'school',              href: resolveRoleUrl(ROLE, 'admin-users-students.html') },
      { type: 'Student',    name: 'Heng Piseth',            sub: 'STU-2243 \xb7 12-A',       icon: 'school',              href: resolveRoleUrl(ROLE, 'admin-users-students.html') },
      { type: 'Teacher',    name: 'Dr. Sarah Jenkins',      sub: 'English Department',       icon: 'co_present',          href: resolveRoleUrl(ROLE, 'admin-users-teachers.html') },
      { type: 'Teacher',    name: 'Dr. Pov Chanthy',        sub: 'Chinese Department',       icon: 'co_present',          href: resolveRoleUrl(ROLE, 'admin-users-teachers.html') },
      { type: 'Admin',      name: 'Ms. Sok Kanha',          sub: 'Campus Admin \xb7 Sen Sok', icon: 'admin_panel_settings',href: resolveRoleUrl(ROLE, 'admin-users-admins.html') },
      { type: 'Principal',  name: 'Dr. Sok Chenda',         sub: 'Sen Sok Campus',           icon: 'military_tech',       href: resolveRoleUrl(ROLE, 'admin-users-principals.html') },
      { type: 'Department', name: 'English Department',     sub: '42 teachers',              icon: 'menu_book',           href: resolveRoleUrl(ROLE, 'admin-departments.html') },
      { type: 'Department', name: 'Khmer Department',       sub: '38 teachers',              icon: 'translate',           href: resolveRoleUrl(ROLE, 'admin-departments.html') },
      { type: 'Department', name: 'Chinese Department',     sub: '24 teachers',              icon: 'language',            href: resolveRoleUrl(ROLE, 'admin-departments.html') },
      { type: 'Campus',     name: 'Sen Sok Campus',         sub: '1,842 students',           icon: 'location_city',       href: resolveRoleUrl(ROLE, 'admin-campuses.html') },
      { type: 'Campus',     name: 'Depo Campus',            sub: '1,560 students',           icon: 'location_city',       href: resolveRoleUrl(ROLE, 'admin-campuses.html') },
      { type: 'Campus',     name: 'Bak Touk Campus',        sub: '1,418 students',           icon: 'location_city',       href: resolveRoleUrl(ROLE, 'admin-campuses.html') },
      { type: 'Class',      name: 'Grade 11-A',             sub: '32 students',              icon: 'school',              href: resolveRoleUrl(ROLE, 'admin-classes.html') },
      { type: 'Lesson',     name: 'Grammar Unit 5 — Tenses', sub: 'English \xb7 PDF',        icon: 'menu_book',           href: resolveRoleUrl(ROLE, 'admin-lessons.html') },
      { type: 'Exam',       name: 'HSK Mock Exam',          sub: 'Grade 12 \xb7 Published',  icon: 'edit_note',           href: resolveRoleUrl(ROLE, 'admin-exams.html') },
    ];

    var searchPanelEl = document.createElement('div');
    searchPanelEl.innerHTML =
      '<div class="hpd hpd-search" id="htbSearchPanel">' +
        '<div class="hpd-search-input-wrap">' +
          '<span class="mi" style="font-size:18px;color:var(--muted,#77777F)" data-ngis-icon="search" aria-hidden="true">search</span>' +
          '<input type="search" id="hpdSearchInput" class="hpd-search-input" placeholder="Search students, teachers, campuses…" aria-label="Search everything">' +
        '</div>' +
        '<div id="htbSearchResults"></div>' +
      '</div>';
    searchPanel = searchPanelEl.firstChild;
    document.body.appendChild(searchPanel);

    var searchResultsEl = document.getElementById('htbSearchResults');
    var searchInputEl   = searchPanel.querySelector('.hpd-search-input');

    function renderSearch(q) {
      q = (q || '').trim().toLowerCase();
      if (!q) {
        searchResultsEl.innerHTML = '<div class="hpd-empty">Type to search students, teachers, campuses, departments, and more.</div>';
        return;
      }
      var matches = SEARCH_INDEX.filter(function (item) {
        return item.name.toLowerCase().indexOf(q) !== -1 ||
               item.sub.toLowerCase().indexOf(q) !== -1 ||
               item.type.toLowerCase().indexOf(q) !== -1;
      }).slice(0, 8);
      if (!matches.length) {
        searchResultsEl.innerHTML = '<div class="hpd-empty">No results for “' + q + '”.</div>';
        return;
      }
      var html = '';
      var lastType = '';
      matches.forEach(function (m) {
        if (m.type !== lastType) { html += '<div class="hpd-section">' + m.type + 's</div>'; lastType = m.type; }
        html +=
          '<a href="' + m.href + '" class="hpd-item">' +
            '<div class="hpd-notif-ico" style="background:var(--primary-soft,rgba(31,107,58,.09))">' +
              '<span class="mi" style="color:var(--primary,#000000)" data-ngis-icon="' + m.icon + '">' + m.icon + '</span>' +
            '</div>' +
            '<div class="hpd-notif-body">' +
              '<div class="hpd-notif-title">' + m.name + '</div>' +
              '<div class="hpd-notif-meta">' + m.sub + '</div>' +
            '</div>' +
          '</a>';
      });
      searchResultsEl.innerHTML = html;
    }
    renderSearch('');
    searchInputEl.addEventListener('input', function () { renderSearch(searchInputEl.value); });

    var searchBtn = document.getElementById('htbSearchBtn');
    if (searchBtn) {
      searchBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        var wasOpen = searchPanel.classList.contains('open');
        closePanels(); closeDD();
        if (!wasOpen) {
          posBelow(searchBtn, searchPanel);
          searchPanel.classList.add('open');
          setTimeout(function () { searchInputEl.focus(); }, 50);
        }
      });
    }
    document.addEventListener('click', function (e) {
      var sb = document.getElementById('htbSearchBtn');
      if (!searchPanel.contains(e.target) && !(sb && sb.contains(e.target))) {
        searchPanel.classList.remove('open');
      }
    });
    document.addEventListener('keydown', function (e) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        closePanels(); closeDD();
        posBelowLeftAligned(searchBtn, searchPanel);
        searchPanel.classList.add('open');
        setTimeout(function () { searchInputEl.focus(); }, 50);
      }
    });
  }

  /* ── Panel positioning ── */
  function posBelow(btn, panel) {
    if (!btn || !panel) return;
    var rect = btn.getBoundingClientRect();
    panel.style.top = (rect.bottom + 8) + 'px';

    if (window.innerWidth <= 600) {
      panel.style.left = '12px';
      panel.style.right = '12px';
      panel.style.width = 'auto';
      panel.style.maxWidth = 'calc(100vw - 24px)';
      panel.style.marginLeft = 'auto';
      panel.style.marginRight = 'auto';
      return;
    }

    panel.style.width = '330px';
    panel.style.maxWidth = 'calc(100vw - 24px)';
    panel.style.left = 'auto';
    panel.style.marginLeft = '0';
    panel.style.marginRight = '0';

    var rightEdge = window.innerWidth - rect.right;
    if (rightEdge < 12) rightEdge = 12;
    if (window.innerWidth - rightEdge - 330 < 12) {
      rightEdge = Math.max(12, window.innerWidth - 330 - 12);
    }
    panel.style.right = rightEdge + 'px';
  }

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
    var sb = document.getElementById('htbSearchBtn');
    if (nb && notifPanel && notifPanel.classList.contains('open')) posBelow(nb, notifPanel);
    if (sb && searchPanel && searchPanel.classList.contains('open')) posBelow(sb, searchPanel);
  }
  window.addEventListener('resize', reposOpen);
  window.addEventListener('scroll', reposOpen, true);

})();
