/* ============================================================
   EduFlow — Layout engine
   Reads window.PAGE = { role, active, user } and renders the
   shared sidebar + topbar, then wires interactions.
   ============================================================ */
(function () {
  "use strict";

  // ---- Navigation config per role ----
  const NAV = {
    admin: {
      brand: "Admin",
      meta: "Saint Patrick's Academy · AY 2024–25",
      links: [
        { id: "dashboard",  label: "Dashboard",  icon: "dashboard",      href: "admin-dashboard.html" },
        { id: "users",      label: "Users",      icon: "group",          href: "admin-users.html" },
        { id: "classes",    label: "Classes",    icon: "class",          href: "admin-classes.html" },
        { id: "timetables", label: "Timetables", icon: "calendar_view_week", href: "admin-timetables.html" },
        { id: "fees",       label: "Fees",       icon: "payments",       href: "admin-fees.html" },
        { id: "reports",    label: "Reports",    icon: "bar_chart",      href: "admin-reports.html" },
        { id: "logs",       label: "Audit Logs", icon: "history",        href: "admin-logs.html" },
        { id: "settings",   label: "Settings",   icon: "settings",       href: "admin-settings.html" },
      ],
    },
    teacher: {
      brand: "Teacher",
      meta: "Mathematics Dept · AY 2024–25",
      links: [
        { id: "dashboard",   label: "Dashboard",   icon: "dashboard",   href: "teacher-dashboard.html" },
        { id: "classes",     label: "My Classes",  icon: "school",      href: "teacher-classes.html" },
        { id: "attendance",  label: "Attendance",  icon: "how_to_reg",  href: "teacher-attendance.html" },
        { id: "grades",      label: "Grades",      icon: "grade",       href: "teacher-grades.html" },
        { id: "assignments", label: "Assignments", icon: "assignment",  href: "teacher-assignments.html" },
        { id: "analytics",   label: "Analytics",   icon: "analytics",   href: "teacher-analytics.html" },
      ],
    },
    student: {
      brand: "Student",
      meta: "Grade 11 · Section A",
      links: [
        { id: "dashboard",   label: "Dashboard",   icon: "dashboard",      href: "student-dashboard.html" },
        { id: "timetable",   label: "Timetable",   icon: "calendar_view_week", href: "student-timetable.html" },
        { id: "attendance",  label: "Attendance",  icon: "how_to_reg",     href: "student-attendance.html" },
        { id: "grades",      label: "Grades",      icon: "grade",          href: "student-grades.html" },
        { id: "assignments", label: "Assignments", icon: "assignment",     href: "student-assignments.html" },
        { id: "documents",   label: "Documents",   icon: "folder",         href: "student-documents.html" },
      ],
    },
    parent: {
      brand: "Parent",
      meta: "Guardian Account",
      links: [
        { id: "dashboard", label: "Dashboard",   icon: "dashboard",  href: "parent-dashboard.html" },
        { id: "children",  label: "My Children", icon: "family_restroom", href: "parent-children.html" },
        { id: "fees",      label: "Fees",        icon: "payments",   href: "parent-fees.html" },
        { id: "messaging", label: "Messaging",   icon: "chat",       href: "parent-messaging.html" },
        { id: "calendar",  label: "Calendar",    icon: "calendar_month", href: "parent-calendar.html" },
        { id: "settings",  label: "Settings",    icon: "settings",   href: "parent-settings.html" },
      ],
    },
  };

  const DEFAULT_USER = {
    admin:   { name: "Alex Mercer",     role: "Super Admin", initials: "AM" },
    teacher: { name: "Dr. Sarah Jenkins", role: "Mathematics", initials: "SJ" },
    student: { name: "Julian Rivers",   role: "Student",     initials: "JR" },
    parent:  { name: "Alex Mercer",     role: "Parent",      initials: "AM" },
  };

  function el(html) {
    const t = document.createElement("template");
    t.innerHTML = html.trim();
    return t.content.firstChild;
  }

  // ---- Theme (guarded; works as downloaded files, no-throw in sandboxes) ----
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} },
  };
  function applyTheme(mode) {
    document.documentElement.setAttribute("data-theme", mode);
    const btn = document.getElementById("themeToggle");
    if (btn) btn.querySelector(".material-symbols-outlined").textContent =
      mode === "dark" ? "light_mode" : "dark_mode";
  }

  function buildSidebar(cfg, active, user) {
    const links = cfg.links.map(l =>
      `<a class="nav-link ${l.id === active ? "active" : ""}" href="${l.href}">
         <span class="material-symbols-outlined">${l.icon}</span>${l.label}
         ${l.badge ? `<span class="pill">${l.badge}</span>` : ""}
       </a>`).join("");

    return el(`
      <aside class="sidebar" id="sidebar">
        <div class="side-brand">
          <div class="brand-mark"><span class="material-symbols-outlined fill">school</span></div>
          <div class="brand-text"><b>EduFlow</b><span>${cfg.brand} Portal</span></div>
        </div>
        <div class="side-meta"><span class="dot-live"></span>${cfg.meta}</div>
        <nav class="side-nav">
          <div class="nav-group-label">Menu</div>
          ${links}
        </nav>
        <div class="side-foot">
          <a class="nav-link" href="help.html"><span class="material-symbols-outlined">help</span>Help Center</a>
          <a class="nav-link" href="index.html" style="color:var(--danger)"><span class="material-symbols-outlined">logout</span>Sign out</a>
        </div>
      </aside>`);
  }

  function buildTopbar(user) {
    return el(`
      <header class="topbar">
        <button class="icon-btn menu-btn" id="menuBtn" aria-label="Open menu">
          <span class="material-symbols-outlined">menu</span>
        </button>
        <div class="search">
          <span class="material-symbols-outlined">search</span>
          <input type="text" placeholder="Search students, classes, documents…" aria-label="Search" />
          <kbd>⌘K</kbd>
        </div>
        <div class="top-right">
          <button class="icon-btn" id="themeToggle" aria-label="Toggle theme"><span class="material-symbols-outlined">dark_mode</span></button>
          <button class="icon-btn" aria-label="Help"><span class="material-symbols-outlined">help</span></button>
          <button class="icon-btn" aria-label="Notifications"><span class="material-symbols-outlined">notifications</span><span class="dot"></span></button>
          <div class="top-divider"></div>
          <button class="user-chip" aria-label="Account">
            <span class="avatar-fallback">${user.initials}</span>
            <span><span class="nm">${user.name}</span><br><span class="rl">${user.role}</span></span>
            <span class="material-symbols-outlined" style="font-size:18px;color:var(--faint)">expand_more</span>
          </button>
        </div>
      </header>`);
  }

  function mount() {
    const PAGE = window.PAGE || { role: "admin", active: "dashboard" };
    const cfg = NAV[PAGE.role] || NAV.admin;
    const user = PAGE.user || DEFAULT_USER[PAGE.role] || DEFAULT_USER.admin;

    document.body.setAttribute("data-role", PAGE.role);

    // Wrap: <body> already contains <main class="main"> with .page inside.
    const main = document.querySelector(".main");
    if (!main) return; // standalone pages (landing, sign-in, help) have no shell
    const shell = el(`<div class="shell"></div>`);
    main.parentNode.insertBefore(shell, main);

    const sidebar = buildSidebar(cfg, PAGE.active, user);
    const scrim = el(`<div class="scrim" id="scrim"></div>`);
    shell.appendChild(sidebar);
    shell.appendChild(main);
    document.body.appendChild(scrim);

    main.insertBefore(buildTopbar(user), main.firstChild);

    // toasts container
    if (!document.querySelector(".toast-wrap")) {
      document.body.appendChild(el(`<div class="toast-wrap" id="toasts"></div>`));
    }

    // ---- interactions ----
    applyTheme(store.get("eduflow-theme") || "light");
    document.getElementById("themeToggle").addEventListener("click", () => {
      const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      store.set("eduflow-theme", next);
      applyTheme(next);
    });

    const menuBtn = document.getElementById("menuBtn");
    const closeNav = () => { sidebar.classList.remove("open"); scrim.classList.remove("show"); };
    menuBtn && menuBtn.addEventListener("click", () => {
      sidebar.classList.toggle("open"); scrim.classList.toggle("show");
    });
    scrim.addEventListener("click", closeNav);
    sidebar.querySelectorAll(".nav-link").forEach(a => a.addEventListener("click", closeNav));

    // ⌘K / Ctrl+K focuses search
    document.addEventListener("keydown", (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        const i = document.querySelector(".search input");
        i && i.focus();
      }
    });
  }

  // ---- public toast helper ----
  window.toast = function (msg, kind) {
    const wrap = document.getElementById("toasts");
    if (!wrap) return;
    const icons = { success: "check_circle", error: "error", info: "info" };
    const t = el(`<div class="toast" style="border-left-color:var(--${kind === 'error' ? 'danger' : kind === 'success' ? 'success' : 'accent'})">
        <span class="material-symbols-outlined" style="color:var(--${kind === 'error' ? 'danger' : kind === 'success' ? 'success' : 'accent'})">${icons[kind] || icons.info}</span>${msg}</div>`);
    wrap.appendChild(t);
    setTimeout(() => { t.style.opacity = "0"; t.style.transition = "opacity .25s"; setTimeout(() => t.remove(), 250); }, 2600);
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount);
  else mount();
})();