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



     Student portal is DEPARTMENT-CENTRIC: the learning modules

     (Attendance, Assignments, Report Cards, Exams, Timetable, Lessons) are

     intentionally NOT top-level items — they live inside each Department.

     Teacher & Admin keep their operator tools, grouped for clarity.

     ------------------------------------------------------------------ */

  const NAV = {

    admin: {

      brand: "Admin", meta: "Institutional Suite · 2025–26",

      groups: [

        { label:"Overview", links:[

          { id:"dashboard", label:"Dashboard", icon:"dashboard", href:"pages/admin/admin.html" },

        ]},

        { id:"users-grp", label:"USER MANAGEMENT", icon:"group", links:[

          { id:"users", label:"User Directory", icon:"manage_accounts", href:"pages/admin/admin-users.html" },

          {
            id: "teachers-mgmt-drop",
            label: "Teachers Management",
            icon: "co_present",
            collapsible: true,
            children: [
              { id: "teacher-profiles", label: "Teacher Profile", href: "pages/admin/admin-teacher-profiles.html" },
              { id: "teacher-class-assignment", label: "Teacher-Class Assignment", href: "pages/admin/admin-teacher-class-assignment.html" },
              { id: "homeroom-assign", label: "Homeroom Teacher Assign", href: "pages/admin/admin-teacher-homeroom.html" },
              { id: "teacher-attendance", label: "Teacher Attendance", href: "pages/admin/admin-teacher-attendance.html" },
              { id: "teacher-discipline", label: "Discipline", href: "pages/admin/admin-teacher-discipline.html" },
            ]
          },

          {
            id: "student-mgmt-drop",
            label: "Student Management",
            icon: "school",
            collapsible: true,
            children: [
              { id: "student-profiles", label: "Student Information", href: "pages/admin/admin-student-profiles.html" },
              { id: "verify-student", label: "Verify Student Update", href: "pages/admin/admin-student-verify.html" },
              { id: "student-assign", label: "Student Assign To Class", href: "pages/admin/admin-student-assign.html" },
              { id: "declare-exemption", label: "Declare Exemption", href: "pages/admin/admin-student-exemption.html" },
              { id: "input-attendance", label: "Input Attendance", href: "pages/admin/admin-attendance.html" },
              {
                id: "academic-result-drop",
                label: "Academic Result",
                collapsible: true,
                children: [
                  { id: "subject-gpa", label: "Subject GPA By Exam", href: "pages/admin/admin-subject-gpa.html" },
                  { id: "semester-gpa", label: "Semester GPA", href: "pages/admin/admin-semester-gpa.html" },
                  { id: "student-failed", label: "Student Failed", href: "pages/admin/admin-student-failed.html" },
                ]
              },
              { id: "absence-stats", label: "Absence Statistics", href: "pages/admin/admin-absence-stats.html" },
              { id: "registration-approve", label: "Registration Form Approve", hasChevron: true, href: "pages/admin/admin-registration-approve.html" },
              { id: "student-commendation", label: "Commendation", href: "pages/admin/admin-student-commendation.html" },
              { id: "student-discipline", label: "Discipline", href: "pages/admin/admin-student-discipline.html" },
            ]
          },

        ]},

        { id:"academic", label:"ACADEMIC STRUCTURE", icon:"apartment", links:[

          { id:"departments", label:"Departments", icon:"apartment",          href:"pages/admin/admin-departments.html" },

          { id:"campuses",    label:"Campuses",    icon:"location_city",      href:"pages/admin/admin-campuses.html" },

          { id:"classes",     label:"Classes",     icon:"school",             href:"pages/admin/admin-classes.html" },

          { id:"timetables",  label:"Timetables",  icon:"calendar_view_week", href:"pages/admin/admin-timetables.html" },

        ]},

        { id:"khmer-suite", label:"TIMETABLE MANAGEMENT", icon:"calendar_view_week", links:[
          { id:"ks-oversight", label:"Timetable Oversight", icon:"monitor_heart", href:"pages/admin/admin-timetable-management.html" },
          { id:"ks-viewer", label:"Timetables Matrix", icon:"calendar_view_week", href:"pages/admin/admin-timetables.html" },
          { id:"ks-subjects", label:"Curriculum Subjects", icon:"menu_book", href:"pages/admin/admin-subjects.html" }
        ]},

        { id:"records", label:"INSTITUTIONAL RECORDS", icon:"folder_shared", links:[

          { id:"services", label:"Student Services", icon:"assignment", href:"pages/admin/admin-services.html" },

          { id:"reports",  label:"Academic Reports", icon:"assessment", href:"pages/admin/admin-reports.html" },

        ]},

        { id:"communication", label:"COMMUNICATION", icon:"campaign", links:[

          { id:"dashboard-content", label:"Dashboard Content", icon:"dashboard_customize", href:"pages/admin/admin-dashboard-content.html" },

          { id:"announcements", label:"School Announcements", icon:"campaign", href:"pages/shared/announcements.html?portal=admin" },

          { id:"news",          label:"News CMS",             icon:"newspaper", href:"pages/admin/admin-news.html" },

        ]},

        { id:"system", label:"SYSTEM & SECURITY", icon:"admin_panel_settings", links:[

          {
            id: "system-mgmt-drop",
            label: "System",
            icon: "settings",
            collapsible: true,
            children: [
              { id: "dashboard-content-sys", label: "Dashboard Content", href: "pages/admin/admin-dashboard-content.html" },
              { id: "school-information", label: "School Information & Settings", href: "pages/admin/admin-school-information.html" },
              { id: "sys-school-info", label: "School Profile (Legacy)", href: "pages/admin/admin-system-school-info.html" },
              {
                id: "sys-year-config-drop",
                label: "School Year Configuration",
                collapsible: true,
                children: [
                  { id: "sys-school-year", label: "School Year", href: "pages/admin/admin-system-school-year.html" },
                  { id: "sys-school-week", label: "School Week", href: "pages/admin/admin-system-school-week.html" },
                  { id: "sys-exam-config", label: "School Exam Configuration", href: "pages/admin/admin-system-exam-config.html" },
                  { id: "sys-score-lock", label: "Score Lock Configuration", href: "pages/admin/admin-system-score-lock.html" },
                  { id: "sys-define-curriculum", label: "Define Curriculum", href: "pages/admin/admin-system-define-curriculum.html" },
                  { id: "sys-design-curriculum", label: "Design Curriculum", href: "pages/admin/admin-system-design-curriculum.html" },
                  { id: "sys-declare-class", label: "Declare Class", href: "pages/admin/admin-system-declare-class.html" },
                  { id: "sys-student-transition", label: "Student Transition", href: "pages/admin/admin-system-student-transition.html" },
                  { id: "sys-technician-assign", label: "Technician & Monitor Assign", href: "pages/admin/admin-system-technician-assign.html" },
                ]
              },
              {
                id: "sys-account-mgmt-drop",
                label: "Account Management",
                collapsible: true,
                children: [
                  { id: "sys-employee-group", label: "Employee Group", href: "pages/admin/admin-system-employee-group.html" },
                  { id: "sys-employee-accounts", label: "Employee Accounts", href: "pages/admin/admin-system-employee-accounts.html" },
                  { id: "sys-student-accounts", label: "Student Accounts", href: "pages/admin/admin-system-student-accounts.html" },
                  { id: "sys-parent-accounts", label: "Parent Accounts", href: "pages/admin/admin-system-parent-accounts.html" },
                ]
              },
              { id: "sys-schedule", label: "Schedule", href: "pages/admin/admin-system-schedule.html" },
              { id: "sys-general-setting", label: "General Setting", href: "pages/admin/admin-system-general-setting.html" },
            ]
          },

          { id:"logs",     label:"Audit Logs",      icon:"history",  href:"pages/admin/admin-logs.html" },

          { id:"settings", label:"System Settings", icon:"settings", href:"pages/admin/admin-settings.html" },

        ]},

        { id:"account-grp", label:"ACCOUNT", icon:"person", links:[

          { id:"profile", label:"Admin Profile", icon:"person", href:"pages/admin/admin-settings.html" },

          { id:"logout",  label:"Log out",       icon:"logout", href:"index.html" },

        ]},

      ],

    },

    teacher: {

      brand: "Teacher", meta: "Faculty Portal · 2025–26",

      groups: [

        { label:"Overview", links:[

          { id:"dashboard",  label:"Home",                       icon:"home",           href:"pages/teacher/teacher.html", chevron:false },

        ]},

        { id:"teaching", label:"TEACHING", icon:"school", links:[

          { id:"attendance", label:"Attendance",                 icon:"how_to_reg",     href:"pages/teacher/teacher-attendance.html" },

          { id:"roster",     label:"Roster & Profiles",          icon:"badge",          href:"pages/teacher/teacher-roster.html" },

          { id:"lessons",    label:"Lessons & Materials",        icon:"menu_book",      href:"pages/teacher/teacher-lessons.html" },

          { id:"departments",label:"Department",                 icon:"apartment",      href:"pages/teacher/teacher-departments.html" },

          { id:"calendar",   label:"Timetable",                  icon:"calendar_month", href:"pages/teacher/teacher-calendar.html" },

        ]},

        { id:"assessment", label:"ASSESSMENT", icon:"grading", links:[

          { id:"submissions", label:"Assignments & Student Work", icon:"description",  href:"pages/teacher/teacher-submissions.html" },

          { id:"reports",     label:"Official Academic Reports",  icon:"assessment",   href:"pages/teacher/teacher-reports.html" },

        ]},

        { id:"communication", label:"COMMUNICATION", icon:"campaign", links:[

          { id:"announcements", label:"Class Announcements",      icon:"campaign",      href:"pages/teacher/teacher-announcements.html" },

        ]},

        { id:"campus-services", label:"CAMPUS & SERVICES", icon:"local_activity", links:[

          { id:"services",       label:"Faculty Services Hub",      icon:"grid_view",     href:"pages/teacher/teacher-services.html" },

          { id:"lost-found",     label:"Lost & Found",              icon:"inventory_2",   href:"pages/teacher/teacher-lost-found.html" },

        ]},

        { id:"account-grp", label:"ACCOUNT", icon:"person", links:[

          { id:"profile",       label:"Settings & Profile",       icon:"settings",      href:"pages/teacher/teacher-profile.html" },

          { id:"logout",        label:"Log out",                  icon:"logout",        href:"index.html" },

        ]},

      ],

    },

    student: {

      brand: "Student", meta: "Student Portal · 2025–26",

      groups: [

        { label:"Main", links:[

          { id:"dashboard", label:"Dashboard", icon:"dashboard", href:"pages/student/student.html" },

        ]},

        { id:"academics", label:"ACADEMICS", icon:"school", links:[

          { id:"departments", label:"Academic Departments", icon:"apartment", href:"pages/shared/departments.html?portal=student" },

          { id:"calendar",    label:"Class Timetable",      icon:"calendar_month", href:"pages/student/student-calendar.html" },

          { id:"student-id",  label:"Digital Student ID",    icon:"badge", href:"pages/student/student-id.html" },

        ]},

        { id:"campus-life", label:"CAMPUS LIFE", icon:"local_activity", links:[

          { id:"services",   label:"Services Hub",       icon:"grid_view", href:"pages/student/student-services.html" },

          { id:"lost-found", label:"Lost & Found",       icon:"inventory_2", href:"pages/student/student-lost-found.html" },

        ]},

        { id:"communication", label:"COMMUNICATION", icon:"campaign", links:[

          { id:"announcements", label:"Announcements", icon:"campaign", href:"pages/student/student-announcements.html" },

        ]},

        { id:"account-grp", label:"ACCOUNT", icon:"person", links:[

          { id:"notifications", label:"Notifications", icon:"notifications", href:"pages/student/student-notifications.html", badge:"5" },

          { id:"profile",       label:"My Profile",    icon:"person",        href:"pages/student/student-profile.html" },

          { id:"logout",        label:"Log out",       icon:"logout",        href:"index.html" },

        ]},

      ],

    },

        principal: {
      brand: "Principal", meta: "School Operations · 2025–26",
      groups: [
        { label: "Overview", links: [
          { id: "dashboard", label: "Home", icon: "home", href: "pages/principal/principal.html" },
        ]},
        { id: "teachers-mgmt", label: "TEACHER MANAGEMENT", icon: "school", links: [
          { id: "teacher-profiles", label: "Teacher Profile", icon: "co_present", href: "pages/principal/principal-teacher-profiles.html" },
        ]},
        { id: "academic-oversight", label: "ACADEMIC OVERSIGHT", icon: "assignment", links: [
          { id: "attendance", label: "Attendance", icon: "how_to_reg", href: "pages/principal/principal-attendance.html" },
            { id: "reports", label: "Student Results & Reports", icon: "assessment", href: "pages/principal/principal-reports.html" },
        ]},
        { id:"khmer-suite", label:"TIMETABLE MANAGEMENT", icon:"calendar_view_week", links:[
          { id:"ks-wizard", label:"Teacher Assignment", icon:"swap_horiz", href:"pages/principal/principal-teacher-class-assignment.html" },
          { id:"ks-builder", label:"Timetable Builder", icon:"grid_view", href:"pages/principal/principal-timetable-builder.html" },
          { id:"ks-viewer", label:"Timetables Matrix", icon:"calendar_view_week", href:"pages/principal/principal-timetables.html" },
          { id:"ks-subjects", label:"Curriculum Subjects", icon:"menu_book", href:"pages/principal/principal-subjects.html" }
        ]},
        { id: "students-mgmt", label: "STUDENT MANAGEMENT", icon: "group", links: [
          { id: "student-profiles", label: "Student Profile", icon: "school", href: "pages/principal/principal-student-profiles.html" },
        ]},
        { id: "approvals-grp", label: "DECISIONS & NOTICES", icon: "verified", links: [
          { id: "principal-school-information", label: "School Information", icon: "account_balance", href: "pages/principal/principal-school-information.html" },
          { id: "announcements", label: "School Announcements", icon: "campaign", href: "pages/shared/announcements.html?portal=principal" },
          { id: "activity", label: "Change History", icon: "history", href: "pages/principal/principal-activity.html" },
        ]},
        { id: "account-grp", label: "ACCOUNT", icon: "person", links: [
          { id: "profile", label: "Settings & Profile", icon: "settings", href: "pages/principal/principal-profile.html" },
          { id: "logout", label: "Log out", icon: "logout", href: "index.html" },
        ]},
      ],
    },
  };



  /* ── Published navigation override (Global Sidebar Manager) ──

     The built-in NAV above is the safe default. When the backend has a
     published navigation configuration for a portal (managed from
     admin-dashboard-content.html → Sidebar Manager), it takes precedence.

     The backend JSON store is the single source of truth; sessionStorage is
     only a render-fast cache so the sidebar paints without a flash. */

  let NAV_OVERRIDE = null;

  const NAV_CACHE_KEY = 'ngis-nav-published';

  try {

    const cached = sessionStorage.getItem(NAV_CACHE_KEY);

    if (cached) NAV_OVERRIDE = JSON.parse(cached);

  } catch (e) { /* ignore malformed cache */ }

  const navReadyPromise = fetch('/api/nav/published')

    .then((r) => (r && r.ok ? r.json() : null))

    .then((res) => {

      if (res && res.success && res.data && typeof res.data === 'object') {

        NAV_OVERRIDE = res.data;

        try { sessionStorage.setItem(NAV_CACHE_KEY, JSON.stringify(res.data)); } catch (e) {}

      }

    })

    .catch(() => { /* keep cache / built-in NAV */ });



  function resolveNav(portalRole) {

    const source = NAV_OVERRIDE || NAV;

    const cfg = source[portalRole];

    // Guard against an empty/partial published config for this portal.

    if (cfg && Array.isArray(cfg.groups) && cfg.groups.length) return cfg;

    return NAV[portalRole] || NAV.student;

  }

  /* Department sub-pages keep "Departments" highlighted in the sidebar,

     since these modules now live inside each department. */

  const DEPT_CHILD = ["attendance","assignments","grades","exams","timetable","lessons","department"];



  /* Mobile bottom-nav: primary destinations per role */

  const BOTTOM = {

    admin: [

      { id:"dashboard",  label:"Home",       icon:"home",      href:"pages/admin/admin.html" },

      { id:"users",      label:"Users",       icon:"group",     href:"pages/admin/admin-users.html" },

      { id:"reports",    label:"Reports",     icon:"assessment",href:"pages/admin/admin-reports.html" },

      { id:"settings",   label:"Settings",    icon:"settings",  href:"pages/admin/admin-settings.html" },

    ],

    teacher: [

      { id: "home", label: "Home", icon: "ph ph-house", href: "pages/teacher/teacher.html" },

      { id: "classes", label: "Classes", icon: "ph ph-chalkboard-teacher", href: "pages/teacher/teacher-roster.html" },

      { id: "submissions", label: "Work", icon: "ph ph-file-text", href: "pages/teacher/teacher-submissions.html" },

      { id: "profile", label: "Profile", icon: "ph ph-user", href: "pages/teacher/teacher-profile.html" },

    ],

    student: [

      { id:"dashboard",    label:"Home",        icon:"home",           href:"pages/student/student.html" },

      { id:"departments",  label:"Department",  icon:"apartment",      href:"pages/shared/departments.html" },

      { id:"calendar",     label:"Schedule",    icon:"calendar_month", href:"pages/student/student-calendar.html" },

      { id:"profile",      label:"Profile",     icon:"person",         href:"pages/student/student-profile.html" },

    ],

    principal: [

      { id:"dashboard",  label:"Home",       icon:"home",           href:"pages/principal/principal.html" },

      { id:"classes",    label:"Classes",    icon:"class",          href:"pages/principal/principal-classes.html" },

      { id:"students",   label:"Students",   icon:"school",         href:"pages/principal/principal-student-profiles.html" },

      { id:"reports",    label:"Reports",    icon:"assessment",     href:"pages/principal/principal-reports.html" },

      { id:"profile",    label:"Profile",    icon:"person",         href:"pages/principal/principal-profile.html" },

    ],

  };



  



  const DEFAULT_USER = {

    admin:     { name:"Sok Panha Heng",  role:"Super Administrator",  initials:"SH" },

    teacher:   { name:"Dr. Sarah Jenkins", role:"Head of Senior Faculty", initials:"SJ" },

    student:   { name:"Nrinphouneta Hok", role:"Student · Grade 11-A", initials:"NH" },

    principal: { name:"Dr. Ly Bunheng",  role:"Campus Principal",     initials:"LB" },

  };



  const PORTAL_HOME = {

    admin: "pages/admin/admin.html",

    teacher: "pages/teacher/teacher.html",

    student: "pages/student/student.html",

    principal: "pages/principal/principal.html"

  };



  /* Resolve the portal from the authenticated session and scoped URL. */

  function readStoredUser(key) {

    try { return JSON.parse(localStorage.getItem(key) || "null"); } catch (e) { return null; }

  }

  function normalizeRole(role) {

    if (!role) return "student";

    role = String(role).toLowerCase();

    if (role === "super_admin" || role === "superadmin") return "admin";

    return role;

  }

  function getSessionRole() {

    const authRole = window.NGISAuth && typeof window.NGISAuth.getRole === "function" ? window.NGISAuth.getRole() : null;

    const user = readStoredUser("ngis_user");

    return normalizeRole(authRole || (user && user.role));

  }

  function resolvePortalRole(pageRole) {

    const path = (window.location.pathname || "").replace(/\\/g, "/");

    const match = path.match(/\/pages\/(admin|teacher|student|parent|principal)\//);

    const pathRole = match ? match[1] : null;



    // Priority 1: Explicit role directory path (e.g. /pages/admin/, /pages/teacher/, /pages/student/, etc.)

    if (pathRole) {

      const normalizedPathRole = normalizeRole(pathRole);

      try { localStorage.setItem("ngis_active_portal", normalizedPathRole); } catch (e) {}

      return normalizedPathRole;

    }



    // Priority 2: Explicit URL query param (?portal=... or ?role=...)

    const params = new URLSearchParams(window.location.search || "");

    const queryRole = (params.get("portal") || params.get("role") || "").toLowerCase();

    if (["admin", "teacher", "student", "principal"].includes(queryRole)) {

      try { localStorage.setItem("ngis_active_portal", queryRole); } catch (e) {}

      return queryRole;

    }



    // Priority 3: Explicit pageRole configured on window.PAGE

    if (pageRole) {

      const normalizedPageRole = normalizeRole(pageRole);

      if (["admin", "teacher", "student", "principal"].includes(normalizedPageRole)) {

        try { localStorage.setItem("ngis_active_portal", normalizedPageRole); } catch (e) {}

        return normalizedPageRole;

      }

    }



    // Priority 4: Stored portal preference or active session role

    const sessionRole = getSessionRole();

    if (sessionRole && ["admin", "teacher", "student", "principal"].includes(sessionRole)) {

      return sessionRole;

    }

    const storedPortal = localStorage.getItem("ngis_active_portal");

    if (storedPortal && ["admin", "teacher", "student", "principal"].includes(storedPortal)) {

      return storedPortal;

    }



    return "student";

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

    document.documentElement.setAttribute("data-theme", "light");

    if (document.body) document.body.setAttribute("data-theme", "light");

    const btn = document.getElementById("themeToggle");

    if (btn) btn.remove();

  }



  function buildSidebar(cfg, active, user) {

    const role = (window.PAGE && window.PAGE.role) || "admin";

    const homeHref = PORTAL_HOME[role] ? `${_P}${PORTAL_HOME[role]}` : `${_P}index.html`;

    const currentUser = user || (window.PAGE && window.PAGE.user) || DEFAULT_USER[role] || DEFAULT_USER.teacher;



    function linkHasId(item, id) {

      if (!item) return false;

      if (item.id === id) return true;

      if ((id === "teachers" || id === "teacher-profiles") && (item.id === "teachers" || item.id === "teacher-profiles" || item.id === "teachers-mgmt-drop")) return true;

      if ((id === "students" || id === "student-profiles") && (item.id === "students" || item.id === "student-profiles" || item.id === "student-mgmt-drop")) return true;

      if (item.children) {
        for (const c of item.children) {
          if (c.id === id) return true;
          if ((id === "teachers" || id === "teacher-profiles") && (c.id === "teachers" || c.id === "teacher-profiles")) return true;
          if ((id === "students" || id === "student-profiles") && (c.id === "students" || c.id === "student-profiles")) return true;
          if (c.children && c.children.some(n => n.id === id)) return true;
        }
      }

      return false;

    }



    // Auto-detect active link if not set or doesn't match any link in this portal

    let effectiveActive = active;

    const curFile = (window.location.pathname || '').replace(/\\/g, '/').split('/').pop().toLowerCase();
    const curSearch = (window.location.search || '').toLowerCase();

    // Query parameter priority match for nested subgroups (e.g., ?view=verify, ?tab=assignments, ?tab=homeroom)
    if (curSearch) {
      for (const g of cfg.groups) {
        for (const l of g.links) {
          if (l.children && l.children.length > 0) {
            for (const sub of l.children) {
              if (sub.children && sub.children.length > 0) {
                for (const n of sub.children) {
                  if (n.href && n.href.includes('?')) {
                    const parts = n.href.split('?');
                    const nFile = parts[0].split('/').pop().toLowerCase();
                    const nQuery = (parts[1] || '').toLowerCase();
                    if (nFile === curFile && curSearch.includes(nQuery)) {
                      effectiveActive = n.id;
                      break;
                    }
                  }
                }
              } else if (sub.href && sub.href.includes('?')) {
                const parts = sub.href.split('?');
                const subFile = parts[0].split('/').pop().toLowerCase();
                const subQuery = (parts[1] || '').toLowerCase();
                if (subFile === curFile && curSearch.includes(subQuery)) {
                  effectiveActive = sub.id;
                  break;
                }
              }
            }
          }
          if (effectiveActive && linkHasId(l, effectiveActive)) break;
        }
      }
    }

    if (!effectiveActive || !cfg.groups.some(g => g.links.some(l => linkHasId(l, effectiveActive)))) {

      for (const g of cfg.groups) {

        for (const l of g.links) {

          if (l.children && l.children.length > 0) {

            for (const sub of l.children) {

              if (sub.children && sub.children.length > 0) {
                for (const n of sub.children) {
                  const nFile = (n.href || '').split('?')[0].split('/').pop().toLowerCase();
                  if (nFile && nFile === curFile) {
                    effectiveActive = n.id;
                    break;
                  }
                }
              } else {
                const linkFile = (sub.href || '').split('?')[0].split('/').pop().toLowerCase();
                if (linkFile && linkFile === curFile) {
                  effectiveActive = sub.id;
                  break;
                }
              }

            }

          } else {

            const linkFile = (l.href || '').split('?')[0].split('/').pop().toLowerCase();

            if (linkFile && linkFile === curFile) {

              effectiveActive = l.id;

              break;

            }

          }

          if (effectiveActive && cfg.groups.some(grp => grp.links.some(lnk => linkHasId(lnk, effectiveActive)))) break;

        }

      }

    }



    function renderNavIcon(icon, className) {
      if (!icon) return "";
      const trimmed = String(icon).trim();
      if (trimmed.startsWith("<svg")) {
        return `<span class="nav-icon ${className} nav-icon-svg" aria-hidden="true">${trimmed}</span>`;
      }
      if (trimmed.startsWith("ph ") || trimmed.startsWith("ph-")) {
        return `<i class="${trimmed} ${className} nav-icon" aria-hidden="true"></i>`;
      }
      return `<span class="material-symbols-outlined ${className} nav-icon" aria-hidden="true">${trimmed}</span>`;
    }

    const groups = cfg.groups.map((g, gi) => {

      if (g.visible === false) return '';

      const links = g.links.map(l => {

        if (l.visible === false) return '';

        if (l.children && l.children.length > 0) {

          const isSubActive = l.children.some(sub => {
            if (sub.id === effectiveActive || ((effectiveActive === "teachers" || effectiveActive === "teacher-profiles") && (sub.id === "teachers" || sub.id === "teacher-profiles")) || ((effectiveActive === "students" || effectiveActive === "student-profiles") && (sub.id === "students" || sub.id === "student-profiles"))) return true;
            if (sub.children && sub.children.some(n => n.id === effectiveActive)) return true;
            return false;
          });

          const sublinks = l.children.map(sub => {
            if (sub.visible === false) return '';
            if (sub.children && sub.children.length > 0) {
              const isNestedActive = sub.children.some(n => n.id === effectiveActive);
              const nestedLinks = sub.children.map(n => {
                if (n.visible === false) return '';
                const isNActive = n.id === effectiveActive;
                return `<a class="nav-link nav-nested-link ${isNActive ? "active" : ""}" href="${_P}${n.href}"${isNActive ? ' aria-current="page"' : ''} title="${esc(n.subtitle || n.label)}" data-id="${n.id}">
                  <span class="nav-link-label">${esc(n.label)}</span>
                  ${n.badge ? `<span class="pill">${n.badge}</span>` : ""}
                </a>`;
              }).join("");

              return `
                <div class="nav-nested-group${sub.collapsible ? ' collapsible' : ''}${isNestedActive ? ' expanded' : ''}" data-nested-id="${sub.id}">
                  <button type="button" class="nav-nested-label" aria-expanded="${isNestedActive ? 'true' : 'false'}" title="${esc(sub.label)}">
                    <span class="nav-link-label">${esc(sub.label)}</span>
                    <span class="material-symbols-outlined ngl-nestedchevron" aria-hidden="true">expand_more</span>
                  </button>
                  <div class="nav-nested-links">
                    <div>${nestedLinks}</div>
                  </div>
                </div>`;
            }

            const isItemActive = sub.id === effectiveActive || ((effectiveActive === "teachers" || effectiveActive === "teacher-profiles") && (sub.id === "teachers" || sub.id === "teacher-profiles")) || ((effectiveActive === "students" || effectiveActive === "student-profiles") && (sub.id === "students" || sub.id === "student-profiles"));
            const chevronHtml = sub.hasChevron ? `<span class="material-symbols-outlined ngl-subchevron-static" aria-hidden="true">expand_more</span>` : "";
            return `<a class="nav-link nav-sub-link ${isItemActive ? "active" : ""}" href="${_P}${sub.href}"${isItemActive ? ' aria-current="page"' : ''} title="${esc(sub.subtitle || sub.label)}" data-id="${sub.id}">
               ${sub.icon ? renderNavIcon(sub.icon, "nav-link-icon") : ""}
               <span class="nav-link-label">${esc(sub.label)}</span>
               ${sub.badge ? `<span class="pill">${sub.badge}</span>` : ""}
               ${chevronHtml}
             </a>`;
          }).join("");

          return `

            <div class="nav-subgroup${l.collapsible ? ' collapsible' : ''}${isSubActive ? ' expanded' : ''}" data-subgroup-id="${l.id}">

              <button type="button" class="nav-subgroup-label" aria-expanded="${isSubActive ? 'true' : 'false'}" title="${esc(l.label)}">

                ${renderNavIcon(l.icon, "nav-link-icon")}

                <span class="nav-link-label">${esc(l.label)}</span>

                <span class="material-symbols-outlined ngl-subchevron" aria-hidden="true">expand_more</span>

              </button>

              <div class="nav-subgroup-links">

                <div>${sublinks}</div>

              </div>

            </div>`;

        }

        return `<a class="nav-link ${l.icon ? '' : 'no-icon'} ${l.id === effectiveActive ? "active" : ""}" href="${_P}${l.href}"${l.id===effectiveActive?' aria-current="page"':''} title="${esc(l.subtitle || l.label)}" data-id="${l.id}">

           ${renderNavIcon(l.icon, "nav-link-icon")}

           <span class="nav-link-label">${esc(l.label)}</span>

           ${l.badge ? `<span class="pill">${l.badge}</span>` : ""}

         </a>`;

      }).join("");

      const groupActive = g.id === effectiveActive || g.links.some(l => linkHasId(l, effectiveActive));

      const labelInner = `

        ${renderNavIcon(g.icon, "nav-group-icon")}

        <span class="nav-group-label-text">${esc(g.label || "")}</span>

        <span class="nav-group-label-rule"></span>`;



      let label = "", linksHtml;

      if (g.collapsible) {

        label = `<button type="button" class="nav-group-label" aria-expanded="false" title="${esc(g.label)}">${labelInner}</button>`;

        linksHtml = `<div class="nav-group-links"><div>${links}</div></div>`;

      } else if (g.href) {

        label = `<a class="nav-group-label nav-group-label-link${groupActive ? " active" : ""}" href="${_P}${g.href}">${labelInner}</a>`;

        linksHtml = links;

      } else if (g.label) {

        label = `<div class="nav-group-label">${labelInner}</div>`;

        linksHtml = links;

      } else {

        label = "";

        linksHtml = links;

      }

      return `

        <div class="nav-group${g.collapsible ? " collapsible" : ""}"${g.id ? ` data-group-id="${g.id}"` : ""}>

          ${label}

          ${linksHtml}

        </div>`;

    }).join("");



    return el(`

      <aside class="sidebar custom-scrollbar" id="sidebar" role="navigation" aria-label="Main navigation" data-purpose="primary-sidebar">

        <div class="side-brand">

          <a class="side-brand-info" href="${homeHref}" aria-label="New Gateway International School">

            <img class="side-brand-crest" src="${_P}assets/images/ngis-seal.svg" alt="NGIS Crest" onerror="this.onerror=null;this.src='${_P}pages/student/LOGO%20NGIS%20(2).png'">

            <div class="side-brand-titles">

              <span class="side-brand-name">NGIS</span>

              <span class="side-brand-school">New Gateway International School</span>

            </div>

          </a>

          <button class="sidebar-collapse-btn" id="sidebarCollapseBtn" title="Collapse sidebar" aria-label="Collapse sidebar" type="button" data-purpose="sidebar-collapse-button">

            <svg class="side-collapse-svg" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">

              <line x1="6" y1="5" x2="6" y2="19"></line>

              <polyline points="16 7 10 12 16 17"></polyline>

            </svg>

          </button>

          <button class="sidebar-close-btn" id="sidebarCloseBtn" title="Close navigation" aria-label="Close navigation" type="button">

            <i class="ph ph-x text-lg" aria-hidden="true"></i>

          </button>

        </div>



        <nav class="side-nav custom-scrollbar" aria-label="Main Navigation">

          ${groups}

        </nav>



        <footer class="side-foot">

          <a class="nav-link side-foot-help" href="${_P}${role === 'student' ? 'pages/student/student-services.html' : role === 'teacher' ? 'pages/teacher/teacher-services.html' : 'pages/shared/announcements.html'}">

            <span class="material-symbols-outlined nav-link-icon nav-icon" aria-hidden="true">help_outline</span>

            <span class="nav-link-label">Help &amp; Support</span>

          </a>

          <a class="nav-link nav-link-danger side-foot-signout" href="${_P}index.html" data-purpose="sign-out-button">

            <span class="material-symbols-outlined nav-link-icon nav-icon" aria-hidden="true">logout</span>

            <span class="nav-link-label">Log out</span>

          </a>

        </footer>

      </aside>`);

  }



  function buildTopbar(user) {

    return el(`

      <header class="topbar" role="banner">

        <button class="icon-btn menu-btn hamburger-btn mobile-hamburger-btn" id="menuBtn" data-action="toggle-sidebar" aria-label="Open menu" aria-controls="sidebar" aria-expanded="false" title="Open navigation">

          <i class="ph ph-list text-xl" aria-hidden="true"></i>

          <span class="material-symbols-outlined" style="display:none">menu</span>

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



  const MOB_NAV_TABS = {

    student: [

      { id: "home", label: "Home", icon: "ph-fill ph-house-simple", href: "pages/student/student.html" },

      { id: "department", label: "Departments", icon: "ph-bold ph-buildings", href: "pages/shared/departments.html" },

      { id: "schedule", label: "Schedule", icon: "ph-bold ph-calendar", href: "pages/student/student-calendar.html" },

      { id: "profile", label: "Profile", icon: "ph-bold ph-user", href: "pages/student/student-profile.html" },

    ],

    teacher: [

      { id: "home", label: "Home", icon: "ph ph-house", href: "pages/teacher/teacher.html" },

      { id: "classes", label: "Classes", icon: "ph ph-chalkboard-teacher", href: "pages/teacher/teacher-roster.html" },

      { id: "submissions", label: "Work", icon: "ph ph-file-text", href: "pages/teacher/teacher-submissions.html" },

      { id: "profile", label: "Profile", icon: "ph ph-user", href: "pages/teacher/teacher-profile.html" },

    ],

    admin: [

      { id: "home", label: "Home", icon: "ph-fill ph-house-simple", href: "pages/admin/admin.html" },

      { id: "users", label: "Users", icon: "ph-bold ph-users-four", href: "pages/admin/admin-users.html" },

      { id: "reports", label: "Reports", icon: "ph-bold ph-chart-line-up", href: "pages/admin/admin-reports.html" },

      { id: "settings", label: "Settings", icon: "ph-bold ph-gear", href: "pages/admin/admin-settings.html" },

    ],

    principal: [

      { id: "home", label: "Home", icon: "ph-fill ph-house-simple", href: "pages/principal/principal.html" },

      { id: "classes", label: "Classes", icon: "ph-bold ph-chalkboard-simple", href: "pages/principal/principal-classes.html" },

      { id: "students", label: "Students", icon: "ph-bold ph-school", href: "pages/principal/principal-student-profiles.html" },

      { id: "reports", label: "Reports", icon: "ph-bold ph-chart-line-up", href: "pages/principal/principal-reports.html" },

      { id: "profile", label: "Profile", icon: "ph-bold ph-user", href: "pages/principal/principal-profile.html" },

    ],

  };



  function getRoleActiveTab(role, active) {

    const path = (window.location.pathname || '').toLowerCase();

    const file = (path.split('/').pop() || '').toLowerCase();

    if (file === `${role}.html` || (active === 'dashboard' && file.indexOf(`${role}-`) === -1)) return 'home';

    

    if (file.indexOf('notification') !== -1 || file.indexOf('announcement') !== -1 || file.indexOf('log') !== -1 || active === 'notifications' || active === 'announcements' || active === 'alerts' || active === 'logs') return 'alerts';

    if (file.indexOf('profile') !== -1 || file.indexOf('setting') !== -1 || active === 'profile' || active === 'settings' || active === 'preferences') {

      return (role === 'admin' || role === 'principal') ? 'settings' : 'profile';

    }

    if (role === 'teacher') {

      if (file === 'teacher.html' || active === 'dashboard') return 'home';

      if (file.indexOf('class') !== -1 || active === 'classes') return 'classes';

      if (file.indexOf('submission') !== -1 || file.indexOf('assignment') !== -1 || active === 'submissions' || active === 'assignments') return 'submissions';

      if (file.indexOf('gradebook') !== -1 || file.indexOf('grade') !== -1 || active === 'gradebook') return 'gradebook';

      if (file.indexOf('profile') !== -1 || active === 'profile') return 'profile';

      return 'home';

    }

    if (role === 'admin') {

      if (file.indexOf('user') !== -1 || active === 'users' || active === 'admins' || active === 'teachers' || active === 'students' || active === 'parents') return 'users';

      if (file.indexOf('report') !== -1 || active === 'reports') return 'reports';

      if (file.indexOf('setting') !== -1 || active === 'settings') return 'settings';

    }

    if (role === 'principal') {

      if (file === 'principal.html' || active === 'dashboard') return 'home';

      if (file.indexOf('approval') !== -1 || active === 'approvals' || active === 'requests') return 'approvals';

      if (file.indexOf('student') !== -1 || active === 'students') return 'students';

      if (file.indexOf('report') !== -1 || file.indexOf('teacher') !== -1 || file.indexOf('document') !== -1 || file.indexOf('activity') !== -1 || active === 'reports' || active === 'teachers' || active === 'documents' || active === 'activity') return 'reports';

      if (file.indexOf('profile') !== -1 || active === 'profile') return 'profile';

      return 'home';

    }

    if (role === 'student') {

      if (file === 'student.html' || active === 'dashboard') return 'home';

      if (file.indexOf('department') !== -1 || active === 'departments') return 'department';

      if (file.indexOf('calendar') !== -1 || file.indexOf('timetable') !== -1 || active === 'calendar' || active === 'timetable') return 'schedule';

      if (file.indexOf('profile') !== -1 || active === 'profile') return 'profile';

      return 'home';

    }

    return 'home';

  }



  function buildBottomNav(role, active) {

    const tabs = MOB_NAV_TABS[role] || MOB_NAV_TABS.student;

    const curTab = getRoleActiveTab(role, active);

    const itemsHtml = tabs.map(tab => {

      const isActive = tab.id === curTab;



      if (tab.isMore) {

        return `

          <button type="button" class="mob-bn-item" data-tab="more" data-action="toggle-more-sheet" aria-label="More teacher pages">

            <span class="mob-bn-icon-row">

              <span class="mob-bn-icon-wrap">

                <i class="${tab.icon}"></i>

              </span>

            </span>

          </button>`;

      }

      return `

        <a href="${_P}${tab.href}" class="mob-bn-item ${isActive ? 'is-active' : ''}" data-tab="${tab.id}" aria-label="${esc(tab.label)}"${isActive ? ' aria-current="page"' : ''}>

          <span class="mob-bn-icon-row">

            <span class="mob-bn-icon-wrap">

              <i class="${tab.icon}"></i>

              ${tab.hasDot ? `<span class="mob-bn-dot"></span>` : ''}

            </span>

          </span>

        </a>`;

    }).join("");



    return el(`

      <nav class="mob-bottomnav" id="mobBottomNav" role="navigation" aria-label="Mobile Navigation" data-purpose="bottom-navigation-bar">

        <div class="mob-bn-glow" aria-hidden="true"></div>

        <div class="mob-bn-shell">

          <div class="mob-bn-track">

            <div class="mob-bn-slider" id="mobBnSlider" aria-hidden="true"></div>

            <div class="mob-bn-inner">

              ${itemsHtml}

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



    // Default Melt/Liquid Dock (Admin, Teacher)

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

    const cfg  = resolveNav(portalRole);

    const user = PAGE.user || DEFAULT_USER[portalRole] || DEFAULT_USER.student;



    // Department-centric portals: keep "Departments" lit on its sub-pages.

    let active = PAGE.active;

    const ALIAS_MAP = {};

    if (ALIAS_MAP[active]) active = ALIAS_MAP[active];

    if (PAGE.role === "student" && DEPT_CHILD.includes(active)) {

      active = "departments";

    }



    document.body.setAttribute("data-role", portalRole);

    document.body.setAttribute("data-portal", portalRole);



    const main = document.querySelector(".main");

    if (!main) return;   // standalone pages (landing) have no app shell



    const shell = el(`<div class="shell"></div>`);

    main.parentNode.insertBefore(shell, main);



    const sidebar = buildSidebar(cfg, active, user);

    const scrim   = el(`<div class="scrim" id="scrim"></div>`);

    /* Sidebar is position:fixed — mount it on <body> so the mobile drawer stays

       reachable on pages that hide their desktop view (e.g. student dashboard). */

    document.body.appendChild(sidebar);

    shell.appendChild(main);

    document.body.appendChild(scrim);

    /* Tells the master sidebar CSS layer (app.css) that the engine owns the

       drawer; without it the static fallback keeps #sidebar visible. */

    document.body.classList.add("ngis-layout-ready");



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

          if (sidebar.classList.contains('collapsed')) {

            setSidebarCollapsed(false);

            setGroupExpanded(g, true);

            store.set(OPEN_GROUP_KEY, g.dataset.groupId || '');

            return;

          }

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



    /* ── Sidebar sub-accordion (nested collapsible sub-groups) ── */

    const collapsibleSubgroups = Array.from(sidebar.querySelectorAll('.nav-subgroup.collapsible'));

    if (collapsibleSubgroups.length) {

      collapsibleSubgroups.forEach(sg => {

        const hasActiveSub = sg.querySelector('.nav-link.active');

        if (hasActiveSub) {

          sg.classList.add('expanded');

          const btn = sg.querySelector('.nav-subgroup-label');

          if (btn) btn.setAttribute('aria-expanded', 'true');

        }



        const btn = sg.querySelector('.nav-subgroup-label');

        if (!btn) return;

        btn.addEventListener('click', (e) => {

          e.preventDefault();

          e.stopPropagation();

          const willOpen = !sg.classList.contains('expanded');

          sg.classList.toggle('expanded', willOpen);

          btn.setAttribute('aria-expanded', String(willOpen));

        });

      });

    }



    /* ── Sidebar 2nd-level nested sub-accordion (e.g. Academic Result) ── */

    const collapsibleNested = Array.from(sidebar.querySelectorAll('.nav-nested-group.collapsible'));

    if (collapsibleNested.length) {

      collapsibleNested.forEach(ng => {

        const hasActiveNested = ng.querySelector('.nav-link.active');

        if (hasActiveNested) {

          ng.classList.add('expanded');

          const btn = ng.querySelector('.nav-nested-label');

          if (btn) btn.setAttribute('aria-expanded', 'true');

        }



        const btn = ng.querySelector('.nav-nested-label');

        if (!btn) return;

        btn.addEventListener('click', (e) => {

          e.preventDefault();

          e.stopPropagation();

          const willOpen = !ng.classList.contains('expanded');

          ng.classList.toggle('expanded', willOpen);

          btn.setAttribute('aria-expanded', String(willOpen));

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



    // Docked Open/Collapse Toggle Button directly on sidebar boundary

    let expandBtn = sidebar.querySelector('#sidebarExpandBtn') || document.getElementById('sidebarExpandBtn');

    if (!expandBtn) {

      expandBtn = el(`

        <button class="sidebar-expand-btn" id="sidebarExpandBtn" title="Open navigation" aria-label="Open menu" data-action="toggle-sidebar" type="button">

          <svg class="side-expand-svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">

            <polyline points="9 18 15 12 9 6"></polyline>

          </svg>

        </button>`);

      sidebar.appendChild(expandBtn);

    } else if (expandBtn && expandBtn.parentElement !== sidebar) {

      sidebar.appendChild(expandBtn);

    }



    const COLLAPSED_KEY = 'ngis-' + (portalRole || PAGE.role || 'user') + '-sidebar-collapsed';

    /* Keep every toggle control's aria-expanded honest with what the user sees:

       on <=1024px the drawer state rules, on desktop the rail expanded state. */

    function isDrawerMode() { return window.innerWidth <= 1024; }

    function syncToggleAria() {

      const visible = isDrawerMode() ? sidebar.classList.contains('open') : !sidebar.classList.contains('collapsed');

      document.querySelectorAll("#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, .hamburger-btn, [data-action='toggle-sidebar']").forEach(btn => {

        if (btn.id === 'sidebarCollapseBtn' || btn.id === 'sidebarExpandBtn') return;

        btn.setAttribute("aria-expanded", String(visible));

      });

    }

    /* Single source of truth for the desktop rail state. Never toggles the

       mobile drawer — open/close of the drawer is owned by openNav/closeNav. */

    function setSidebarCollapsed(collapsed) {

      /* Desktop responsive view MUST always keep the sidebar fully open:
         refuse every collapse request while not in drawer mode so the rail
         never shrinks to the icon-only strip. Mobile drawer is unaffected. */

      if (collapsed && !isDrawerMode()) collapsed = false;

      const brandLogo = sidebar.querySelector('.side-brand-crest') || sidebar.querySelector('.side-brand-logo-img');

      if (collapsed) {

        sidebar.classList.add('collapsed');

        main.classList.add('sidebar-collapsed');

        document.body.classList.add('sidebar-collapsed');

        expandBtn.setAttribute('title', 'Expand sidebar');

        expandBtn.setAttribute('aria-label', 'Expand navigation');

        if (brandLogo && brandLogo.classList.contains('side-brand-logo-img')) {

          if (!brandLogo.dataset.origSrc) brandLogo.dataset.origSrc = brandLogo.src;

          brandLogo.src = _P + 'assets/images/moeys-sis-logo.png';

        }

        store.set(COLLAPSED_KEY, '1');

      } else {

        sidebar.classList.remove('collapsed');

        main.classList.remove('sidebar-collapsed');

        document.body.classList.remove('sidebar-collapsed');

        expandBtn.setAttribute('title', 'Collapse sidebar');

        expandBtn.setAttribute('aria-label', 'Collapse sidebar');

        if (brandLogo && brandLogo.classList.contains('side-brand-logo-img') && brandLogo.dataset.origSrc) {

          brandLogo.src = brandLogo.dataset.origSrc;

        }

        store.set(COLLAPSED_KEY, '0');

        setTimeout(() => scrollActiveItemIntoView(false), 160);

      }

      syncToggleAria();

    }

    // Restore persisted state or default to collapsed on admin as requested

    const savedCollapsed = store.get(COLLAPSED_KEY);

    if (savedCollapsed === '1' || (savedCollapsed === null && PAGE.role === 'admin')) {

      setSidebarCollapsed(true);

    } else {

      setSidebarCollapsed(false);

    }



    const sideBrand = sidebar.querySelector('.side-brand');

    if (sideBrand) {

      sideBrand.addEventListener('click', (e) => {

        if (sidebar.classList.contains('collapsed')) {

          e.preventDefault();

          e.stopPropagation();

          setSidebarCollapsed(false);

        }

      });

    }



    if (collapseBtn) {

      collapseBtn.addEventListener('click', (e) => {

        e.stopPropagation();

        setSidebarCollapsed(true);

      });

    }

    if (expandBtn) {

      expandBtn.addEventListener('click', (e) => {

        e.stopPropagation();

        const isCurrentlyCollapsed = sidebar.classList.contains('collapsed');

        setSidebarCollapsed(!isCurrentlyCollapsed);

      });

    }


    /* Desktop view: the sidebar is locked open, so hide the rail collapse /
       expand toggles entirely (there is no control to close it) and force it
       expanded. On drawer widths (<=1024px) restore them so CSS governs and the
       hamburger-driven drawer keeps working normally. */

    function syncRailLockUI() {

      const lockOpen = !isDrawerMode();

      const hide = (b) => { if (b) { if (lockOpen) b.style.setProperty('display', 'none', 'important'); else b.style.removeProperty('display'); } };

      hide(collapseBtn);

      hide(expandBtn);

      if (lockOpen && sidebar.classList.contains('collapsed')) setSidebarCollapsed(false);

    }

    syncRailLockUI();

    window.addEventListener('resize', syncRailLockUI);



    let bNav = document.getElementById("mobBottomNav");

    if (!bNav) {

      bNav = buildBottomNav(PAGE.role, active);

      document.body.appendChild(bNav);

    }



    const legacyNav = document.getElementById("bottomnav");

    if (legacyNav) legacyNav.remove();

    initBottomNav(bNav);



    // Ensure Phosphor icons are available for mobile navigation across all portals

    if (!document.querySelector('script[src*="@phosphor-icons/web"]')) {

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



    /* Theme: enforce light mode */

    store.set("ngis-theme", "light");

    applyTheme("light");



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



    /* Mobile/tablet drawer with smooth bottomnav disappearance.

       The rail (desktop) state and the drawer state are kept in sync through

       setSidebarCollapsed so nothing desyncs when the viewport crosses 1024px. */

    const openNav = () => {

      if (sidebar.classList.contains("collapsed")) {

        // Expand the rail too, so desktop layout/storage stay truthful.
        setSidebarCollapsed(false);

      }

      sidebar.classList.add("open");

      scrim.classList.add("show");

      document.body.classList.add("sidebar-open");

      const bNavEl = document.getElementById("mobBottomNav") || document.getElementById("bottomnav");

      if (bNavEl) bNavEl.classList.add("hidden-by-sidebar");

      syncToggleAria();

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

      // In drawer widths the rail class is inert; restore the persisted

      // desktop preference so widening the window lands back in the right state.

      if (isDrawerMode() && store.get(COLLAPSED_KEY) === '1') {

        sidebar.classList.add('collapsed');

      }

      syncToggleAria();

    };



    const toggleNav = () => {

      if (isDrawerMode()) {

        if (sidebar.classList.contains("open")) closeNav();

        else openNav();

      } else {

        if (sidebar.classList.contains("open")) closeNav();

        const isCollapsed = sidebar.classList.contains("collapsed");

        setSidebarCollapsed(!isCollapsed);

      }

      syncToggleAria();

    };



    // Crossing the drawer/desktop boundary must never leave stale states behind.

    const drawerMQ = window.matchMedia("(max-width: 1024px)");

    const onBreakpointCross = () => {

      // Drop any drawer state first, then restore the desktop rail preference.

      sidebar.classList.remove("open");

      scrim.classList.remove("show");

      document.body.classList.remove("sidebar-open");

      const bNavEl = document.getElementById("mobBottomNav") || document.getElementById("bottomnav");

      if (bNavEl) bNavEl.classList.remove("hidden-by-sidebar");

      if (!isDrawerMode()) {

        setSidebarCollapsed(store.get(COLLAPSED_KEY) === '1');

      }

      syncRailLockUI();

      syncToggleAria();

    };

    if (typeof drawerMQ.addEventListener === "function") drawerMQ.addEventListener("change", onBreakpointCross);

    else if (typeof drawerMQ.addListener === "function") drawerMQ.addListener(onBreakpointCross);



    window.openSidebar = openNav;

    window.closeSidebar = closeNav;

    window.toggleSidebar = toggleNav;



    const wireButtons = () => {

      let existing = document.querySelector("#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, .hamburger-btn, [data-action='toggle-sidebar']");

      const target = document.querySelector(".htb-left, .hero-topbar, .topbar, .header, header, .lh-inner, .dir-header-inner");

      if (!existing && target) {

        const hb = el(`

          <button type="button" class="htb-hamburger hamburger-btn mobile-hamburger-btn icon-btn" id="htbHamburger" data-action="toggle-sidebar" aria-label="Open menu" aria-expanded="false" title="Open navigation">

            <i class="ph ph-list text-xl"></i>

            <span class="material-symbols-outlined" style="display:none">menu</span>

          </button>

        `);

        if (target.classList.contains("htb-left")) {

          target.insertBefore(hb, target.firstChild);

        } else {

          target.prepend(hb);

        }

        existing = hb;

      }

      document.querySelectorAll("#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, .hamburger-btn, [data-action='toggle-sidebar']").forEach(btn => {

        if (btn.id === 'sidebarCollapseBtn' || btn.id === 'sidebarExpandBtn') return;

        // Always ensure hamburger button is placed to the far left of its parent container

        if (btn.parentElement && btn.parentElement.firstElementChild !== btn) {

          btn.parentElement.insertBefore(btn, btn.parentElement.firstElementChild);

        }

        if (btn.id === 'sidebarCollapseBtn' || btn.id === 'sidebarExpandBtn') return;

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

      if (btn.id === 'sidebarCollapseBtn' || btn.id === 'sidebarExpandBtn') return;

      if (e.__sidebarHandled) return;

      e.__sidebarHandled = true;

      e.preventDefault();

      e.stopPropagation();

      e.stopImmediatePropagation();

      toggleNav();

    });



    const closeBtn = sidebar.querySelector('#sidebarCloseBtn');

    if (closeBtn) {

      closeBtn.addEventListener('click', (e) => {

        e.stopPropagation();

        closeNav();

      });

    }



    // Touch swipe left to close drawer

    let touchStartX = 0;

    sidebar.addEventListener('touchstart', (e) => {

      touchStartX = e.touches[0].clientX;

    }, { passive: true });

    sidebar.addEventListener('touchend', (e) => {

      const touchEndX = e.changedTouches[0].clientX;

      if (touchStartX - touchEndX > 50) {

        closeNav();

      }

    }, { passive: true });



    scrim.addEventListener("click", closeNav);

    sidebar.querySelectorAll(".nav-link").forEach(a => a.addEventListener("click", closeNav));

    document.addEventListener("keydown", e => { if (e.key === "Escape") closeNav(); });



    // Universal Drawer & Modal delegation

    document.addEventListener("click", (e) => {

      const openDrawer = e.target.closest("[data-open-drawer]");

      if (openDrawer) {

        e.preventDefault();

        const id = openDrawer.getAttribute("data-open-drawer");

        const drawer = document.querySelector(`.drawer-overlay[data-drawer="${id}"], .drawer-overlay#${id}, #${id}.drawer-overlay, #${id}`);

        if (drawer) {

          drawer.classList.add("show", "open");

          const inner = drawer.querySelector(".drawer");

          if (inner) inner.classList.add("show", "open");

        }

        return;

      }

      const closeDrawer = e.target.closest("[data-close-drawer]");

      if (closeDrawer) {

        e.preventDefault();

        const drawer = closeDrawer.closest(".drawer-overlay, aside.drawer");

        if (drawer) {

          drawer.classList.remove("show", "open");

          if (drawer.parentElement && drawer.parentElement.classList.contains("drawer-overlay")) {

            drawer.parentElement.classList.remove("show", "open");

          }

        }

        return;

      }

      const openModal = e.target.closest("[data-open-modal]");

      if (openModal) {

        e.preventDefault();

        const id = openModal.getAttribute("data-open-modal");

        const modal = document.querySelector(`.modal-overlay[data-modal="${id}"], .modal-overlay#${id}, #${id}.modal-overlay, #${id}`);

        if (modal) modal.classList.add("show", "open");

        return;

      }

      const closeModal = e.target.closest("[data-close-modal], [data-dismiss='modal']");

      if (closeModal) {

        e.preventDefault();

        const modal = closeModal.closest(".modal-overlay, .modal");

        if (modal) modal.classList.remove("show", "open");

        return;

      }

    });



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

      // Keep the layout companions truthful if the rail class is changed externally.

      const isCollapsed = sidebar.classList.contains("collapsed");

      main.classList.toggle("sidebar-collapsed", isCollapsed);

      document.body.classList.toggle("sidebar-collapsed", isCollapsed);

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



    /* UI States & Master Components Engine (Rules 1-5 Reusable Standards) */
    if (!document.querySelector('link[href*="ui-states.css"]')) {
      const lu = document.createElement("link");
      lu.rel = "stylesheet";
      lu.href = _P + "assets/css/ui-states.css";
      document.head.appendChild(lu);
    }

    const sharedComponents = [
      "assets/js/error-messages.js",
      "assets/js/error-boundary.js",
      "assets/components/skeleton.js",
      "assets/components/error-state.js",
      "assets/components/empty-state.js",
      "assets/components/primary-button.js",
      "assets/components/cancel-dialog.js",
      "assets/components/onboarding-layout.js",
      "assets/js/ui-states.js",
      "assets/js/action-icons.js"
    ];

    sharedComponents.forEach(scriptPath => {
      const scriptTag = document.createElement("script");
      scriptTag.src = _P + scriptPath;
      scriptTag.defer = true;
      document.body.appendChild(scriptTag);
    });
  }

  window.toast = function(msg, kind, detail, options) {

    kind = kind || "info";

    if (window.NGISUI && window.NGISUI.toast) {

      const fn = window.NGISUI.toast[kind] || window.NGISUI.toast.info;

      return fn.call(window.NGISUI.toast, msg, detail || "", options || {});

    }

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



  /* Boot: wait briefly for the published navigation so the sidebar paints
     from the managed configuration when one exists. If the request is slow
     or unavailable we mount immediately with the cached / built-in NAV. */
  function boot() {
    Promise.race([
      navReadyPromise,
      new Promise((resolve) => setTimeout(resolve, 1200)),
    ]).then(mount);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);

  else boot();

})();

