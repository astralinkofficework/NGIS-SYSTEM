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
        { id:"comms", label:"Communication", icon:"forum", collapsible:true, links:[
          { id:"announcements",  label:"Announcements", icon:"campaign",  href:"pages/shared/announcements.html" },
          { id:"news",           label:"News CMS",       icon:"newspaper", href:"pages/admin/admin-news.html" },
          { id:"notifications",  label:"Notifications", icon:"notifications", href:"pages/admin/admin-logs.html" },
          { id:"group-chat",     label:"Group Chat",    icon:"groups",   href:"pages/shared/group-chat.html", badge:"4" },
          { id:"chat",           label:"Direct Chat",   icon:"chat",     href:"pages/shared/chat.html", badge:"2" },
        ]},
        { id:"administration", label:"Administration", icon:"admin_panel_settings", collapsible:true, links:[
          { id:"logs",        label:"Audit Logs",         icon:"history",     href:"pages/admin/admin-logs.html" },
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
        { label:"Communication", icon:"forum", links:[
          { id:"announcements", label:"Announcements", icon:"campaign", href:"pages/shared/announcements.html", badge:"0" },
          { id:"group-chat",    label:"Group Chat",    icon:"groups",   href:"pages/shared/group-chat.html", badge:"3" },
          { id:"chat",          label:"Direct Chat",   icon:"chat",     href:"pages/shared/chat.html", badge:"2" },
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
          { id:"lost-found",  label:"Lost & Found", icon:"inventory_2", href:"pages/student/student-lost-found.html" },
        ]},
        { label:"Communication", icon:"forum", links:[
          { id:"announcements", label:"Announcements", icon:"campaign", href:"pages/shared/announcements.html", badge:"3" },
          { id:"group-chat",    label:"Group Chat",    icon:"groups",   href:"pages/shared/group-chat.html", badge:"2" },
          { id:"chat",          label:"Direct Chat",   icon:"chat",     href:"pages/shared/chat.html", badge:"3" },
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
        { label:"Communication", icon:"forum", links:[
          { id:"announcements", label:"Announcements", icon:"campaign", href:"pages/shared/announcements.html", badge:"1" },
          { id:"group-chat",    label:"Group Chat",    icon:"groups",   href:"pages/shared/group-chat.html", badge:"1" },
          { id:"chat",          label:"Direct Chat",   icon:"chat",     href:"pages/shared/chat.html", badge:"1" },
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

  /* Mobile bottom-nav: five primary destinations per role */
  const BOTTOM = {
    admin: [
      { id:"dashboard",  label:"Home",       icon:"home",      href:"pages/admin/admin.html" },
      { id:"users",      label:"Users",       icon:"group",     href:"pages/admin/admin-users.html" },
      { id:"group-chat", label:"Group Chat",  icon:"groups",    href:"pages/shared/group-chat.html", badge:"4" },
      { id:"reports",    label:"Reports",     icon:"assessment",href:"pages/admin/admin-reports.html" },
      { id:"settings",   label:"Settings",    icon:"settings",  href:"pages/admin/admin-settings.html" },
    ],
    teacher: [
      { id:"dashboard",  label:"Home",       icon:"home",          href:"pages/teacher/teacher.html" },
      { id:"classes",    label:"Classes",    icon:"school",        href:"pages/teacher/teacher-classes.html" },
      { id:"group-chat", label:"Group Chat", icon:"groups",        href:"pages/shared/group-chat.html", badge:"3" },
      { id:"notifications",label:"Alerts",   icon:"notifications", href:"pages/teacher/teacher-notifications.html", badge:"3" },
      { id:"profile",    label:"Profile",    icon:"person",        href:"pages/teacher/teacher-profile.html" },
    ],
    student: [
      { id:"dashboard",    label:"Home",        icon:"home",        href:"pages/student/student.html" },
      { id:"departments",  label:"Departments", icon:"apartment",   href:"pages/shared/departments.html" },
      { id:"services",     label:"Services",    icon:"assignment",  href:"pages/student/student-services.html" },
      { id:"announcements",label:"Alerts",      icon:"campaign",    href:"pages/shared/announcements.html", badge:"3" },
      { id:"profile",      label:"Profile",     icon:"person",      href:"pages/student/student-profile.html" },
    ],
    parent: [
      { id:"dashboard",    label:"Home",       icon:"home",           href:"pages/parent/parent.html" },
      { id:"departments",  label:"Departments",icon:"apartment",      href:"pages/shared/departments.html" },
      { id:"services",     label:"Services",   icon:"assignment",     href:"pages/parent/parent-services.html" },
      { id:"group-chat",   label:"Group Chat", icon:"groups",         href:"pages/shared/group-chat.html", badge:"1" },
      { id:"notifications",label:"Alerts",     icon:"notifications",  href:"pages/parent/parent-notifications.html", badge:"2" },
    ],
  };

  const DEFAULT_USER = {
    admin:   { name:"Sok Panha Heng",    role:"Super Administrator",  initials:"SH" },
    teacher: { name:"Dr. Sarah Jenkins", role:"Mathematics Dept.",    initials:"SJ" },
    student: { name:"Kosal Rith Mony",   role:"Student · Grade 11-A", initials:"KM" },
    parent:  { name:"Chan Dara Vuth",    role:"Parent / Guardian",    initials:"CV" },
  };

  const PORTAL_HOME = { admin:"pages/admin/admin.html", teacher:"pages/teacher/teacher.html", student:"pages/student/student.html", parent:"pages/parent/parent.html" };

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
    const groups = cfg.groups.map((g, gi) => {
      const links = g.links.map(l =>
        `<a class="nav-link ${l.id === active ? "active" : ""}" href="${_P}${l.href}"${l.id===active?' aria-current="page"':''}>
           <div class="nav-link-icon-bubble">
             <span class="material-symbols-outlined">${l.icon}</span>
           </div>
           <span class="nav-link-label">${esc(l.label)}</span>
           ${l.badge ? `<span class="pill">${l.badge}</span>` : ""}
         </a>`
      ).join("");
      const groupActive = g.id === active || g.links.some(l => l.id === active);
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
            <svg class="side-collapse-svg" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <rect height="16" rx="2" stroke-linecap="round" stroke-linejoin="round" width="18" x="3" y="4"></rect>
              <path d="M9 4v16" stroke-linecap="round" stroke-linejoin="round"></path>
              <path d="M15 10l-2 2 2 2" stroke-linecap="round" stroke-linejoin="round"></path>
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

  function buildBottomNav(role, active) {
    const list = BOTTOM[role] || BOTTOM.admin;
    const items = list.map(it => {
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
    }).join("");

    return el(`
      <nav class="bottomnav" id="bottomnav" role="navigation" aria-label="Mobile Navigation">
        <div class="bottomnav-glow" aria-hidden="true"></div>
        <div class="bottomnav-shell">
          <div class="bottomnav-track">
            <div class="bottomnav-melt-slider" id="bnMeltSlider" aria-hidden="true">
              <span class="melt-slider-core"></span>
            </div>
            <div class="bottomnav-inner">
              ${items}
            </div>
          </div>
        </div>
      </nav>
    `);
  }

  function initBottomNav(navEl) {
    if (!navEl) return;
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
    const PAGE = window.PAGE || { role:"admin", active:"dashboard" };
    const cfg  = NAV[PAGE.role] || NAV.admin;
    const user = PAGE.user || DEFAULT_USER[PAGE.role] || DEFAULT_USER.admin;
    _P = (window.location.pathname || '').indexOf('/pages/') !== -1 ? '../../' : '';

    // Department-centric portals: keep "Departments" lit on its sub-pages.
    let active = PAGE.active;
    if ((PAGE.role === "student" || PAGE.role === "parent") && DEPT_CHILD.includes(active)) {
      active = "departments";
    }

    document.body.setAttribute("data-role", PAGE.role);

    const main = document.querySelector(".main");
    if (!main) return;   // standalone pages (landing) have no app shell

    const shell = el(`<div class="shell"></div>`);
    main.parentNode.insertBefore(shell, main);

    const sidebar = buildSidebar(cfg, active);
    const scrim   = el(`<div class="scrim" id="scrim"></div>`);
    shell.appendChild(sidebar);
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
        });
      });
    }

    /* ── Sidebar collapse / expand (desktop) ── */
    let collapseBtn = sidebar.querySelector('#sidebarCollapseBtn');
    if (!collapseBtn) {
      collapseBtn = el(`
        <button class="sidebar-collapse-btn" id="sidebarCollapseBtn" title="Collapse sidebar" aria-label="Collapse sidebar">
          <span class="material-symbols-outlined">left_panel_close</span>
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
      }
    }
    // Restore persisted state
    if (store.get(COLLAPSED_KEY) === '1') setSidebarCollapsed(true);

    collapseBtn.addEventListener('click', () => setSidebarCollapsed(true));
    expandBtn.addEventListener('click',   () => setSidebarCollapsed(false));

    const bNav = buildBottomNav(PAGE.role, active);
    document.body.appendChild(bNav);
    initBottomNav(bNav);

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
      const bNavEl = document.getElementById("bottomnav");
      if (bNavEl) bNavEl.classList.add("hidden-by-sidebar");
      document.querySelectorAll("#menuBtn, #htbHamburger, .htb-hamburger, [data-action='toggle-sidebar']").forEach(btn => btn.setAttribute("aria-expanded", "true"));
    };

    const closeNav = () => {
      sidebar.classList.remove("open");
      scrim.classList.remove("show");
      document.body.classList.remove("sidebar-open");
      const bNavEl = document.getElementById("bottomnav");
      if (bNavEl) {
        bNavEl.classList.remove("hidden-by-sidebar");
        setTimeout(() => {
          if (typeof window.__updateBottomNavSlider === "function") {
            window.__updateBottomNavSlider(true);
          }
        }, 120);
      }
      document.querySelectorAll("#menuBtn, #htbHamburger, .htb-hamburger, [data-action='toggle-sidebar']").forEach(btn => btn.setAttribute("aria-expanded", "false"));
    };

    const toggleNav = () => {
      if (sidebar.classList.contains("open")) closeNav();
      else openNav();
    };

    window.openSidebar = openNav;
    window.closeSidebar = closeNav;
    window.toggleSidebar = toggleNav;

    const wireButtons = () => {
      document.querySelectorAll("#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, [data-action='toggle-sidebar']").forEach(btn => {
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
      const btn = e.target.closest("#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, [data-action='toggle-sidebar']");
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
      const bNavEl = document.getElementById("bottomnav");
      if (bNavEl) bNavEl.classList.toggle("hidden-by-sidebar", isOpen);
    });
    sidebarObserver.observe(sidebar, { attributes: true, attributeFilter: ["class"] });

    if (page) page.classList.add("anim-fade");

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
