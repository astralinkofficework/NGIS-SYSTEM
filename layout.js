/* ============================================================
   NGIS Layout Engine v3.0 — New Gateway International School
   Reads window.PAGE = { role, active, user } and renders the
   shared sidebar, topbar, mobile bottom-nav and breadcrumbs,
   then wires interactions. No build step — runs as plain files.
   ============================================================ */
(function () {
  "use strict";

  /* ------------------------------------------------------------------
     Categorised navigation per role (desktop sidebar).
     Each role has ordered GROUPS; every group has a title + icon and a
     list of links. Dividers + section labels are rendered between groups.

     Student & Parent portals are DEPARTMENT-CENTRIC: the learning modules
     (Attendance, Assignments, Report Cards, Exams, Timetable, Lessons) are
     intentionally NOT top-level items — they live inside each Department.
     Teacher & Admin keep their operator tools, grouped for clarity.
     ------------------------------------------------------------------ */
  const NAV = {
    admin: {
      brand: "Admin", meta: "New Gateway International School",
      groups: [
        { label:"Main", icon:"home", links:[
          { id:"dashboard", label:"Dashboard", icon:"dashboard", href:"pages/admin/admin.html" },
        ]},
        { id:"users", label:"User Management", icon:"group", collapsible:true, links:[
          { id:"students",   label:"Students",   icon:"school",             href:"pages/admin/admin-users.html?role=students" },
          { id:"teachers",   label:"Teachers",   icon:"co_present",         href:"pages/admin/admin-users.html?role=teachers" },
          { id:"parents",    label:"Parents",    icon:"family_restroom",    href:"pages/admin/admin-users.html?role=parents" },
          { id:"admins",     label:"Admins",     icon:"admin_panel_settings", href:"pages/admin/admin-users.html?role=admins" },
          { id:"principals", label:"Principals", icon:"military_tech",      href:"pages/admin/admin-users.html?role=principals" },
        ]},
        { id:"academic", label:"Academic", icon:"apartment", collapsible:true, links:[
          { id:"departments", label:"Departments", icon:"apartment",          href:"pages/admin/admin-departments.html" },
          { id:"campuses",    label:"Campuses",    icon:"location_city",      href:"pages/admin/admin-campuses.html" },
          { id:"classes",     label:"Classes",     icon:"school",             href:"pages/admin/admin-classes.html" },
          { id:"timetables",  label:"Timetable",   icon:"calendar_view_week", href:"pages/admin/admin-timetables.html" },
        ]},
        { id:"learning", label:"Learning", icon:"menu_book", collapsible:true, links:[
          { id:"lessons",     label:"Lessons",     icon:"menu_book",  href:"pages/admin/admin-lessons.html" },
          { id:"assignments", label:"Assignments", icon:"assignment", href:"pages/admin/admin-assignments.html" },
          { id:"exams",       label:"Exams",       icon:"edit_note",  href:"pages/admin/admin-exams.html" },
          { id:"grades",      label:"Grades",      icon:"grade",      href:"pages/admin/admin-grades.html" },
          { id:"lost-found",  label:"Lost & Found", icon:"inventory_2", href:"pages/student/student-lost-found.html" },
        ]},
        { id:"records", label:"Student Records", icon:"folder_shared", collapsible:true, links:[
          { id:"services",    label:"Student Services", icon:"assignment", href:"pages/admin/admin-services.html" },
          { id:"profiles",    label:"Student Profiles", icon:"badge",      href:"pages/admin/admin-users.html?role=students" },
          { id:"reports",     label:"Reports",         icon:"assessment", href:"pages/admin/admin-reports.html" },
        ]},
        { id:"messaging", label:"Messaging", icon:"forum", links:[
          { id:"chat",                label:"Direct Messages", icon:"mail", href:"pages/shared/chat.html", badge:"2" },
          { id:"class-chats",         label:"Class Chats", icon:"school", href:"pages/messaging/class-chats.html" },
          { id:"group-chat",          label:"Group Chats", icon:"groups", href:"pages/shared/group-chat.html", badge:"4" },
          { id:"department-channels", label:"Department Channels", icon:"apartment", href:"pages/messaging/department-channels.html" },
          { id:"campus-announcements", label:"Campus Announcements", icon:"campaign", href:"pages/messaging/campus-announcements.html" },
          { id:"announcements",       label:"School Announcements", icon:"newspaper", href:"pages/shared/announcements.html", badge:"3" },
          { id:"message-requests",    label:"Message Requests", icon:"mail", href:"pages/messaging/message-requests.html", badge:"3" },
          { id:"archived",            label:"Archived", icon:"archive", href:"pages/messaging/archived.html" },
          { id:"pinned",              label:"Pinned Messages", icon:"push_pin", href:"pages/messaging/pinned.html" },
        ]},
        { id:"comms", label:"Communication Tools", icon:"campaign", collapsible:true, links:[
          { id:"news",           label:"News CMS",       icon:"newspaper", href:"pages/admin/admin-news.html" },
          { id:"notifications",  label:"Notifications", icon:"notifications", href:"pages/admin/admin-logs.html" },
        ]},
        { id:"administration", label:"Administration", icon:"admin_panel_settings", collapsible:true, links:[
          { id:"logs",        label:"Audit Logs",         icon:"history",     href:"pages/admin/admin-logs.html" },
          { id:"messaging-admin", label:"Messaging Administration", icon:"forum", href:"pages/messaging/messaging-admin.html" },
          { id:"telegram-config", label:"Telegram Configuration", icon:"smart_toy", href:"pages/messaging/telegram-config.html" },
          { id:"messaging-audit", label:"Messaging Audit Logs", icon:"receipt_long", href:"pages/messaging/audit-logs.html" },
          { id:"roles",       label:"Roles & Permissions", icon:"shield_person", href:"pages/admin/admin-settings.html?tab=roles" },
          { id:"settings",    label:"System Settings",    icon:"settings",    href:"pages/admin/admin-settings.html" },
          { id:"backup",      label:"Backup & Restore",   icon:"backup",      href:"pages/admin/admin-settings.html?tab=backup" },
        ]},
        { id:"account", label:"Account", icon:"person", collapsible:true, links:[
          { id:"profile",     label:"My Profile", icon:"person",  href:"pages/admin/admin-settings.html" },
          { id:"preferences", label:"Preferences", icon:"tune",   href:"pages/admin/admin-settings.html?tab=notifications" },
          { id:"logout",      label:"Logout",     icon:"logout",  href:"index.html" },
        ]},
      ],
    },
    teacher: {
      brand: "Teacher", meta: "Academic Year 2025–26",
      groups: [
        { label:"Main", icon:"home", links:[
          { id:"dashboard", label:"Dashboard", icon:"dashboard", href:"pages/teacher/teacher.html" },
        ]},
        { label:"Teaching", icon:"school", links:[
          { id:"departments", label:"Departments", icon:"apartment", href:"pages/shared/departments.html" },
          { id:"classes",     label:"My Classes",  icon:"school",    href:"pages/teacher/teacher-classes.html" },
          { id:"lost-found",  label:"Lost & Found", icon:"inventory_2", href:"pages/student/student-lost-found.html" },
        ]},
        { id:"messaging", label:"Messaging", icon:"forum", links:[
          { id:"chat",                label:"Direct Messages", icon:"mail", href:"pages/shared/chat.html", badge:"2" },
          { id:"class-chats",         label:"Class Chats", icon:"school", href:"pages/messaging/class-chats.html" },
          { id:"group-chat",          label:"Group Chats", icon:"groups", href:"pages/shared/group-chat.html", badge:"3" },
          { id:"department-channels", label:"Department Channels", icon:"apartment", href:"pages/messaging/department-channels.html" },
          { id:"campus-announcements", label:"Campus Announcements", icon:"campaign", href:"pages/messaging/campus-announcements.html" },
          { id:"announcements",       label:"School Announcements", icon:"newspaper", href:"pages/shared/announcements.html", badge:"3" },
          { id:"message-requests",    label:"Message Requests", icon:"mail", href:"pages/messaging/message-requests.html", badge:"2" },
          { id:"pinned",              label:"Pinned Messages", icon:"push_pin", href:"pages/messaging/pinned.html" },
        ]},
        { label:"Account", icon:"person", links:[
          { id:"notifications", label:"Notifications", icon:"notifications", href:"pages/teacher/teacher-notifications.html", badge:"3" },
          { id:"profile",       label:"My Profile",    icon:"person",        href:"pages/teacher/teacher-profile.html" },
        ]},
      ],
    },
    student: {
      brand: "Student", meta: "Grade 11 · Section A · 2025–26",
      groups: [
        { label:"Main", icon:"home", links:[
          { id:"dashboard", label:"Dashboard", icon:"dashboard", href:"pages/student/student.html" },
        ]},
        { label:"Learning", icon:"school", links:[
          { id:"departments", label:"Departments", icon:"apartment", href:"pages/shared/departments.html" },
          { id:"services",    label:"Services Hub", icon:"grid_view", href:"pages/student/student-services.html" },
          { id:"clubs",       label:"Clubs & Activities", icon:"diversity_3", href:"pages/student/student-clubs.html" },
          { id:"lost-found",  label:"Lost & Found", icon:"inventory_2", href:"pages/student/student-lost-found.html" },
        ]},
        { id:"messaging", label:"Messaging", icon:"forum", links:[
          { id:"chat",                label:"Direct Messages", icon:"mail", href:"pages/shared/chat.html", badge:"3" },
          { id:"class-chats",         label:"Class Chats", icon:"school", href:"pages/messaging/class-chats.html", badge:"3" },
          { id:"group-chat",          label:"Group Chats", icon:"groups", href:"pages/shared/group-chat.html", badge:"2" },
          { id:"department-channels", label:"Department Channels", icon:"apartment", href:"pages/messaging/department-channels.html" },
          { id:"teacher-chat",        label:"Teacher Chat", icon:"chat", href:"pages/student/student-chat.html", badge:"3" },
          { id:"announcements",       label:"School Announcements", icon:"newspaper", href:"pages/shared/announcements.html", badge:"3" },
        ]},
        { label:"Account", icon:"person", links:[
          { id:"notifications", label:"Notifications", icon:"notifications", href:"pages/student/student-notifications.html", badge:"5" },
          { id:"profile",       label:"My Profile",    icon:"person",        href:"pages/student/student-profile.html" },
        ]},
      ],
    },
    parent: {
      brand: "Parent", meta: "Guardian Account · 2025–26",
      groups: [
        { label:"Main", icon:"home", links:[
          { id:"dashboard", label:"Dashboard",   icon:"dashboard",       href:"pages/parent/parent.html" },
          { id:"children",  label:"My Children", icon:"family_restroom", href:"pages/parent/parent-children.html" },
        ]},
        { label:"Learning", icon:"school", links:[
          { id:"departments", label:"Departments", icon:"apartment", href:"pages/shared/departments.html" },
          { id:"services",    label:"Student Services", icon:"assignment", href:"pages/parent/parent-services.html" },
          { id:"lost-found",  label:"Lost & Found", icon:"inventory_2", href:"pages/student/student-lost-found.html" },
        ]},
        { id:"messaging", label:"Messaging", icon:"forum", links:[
          { id:"chat",                label:"Direct Messages", icon:"mail", href:"pages/shared/chat.html", badge:"1" },
          { id:"announcements",       label:"School Announcements", icon:"newspaper", href:"pages/shared/announcements.html", badge:"1" },
          { id:"group-chat",          label:"Group Chats", icon:"groups", href:"pages/shared/group-chat.html", badge:"1" },
        ]},
        { label:"Account", icon:"person", links:[
          { id:"notifications", label:"Notifications", icon:"notifications", href:"pages/parent/parent-notifications.html", badge:"2" },
          { id:"profile",       label:"My Profile",    icon:"person",        href:"pages/parent/parent-profile.html" },
        ]},
      ],
    },
  };

  /* Department sub-pages keep "Departments" highlighted in the sidebar,
     since these modules now live inside each department. */
  const DEPT_CHILD = ["attendance","assignments","grades","exams","timetable","lessons","department"];

  /* Mobile bottom-nav: four primary destinations per role + central quick-chat action */
  const BOTTOM = {
    admin: [
      { id:"dashboard",  label:"Home",       icon:"home",      href:"pages/admin/admin.html" },
      { id:"users",      label:"Users",       icon:"group",     href:"pages/admin/admin-users.html" },
      { id:"reports",    label:"Reports",     icon:"assessment",href:"pages/admin/admin-reports.html" },
      { id:"settings",   label:"Settings",    icon:"settings",  href:"pages/admin/admin-settings.html" },
    ],
    teacher: [
      { id:"dashboard",  label:"Home",       icon:"home",          href:"pages/teacher/teacher.html" },
      { id:"classes",    label:"Classes",    icon:"school",        href:"pages/teacher/teacher-classes.html" },
      { id:"notifications",label:"Alerts",   icon:"notifications", href:"pages/teacher/teacher-notifications.html", badge:"3" },
      { id:"profile",    label:"Profile",    icon:"person",        href:"pages/teacher/teacher-profile.html" },
    ],
    student: [
      { id:"dashboard",    label:"Home",       icon:"home",      href:"pages/student/student.html" },
      { id:"departments",  label:"Department", icon:"apartment", href:"pages/shared/departments.html" },
      { id:"announcements",label:"Alerts",     icon:"campaign",  href:"pages/shared/announcements.html", badge:"3" },
      { id:"profile",      label:"Profile",    icon:"person",    href:"pages/student/student-profile.html" },
    ],
    parent: [
      { id:"dashboard",  label:"Home",       icon:"home",           href:"pages/parent/parent.html" },
      { id:"departments",label:"Departments",icon:"apartment",      href:"pages/shared/departments.html" },
      { id:"services",   label:"Services",   icon:"assignment",     href:"pages/parent/parent-services.html" },
      { id:"notifications",label:"Alerts",   icon:"notifications",  href:"pages/parent/parent-notifications.html", badge:"2" },
    ],
  };

  /* Central quick-chat action shown between the left and right dock items */
  const CHAT = {
    admin:   { label:"Group Chat", href:"pages/shared/group-chat.html", badge:"4" },
    teacher: { label:"Chat",       href:"pages/shared/chat.html", badge:"3" },
    student: { label:"Chat",       href:"pages/shared/chat.html", badge:"3" },
    parent:  { label:"Group Chat", href:"pages/shared/group-chat.html", badge:"1" },
  };

  const DEFAULT_USER = {
    admin:   { name:"Sok Panha Heng",    role:"Super Administrator",  initials:"SH" },
    teacher: { name:"Dr. Sarah Jenkins", role:"Mathematics Dept.",    initials:"SJ" },
    student: { name:"Nrinphouneta Hok",   role:"Student · Grade 11-A", initials:"NH" },
    parent:  { name:"Chan Dara Vuth",    role:"Parent / Guardian",    initials:"CV" },
  };

  const PORTAL_HOME = { admin:"pages/admin/admin.html", teacher:"pages/teacher/teacher.html", student:"pages/student/student.html", parent:"pages/parent/parent.html" };

  /* Resolve the portal from the authenticated session and scoped URL. */
  function readStoredUser(key) {
    try { return JSON.parse(localStorage.getItem(key) || "null"); } catch (e) { return null; }
  }
  function normalizeRole(role) { return role === "super_admin" ? "admin" : role; }
  function getSessionRole() {
    const authRole = window.NGISAuth && typeof window.NGISAuth.getRole === "function" ? window.NGISAuth.getRole() : null;
    const user = readStoredUser("ngis_user") || readStoredUser("ngis_chat_user");
    return normalizeRole(authRole || (user && user.role));
  }
  function resolvePortalRole(pageRole) {
    const path = window.location.pathname || "";
    const match = path.match(/\/pages\/(admin|teacher|student|parent)\//);
    const pathRole = match ? match[1] : null;
    if (pathRole) {
      try { localStorage.setItem("ngis_active_portal", pathRole); } catch (e) {}
      return pathRole;
    }
    const params = new URLSearchParams(window.location.search || "");
    const queryRole = (params.get("portal") || params.get("role") || "").toLowerCase();
    if (["admin", "teacher", "student", "parent"].includes(queryRole)) {
      try { localStorage.setItem("ngis_active_portal", queryRole); } catch (e) {}
      return queryRole;
    }
    const storedPortal = localStorage.getItem("ngis_active_portal");
    if (storedPortal && ["admin", "teacher", "student", "parent"].includes(storedPortal)) {
      return storedPortal;
    }
    return normalizeRole(pageRole) || getSessionRole() || "student";
  }

  /* Path prefix — resolves root-relative hrefs from any depth.
     Pages under pages/<role>/ are 2 levels deep → prefix = ../../
     Root-level pages (index.html, project-map.html) → prefix = ''       */
  let _P = '';

  function el(html) {
    const t = document.createElement("template");
    t.innerHTML = html.trim();
    return t.content.firstChild;
  }
  function esc(s){ return String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }

  const store = {
    get(k){ try { return localStorage.getItem(k); } catch(e){ return null; } },
    set(k,v){ try { localStorage.setItem(k,v); } catch(e){} },
  };

  function applyTheme(mode) {
    document.documentElement.setAttribute("data-theme", mode);
    const btn = document.getElementById("themeToggle");
    if (btn) {
      const ic = btn.querySelector(".material-symbols-outlined");
      if (ic) ic.textContent = mode === "dark" ? "light_mode" : "dark_mode";
    }
  }

  function buildSidebar(cfg, active) {
    const role = (window.PAGE && window.PAGE.role) || "admin";
    const homeHref = PORTAL_HOME[role] ? `${_P}${PORTAL_HOME[role]}` : `${_P}index.html`;

    // Auto-detect active link if not set or doesn't match any link in this portal
    let effectiveActive = active;
    if (!effectiveActive || !cfg.groups.some(g => g.links.some(l => l.id === effectiveActive))) {
      const curFile = (window.location.pathname || '').replace(/\\/g, '/').split('/').pop().toLowerCase();
      for (const g of cfg.groups) {
        for (const l of g.links) {
          const linkFile = (l.href || '').split('?')[0].split('/').pop().toLowerCase();
          if (linkFile && linkFile === curFile) {
            effectiveActive = l.id;
            break;
          }
        }
        if (effectiveActive && cfg.groups.some(g => g.links.some(l => l.id === effectiveActive))) break;
      }
    }

    const groups = cfg.groups.map((g, gi) => {
      const links = g.links.map(l =>
        `<a class="nav-link ${l.id === effectiveActive ? "active" : ""}" href="${_P}${l.href}"${l.id===effectiveActive?' aria-current="page"':''} data-id="${l.id}">
           <div class="nav-link-icon-bubble">
             <span class="material-symbols-outlined">${l.icon}</span>
           </div>
           <span class="nav-link-label">${esc(l.label)}</span>
           ${l.badge ? `<span class="pill">${l.badge}</span>` : ""}
         </a>`
      ).join("");
      const groupActive = g.id === effectiveActive || g.links.some(l => l.id === effectiveActive);
      const labelInner = `${g.icon ? `<span class="material-symbols-outlined nav-group-icon">${g.icon}</span>` : ""}<span>${esc(g.label)}</span>${g.collapsible ? `<span class="material-symbols-outlined ngl-chevron">expand_more</span>` : ""}`;

      let label, linksHtml;
      if (g.collapsible) {
        label = `<button type="button" class="nav-group-label" aria-expanded="false" title="${esc(g.label)}">${labelInner}</button>`;
        linksHtml = `<div class="nav-group-links"><div>${links}</div></div>`;
      } else if (g.href) {
        label = `<a class="nav-group-label nav-group-label-link${groupActive ? " active" : ""}" href="${_P}${g.href}">${labelInner}</a>`;
        linksHtml = links;
      } else {
        label = `<div class="nav-group-label">${labelInner}</div>`;
        linksHtml = links;
      }
      return `
        <div class="nav-group${g.collapsible ? " collapsible" : ""}"${g.id ? ` data-group-id="${g.id}"` : ""}>
          ${label}
          ${linksHtml}
        </div>
        ${gi < cfg.groups.length - 1 ? `<div class="nav-divider" role="separator"></div>` : ""}`;
    }).join("");

    return el(`
      <aside class="sidebar custom-scrollbar" id="sidebar" role="navigation" aria-label="Main navigation" data-purpose="primary-sidebar">
        <header class="side-brand">
          <a class="side-brand-info" href="${homeHref}" aria-label="New Gateway International School">
            <img class="side-brand-logo-img" src="${_P}assets/images/logo.png" alt="New Gateway International School" onerror="this.onerror=null;this.src='${_P}pages/student/LOGO%20NGIS%20(2).png'">
          </a>
          <button class="sidebar-collapse-btn" id="sidebarCollapseBtn" title="Toggle sidebar" aria-label="Toggle sidebar" type="button" data-purpose="sidebar-collapse-button">
            <svg class="side-collapse-svg" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
              <rect x="3" y="4" width="18" height="16" rx="2"></rect>
              <path d="M9 4v16"></path>
              <path d="M15 10l-2 2 2 2"></path>
            </svg>
          </button>
        </header>
        <nav class="side-nav custom-scrollbar" aria-label="Main Navigation">
          ${groups}
        </nav>
        <footer class="side-foot">
          <a class="nav-link side-foot-help" href="${_P}index.html">
            <div class="nav-link-icon-bubble">
              <span class="material-symbols-outlined">help_outline</span>
            </div>
            <span class="nav-link-label">Help &amp; Support</span>
          </a>
          <a class="nav-link nav-link-danger side-foot-signout" href="${_P}index.html" data-purpose="sign-out-button">
            <div class="nav-link-icon-bubble">
              <svg class="side-foot-svg" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                <path d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" stroke-linecap="round" stroke-linejoin="round"></path>
              </svg>
            </div>
            <span class="nav-link-label">Sign Out</span>
          </a>
        </footer>
      </aside>`);
  }

  function buildTopbar(user) {
    return el(`
      <header class="topbar" role="banner">
        <button class="icon-btn menu-btn" id="menuBtn" aria-label="Open menu" aria-controls="sidebar" aria-expanded="false">
          <span class="material-symbols-outlined">menu</span>
        </button>
        <div class="search" role="search">
          <span class="material-symbols-outlined">search</span>
          <input type="search" placeholder="Search students, classes, documents…" aria-label="Search"/>
          <kbd>⌘K</kbd>
        </div>
        <div class="top-right">
          <button class="lang-btn" id="langBtn" aria-label="Switch language">
            <span class="material-symbols-outlined" style="font-size:18px">language</span>
            <span>EN</span>
          </button>
          <button class="icon-btn" id="themeToggle" aria-label="Toggle dark mode">
            <span class="material-symbols-outlined">dark_mode</span>
          </button>
          <a class="icon-btn" href="${_P}${PORTAL_HOME[document.body.dataset.role]||'index.html'}" aria-label="Notifications">
            <span class="material-symbols-outlined">notifications</span>
            <span class="dot"></span>
          </a>
          <div class="top-divider"></div>
          <button class="user-chip" aria-label="Account menu">
            <span class="avatar-fallback">${esc(user.initials)}</span>
            <span><span class="nm">${esc(user.name)}</span><br><span class="rl">${esc(user.role)}</span></span>
            <span class="material-symbols-outlined" style="font-size:18px;color:var(--faint)">expand_more</span>
          </button>
        </div>
      </header>`);
  }

  function getStudentActiveTab(active) {
    const path = (window.location.pathname || '').toLowerCase();
    const file = (path.split('/').pop() || '').toLowerCase();
    if (file === 'student.html' || (active === 'dashboard' && file.indexOf('student-') === -1)) return 'home';
    if (file.indexOf('chat') !== -1 || active === 'chat' || active === 'teacher-chat' || active === 'group-chat') return 'chat';
    if (file.indexOf('notification') !== -1 || file.indexOf('announcement') !== -1 || active === 'notifications' || active === 'announcements' || active === 'alerts') return 'alerts';
    if (file.indexOf('profile') !== -1 || file.indexOf('student-id') !== -1 || active === 'profile' || active === 'student-id') return 'profile';
    return 'department';
  }

  function buildStudentBottomNav(active) {
    const curTab = getStudentActiveTab(active);
    return el(`
      <nav class="mob-bottomnav" id="mobBottomNav" role="navigation" aria-label="Mobile Navigation" data-purpose="bottom-navigation-bar">
        <div class="mob-bn-glow" aria-hidden="true"></div>
        <div class="mob-bn-shell">
          <div class="mob-bn-track">
            <div class="mob-bn-slider" id="mobBnSlider" aria-hidden="true"></div>
            <div class="mob-bn-inner">
              <a href="${_P}pages/student/student.html" class="mob-bn-item ${curTab === 'home' ? 'is-active' : ''}" data-tab="home" aria-label="Home"${curTab === 'home' ? ' aria-current="page"' : ''}>
                <span class="mob-bn-icon-row">
                  <i class="ph-fill ph-house-simple"></i>
                </span>
              </a>
              <a href="${_P}pages/shared/departments.html" class="mob-bn-item ${curTab === 'department' ? 'is-active' : ''}" data-tab="department" aria-label="Department"${curTab === 'department' ? ' aria-current="page"' : ''}>
                <span class="mob-bn-icon-row">
                  <i class="ph-bold ph-buildings"></i>
                </span>
              </a>
              <a href="${_P}pages/student/student-chat.html" class="mob-bn-item mob-bn-chat ${curTab === 'chat' ? 'is-active' : ''}" data-tab="chat" aria-label="Chat"${curTab === 'chat' ? ' aria-current="page"' : ''}>
                <span class="mob-bn-icon-row">
                  <span class="mob-bn-chat-core">
                    <i class="ph-fill ph-chat-circle-dots"></i>
                  </span>
                </span>
              </a>
              <a href="${_P}pages/student/student-notifications.html" class="mob-bn-item ${curTab === 'alerts' ? 'is-active' : ''}" data-tab="alerts" aria-label="Alerts"${curTab === 'alerts' ? ' aria-current="page"' : ''}>
                <span class="mob-bn-icon-row">
                  <span class="mob-bn-icon-wrap">
                    <i class="ph-bold ph-bell"></i>
                    <span class="mob-bn-dot"></span>
                  </span>
                </span>
              </a>
              <a href="${_P}pages/student/student-profile.html" class="mob-bn-item ${curTab === 'profile' ? 'is-active' : ''}" data-tab="profile" aria-label="Profile"${curTab === 'profile' ? ' aria-current="page"' : ''}>
                <span class="mob-bn-icon-row">
                  <i class="ph-bold ph-user"></i>
                </span>
              </a>
            </div>
          </div>
        </div>
      </nav>
    `);
  }

  function buildBottomNav(role, active) {
    if (role === 'student') {
      return buildStudentBottomNav(active);
    }
    const list = BOTTOM[role] || BOTTOM.admin;
    const chat = CHAT[role] || CHAT.admin;
    const chatActive = active === "group-chat" || active === "chat";
    const itemHtml = it => {
      const isActive = it.id === active;
      return `
        <a class="bn-item ${isActive ? "active" : ""}" href="${_P}${it.href}" data-tab="${it.id}" aria-label="${esc(it.label)}"${isActive ? ' aria-current="page"' : ''}>
          <div class="bn-icon-bubble">
            <span class="material-symbols-outlined bn-icon">${it.icon}</span>
            ${it.badge ? `<span class="bn-badge">${it.badge}</span>` : ""}
          </div>
          <span class="bn-label">${esc(it.label)}</span>
          <span class="bn-droplet" aria-hidden="true"></span>
        </a>`;
    };
    const leftItems  = list.slice(0, 2).map(itemHtml).join("");
    const rightItems = list.slice(2).map(itemHtml).join("");
    const chatHtml = `
      <div class="bn-chat-wrap">
        <a class="bn-chat-btn" href="${_P}${chat.href}" data-tab="chat" aria-label="${esc(chat.label)}"${chatActive ? ' aria-current="page"' : ''}>
          <span class="material-symbols-outlined bn-icon">chat</span>
          ${chat.badge ? `<span class="bn-badge">${chat.badge}</span>` : ""}
        </a>
      </div>`;

    return el(`
      <nav class="bottomnav" id="bottomnav" role="navigation" aria-label="Mobile Navigation">
        <div class="bottomnav-glow" aria-hidden="true"></div>
        <div class="bottomnav-shell">
          <div class="bottomnav-track">
            <div class="bottomnav-melt-slider" id="bnMeltSlider" aria-hidden="true">
              <span class="melt-slider-core"></span>
            </div>
            <div class="bottomnav-inner">
              ${leftItems}
              ${chatHtml}
              ${rightItems}
            </div>
          </div>
        </div>
      </nav>
    `);
  }

  function initBottomNav(navEl) {
    if (!navEl) return;

    // Student Floating Pill Dock
    if (navEl.classList.contains("mob-bottomnav") || navEl.id === "mobBottomNav") {
      const slider = navEl.querySelector("#mobBnSlider");
      const inner = navEl.querySelector(".mob-bn-inner");
      const items = Array.from(navEl.querySelectorAll(".mob-bn-item"));
      if (!slider || !inner || !items.length) return;

      function updateMobSlider(animate = true) {
        const activeItem = navEl.querySelector(".mob-bn-item.is-active");
        if (!activeItem || window.innerWidth > 768) {
          slider.style.opacity = "0";
          return;
        }
        const innerRect = inner.getBoundingClientRect();
        const itemRect = activeItem.getBoundingClientRect();
        if (itemRect.width === 0) return;
        const left = itemRect.left - innerRect.left;
        const width = itemRect.width;

        if (!animate) {
          slider.style.transition = "none";
        } else {
          slider.style.transition = "transform 0.45s cubic-bezier(0.34, 1.45, 0.64, 1), width 0.38s cubic-bezier(0.34, 1.45, 0.64, 1), opacity 0.25s ease";
        }
        slider.style.width = Math.round(width) + "px";
        slider.style.transform = "translateX(" + Math.round(left) + "px)";
        slider.style.opacity = "1";
        if (!animate) {
          void slider.offsetWidth;
          slider.style.transition = "";
        }
      }

      window.__updateBottomNavSlider = updateMobSlider;

      function schedule() {
        requestAnimationFrame(() => updateMobSlider(false));
      }

      schedule();
      setTimeout(() => updateMobSlider(false), 30);
      setTimeout(() => updateMobSlider(true), 160);
      setTimeout(() => updateMobSlider(true), 400);

      window.addEventListener("load", schedule, { passive: true });
      window.addEventListener("resize", schedule, { passive: true });
      window.addEventListener("orientationchange", () => setTimeout(schedule, 80), { passive: true });

      items.forEach(item => {
        item.addEventListener("click", function () {
          items.forEach(it => {
            it.classList.remove("is-active");
            it.removeAttribute("aria-current");
          });
          item.classList.add("is-active");
          item.setAttribute("aria-current", "page");
          updateMobSlider(true);
        });
      });
      return;
    }

    // Default Melt/Liquid Dock (Admin, Teacher, Parent)
    const slider = navEl.querySelector("#bnMeltSlider");
    const inner = navEl.querySelector(".bottomnav-inner");
    const items = Array.from(navEl.querySelectorAll(".bn-item"));
    if (!slider || !inner || !items.length) return;

    function updateSlider(animate = true) {
      const activeItem = navEl.querySelector(".bn-item.active");
      if (!activeItem || window.innerWidth > 768) {
        slider.style.opacity = "0";
        return;
      }

      const innerRect = inner.getBoundingClientRect();
      const itemRect = activeItem.getBoundingClientRect();
      const left = itemRect.left - innerRect.left;
      const width = itemRect.width;

      if (!animate) {
        slider.style.transition = "none";
      } else {
        slider.style.transition = "transform 0.45s cubic-bezier(0.34, 1.45, 0.64, 1), width 0.38s cubic-bezier(0.34, 1.45, 0.64, 1), opacity 0.25s ease";
      }
      slider.style.width = Math.round(width) + "px";
      slider.style.transform = "translateX(" + Math.round(left) + "px)";
      slider.style.opacity = "1";
    }

    window.__updateBottomNavSlider = updateSlider;

    setTimeout(() => updateSlider(false), 30);
    setTimeout(() => updateSlider(true), 160);
    setTimeout(() => updateSlider(true), 400);

    window.addEventListener("resize", () => updateSlider(false), { passive: true });
    window.addEventListener("orientationchange", () => setTimeout(() => updateSlider(false), 80), { passive: true });

    items.forEach(item => {
      item.addEventListener("click", function() {
        items.forEach(it => {
          it.classList.remove("active");
          it.removeAttribute("aria-current");
        });
        item.classList.add("active");
        item.setAttribute("aria-current", "page");
        updateSlider(true);

        const bubble = item.querySelector(".bn-icon-bubble");
        if (bubble) {
          bubble.classList.remove("bn-pop");
          void bubble.offsetWidth;
          bubble.classList.add("bn-pop");
        }
      });
    });
  }

  function buildBreadcrumb(cfg, role, active) {
    return null; // Breadcrumb removed per user request
  }

  function mount() {
    const PAGE = window.PAGE || { role:"student", active:"dashboard" };
    _P = (window.location.pathname || '').indexOf('/pages/') !== -1 ? '../../' : '';
    const portalRole = resolvePortalRole(PAGE.role);
    PAGE.role = portalRole;
    window.PAGE = PAGE;
    const cfg  = NAV[portalRole] || NAV.student;
    const user = PAGE.user || DEFAULT_USER[portalRole] || DEFAULT_USER.student;

    // Department-centric portals: keep "Departments" lit on its sub-pages.
    let active = PAGE.active;
    const ALIAS_MAP = {
      'class-chat': 'class-chats',
      'archived-conversations': 'archived',
      'pinned-messages': 'pinned',
      'audit-logs': 'messaging-audit',
      'audit': 'messaging-audit'
    };
    if (ALIAS_MAP[active]) active = ALIAS_MAP[active];
    if ((PAGE.role === "student" || PAGE.role === "parent") && DEPT_CHILD.includes(active)) {
      active = "departments";
    }

    document.body.setAttribute("data-role", portalRole);
    document.body.setAttribute("data-portal", portalRole);

    const main = document.querySelector(".main");
    if (!main) return;   // standalone pages (landing) have no app shell

    const shell = el(`<div class="shell"></div>`);
    main.parentNode.insertBefore(shell, main);

    const sidebar = buildSidebar(cfg, active);
    const scrim   = el(`<div class="scrim" id="scrim"></div>`);
    /* Sidebar is position:fixed — mount it on <body> so the mobile drawer stays
       reachable on pages that hide their desktop view (e.g. student dashboard). */
    document.body.appendChild(sidebar);
    shell.appendChild(main);
    document.body.appendChild(scrim);

    /* ── Sidebar accordion (collapsible groups — admin only) ── */
    const OPEN_GROUP_KEY = `ngis-${PAGE.role}-open-group`;
    const collapsibleGroups = Array.from(sidebar.querySelectorAll('.nav-group.collapsible'));
    if (collapsibleGroups.length) {
      const activeGroupEl = collapsibleGroups.find(g => g.querySelector('.nav-link.active'));
      const initialId = activeGroupEl ? activeGroupEl.dataset.groupId : store.get(OPEN_GROUP_KEY);

      const setGroupExpanded = (groupEl, expanded) => {
        groupEl.classList.toggle('expanded', expanded);
        const btn = groupEl.querySelector('.nav-group-label');
        if (btn && btn.tagName === 'BUTTON') btn.setAttribute('aria-expanded', String(expanded));
      };

      collapsibleGroups.forEach(g => setGroupExpanded(g, g.dataset.groupId === initialId));

      collapsibleGroups.forEach(g => {
        const btn = g.querySelector('.nav-group-label');
        if (!btn || btn.tagName !== 'BUTTON') return;
        btn.addEventListener('click', () => {
          const willOpen = !g.classList.contains('expanded');
          collapsibleGroups.forEach(other => setGroupExpanded(other, other === g && willOpen));
          store.set(OPEN_GROUP_KEY, willOpen ? g.dataset.groupId : '');
          if (willOpen) {
            setTimeout(() => {
              const activeElInGroup = g.querySelector('.nav-link.active');
              if (activeElInGroup) {
                scrollActiveItemIntoView(true);
              } else if (sideNav) {
                const groupRect = g.getBoundingClientRect();
                const navRect = sideNav.getBoundingClientRect();
                if (groupRect.bottom > navRect.bottom - 20) {
                  const needed = (groupRect.bottom - navRect.bottom) + 30;
                  const maxScroll = Math.max(0, sideNav.scrollHeight - sideNav.clientHeight);
                  const target = Math.min(maxScroll, sideNav.scrollTop + needed);
                  sideNav.scrollTo({ top: target, behavior: 'smooth' });
                }
              }
            }, 220);
          }
        });
      });
    }

    /* ── Sidebar Scroll Position Preservation & Targeted Auto-Scroll ── */
    const sideNav = sidebar.querySelector('.side-nav') || sidebar;
    const SCROLL_KEY = `ngis-${portalRole}-sidebar-scroll`;
    const GLOBAL_SCROLL_KEY = 'ngis-sidebar-scroll';
    const NAV_FLAG_KEY = 'ngis-sidebar-clicked-nav';

    const scrollActiveItemIntoView = (forceEnsure = false) => {
      if (!sideNav) return;
      const activeEl = sidebar.querySelector('.nav-link.active') || sidebar.querySelector('.nav-group-label-link.active');
      if (!activeEl) return;

      const sideNavRect = sideNav.getBoundingClientRect();
      const activeRect = activeEl.getBoundingClientRect();
      if (sideNavRect.height === 0 || activeRect.height === 0) return;

      const activeTop = (activeRect.top - sideNavRect.top) + sideNav.scrollTop;
      const activeBottom = activeTop + activeRect.height;
      const clientH = sideNav.clientHeight;
      const scrollH = sideNav.scrollHeight;
      const maxScroll = Math.max(0, scrollH - clientH);
      if (maxScroll <= 0) return;

      const pad = 28;
      const isTopCut = activeTop < sideNav.scrollTop + pad;
      const isBottomCut = activeBottom > sideNav.scrollTop + clientH - pad;

      if (forceEnsure || isTopCut || isBottomCut) {
        const group = activeEl.closest('.nav-group');
        const groupLabel = group ? group.querySelector('.nav-group-label') : null;
        let groupTop = activeTop;
        if (groupLabel) {
          const glRect = groupLabel.getBoundingClientRect();
          groupTop = (glRect.top - sideNavRect.top) + sideNav.scrollTop;
        }

        const spanFromGroup = activeBottom - groupTop;
        let target;
        if (spanFromGroup + pad * 2 <= clientH) {
          // Both group header and active item fit comfortably in view
          target = groupTop - 12;
        } else {
          // Center the active element in the sidebar viewport
          target = activeTop - (clientH / 2) + (activeRect.height / 2);
        }

        target = Math.min(Math.max(0, Math.round(target)), maxScroll);
        sideNav.scrollTop = target;
        try {
          sessionStorage.setItem(SCROLL_KEY, String(target));
          sessionStorage.setItem(GLOBAL_SCROLL_KEY, String(target));
        } catch (e) {}
      }
    };

    const restoreSidebarScroll = () => {
      if (!sideNav) return;
      let wasNavigating = false;
      try {
        wasNavigating = sessionStorage.getItem(NAV_FLAG_KEY) === '1';
        if (wasNavigating) sessionStorage.removeItem(NAV_FLAG_KEY);
      } catch (e) {}

      const saved = sessionStorage.getItem(SCROLL_KEY) || sessionStorage.getItem(GLOBAL_SCROLL_KEY);
      if (saved !== null && !isNaN(Number(saved))) {
        const parsed = Number(saved);
        const maxScroll = Math.max(0, sideNav.scrollHeight - sideNav.clientHeight);
        sideNav.scrollTop = Math.min(Math.max(0, parsed), maxScroll);
      }

      scrollActiveItemIntoView(wasNavigating);
    };

    // Restore immediately and queue on subsequent animation frames / timer ticks
    restoreSidebarScroll();
    requestAnimationFrame(() => restoreSidebarScroll());
    setTimeout(restoreSidebarScroll, 50);
    setTimeout(restoreSidebarScroll, 160);
    setTimeout(restoreSidebarScroll, 260);

    window.addEventListener("load", () => setTimeout(restoreSidebarScroll, 80), { passive: true });
    window.addEventListener("pageshow", () => setTimeout(restoreSidebarScroll, 50), { passive: true });

    // Track scroll events on sideNav
    let sideNavScrollRaf = null;
    sideNav.addEventListener("scroll", () => {
      if (sideNavScrollRaf) cancelAnimationFrame(sideNavScrollRaf);
      sideNavScrollRaf = requestAnimationFrame(() => {
        try {
          sessionStorage.setItem(SCROLL_KEY, String(sideNav.scrollTop));
          sessionStorage.setItem(GLOBAL_SCROLL_KEY, String(sideNav.scrollTop));
        } catch (e) {}
      });
    }, { passive: true });

    // Click handler on sidebar links to capture scroll position and mark navigation
    sidebar.addEventListener("click", (e) => {
      const link = e.target.closest("a");
      if (!link) return;
      try {
        sessionStorage.setItem(SCROLL_KEY, String(sideNav.scrollTop));
        sessionStorage.setItem(GLOBAL_SCROLL_KEY, String(sideNav.scrollTop));
        sessionStorage.setItem(NAV_FLAG_KEY, "1");
      } catch (e) {}
    }, { capture: true });

    window.addEventListener("beforeunload", () => {
      try {
        sessionStorage.setItem(SCROLL_KEY, String(sideNav.scrollTop));
        sessionStorage.setItem(GLOBAL_SCROLL_KEY, String(sideNav.scrollTop));
      } catch (e) {}
    });

    /* ── Sidebar collapse / expand (desktop) ── */
    let collapseBtn = sidebar.querySelector('#sidebarCollapseBtn');
    if (!collapseBtn) {
      collapseBtn = el(`
        <button class="sidebar-collapse-btn" id="sidebarCollapseBtn" title="Collapse sidebar" aria-label="Collapse sidebar" type="button" data-purpose="sidebar-collapse-button">
          <svg class="side-collapse-svg" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
            <rect x="3" y="4" width="18" height="16" rx="2"></rect>
            <path d="M9 4v16"></path>
            <path d="M15 10l-2 2 2 2"></path>
          </svg>
        </button>`);
      sidebar.querySelector('.side-brand').appendChild(collapseBtn);
    }

    const expandBtn = el(`
      <button class="sidebar-expand-btn" id="sidebarExpandBtn" title="Expand sidebar" aria-label="Expand sidebar">
        <span class="material-symbols-outlined">left_panel_open</span>
      </button>`);
    document.body.appendChild(expandBtn);

    const COLLAPSED_KEY = 'ngis-sidebar-collapsed';
    function setSidebarCollapsed(collapsed) {
      if (collapsed) {
        sidebar.classList.add('collapsed');
        main.classList.add('sidebar-collapsed');
        expandBtn.classList.add('visible');
        store.set(COLLAPSED_KEY, '1');
      } else {
        sidebar.classList.remove('collapsed');
        main.classList.remove('sidebar-collapsed');
        expandBtn.classList.remove('visible');
        store.set(COLLAPSED_KEY, '0');
        setTimeout(() => scrollActiveItemIntoView(false), 160);
      }
      const isExpanded = !collapsed;
      document.querySelectorAll("#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, .hamburger-btn, [data-action='toggle-sidebar']").forEach(btn => {
        btn.setAttribute("aria-expanded", String(isExpanded));
      });
    }
    // Restore persisted state
    if (store.get(COLLAPSED_KEY) === '1') setSidebarCollapsed(true);

    collapseBtn.addEventListener('click', () => setSidebarCollapsed(true));
    expandBtn.addEventListener('click',   () => setSidebarCollapsed(false));

    let bNav = document.getElementById("mobBottomNav");
    if (!bNav) {
      bNav = buildBottomNav(PAGE.role, active);
      document.body.appendChild(bNav);
    }
    if (PAGE.role === 'student') {
      const legacyNav = document.getElementById("bottomnav");
      if (legacyNav) legacyNav.remove();
    }
    initBottomNav(bNav);

    // Ensure Phosphor icons are available for student mobile navigation
    if (PAGE.role === 'student' && !document.querySelector('script[src*="@phosphor-icons/web"]')) {
      const ph = document.createElement("script");
      ph.src = "https://unpkg.com/@phosphor-icons/web";
      ph.async = true;
      document.head.appendChild(ph);
    }

    // Auto-breadcrumb removed per user request
    // const page = document.querySelector(".page");
    // const crumb = buildBreadcrumb(cfg, PAGE.role, active);
    // if (page && crumb) page.insertBefore(crumb, page.firstChild);

    if (!document.querySelector(".toast-wrap")) {
      document.body.appendChild(el(`<div class="toast-wrap" id="toasts" role="region" aria-live="polite"></div>`));
    }

    /* Theme */
    applyTheme(store.get("ngis-theme") || "light");
    const themeToggle = document.getElementById("themeToggle");
    if (themeToggle) themeToggle.addEventListener("click", () => {
      const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      store.set("ngis-theme", next);
      applyTheme(next);
    });

    /* Language toggle */
    const langBtn = document.getElementById("langBtn");
    if (langBtn) {
      let lang = "EN";
      langBtn.addEventListener("click", () => {
        lang = lang === "EN" ? "KH" : "EN";
        langBtn.querySelector("span:last-child").textContent = lang;
        window.toast(lang === "KH" ? "ភាសាខ្មែរ​ត្រូវបានជ្រើស" : "English selected", "info");
      });
    }

    /* Mobile drawer with smooth bottomnav disappearance */
    const openNav = () => {
      sidebar.classList.add("open");
      scrim.classList.add("show");
      document.body.classList.add("sidebar-open");
      const bNavEl = document.getElementById("mobBottomNav") || document.getElementById("bottomnav");
      if (bNavEl) bNavEl.classList.add("hidden-by-sidebar");
      document.querySelectorAll("#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, .hamburger-btn, [data-action='toggle-sidebar']").forEach(btn => btn.setAttribute("aria-expanded", "true"));
      setTimeout(() => scrollActiveItemIntoView(true), 160);
    };

    const closeNav = () => {
      sidebar.classList.remove("open");
      scrim.classList.remove("show");
      document.body.classList.remove("sidebar-open");
      const bNavEl = document.getElementById("mobBottomNav") || document.getElementById("bottomnav");
      if (bNavEl) {
        bNavEl.classList.remove("hidden-by-sidebar");
        setTimeout(() => {
          if (typeof window.__updateBottomNavSlider === "function") {
            window.__updateBottomNavSlider(true);
          }
        }, 120);
      }
      document.querySelectorAll("#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, .hamburger-btn, [data-action='toggle-sidebar']").forEach(btn => btn.setAttribute("aria-expanded", "false"));
    };

    const toggleNav = () => {
      if (window.innerWidth > 1024) {
        const isCollapsed = sidebar.classList.contains("collapsed");
        setSidebarCollapsed(!isCollapsed);
      } else {
        if (sidebar.classList.contains("open")) closeNav();
        else openNav();
      }
    };

    window.openSidebar = openNav;
    window.closeSidebar = closeNav;
    window.toggleSidebar = toggleNav;

    const wireButtons = () => {
      document.querySelectorAll("#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, .hamburger-btn, [data-action='toggle-sidebar']").forEach(btn => {
        if (btn.dataset.sidebarBound) return;
        btn.dataset.sidebarBound = "true";
        btn.addEventListener("click", (e) => {
          if (e.__sidebarHandled) return;
          e.__sidebarHandled = true;
          e.preventDefault();
          e.stopPropagation();
          e.stopImmediatePropagation();
          toggleNav();
        });
      });
    };
    wireButtons();
    setTimeout(wireButtons, 150);

    // Attach to menuBtn and hamburger buttons reliably (delegated fallback)
    document.addEventListener("click", (e) => {
      const btn = e.target.closest("#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, .hamburger-btn, [data-action='toggle-sidebar']");
      if (!btn) return;
      if (e.__sidebarHandled) return;
      e.__sidebarHandled = true;
      e.preventDefault();
      e.stopPropagation();
      e.stopImmediatePropagation();
      toggleNav();
    });

    scrim.addEventListener("click", closeNav);
    sidebar.querySelectorAll(".nav-link").forEach(a => a.addEventListener("click", closeNav));
    document.addEventListener("keydown", e => { if (e.key === "Escape") closeNav(); });

    // Edge swipe gestures
    let tx = 0;
    document.addEventListener("touchstart", e => { tx = e.touches[0].clientX; }, { passive: true });
    document.addEventListener("touchend", e => {
      const dx = e.changedTouches[0].clientX - tx;
      if (tx < 28 && dx > 60) openNav();
      else if (dx < -60 && sidebar.classList.contains("open")) closeNav();
    }, { passive: true });

    /* ⌘K / Ctrl+K focuses search */
    document.addEventListener("keydown", (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        const i = document.querySelector(".search input");
        if (i) i.focus();
      }
    });

    // MutationObserver fallback: if any external code directly alters sidebar classes
    const sidebarObserver = new MutationObserver(() => {
      const isOpen = sidebar.classList.contains("open");
      document.body.classList.toggle("sidebar-open", isOpen);
      const bNavEl = document.getElementById("mobBottomNav") || document.getElementById("bottomnav");
      if (bNavEl) bNavEl.classList.toggle("hidden-by-sidebar", isOpen);
    });
    sidebarObserver.observe(sidebar, { attributes: true, attributeFilter: ["class"] });

    const pageEl = document.querySelector(".page");
    if (pageEl) pageEl.classList.add("anim-fade");

    /* Interactive layer */
    const s = document.createElement("script");
    s.src = _P + "assets/js/app.js";
    document.body.appendChild(s);
  }

  window.toast = function(msg, kind) {
    kind = kind || "info";
    const wrap = document.getElementById("toasts");
    if (!wrap) return;
    const icons = { success:"check_circle", error:"error", warning:"warning", info:"info" };
    const color = { success:"success", error:"danger", warning:"warning", info:"primary" }[kind] || "primary";
    const t = el(`
      <div class="toast" role="alert" style="border-left-color:var(--${color})">
        <span class="material-symbols-outlined" style="color:var(--${color})">${icons[kind]||icons.info}</span>
        ${esc(msg)}
      </div>`);
    wrap.appendChild(t);
    setTimeout(() => { t.style.opacity="0"; t.style.transition="opacity var(--t-base)"; setTimeout(()=>t.remove(),220); }, 2800);
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount);
  else mount();
})();
