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
        { label:"Management", icon:"school", links:[
          { id:"users",       label:"Users",       icon:"group",              href:"pages/admin/admin-users.html" },
          { id:"departments", label:"Departments", icon:"apartment",          href:"pages/shared/departments.html" },
          { id:"classes",     label:"Classes",     icon:"school",             href:"pages/admin/admin-classes.html" },
          { id:"timetables",  label:"Timetables",  icon:"calendar_view_week", href:"pages/admin/admin-timetables.html" },
          { id:"reports",     label:"Reports",     icon:"assessment",         href:"pages/admin/admin-reports.html" },
          { id:"fees",        label:"Fees",        icon:"payments",           href:"pages/admin/admin-fees.html" },
          { id:"logs",        label:"Audit Logs",  icon:"history",            href:"pages/admin/admin-logs.html" },
        ]},
        { label:"Communication", icon:"forum", links:[
          { id:"announcements", label:"Announcements", icon:"campaign", href:"pages/shared/announcements.html" },
          { id:"group-chat",    label:"Group Chat",    icon:"groups",   href:"pages/shared/group-chat.html", badge:"4" },
          { id:"chat",          label:"Direct Chat",   icon:"chat",     href:"pages/shared/chat.html", badge:"2" },
        ]},
        { label:"Account", icon:"person", links:[
          { id:"settings", label:"Settings", icon:"settings", href:"pages/admin/admin-settings.html" },
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
      { id:"group-chat",   label:"Group Chat",  icon:"groups",      href:"pages/shared/group-chat.html", badge:"2" },
      { id:"announcements",label:"Alerts",      icon:"campaign",    href:"pages/shared/announcements.html", badge:"3" },
      { id:"profile",      label:"Profile",     icon:"person",      href:"pages/student/student-profile.html" },
    ],
    parent: [
      { id:"dashboard",    label:"Home",       icon:"home",           href:"pages/parent/parent.html" },
      { id:"departments",  label:"Departments",icon:"apartment",      href:"pages/shared/departments.html" },
      { id:"group-chat",   label:"Group Chat", icon:"groups",         href:"pages/shared/group-chat.html", badge:"1" },
      { id:"notifications",label:"Alerts",     icon:"notifications",  href:"pages/parent/parent-notifications.html", badge:"2" },
      { id:"profile",      label:"Profile",    icon:"person",         href:"pages/parent/parent-profile.html" },
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
    const groups = cfg.groups.map((g, gi) => {
      const links = g.links.map(l =>
        `<a class="nav-link ${l.id === active ? "active" : ""}" href="${_P}${l.href}"${l.id===active?' aria-current="page"':''}>
           <span class="nav-link-icon"><span class="material-symbols-outlined">${l.icon}</span></span>
           <span class="nav-link-label">${esc(l.label)}</span>
           ${l.badge ? `<span class="pill">${l.badge}</span>` : ""}
         </a>`
      ).join("");
      return `
        <div class="nav-group">
          <div class="nav-group-label">
            ${g.icon ? `<span class="material-symbols-outlined">${g.icon}</span>` : ""}
            <span>${esc(g.label)}</span>
          </div>
          ${links}
        </div>
        ${gi < cfg.groups.length - 1 ? `<div class="nav-divider" role="separator"></div>` : ""}`;
    }).join("");

    return el(`
      <aside class="sidebar" id="sidebar" role="navigation" aria-label="Main navigation">
        <div class="side-brand">
          <div class="brand-mark"><span class="ngis-logo">NG</span></div>
          <div class="brand-text"><b>NGIS</b><span>${esc(cfg.brand)} Portal</span></div>
        </div>
        <div class="side-meta"><span class="dot-live"></span>${esc(cfg.meta)}</div>
        <nav class="side-nav">
          ${groups}
        </nav>
        <div class="side-foot">
          <a class="nav-link" href="${_P}index.html"><span class="nav-link-icon"><span class="material-symbols-outlined">help_outline</span></span><span class="nav-link-label">Help &amp; Support</span></a>
          <a class="nav-link nav-link-danger" href="${_P}index.html"><span class="nav-link-icon"><span class="material-symbols-outlined">logout</span></span><span class="nav-link-label">Sign Out</span></a>
        </div>
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
    const items = (BOTTOM[role] || BOTTOM.admin).map(it =>
      `<a class="bn-item ${it.id===active?"active":""}" href="${_P}${it.href}"${it.id===active?' aria-current="page"':''}>
         <span class="material-symbols-outlined">${it.icon}</span>
         <span>${it.label}</span>
         ${it.badge?`<span class="bn-badge">${it.badge}</span>`:""}
       </a>`
    ).join("");
    return el(`<nav class="bottomnav" role="navigation" aria-label="Primary"><div class="bottomnav-inner">${items}</div></nav>`);
  }

  function buildBreadcrumb(cfg, role, active) {
    const all = cfg.groups.reduce((acc, g) => acc.concat(g.links), []);
    const cur = all.find(l => l.id === active);
    if (!cur || active === "dashboard") return null;   // dashboards don't need a crumb
    return el(`
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="${_P}${PORTAL_HOME[role]}">${esc(cfg.brand)} Portal</a>
        <span class="material-symbols-outlined sep">chevron_right</span>
        <span class="cur" aria-current="page">${esc(cur.label)}</span>
      </nav>`);
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

    main.insertBefore(buildTopbar(user), main.firstChild);
    document.body.appendChild(buildBottomNav(PAGE.role, active));

    // Auto-breadcrumb at the top of the page body
    const page = document.querySelector(".page");
    const crumb = buildBreadcrumb(cfg, PAGE.role, active);
    if (page && crumb) page.insertBefore(crumb, page.firstChild);

    if (!document.querySelector(".toast-wrap")) {
      document.body.appendChild(el(`<div class="toast-wrap" id="toasts" role="region" aria-live="polite"></div>`));
    }

    /* Theme */
    applyTheme(store.get("ngis-theme") || "light");
    document.getElementById("themeToggle").addEventListener("click", () => {
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

    /* Mobile drawer */
    const menuBtn = document.getElementById("menuBtn");
    const openNav  = () => { sidebar.classList.add("open"); scrim.classList.add("show"); menuBtn.setAttribute("aria-expanded","true"); };
    const closeNav = () => { sidebar.classList.remove("open"); scrim.classList.remove("show"); menuBtn.setAttribute("aria-expanded","false"); };
    if (menuBtn) menuBtn.addEventListener("click", () => sidebar.classList.contains("open") ? closeNav() : openNav());
    scrim.addEventListener("click", closeNav);
    sidebar.querySelectorAll(".nav-link").forEach(a => a.addEventListener("click", closeNav));
    document.addEventListener("keydown", e => { if (e.key === "Escape") closeNav(); });

    /* ⌘K / Ctrl+K focuses search */
    document.addEventListener("keydown", (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        const i = document.querySelector(".search input");
        if (i) i.focus();
      }
    });

    /* Edge swipe to open / swipe to close (passive, subtle) */
    let tx = 0;
    document.addEventListener("touchstart", e => { tx = e.touches[0].clientX; }, { passive:true });
    document.addEventListener("touchend", e => {
      const dx = e.changedTouches[0].clientX - tx;
      if (tx < 24 && dx > 60) openNav();
      else if (dx < -60) closeNav();
    }, { passive:true });

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
