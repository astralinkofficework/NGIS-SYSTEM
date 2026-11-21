/* ============================================================

   NGIS Layout Engine v3.0 — New Gateway International School

   Reads window.PAGE = { role, active, user } and renders the

   shared sidebar, topbar, mobile bottom-nav and breadcrumbs,

   then wires interactions. No build step — runs as plain files.

   ============================================================ */

(function () {

  "use strict";

  /* ── Shared Bootstrap-icon engine loader (idempotent) ──────────
     The sidebar renders icons as data-ngis-icon slots with their
     Material/Phosphor ligature as text fallback. This ensures the
     official icon engine (action-icons.js, Bootstrap Icons SVGs) is
     present to hydrate them — even on pages that forgot to include
     it — without duplicating script tags when it already is. */
  try {
    if (!window.__NGIS_ICON_ENGINE__) {
      window.__NGIS_ICON_ENGINE__ = true;
      if (!(window.NGIS && window.NGIS.icon) && !document.querySelector('script[src*="action-icons.js"]')) {
        const _root = (window.location.pathname || "").indexOf("/pages/") !== -1 ? "../../" : "";
        if (!document.querySelector('link[href*="action-icons.css"]')) {
          const _l = document.createElement("link");
          _l.rel = "stylesheet";
          _l.href = _root + "assets/css/action-icons.css?v=1.13.2";
          document.head.appendChild(_l);
        }
        const _s = document.createElement("script");
        _s.src = _root + "assets/js/action-icons.js?v=1.13.2";
        _s.defer = true;
        document.head.appendChild(_s);
      }
    }
  } catch (e) { /* icons fall back to ligature glyphs */ }

  /* Remembers which sidebar link the user clicked so the sidebar stays anchored
     to that exact section after navigation (matters when one page is reachable
     from more than one nav group). */
  const CLICKED_NAV_KEY = "ngis-sidebar-active-id";



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

        { id:"users-grp", label:"USER & ACCESS MANAGEMENT", icon:"group", links:[

          {
            id: "users-directories-drop",
            label: "Account Directories",
            icon: "group",
            collapsible: true,
            children: [
              { id: "users-students", label: "Student Accounts", href: "pages/admin/admin-users-students.html" },
              { id: "users-teachers", label: "Teacher Accounts", href: "pages/admin/admin-users-teachers.html" },
              { id: "users-staff", label: "Staff Accounts", href: "pages/admin/admin-users-staff.html" },
              { id: "users-principals", label: "Principal Accounts", href: "pages/admin/admin-users-principals.html" },
              { id: "users-admins", label: "Admin Accounts", href: "pages/admin/admin-users-admins.html" },
            ]
          },

          { id: "roles-permissions", label: "Roles & Access Control", icon: "admin_panel_settings", href: "pages/admin/admin-roles-permissions.html" },

          {
            id: "teachers-mgmt-drop",
            label: "Teachers Management",
            icon: "co_present",
            collapsible: true,
            children: [
              { id: "teacher-profiles", label: "Teacher Profile", href: "pages/admin/admin-teacher-profiles.html" },
              { id: "teacher-class-assignment", label: "Teacher-Class Assignment", href: "pages/admin/admin-teacher-class-assignment.html" },
              { id: "verify-teacher", label: "Verify Teacher Update", href: "pages/admin/admin-teacher-verify.html" },
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
              { id: "input-attendance", label: "Input Attendance", href: "pages/admin/admin-attendance.html" },
              { id: "absence-stats", label: "Absence Statistics", href: "pages/admin/admin-absence-stats.html" },
            ]
          },

        ]},

        { id:"khmer-suite", label:"CURRICULUM", icon:"menu_book", links:[

          { id:"ks-subjects", label:"Curriculum Subjects", icon:"menu_book", href:"pages/admin/admin-subjects.html" }

        ]},

        { id:"academic", label:"ACADEMIC STRUCTURE", icon:"apartment", links:[

          { id:"departments", label:"Departments", icon:"apartment",          href:"pages/admin/admin-departments.html" },

          { id:"campuses",    label:"Campuses",    icon:"location_city",      href:"pages/admin/admin-campuses.html" },

          { id:"classes",     label:"Classes",     icon:"school",             href:"pages/admin/admin-classes.html" },

          { id:"timetables",  label:"Timetables",  icon:"calendar_view_week", href:"pages/admin/admin-timetables.html" },

        ]},

        { id:"records", label:"INSTITUTIONAL RECORDS", icon:"folder_shared", links:[

          { id:"services", label:"Student Services", icon:"assignment", href:"pages/admin/admin-services.html" },

          { id:"lost-found", label:"Lost & Found", icon:"inventory_2", href:"pages/admin/admin-lost-found.html" },

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
              { id: "sys-schedule", label: "Schedule", href: "pages/admin/admin-system-schedule.html" },
              { id: "sys-general-setting", label: "General Setting", href: "pages/admin/admin-system-general-setting.html" },
            ]
          },

          {
            id: "sys-year-config-drop",
            label: "School Year Configuration",
            icon: "calendar_today",
            collapsible: true,
            children: [
              { id: "sys-school-year", label: "School Year", href: "pages/admin/admin-system-school-year.html" },
              { id: "sys-school-week", label: "School Week", href: "pages/admin/admin-system-school-week.html" },
              { id: "sys-exam-config", label: "School Exam Configuration", href: "pages/admin/admin-system-exam-config.html" }
            ]
          },

          { id:"logs",     label:"Audit Logs",      icon:"history",  href:"pages/admin/admin-logs.html" },

          { id:"security", label:"Security Center", icon:"security", href:"pages/admin/admin-security.html" },

          { id:"settings", label:"System Settings", icon:"settings", href:"pages/admin/admin-settings.html" },

        ]},

        { id:"account-grp", label:"ACCOUNT", icon:"person", links:[

          { id:"profile", label:"Admin Profile", icon:"person", href:"pages/admin/admin-settings.html" },

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

          { id:"attendance", label:"Daily Attendance", icon:"how_to_reg", href:"pages/teacher/teacher-attendance.html" },

          { id:"roster",     label:"Roster & Profiles",          icon:"badge",          href:"pages/teacher/teacher-roster.html" },

          { id:"lessons",    label:"Lessons & Materials",        icon:"menu_book",      href:"pages/teacher/teacher-lessons.html" },

          { id:"departments",label:"Department",                 icon:"apartment",      href:"pages/teacher/teacher-departments.html" },

          { id:"calendar",   label:"Timetable",                  icon:"calendar_month", href:"pages/teacher/teacher-calendar.html" },

        ]},

        { id:"assessment", label:"ASSESSMENT", icon:"grading", links:[

          { id:"gradebook",   label:"Gradebook & Marks",          icon:"fact_check",     href:"pages/teacher/teacher-gradebook.html" },

          { id:"submissions", label:"Assignments & Student Work", icon:"description",  href:"pages/teacher/teacher-submissions.html" },

          { id:"reports",     label:"Official Academic Reports",  icon:"assessment",   href:"pages/teacher/teacher-reports.html" },

        ]},

        { id:"communication", label:"COMMUNICATION", icon:"campaign", links:[

          /* Shared announcements page — one backend, one reader experience for
             every portal. The ?portal hint only selects the UI context; the
             authenticated session (and the backend) still own permissions. */
          { id:"announcements", label:"Announcements", icon:"campaign", href:"pages/shared/announcements.html?portal=teacher" },

        ]},

        { id:"campus-services", label:"CAMPUS & SERVICES", icon:"local_activity", links:[

          { id:"services",       label:"Faculty Services Hub",      icon:"grid_view",     href:"pages/teacher/teacher-services.html" },

          { id:"lost-found",     label:"Lost & Found",              icon:"inventory_2",   href:"pages/teacher/teacher-lost-found.html" },

        ]},

        { id:"account-grp", label:"ACCOUNT", icon:"person", links:[

          { id:"profile",       label:"Settings & Profile",       icon:"settings",      href:"pages/teacher/teacher-profile.html" },

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

          { id:"calendar", label:"Academic Calendar", icon:"calendar", href:"pages/student/student-calendar.html" },

          { id:"timetable", label:"Class Timetable", icon:"calendar_view_week", href:"pages/student/student-timetable.html" },

          {
            id: "departments-drop",
            label: "Academic Departments",
            icon: "apartment",
            collapsible: true,
            children: [
              { id: "departments", label: "All Departments", icon: "grid_view", href: "pages/shared/departments.html?portal=student" },
              { id: "dept-khmer", label: "Khmer Studies", icon: "translate", href: "pages/shared/department.html?id=khmer&portal=student" },
              { id: "dept-english", label: "English Language", icon: "menu_book", href: "pages/shared/department.html?id=english&portal=student" },
              { id: "dept-chinese", label: "Chinese Language", icon: "public", href: "pages/shared/department.html?id=chinese&portal=student" },
              { id: "dept-math", label: "Mathematics", icon: "calculate", href: "pages/shared/department.html?id=math&portal=student" },
              { id: "dept-science", label: "Science & STEM", icon: "science", href: "pages/shared/department.html?id=science&portal=student" },
              { id: "dept-social", label: "Social Studies", icon: "history_edu", href: "pages/shared/department.html?id=social&portal=student" }
            ]
          },

        ]},

        { id:"campus-life", label:"CAMPUS LIFE", icon:"local_activity", links:[

          { id:"services",   label:"Services Hub",       icon:"grid_view", href:"pages/student/student-services.html" },

          { id:"lost-found", label:"Lost & Found",       icon:"inventory_2", href:"pages/student/student-lost-found.html" },

        ]},

        { id:"communication", label:"COMMUNICATION", icon:"campaign", links:[

          /* Shared announcements page (see teacher note above): students read
             the same school-wide feed; publishing controls stay admin-only. */
          { id:"announcements", label:"Announcements", icon:"campaign", href:"pages/shared/announcements.html?portal=student" },

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
          { id: "classes", label: "Classes & Cohorts", icon: "class", href: "pages/principal/principal-classes.html" },
          {
            id: "departments-drop",
            label: "Academic Departments",
            icon: "apartment",
            collapsible: true,
            children: [
              { id: "departments", label: "All Departments", icon: "grid_view", href: "pages/principal/principal-departments.html" },
              { id: "pdept-khm", label: "Khmer Studies", icon: "translate", href: "pages/principal/principal-departments.html?dept=dept-khm" },
              { id: "pdept-eng", label: "English Dept", icon: "menu_book", href: "pages/principal/principal-departments.html?dept=dept-eng" },
              { id: "pdept-chn", label: "Chinese Language", icon: "public", href: "pages/principal/principal-departments.html?dept=dept-chn" },
              { id: "pdept-mat", label: "Mathematics", icon: "calculate", href: "pages/principal/principal-departments.html?dept=dept-mat" },
              { id: "pdept-sci", label: "Science Wing", icon: "science", href: "pages/principal/principal-departments.html?dept=dept-sci" },
              { id: "pdept-hum", label: "Humanities", icon: "history_edu", href: "pages/principal/principal-departments.html?dept=dept-hum" }
            ]
          },
          { id: "reports", label: "Student Results & Reports", icon: "assessment", href: "pages/principal/principal-reports.html" },
        ]},
        { id:"khmer-suite", label:"TIMETABLE MANAGEMENT", icon:"calendar_view_week", links:[

          { id:"ks-wizard", label:"Teacher Assignment", icon:"swap_horiz", href:"pages/principal/principal-teacher-class-assignment.html" },
          { id:"ks-builder", label:"Timetable Builder", icon:"grid_view", href:"pages/principal/principal-timetable-builder.html" },
          { id:"ks-subjects", label:"Curriculum Subjects", icon:"menu_book", href:"pages/principal/principal-subjects.html" }
        ]},
        { id: "students-mgmt", label: "STUDENT MANAGEMENT", icon: "group", links: [
          { id: "student-profiles", label: "Student Profile", icon: "school", href: "pages/principal/principal-student-profiles.html" },
        ]},
        { id: "approvals-grp", label: "DECISIONS & NOTICES", icon: "verified", links: [
          { id: "principal-school-information", label: "School Information", icon: "account_balance", href: "pages/principal/principal-school-information.html" },
          { id: "services", label: "Services Hub", icon: "grid_view", href: "pages/principal/principal-services.html" },
          { id: "announcements", label: "School Announcements", icon: "campaign", href: "pages/shared/announcements.html?portal=principal" },
          { id: "activity", label: "Change History", icon: "history", href: "pages/principal/principal-activity.html" },
        ]},
        { id: "account-grp", label: "ACCOUNT", icon: "person", links: [
          { id: "profile", label: "Settings & Profile", icon: "settings", href: "pages/principal/principal-profile.html" },
        ]},
      ],
    },

    superadmin: {
      brand: "Super Admin", meta: "Root System Suite · 2025–26",
      groups: [
        { label: "Overview", links: [
          { id: "sa-dashboard", label: "System Overview", icon: "dashboard", href: "pages/admin/admin.html", locked: true }
        ]},
        { id: "sa-cms-grp", label: "CONTENT & NAVIGATION", icon: "tune", links: [
          { id: "sa-sidebar-mgr", label: "Global Sidebar Manager", icon: "menu_open", href: "pages/admin/admin-dashboard-content.html" },
          { id: "sa-hero-banners", label: "Hero & Banners CMS", icon: "view_carousel", href: "pages/admin/admin-dashboard-content.html#tabHero" }
        ]},
        { id: "sa-users-grp", label: "IDENTITY & ACCESS", icon: "manage_accounts", links: [
          { id: "sa-users-reg", label: "Central Registry", icon: "dashboard", href: "pages/admin/admin-users-students.html" },
          { id: "sa-directories-drop", label: "User Directories", icon: "group", collapsible: true, children: [
            { id: "sa-students", label: "Student Accounts", href: "pages/admin/admin-users-students.html" },
            { id: "sa-teachers", label: "Teacher Accounts", href: "pages/admin/admin-users-teachers.html" },
            { id: "sa-staff", label: "Staff Accounts", href: "pages/admin/admin-users-staff.html" },
            { id: "sa-principals", label: "Principal Accounts", href: "pages/admin/admin-users-principals.html" },
            { id: "sa-admins", label: "Admin Accounts", href: "pages/admin/admin-users-admins.html" }
          ]}
        ]},
        { id: "sa-academics-grp", label: "ACADEMIC ARCHITECTURE", icon: "school", links: [
          { id: "sa-teacher-assign", label: "Teacher Class Assignment", icon: "co_present", href: "pages/admin/admin-teacher-class-assignment.html" }
        ]},
        { id: "sa-comm-grp", label: "COMMUNICATION", icon: "campaign", links: [
          { id: "announcements", label: "School Announcements", icon: "campaign", href: "pages/shared/announcements.html?portal=superadmin" }
        ]},
        { id: "sa-infra-grp", label: "INSTITUTIONAL SUITE", icon: "business", links: [
          { id: "sa-campuses", label: "Campus Infrastructure", icon: "location_city", href: "pages/admin/admin-campuses.html" },
          { id: "sa-departments", label: "Departments", icon: "domain", href: "pages/admin/admin-departments.html" },
          { id: "sa-dictionary", label: "Data Dictionary", icon: "menu_book", href: "pages/admin/admin-data-dictionary.html" },
          { id: "sa-school-info", label: "School Information", icon: "account_balance", href: "pages/admin/admin-school-information.html" }
        ]},
        { id: "sa-sec-grp", label: "GOVERNANCE & SECURITY", icon: "security", links: [
          { id: "sa-audit-logs", label: "Audit Logs", icon: "history", href: "pages/admin/admin-logs.html" },
          { id: "sa-security", label: "Security Center", icon: "security", href: "pages/admin/admin-security.html" },
          { id: "sa-settings", label: "System General Settings", icon: "settings", href: "pages/admin/admin-system-general-setting.html" }
        ]},
        { id: "account-grp", label: "ACCOUNT", icon: "person", links: [
          { id: "sa-profile", label: "Admin Profile", icon: "manage_accounts", href: "pages/admin/admin-settings.html" },
        ]}
      ]
    },

    staff: {
      brand: "Staff", meta: "Campus Operations Hub · 2025–26",
      groups: [
        { label: "Overview", links: [
          { id: "staff-services", label: "Campus Services Hub", icon: "grid_view", href: "pages/admin/admin-services.html", locked: true }
        ]},
        { id: "staff-ops-grp", label: "CAMPUS OPERATIONS", icon: "business_center", links: [
          { id: "staff-lost-found", label: "Lost & Found Registry", icon: "inventory_2", href: "pages/principal/principal-lost-found.html" },
          { id: "staff-campuses", label: "Campus Directory", icon: "location_city", href: "pages/admin/admin-campuses.html" },
          { id: "staff-school-info", label: "School Information", icon: "account_balance", href: "pages/admin/admin-school-information.html" }
        ]},
        { id: "staff-comm-grp", label: "COMMUNICATION", icon: "campaign", links: [
          { id: "staff-announcements", label: "Announcements", icon: "campaign", href: "pages/shared/announcements.html?portal=staff" },
          { id: "staff-news", label: "Institutional News", icon: "newspaper", href: "pages/shared/news.html?portal=staff" }
        ]},
        { id: "account-grp", label: "ACCOUNT", icon: "person", links: [
          { id: "staff-profile", label: "Staff Profile & Settings", icon: "settings", href: "pages/admin/admin-settings.html" },
        ]}
      ]
    },
  };



  /* ── Published navigation override (Global Sidebar Manager) ──

     The built-in NAV above is the safe default. When the backend has a
     published navigation configuration for a portal (managed from
     admin-dashboard-content.html → Sidebar Manager), it takes precedence.

     The backend JSON store is the single source of truth; sessionStorage is
     only a render-fast cache so the sidebar paints without a flash. */

  let NAV_OVERRIDE = null;

  const NAV_CACHE_KEY = 'ngis-nav-published-v5';

  function sanitizeNavTree(data) {
    if (!data || typeof data !== 'object') return data;
    const cleanGroups = (groups) => {
      if (!Array.isArray(groups)) return groups;
      return groups.map(g => {
        if (!g || !Array.isArray(g.links)) return g;
        const links = g.links.filter(l => {
          if (!l) return false;
          if (l.id === 'sys-account-mgmt-drop' || l.label === 'Account Management') return false;
          return true;
        }).map(l => {
          if (l && Array.isArray(l.children)) {
            l.children = l.children.filter(c =>
              c &&
              c.id !== 'sys-account-mgmt-drop' &&
              c.label !== 'Account Management' &&
              c.id !== 'sys-employee-group' &&
              c.id !== 'sys-employee-accounts' &&
              c.id !== 'sys-student-accounts' &&
              c.id !== 'sys-parent-accounts'
            );
          }
          return l;
        });
        return Object.assign({}, g, { links });
      });
    };

    if (Array.isArray(data.groups)) {
      return Object.assign({}, data, { groups: cleanGroups(data.groups) });
    }
    const res = {};
    for (const k of Object.keys(data)) {
      const portal = data[k];
      if (portal && Array.isArray(portal.groups)) {
        res[k] = Object.assign({}, portal, { groups: cleanGroups(portal.groups) });
      } else {
        res[k] = portal;
      }
    }
    return res;
  }

  try {
    sessionStorage.removeItem('ngis-nav-published');
    sessionStorage.removeItem('ngis-published-nav-cache');
    const cached = sessionStorage.getItem(NAV_CACHE_KEY);
    if (cached) NAV_OVERRIDE = sanitizeNavTree(JSON.parse(cached));
  } catch (e) { /* ignore malformed cache */ }

  const navReadyPromise = fetch('/api/nav/published')
    .then((r) => (r && r.ok ? r.json() : null))
    .then((res) => {
      if (res && res.success && res.data && typeof res.data === 'object') {
        NAV_OVERRIDE = sanitizeNavTree(res.data);
        try { sessionStorage.setItem(NAV_CACHE_KEY, JSON.stringify(NAV_OVERRIDE)); } catch (e) {}
      }
    })
    .catch(() => { /* keep cache / built-in NAV */ });



  function resolveNav(portalRole) {
    const source = NAV_OVERRIDE || NAV;
    let targetRole = portalRole;
    if (targetRole === 'super_admin') targetRole = 'superadmin';
    const cfg = source[targetRole] || source[portalRole];

    // Guard against an empty/partial published config for this portal.
    if (cfg && Array.isArray(cfg.groups) && cfg.groups.length) return cfg;

    return NAV[portalRole] || NAV[targetRole] || NAV.admin || NAV.student;
  }

  /* Department sub-pages keep "Departments" highlighted in the sidebar,

     since these modules now live inside each department. */

  const DEPT_CHILD = ["attendance","assignments","grades","exams","timetable","lessons","department"];



  /* Mobile bottom-nav: primary destinations per role */

  const BOTTOM = {

    admin: [

      { id:"dashboard",  label:"Home",       icon:"home",      href:"pages/admin/admin.html" },

      { id:"users",      label:"Users",       icon:"group",     href:"pages/admin/admin-users-students.html" },

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

      { id:"profile",      label:"Profile",     icon:"person",         href:"pages/student/student-profile.html" },

    ],

    principal: [

      { id:"dashboard",  label:"Home",       icon:"home",           href:"pages/principal/principal.html" },

      { id:"classes",    label:"Classes",    icon:"class",          href:"pages/principal/principal-classes.html" },

      { id:"students",   label:"Students",   icon:"school",         href:"pages/principal/principal-student-profiles.html" },

      { id:"reports",    label:"Reports",    icon:"assessment",     href:"pages/principal/principal-reports.html" },

      { id:"profile",    label:"Profile",    icon:"person",         href:"pages/principal/principal-profile.html" },

    ],

    superadmin: [

      { id:"dashboard",  label:"Home",       icon:"home",           href:"pages/admin/admin.html" },

      { id:"users",      label:"Users",      icon:"group",          href:"pages/admin/admin-users-students.html" },

      { id:"reports",    label:"CMS",        icon:"tune",           href:"pages/admin/admin-dashboard-content.html" },

      { id:"settings",   label:"Settings",   icon:"settings",       href:"pages/admin/admin-settings.html" },

    ],

    staff: [

      { id:"services",   label:"Services",   icon:"grid_view",      href:"pages/admin/admin-services.html" },

      { id:"lost-found", label:"Lost&Found", icon:"inventory_2",    href:"pages/principal/principal-lost-found.html" },

      { id:"campuses",   label:"Campuses",   icon:"location_city",  href:"pages/admin/admin-campuses.html" },

      { id:"settings",   label:"Account",    icon:"settings",       href:"pages/admin/admin-settings.html" },

    ],

  };



  



  const DEFAULT_USER = {

    admin:      { name:"Sok Panha Heng",  role:"School Administrator",    initials:"SH" },

    superadmin: { name:"Sok Panha Heng",  role:"Super Administrator",     initials:"SH" },

    staff:      { name:"Chanthou Meas",   role:"Campus Operations Staff", initials:"CM" },

    teacher:    { name:"Dr. Sarah Jenkins", role:"Head of Senior Faculty", initials:"SJ" },

    student:    { name:"Nrinphouneta Hok", role:"Student · Grade 11-A",    initials:"NH" },

    principal:  { name:"Dr. Ly Bunheng",  role:"Campus Principal",        initials:"LB" },

  };



  const PORTAL_HOME = {

    admin: "pages/admin/admin.html",

    superadmin: "pages/admin/admin.html?portal=superadmin",

    staff: "pages/admin/admin-services.html?portal=staff",

    teacher: "pages/teacher/teacher.html",

    student: "pages/student/student.html",

    principal: "pages/principal/principal.html"

  };



  /* Resolve the portal from the authenticated session and scoped URL. */

  const VALID_PORTALS = ["admin", "superadmin", "principal", "teacher", "student", "staff"];

  const STAFF_ALLOWED_FILES = [
    "admin-services.html",
    "admin-lost-found.html",
    "principal-lost-found.html",
    "admin-campuses.html",
    "admin-school-information.html",
    "admin-settings.html"
  ];

  const PRINCIPAL_ADMIN_SHARED_FILES = [
    "admin-school-information.html",
    "admin-dashboard-content.html",
    "admin-timetables.html"
  ];

  function readStoredUser(key) {

    try { return JSON.parse(localStorage.getItem(key) || "null"); } catch (e) { return null; }

  }

  function normalizeRole(role) {

    if (!role) return "student";

    role = String(role).trim().toLowerCase();

    if (role === "super_admin" || role === "superadmin") return "superadmin";

    if (role === "editor") return "admin";

    return role;

  }

  function hasExplicitAuthSession() {

    if (window.NGISAuth && typeof window.NGISAuth.hasExplicitSession === "function") {

      return window.NGISAuth.hasExplicitSession();

    }

    try {

      if (localStorage.getItem("ngis_session_mode") === "passive") return false;

      const u = readStoredUser("ngis_user");

      return Boolean(u && u.role);

    } catch (e) { return false; }

  }

  function getSessionRole() {

    const authRole = window.NGISAuth && typeof window.NGISAuth.getRole === "function" ? window.NGISAuth.getRole() : null;

    const user = readStoredUser("ngis_user");

    return normalizeRole(authRole || (user && (user.portal || user.role)));

  }

  function canPortalServeCurrentPath(candidatePortal, pathSeg, curFile) {

    if (!VALID_PORTALS.includes(candidatePortal)) return false;

    if (!pathSeg || pathSeg === "shared") return true;

    if (candidatePortal === "staff") return STAFF_ALLOWED_FILES.includes(curFile);

    if (candidatePortal === "superadmin" || candidatePortal === "admin") {

      return pathSeg === "admin" || pathSeg === "principal";

    }

    if (candidatePortal === "principal") {

      return pathSeg === "principal" || PRINCIPAL_ADMIN_SHARED_FILES.includes(curFile);

    }

    return pathSeg === candidatePortal;

  }

  /* Sidebar System v2 — portal identity guard.
     A portal that owns a directory (/pages/admin, /pages/principal,
     /pages/teacher, /pages/student) always keeps its own sidebar. Only the two
     preview roles, which have no directory of their own, may render on top of
     another portal's page, and only where their published nav actually links:
       superadmin -> /pages/admin/*
       staff      -> /pages/admin/<STAFF_ALLOWED_FILES> + principal-lost-found.html
     Shared pages have no owner and keep the existing query/session resolution.
     Without this guard, ?portal=admin or a sticky preference could show the
     Admin sidebar (49 links) on a Principal Portal page. */
  function directoryOwnedRole(pathSeg) {

    if (!pathSeg || pathSeg === "shared" || pathSeg === "parent") return "";

    const r = normalizeRole(pathSeg);

    return ["admin", "principal", "teacher", "student"].includes(r) ? r : "";

  }

  function canOverrideDirectoryRole(candidate, pathSeg, curFile, dirRole) {

    if (!candidate || !VALID_PORTALS.includes(candidate)) return false;

    if (!dirRole) return true;

    if (candidate === dirRole) return true;

    if (candidate === "superadmin") return pathSeg === "admin";

    if (candidate === "staff") {
      return (pathSeg === "admin" && STAFF_ALLOWED_FILES.includes(curFile)) ||
        curFile === "principal-lost-found.html";
    }

    return false;

  }

  function resolvePortalRole(pageRole) {

    const path = (window.location.pathname || "").replace(/\\/g, "/").toLowerCase();

    const match = path.match(/\/pages\/(admin|teacher|student|parent|principal|shared)\//);

    const pathSeg = match ? match[1] : null;

    const curFile = (path.split("/").pop() || "").toLowerCase();

    const dirRole = directoryOwnedRole(pathSeg);

    const params = new URLSearchParams(window.location.search || "");

    const rawQuery = params.get("portal") || params.get("role") || "";

    const queryRole = rawQuery ? normalizeRole(rawQuery) : "";

    const explicitSession = hasExplicitAuthSession();

    const sessionRole = explicitSession ? getSessionRole() : null;

    let storedPortal = "";

    try { storedPortal = localStorage.getItem("ngis_active_portal") || ""; } catch (e) {}

    if (storedPortal) storedPortal = normalizeRole(storedPortal);

    // Priority 1: Explicit authenticated session locks role cleanly (admins/superadmins may still preview compatible portals via ?portal=)

    if (explicitSession && sessionRole && VALID_PORTALS.includes(sessionRole)) {

      if (queryRole && VALID_PORTALS.includes(queryRole) && canPortalServeCurrentPath(queryRole, pathSeg, curFile) &&
          canOverrideDirectoryRole(queryRole, pathSeg, curFile, dirRole)) {

        if (queryRole === sessionRole || sessionRole === "superadmin" || (sessionRole === "admin" && queryRole !== "student")) {

          try { localStorage.setItem("ngis_active_portal", queryRole); } catch (e) {}

          return queryRole;

        }

      }

      if (canPortalServeCurrentPath(sessionRole, pathSeg, curFile) &&
          canOverrideDirectoryRole(sessionRole, pathSeg, curFile, dirRole)) {

        try { localStorage.setItem("ngis_active_portal", sessionRole); } catch (e) {}

        return sessionRole;

      }

    }

    // Priority 2: Explicit ?portal= or ?role= query param when structurally valid for this page

    if (queryRole && canPortalServeCurrentPath(queryRole, pathSeg, curFile) &&
        canOverrideDirectoryRole(queryRole, pathSeg, curFile, dirRole)) {

      try { localStorage.setItem("ngis_active_portal", queryRole); } catch (e) {}

      return queryRole;

    }

    // Priority 3: Sticky multi-portal contexts (staff / superadmin) across permitted admin/principal/shared pages

    if ((storedPortal === "staff" || storedPortal === "superadmin") && canPortalServeCurrentPath(storedPortal, pathSeg, curFile) &&
        canOverrideDirectoryRole(storedPortal, pathSeg, curFile, dirRole)) {

      return storedPortal;

    }

    // Priority 4: Role directory path (/pages/admin/, /pages/teacher/, /pages/student/, /pages/principal/)

    if (pathSeg && pathSeg !== "shared") {

      const normalizedPathRole = normalizeRole(pathSeg);

      if (VALID_PORTALS.includes(normalizedPathRole)) {

        try { localStorage.setItem("ngis_active_portal", normalizedPathRole); } catch (e) {}

        return normalizedPathRole;

      }

    }

    // Priority 5: Explicit pageRole configured on window.PAGE (on shared/root pages)

    if (pageRole) {

      const normalizedPageRole = normalizeRole(pageRole);

      if (canPortalServeCurrentPath(normalizedPageRole, pathSeg, curFile)) {

        try { localStorage.setItem("ngis_active_portal", normalizedPageRole); } catch (e) {}

        return normalizedPageRole;

      }

    }

    // Priority 6: Stored portal preference or passive session fallback

    if (storedPortal && canPortalServeCurrentPath(storedPortal, pathSeg, curFile) &&
        canOverrideDirectoryRole(storedPortal, pathSeg, curFile, dirRole)) {

      return storedPortal;

    }

    const fallbackSession = getSessionRole();

    if (fallbackSession && canPortalServeCurrentPath(fallbackSession, pathSeg, curFile) &&
        canOverrideDirectoryRole(fallbackSession, pathSeg, curFile, dirRole)) {

      return fallbackSession;

    }

    return "student";

  }

  function buildPortalHref(rawHref, portalRole) {

    if (!rawHref) return "#";

    const s = String(rawHref);

    if (s.startsWith("#") || s.startsWith("http://") || s.startsWith("https://") || s.startsWith("mailto:") || s.startsWith("tel:")) {

      return s;

    }

    const clean = s.split("?")[0].split("#")[0];

    if (clean === "index.html" || clean === "") return `${_P}${s}`;

    const hashIdx = s.indexOf("#");

    const hashPart = hashIdx !== -1 ? s.slice(hashIdx) : "";

    const withoutHash = hashIdx !== -1 ? s.slice(0, hashIdx) : s;

    const qIdx = withoutHash.indexOf("?");

    const pathPart = qIdx !== -1 ? withoutHash.slice(0, qIdx) : withoutHash;

    const queryPart = qIdx !== -1 ? withoutHash.slice(qIdx + 1) : "";

    const params = new URLSearchParams(queryPart);

    if (portalRole && (pathPart.startsWith("pages/shared/") || portalRole === "staff" || portalRole === "superadmin")) {

      params.set("portal", portalRole);

    }

    const qOut = params.toString();

    return `${_P}${pathPart}${qOut ? "?" + qOut : ""}${hashPart}`;

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



  function buildSidebar(cfg, active, user, portalRole) {

    const role = portalRole || resolvePortalRole(window.PAGE && window.PAGE.role);

    const homeHref = buildPortalHref(PORTAL_HOME[role] || "index.html", role);

    const currentUser = user || (window.PAGE && window.PAGE.user) || DEFAULT_USER[role] || DEFAULT_USER.teacher;



    function isMatchingNavId(itemId, targetId) {

      if (!itemId || !targetId) return false;

      if (itemId === targetId) return true;

      if ((targetId === "teachers" || targetId === "teacher-profiles") && (itemId === "teachers" || itemId === "teacher-profiles" || itemId === "teachers-mgmt-drop")) return true;

      if ((targetId === "students" || targetId === "student-profiles") && (itemId === "students" || itemId === "student-profiles" || itemId === "student-mgmt-drop")) return true;

      return false;

    }

    function linkHasId(item, id) {

      if (!item) return false;

      if (isMatchingNavId(item.id, id)) return true;

      if (Array.isArray(item.children)) {

        return item.children.some(c => linkHasId(c, id));

      }

      return false;

    }



    const curFile = (window.location.pathname || '').replace(/\\/g, '/').split('/').pop().toLowerCase();

    const curSearch = (window.location.search || '');

    const curParams = new URLSearchParams(curSearch);

    const curHash = (window.location.hash || '').toLowerCase();



    function hrefMatchScore(rawHref) {

      if (!rawHref) return -1;

      const s = String(rawHref);

      if (s.startsWith('#') || s.startsWith('http://') || s.startsWith('https://')) return -1;

      const hashIdx = s.indexOf('#');

      const hashPart = hashIdx !== -1 ? s.slice(hashIdx).toLowerCase() : '';

      const withoutHash = hashIdx !== -1 ? s.slice(0, hashIdx) : s;

      const qIdx = withoutHash.indexOf('?');

      const pathPart = qIdx !== -1 ? withoutHash.slice(0, qIdx) : withoutHash;

      const queryPart = qIdx !== -1 ? withoutHash.slice(qIdx + 1) : '';

      const file = pathPart.replace(/\\/g, '/').split('/').pop().toLowerCase();

      if (!file || file !== curFile) return -1;



      if (hashPart) {

        if (curHash !== hashPart) return -1;

      }



      const linkParams = new URLSearchParams(queryPart);

      let score = 1;

      for (const [k, v] of linkParams.entries()) {

        const lk = k.toLowerCase();

        if (lk === 'portal' || lk === 'role') continue;

        const actual = curParams.get(k);

        if (actual === null || actual.toLowerCase() !== String(v).toLowerCase()) {

          return -1;

        }

        score += 10;

      }

      if (hashPart && curHash === hashPart) score += 20;

      else if (!hashPart && !curHash) score += 2;

      return score;

    }



    function collectLeaves(items, out) {

      if (!Array.isArray(items)) return;

      for (const item of items) {

        if (!item || item.visible === false) continue;

        if (Array.isArray(item.children) && item.children.length > 0) {

          collectLeaves(item.children, out);

        } else if (item.href) {

          out.push({ id: item.id, href: item.href, score: hrefMatchScore(item.href) });

        }

      }

    }



    function resolveEffectiveActive(activeCandidate) {

      const leaves = [];

      for (const g of cfg.groups) {

        if (g.visible === false) continue;

        if (g.href) leaves.push({ id: g.id, href: g.href, score: hrefMatchScore(g.href) });

        collectLeaves(g.links, leaves);

      }

      const matchingLeaves = leaves.filter(l => l.score > 0).sort((a, b) => b.score - a.score);

      const bestScore = matchingLeaves.length ? matchingLeaves[0].score : 0;



      // 1. Honor clicked sidebar link when its target file/query/hash still matches the URL

      try {

        const rawClicked = sessionStorage.getItem(CLICKED_NAV_KEY);

        if (rawClicked) {

          let clickedId = rawClicked;

          let clickedPortal = '';

          if (rawClicked.startsWith('{')) {

            const parsed = JSON.parse(rawClicked);

            clickedId = parsed.id || '';

            clickedPortal = parsed.portal || '';

          }

          if (clickedId && (!clickedPortal || clickedPortal === role)) {

            const clickedLeaf = leaves.find(l => l.id === clickedId);

            if (clickedLeaf && clickedLeaf.score >= Math.max(1, bestScore)) {

              return clickedId;

            }

          }

        }

      } catch (e) {}



      /* 1b. A declared PAGE.active that resolves to the current file with the
         best available score must win. Several nav entries can point at the
         same .html file; without this guard the first one alphabetically
         steals the active state from the page's own declared id. */
      if (activeCandidate) {
        const declaredLeaf = leaves.find(l => isMatchingNavId(l.id, activeCandidate));
        if (declaredLeaf && declaredLeaf.score > 0 && declaredLeaf.score >= bestScore) {
          return declaredLeaf.id;
        }
      }



      // 2. Specific query or hash parameter match wins (e.g., ?view=verify, ?tab=homeroom, #tabHero)

      if (bestScore > 1 && matchingLeaves.length) {

        return matchingLeaves[0].id;

      }



      // 3. Declared PAGE.active only if it points to the current file OR the current file is an unlisted subpage (e.g., department detail)

      if (activeCandidate) {

        const declaredLeaf = leaves.find(l => isMatchingNavId(l.id, activeCandidate));

        if (declaredLeaf && declaredLeaf.score > 0) {

          return declaredLeaf.id;

        }

        if (matchingLeaves.length === 0 && cfg.groups.some(g => g.id === activeCandidate || (g.links && g.links.some(l => linkHasId(l, activeCandidate))))) {

          return activeCandidate;

        }

      }



      // 4. First matching leaf for the current file

      if (matchingLeaves.length) {

        return matchingLeaves[0].id;

      }



      return activeCandidate;

    }



    let effectiveActive = resolveEffectiveActive(active);



    function renderNavIcon(icon, className) {
      if (!icon) return "";
      const trimmed = String(icon).trim();
      if (trimmed.startsWith("<svg")) {
        return `<span class="nav-icon ${className} nav-icon-svg" aria-hidden="true">${trimmed}</span>`;
      }
      if (trimmed.startsWith("ph ") || trimmed.startsWith("ph-")) {
        /* Phosphor glyph: upgrade to the shared Bootstrap-icon engine while
           keeping the Phosphor ligature as a no-engine fallback. */
        const phName = trimmed.replace(/^ph[\s-]+/, "").replace(/^ph-/, "");
        return `<i class="${trimmed} ${className} nav-icon" data-ngis-icon="${esc(phName)}" aria-hidden="true">${esc(phName)}</i>`;
      }
      /* Material Symbols glyph with a data-ngis-icon slot: the shared icon
         engine (action-icons.js) replaces it with the official Bootstrap
         Icons SVG when present; the ligature text remains a graceful
         fallback so the sidebar never loses its icons. */
      return `<span class="material-symbols-outlined ${className} nav-icon" data-ngis-icon="${esc(trimmed)}" aria-hidden="true">${esc(trimmed)}</span>`;
    }

    const groups = cfg.groups.map((g, gi) => {

      if (g.visible === false) return '';

      const links = g.links.map(l => {

        if (l.visible === false) return '';

        if (l.children && l.children.length > 0) {

          const isSubActive = l.children.some(sub => linkHasId(sub, effectiveActive));

          const sublinks = l.children.map(sub => {
            if (sub.visible === false) return '';
            if (sub.children && sub.children.length > 0) {
              const isNestedActive = sub.children.some(n => linkHasId(n, effectiveActive));
              const nestedLinks = sub.children.map(n => {
                if (n.visible === false) return '';
                const isNActive = isMatchingNavId(n.id, effectiveActive);
                const nHref = buildPortalHref(n.href, role);
                return `<a class="nav-link nav-nested-link ${isNActive ? "active" : ""}" href="${nHref}" data-raw-href="${esc(n.href || '')}"${isNActive ? ' aria-current="page"' : ''} title="${esc(n.subtitle || n.label)}" data-id="${n.id}">
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

            const isItemActive = isMatchingNavId(sub.id, effectiveActive);
            const chevronHtml = sub.hasChevron ? `<span class="material-symbols-outlined ngl-subchevron-static" aria-hidden="true">expand_more</span>` : "";
            const subHref = buildPortalHref(sub.href, role);
            return `<a class="nav-link nav-sub-link ${isItemActive ? "active" : ""}" href="${subHref}" data-raw-href="${esc(sub.href || '')}"${isItemActive ? ' aria-current="page"' : ''} title="${esc(sub.subtitle || sub.label)}" data-id="${sub.id}">
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

        const isTopActive = isMatchingNavId(l.id, effectiveActive);
        const topHref = buildPortalHref(l.href, role);
        return `<a class="nav-link ${l.icon ? '' : 'no-icon'} ${isTopActive ? "active" : ""}" href="${topHref}" data-raw-href="${esc(l.href || '')}"${isTopActive?' aria-current="page"':''} title="${esc(l.subtitle || l.label)}" data-id="${l.id}">

           ${renderNavIcon(l.icon, "nav-link-icon")}

           <span class="nav-link-label">${esc(l.label)}</span>

           ${l.badge ? `<span class="pill">${l.badge}</span>` : ""}

         </a>`;

      }).join("");

      const groupActive = isMatchingNavId(g.id, effectiveActive) || g.links.some(l => linkHasId(l, effectiveActive));

      const labelInner = `

        ${renderNavIcon(g.icon, "nav-group-icon")}

        <span class="nav-group-label-text">${esc(g.label || "")}</span>

        <span class="nav-group-label-rule"></span>`;



      let label = "", linksHtml;

      if (g.collapsible) {

        label = `<button type="button" class="nav-group-label" aria-expanded="${groupActive ? "true" : "false"}" title="${esc(g.label)}">${labelInner}</button>`;

        linksHtml = `<div class="nav-group-links"><div>${links}</div></div>`;

      } else if (g.href) {

        label = `<a class="nav-group-label nav-group-label-link${groupActive ? " active" : ""}" href="${buildPortalHref(g.href, role)}" data-raw-href="${esc(g.href)}" data-id="${esc(g.id || '')}">${labelInner}</a>`;

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



    const helpRaw = role === 'student' ? 'pages/student/student-services.html'
      : role === 'teacher' ? 'pages/teacher/teacher-services.html'
      : role === 'principal' ? 'pages/principal/principal-services.html'
      : 'pages/admin/admin-services.html';

    return el(`

      <aside class="sidebar custom-scrollbar" id="sidebar" role="navigation" aria-label="Main navigation" data-purpose="primary-sidebar" data-portal-role="${esc(role)}">

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

        <div class="sb-search-wrap">
          <div class="sb-search-box">
            <span class="material-symbols-outlined sb-search-icon" aria-hidden="true">search</span>
            <input type="search" class="sb-search-input" id="sidebarSearchInput" placeholder="Find a page…" aria-label="Filter navigation links" autocomplete="off">
          </div>
        </div>

        <nav class="side-nav custom-scrollbar" aria-label="Main Navigation">

          ${groups}

        </nav>



        <footer class="side-foot">

          <a class="nav-link side-foot-help" href="${buildPortalHref(helpRaw, role)}">

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

      { id: "home", label: "Home", icon: "ph ph-house", href: "pages/student/student.html" },

      { id: "department", label: "Depts", icon: "ph ph-buildings", href: "pages/shared/departments.html" },

      { id: "profile", label: "Account", icon: "ph ph-user", href: "pages/student/student-profile.html" },

    ],

    teacher: [

      { id: "home", label: "Home", icon: "ph ph-house", href: "pages/teacher/teacher.html" },

      { id: "classes", label: "Classes", icon: "ph ph-chalkboard-teacher", href: "pages/teacher/teacher-roster.html" },

      { id: "submissions", label: "Work", icon: "ph ph-file-text", href: "pages/teacher/teacher-submissions.html" },

      { id: "profile", label: "Account", icon: "ph ph-user", href: "pages/teacher/teacher-profile.html" },

    ],

    admin: [

      { id: "home", label: "Home", icon: "ph ph-house", href: "pages/admin/admin.html" },

      { id: "users", label: "Users", icon: "ph ph-users", href: "pages/admin/admin-users-students.html" },

      { id: "reports", label: "Reports", icon: "ph ph-chart-bar", href: "pages/admin/admin-reports.html" },

      { id: "settings", label: "Settings", icon: "ph ph-gear", href: "pages/admin/admin-settings.html" },

    ],

    superadmin: [

      { id: "home", label: "Home", icon: "ph ph-house", href: "pages/admin/admin.html" },

      { id: "users", label: "Users", icon: "ph ph-users", href: "pages/admin/admin-users-students.html" },

      { id: "reports", label: "CMS", icon: "ph ph-sliders", href: "pages/admin/admin-dashboard-content.html" },

      { id: "settings", label: "Settings", icon: "ph ph-gear", href: "pages/admin/admin-settings.html" },

    ],

    staff: [

      { id: "services", label: "Services", icon: "ph ph-grid-four", href: "pages/admin/admin-services.html" },

      { id: "lost-found", label: "Lost & Found", icon: "ph ph-package", href: "pages/principal/principal-lost-found.html" },

      { id: "campuses", label: "Campuses", icon: "ph ph-buildings", href: "pages/admin/admin-campuses.html" },

      { id: "settings", label: "Account", icon: "ph ph-gear", href: "pages/admin/admin-settings.html" },

    ],

    principal: [

      { id: "home", label: "Home", icon: "ph ph-house", href: "pages/principal/principal.html" },

      { id: "classes", label: "Classes", icon: "ph ph-chalkboard", href: "pages/principal/principal-classes.html" },

      { id: "students", label: "Students", icon: "ph ph-graduation-cap", href: "pages/principal/principal-student-profiles.html" },

      { id: "reports", label: "Reports", icon: "ph ph-chart-bar", href: "pages/principal/principal-reports.html" },

      { id: "profile", label: "Account", icon: "ph ph-user", href: "pages/principal/principal-profile.html" },

    ],

  };



  function getRoleActiveTab(role, active) {

    const path = (window.location.pathname || '').toLowerCase();

    const file = (path.split('/').pop() || '').toLowerCase();

    if (file === `${role}.html` || (active === 'dashboard' && file.indexOf(`${role}-`) === -1)) return 'home';

    

    if (file.indexOf('notification') !== -1 || file.indexOf('announcement') !== -1 || file.indexOf('log') !== -1 || active === 'notifications' || active === 'announcements' || active === 'alerts' || active === 'logs') return 'alerts';

    if (file.indexOf('profile') !== -1 || file.indexOf('setting') !== -1 || active === 'profile' || active === 'settings' || active === 'preferences') {

      return (role === 'admin' || role === 'superadmin' || role === 'principal' || role === 'staff') ? 'settings' : 'profile';

    }

    if (role === 'teacher') {

      if (file === 'teacher.html' || active === 'dashboard') return 'home';

      if (file.indexOf('class') !== -1 || active === 'classes') return 'classes';

      if (file.indexOf('submission') !== -1 || file.indexOf('assignment') !== -1 || active === 'submissions' || active === 'assignments') return 'submissions';

      if (file.indexOf('gradebook') !== -1 || file.indexOf('grade') !== -1 || active === 'gradebook') return 'gradebook';

      if (file.indexOf('profile') !== -1 || active === 'profile') return 'profile';

      return 'home';

    }

    if (role === 'admin' || role === 'superadmin') {

      if (file.indexOf('user') !== -1 || active === 'users' || active === 'admins' || active === 'teachers' || active === 'students' || active === 'parents') return 'users';

      if (file.indexOf('report') !== -1 || file.indexOf('dashboard-content') !== -1 || active === 'reports' || active === 'dashboard-content') return 'reports';

      if (file.indexOf('setting') !== -1 || active === 'settings') return 'settings';

    }

    if (role === 'staff') {

      if (file.indexOf('lost-found') !== -1 || active === 'lost-found' || active === 'staff-lost-found') return 'lost-found';

      if (file.indexOf('campus') !== -1 || active === 'campuses' || active === 'staff-campuses') return 'campuses';

      if (file.indexOf('setting') !== -1 || active === 'settings' || active === 'staff-profile') return 'settings';

      return 'services';

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

            <span class="mob-bn-label">${esc(tab.label)}</span>

          </button>`;

      }

      return `

        <a href="${buildPortalHref(tab.href, role)}" class="mob-bn-item ${isActive ? 'is-active' : ''}" data-tab="${tab.id}" aria-label="${esc(tab.label)}"${isActive ? ' aria-current="page"' : ''}>

          <span class="mob-bn-icon-row">

            <span class="mob-bn-icon-wrap">

              <i class="${tab.icon}"></i>

              ${tab.hasDot ? `<span class="mob-bn-dot"></span>` : ''}

            </span>

          </span>

          <span class="mob-bn-label">${esc(tab.label)}</span>

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

    /* Legacy/renamed page ids mapped onto their current nav entry so the
       sidebar still highlights correctly after navigation. Ids that don't
       exist in the current portal's nav are harmless no-ops. */
    const ALIAS_MAP = {
      "ks-wizard": "teacher-class-assignment",
      "dict-school": "sa-dictionary",
      "dict-students": "sa-dictionary",
      "dict-teachers": "sa-dictionary",
      "dict-timetable": "sa-dictionary",
      "dict-additional": "sa-dictionary",
      "gradebook": "assessment",
    };

    if (ALIAS_MAP[active]) active = ALIAS_MAP[active];

    if (portalRole === "student" && DEPT_CHILD.includes(active)) {

      active = "departments";

    }



    document.body.setAttribute("data-role", portalRole);

    document.body.setAttribute("data-portal", portalRole);



    const main = document.querySelector(".main");

    if (!main) return;   // standalone pages (landing) have no app shell



    const shell = el(`<div class="shell"></div>`);

    main.parentNode.insertBefore(shell, main);



    const sidebar = buildSidebar(cfg, active, user, portalRole);

    const scrim   = el(`<div class="scrim" id="scrim"></div>`);

    /* Sidebar is position:fixed — mount it on <body> so the mobile drawer stays

       reachable on pages that hide their desktop view (e.g. student dashboard). */

    document.body.appendChild(sidebar);

    shell.appendChild(main);

    document.body.appendChild(scrim);

    /* Tells the master sidebar CSS layer (app.css) that the engine owns the

       drawer; without it the static fallback keeps #sidebar visible. */

    document.body.classList.add("ngis-layout-ready");



    /* ── Persistent multi-level sidebar expansion helpers ── */

    function readOpenIds(storageKey) {

      try {

        const raw = store.get(storageKey);

        if (!raw) return [];

        if (raw.startsWith('[')) {

          const arr = JSON.parse(raw);

          return Array.isArray(arr) ? arr.filter(Boolean) : [];

        }

        return [raw];

      } catch (e) { return []; }

    }

    function saveOpenIds(storageKey, elements, attrName) {

      const ids = elements.filter(node => node.classList.contains('expanded')).map(node => node.getAttribute(attrName)).filter(Boolean);

      try { store.set(storageKey, JSON.stringify(ids)); } catch (e) {}

    }

    const OPEN_GROUPS_KEY = `ngis-${portalRole}-open-groups`;

    const OPEN_SUBGROUPS_KEY = `ngis-${portalRole}-open-subgroups`;

    const OPEN_NESTED_KEY = `ngis-${portalRole}-open-nested`;



    /* ── Sidebar collapsible groups ── */

    const collapsibleGroups = Array.from(sidebar.querySelectorAll('.nav-group.collapsible'));

    const setGroupExpanded = (groupEl, expanded) => {

      groupEl.classList.toggle('expanded', expanded);

      const btn = groupEl.querySelector('.nav-group-label');

      if (btn && btn.tagName === 'BUTTON') btn.setAttribute('aria-expanded', String(expanded));

    };

    if (collapsibleGroups.length) {

      const savedGroups = readOpenIds(OPEN_GROUPS_KEY);

      const legacySingle = store.get(`ngis-${portalRole}-open-group`);

      if (legacySingle && !savedGroups.includes(legacySingle)) savedGroups.push(legacySingle);

      const hasSavedGroups = store.get(OPEN_GROUPS_KEY) !== null;



      collapsibleGroups.forEach(g => {

        const gid = g.dataset.groupId || '';

        const hasActive = Boolean(g.querySelector('.nav-link.active'));

        const shouldOpen = hasActive || (hasSavedGroups ? savedGroups.includes(gid) : (gid && legacySingle === gid));

        setGroupExpanded(g, shouldOpen);

      });

      saveOpenIds(OPEN_GROUPS_KEY, collapsibleGroups, 'data-group-id');



      collapsibleGroups.forEach(g => {

        const btn = g.querySelector('.nav-group-label');

        if (!btn || btn.tagName !== 'BUTTON') return;

        btn.addEventListener('click', () => {

          if (sidebar.classList.contains('collapsed')) {

            setSidebarCollapsed(false);

            setGroupExpanded(g, true);

            saveOpenIds(OPEN_GROUPS_KEY, collapsibleGroups, 'data-group-id');

            return;

          }

          const willOpen = !g.classList.contains('expanded');

          setGroupExpanded(g, willOpen);

          saveOpenIds(OPEN_GROUPS_KEY, collapsibleGroups, 'data-group-id');

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



    /* ── Sidebar sub-accordion (1st-level collapsible sub-groups) ── */

    const collapsibleSubgroups = Array.from(sidebar.querySelectorAll('.nav-subgroup.collapsible'));

    const setSubgroupExpanded = (sg, expanded) => {

      sg.classList.toggle('expanded', expanded);

      const btn = sg.querySelector('.nav-subgroup-label');

      if (btn) btn.setAttribute('aria-expanded', String(expanded));

    };

    if (collapsibleSubgroups.length) {

      const savedSubs = readOpenIds(OPEN_SUBGROUPS_KEY);

      collapsibleSubgroups.forEach(sg => {

        const sgId = sg.dataset.subgroupId || '';

        const hasActiveSub = Boolean(sg.querySelector('.nav-link.active'));

        const shouldOpen = hasActiveSub || savedSubs.includes(sgId);

        setSubgroupExpanded(sg, shouldOpen);

      });

      saveOpenIds(OPEN_SUBGROUPS_KEY, collapsibleSubgroups, 'data-subgroup-id');



      collapsibleSubgroups.forEach(sg => {

        const btn = sg.querySelector('.nav-subgroup-label');

        if (!btn) return;

        btn.addEventListener('click', (e) => {

          e.preventDefault();

          e.stopPropagation();

          if (sidebar.classList.contains('collapsed')) {

            setSidebarCollapsed(false);

            setSubgroupExpanded(sg, true);

            saveOpenIds(OPEN_SUBGROUPS_KEY, collapsibleSubgroups, 'data-subgroup-id');

            return;

          }

          const willOpen = !sg.classList.contains('expanded');

          setSubgroupExpanded(sg, willOpen);

          saveOpenIds(OPEN_SUBGROUPS_KEY, collapsibleSubgroups, 'data-subgroup-id');

        });

      });

    }



    /* ── Sidebar 2nd-level nested sub-accordion (e.g. Data Dictionary / Academic Result) ── */

    const collapsibleNested = Array.from(sidebar.querySelectorAll('.nav-nested-group.collapsible'));

    const setNestedExpanded = (ng, expanded) => {

      ng.classList.toggle('expanded', expanded);

      const btn = ng.querySelector('.nav-nested-label');

      if (btn) btn.setAttribute('aria-expanded', String(expanded));

    };

    if (collapsibleNested.length) {

      const savedNested = readOpenIds(OPEN_NESTED_KEY);

      collapsibleNested.forEach(ng => {

        const ngId = ng.dataset.nestedId || '';

        const hasActiveNested = Boolean(ng.querySelector('.nav-link.active'));

        const shouldOpen = hasActiveNested || savedNested.includes(ngId);

        setNestedExpanded(ng, shouldOpen);

        if (shouldOpen) {

          const parentSub = ng.closest('.nav-subgroup.collapsible');

          if (parentSub) setSubgroupExpanded(parentSub, true);

        }

      });

      saveOpenIds(OPEN_NESTED_KEY, collapsibleNested, 'data-nested-id');

      if (collapsibleSubgroups.length) saveOpenIds(OPEN_SUBGROUPS_KEY, collapsibleSubgroups, 'data-subgroup-id');



      collapsibleNested.forEach(ng => {

        const btn = ng.querySelector('.nav-nested-label');

        if (!btn) return;

        btn.addEventListener('click', (e) => {

          e.preventDefault();

          e.stopPropagation();

          const willOpen = !ng.classList.contains('expanded');

          setNestedExpanded(ng, willOpen);

          saveOpenIds(OPEN_NESTED_KEY, collapsibleNested, 'data-nested-id');

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



    // Click handler on sidebar links to capture scroll position, clicked item, and sign-out state

    sidebar.addEventListener("click", (e) => {

      const link = e.target.closest("a");

      if (!link) return;

      const isLogout = link.classList.contains("side-foot-signout") || (link.dataset && link.dataset.id === "logout");

      if (isLogout) {

        try {

          if (window.NGISAuth && typeof window.NGISAuth.clearSession === "function") {

            window.NGISAuth.clearSession();

          } else {

            localStorage.removeItem("ngis_token");

            localStorage.removeItem("ngis_user");

            localStorage.removeItem("ngis_active_portal");

            localStorage.removeItem("ngis_session_mode");

          }

          sessionStorage.removeItem(CLICKED_NAV_KEY);

        } catch (err) {}

        return;

      }

      try {

        sessionStorage.setItem(SCROLL_KEY, String(sideNav.scrollTop));

        sessionStorage.setItem(GLOBAL_SCROLL_KEY, String(sideNav.scrollTop));

        sessionStorage.setItem(NAV_FLAG_KEY, "1");

        if (link.dataset && link.dataset.id) {

          sessionStorage.setItem(CLICKED_NAV_KEY, JSON.stringify({ id: link.dataset.id, portal: portalRole }));

        }

      } catch (err) {}

    }, { capture: true });

    // Update active state when navigating to same-page hash targets (e.g. #tabHero)

    window.addEventListener("hashchange", () => {

      const curHashNow = (window.location.hash || "").toLowerCase();

      const curFileNow = (window.location.pathname || "").replace(/\\/g, "/").split("/").pop().toLowerCase();

      const linksNow = Array.from(sidebar.querySelectorAll("a.nav-link[data-id]"));

      let bestMatch = null;

      linksNow.forEach(a => {

        const raw = a.getAttribute("data-raw-href") || a.getAttribute("href") || "";

        const hIdx = raw.indexOf("#");

        const hPart = hIdx !== -1 ? raw.slice(hIdx).toLowerCase() : "";

        const clean = raw.split("#")[0].split("?")[0].split("/").pop().toLowerCase();

        if (clean === curFileNow && hPart && hPart === curHashNow) bestMatch = a;

      });

      if (!bestMatch && !curHashNow) {

        bestMatch = linksNow.find(a => {

          const raw = a.getAttribute("data-raw-href") || "";

          return !raw.includes("#") && raw.split("?")[0].split("/").pop().toLowerCase() === curFileNow;

        }) || null;

      }

      if (bestMatch) {

        linksNow.forEach(a => {

          const act = a === bestMatch;

          a.classList.toggle("active", act);

          if (act) a.setAttribute("aria-current", "page");

          else a.removeAttribute("aria-current");

        });

      }

    });



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

      if (isDrawerMode()) collapsed = false;

      const brandLogo = sidebar.querySelector('.side-brand-crest') || sidebar.querySelector('.side-brand-logo-img');

      if (collapsed) {

        sidebar.classList.add('collapsed');

        main.classList.add('sidebar-collapsed');

        document.body.classList.add('sidebar-collapsed');

        if (collapseBtn) {
          collapseBtn.setAttribute('title', 'Expand sidebar');
          collapseBtn.setAttribute('aria-label', 'Expand navigation');
          collapseBtn.setAttribute('aria-expanded', 'false');
        }

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

        if (collapseBtn) {
          collapseBtn.setAttribute('title', 'Collapse sidebar');
          collapseBtn.setAttribute('aria-label', 'Collapse sidebar');
          collapseBtn.setAttribute('aria-expanded', 'true');
        }

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

    const savedCollapsed = store.get(COLLAPSED_KEY);

    if (savedCollapsed === '1') {

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

        setSidebarCollapsed(!sidebar.classList.contains('collapsed'));

      });

    }

    if (expandBtn) {

      expandBtn.addEventListener('click', (e) => {

        e.stopPropagation();

        const isCurrentlyCollapsed = sidebar.classList.contains('collapsed');

        setSidebarCollapsed(!isCurrentlyCollapsed);

      });

    }

    const searchInput = sidebar.querySelector('#sidebarSearchInput');
    if (searchInput) {
      searchInput.addEventListener('input', () => {
        const q = searchInput.value.trim().toLowerCase();
        if (!q) {
          sidebar.querySelectorAll('.nav-group, .nav-subgroup, .nav-nested-group, .nav-link').forEach(elNode => {
            elNode.style.display = '';
          });
          const savedGroups = readOpenIds(OPEN_GROUPS_KEY);
          const savedSubs = readOpenIds(OPEN_SUBGROUPS_KEY);
          const savedNested = readOpenIds(OPEN_NESTED_KEY);
          collapsibleGroups.forEach(g => setGroupExpanded(g, Boolean(g.querySelector('.nav-link.active')) || savedGroups.includes(g.dataset.groupId || '')));
          collapsibleSubgroups.forEach(sg => setSubgroupExpanded(sg, Boolean(sg.querySelector('.nav-link.active')) || savedSubs.includes(sg.dataset.subgroupId || '')));
          collapsibleNested.forEach(ng => setNestedExpanded(ng, Boolean(ng.querySelector('.nav-link.active')) || savedNested.includes(ng.dataset.nestedId || '')));
          return;
        }
        sidebar.querySelectorAll('.nav-group').forEach(grp => {
          let groupVisibleCount = 0;
          grp.querySelectorAll('.nav-subgroup').forEach(sub => {
            const subTitle = (sub.querySelector('.nav-subgroup-label')?.textContent || '').toLowerCase();
            const subMatch = subTitle.indexOf(q) !== -1;
            let childMatches = 0;
            sub.querySelectorAll('.nav-nested-group').forEach(nested => {
              const nTitle = (nested.querySelector('.nav-nested-label')?.textContent || '').toLowerCase();
              const nTitleMatch = subMatch || nTitle.indexOf(q) !== -1;
              let nestedCount = 0;
              nested.querySelectorAll('.nav-nested-link').forEach(nl => {
                const nTxt = (nl.textContent || '').toLowerCase();
                const nShow = nTitleMatch || nTxt.indexOf(q) !== -1;
                nl.style.display = nShow ? '' : 'none';
                if (nShow) nestedCount++;
              });
              const showNested = nestedCount > 0;
              nested.style.display = showNested ? '' : 'none';
              if (showNested) {
                nested.classList.add('expanded');
                childMatches += nestedCount;
              }
            });
            sub.querySelectorAll(':scope > .nav-subgroup-links > div > .nav-sub-link').forEach(link => {
              const txt = (link.textContent || '').toLowerCase();
              const show = subMatch || txt.indexOf(q) !== -1;
              link.style.display = show ? '' : 'none';
              if (show) childMatches++;
            });
            const showSub = subMatch || childMatches > 0;
            sub.style.display = showSub ? '' : 'none';
            if (showSub) sub.classList.add('expanded');
            if (showSub) groupVisibleCount++;
          });
          grp.querySelectorAll(':scope > .nav-link, :scope > .nav-group-links > div > .nav-link').forEach(link => {
            const txt = (link.textContent || '').toLowerCase();
            const show = txt.indexOf(q) !== -1;
            link.style.display = show ? '' : 'none';
            if (show) groupVisibleCount++;
          });
          grp.style.display = groupVisibleCount > 0 ? '' : 'none';
          if (groupVisibleCount > 0 && grp.classList.contains('collapsible')) {
            setGroupExpanded(grp, true);
          }
        });
      });
    }

    /* Desktop view: keep collapse/expand controls available (>=1025px),
       and hide them in mobile/tablet drawer mode (<=1024px). */

    function syncRailLockUI() {

      const inDrawer = isDrawerMode();

      if (collapseBtn) {
        if (inDrawer) collapseBtn.style.setProperty('display', 'none', 'important');
        else collapseBtn.style.removeProperty('display');
      }

      if (expandBtn) {
        if (inDrawer) expandBtn.style.setProperty('display', 'none', 'important');
        else expandBtn.style.removeProperty('display');
      }

      if (inDrawer && sidebar.classList.contains('collapsed')) {
        sidebar.classList.remove('collapsed');
        main.classList.remove('sidebar-collapsed');
        document.body.classList.remove('sidebar-collapsed');
      }

    }

    syncRailLockUI();

    window.addEventListener('resize', syncRailLockUI);



    let bNav = document.getElementById("mobBottomNav");

    if (!bNav) {

      bNav = buildBottomNav(portalRole, active);

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
        const rawId = openDrawer.getAttribute("data-open-drawer");
        if (!rawId || !rawId.trim()) return;
        const id = rawId.trim().replace(/^#/, "");
        if (!id) return;
        let drawer = null;
        try {
          drawer = document.querySelector(`.drawer-overlay[data-drawer="${id}"], .drawer-overlay#${id}, #${id}.drawer-overlay, #${id}`);
        } catch (_) {
          drawer = document.getElementById(id);
        }
        if (drawer) {
          drawer.classList.add("show");
          drawer.classList.add("open");
          const inner = drawer.querySelector(".drawer");
          if (inner) {
            inner.classList.add("show");
            inner.classList.add("open");
          }
        }
        return;
      }

      const closeDrawer = e.target.closest("[data-close-drawer]");
      if (closeDrawer) {
        e.preventDefault();
        const drawer = closeDrawer.closest(".drawer-overlay, aside.drawer");
        if (drawer) {
          drawer.classList.remove("show");
          drawer.classList.remove("open");
          if (drawer.parentElement && drawer.parentElement.classList.contains("drawer-overlay")) {
            drawer.parentElement.classList.remove("show");
            drawer.parentElement.classList.remove("open");
          }
        }
        return;
      }

      const openModal = e.target.closest("[data-open-modal]");
      if (openModal) {
        e.preventDefault();
        const rawId = openModal.getAttribute("data-open-modal");
        if (!rawId || !rawId.trim()) return;
        const id = rawId.trim().replace(/^#/, "");
        if (!id) return;
        let modal = null;
        try {
          modal = document.querySelector(`.modal-overlay[data-modal="${id}"], .modal-overlay#${id}, #${id}.modal-overlay, #${id}`);
        } catch (_) {
          modal = document.getElementById(id);
        }
        if (modal) {
          modal.classList.add("show");
          modal.classList.add("open");
        }
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

    /* UI Cleanup & Zero-Border Zero-Shadow Master System */
    let cleanupLink = document.querySelector('link[href*="ui-cleanup.css"]');
    if (!cleanupLink) {
      cleanupLink = document.createElement("link");
      cleanupLink.rel = "stylesheet";
      cleanupLink.href = _P + "assets/css/ui-cleanup.css";
      document.head.appendChild(cleanupLink);
    } else {
      document.head.appendChild(cleanupLink);
    }

    /* Shared search system must load AFTER ui-cleanup/shared-components so the
       single .ngis-search pattern wins by source order, not page-level hacks. */
    if (!document.querySelector('link[href*="ngis-search.css"]')) {
      const searchCss = document.createElement("link");
      searchCss.rel = "stylesheet";
      searchCss.href = _P + "assets/css/ngis-search.css";
      document.head.appendChild(searchCss);
    }

    /* Semantic urgency-state system (global status-aware colors) */
    if (!document.querySelector('link[href*="semantic-states.css"]')) {
      const lss = document.createElement("link");
      lss.rel = "stylesheet";
      lss.href = _P + "assets/css/semantic-states.css";
      document.head.appendChild(lss);
    }

    /* Measured sticky application header — must load after the cleanup layers
       so its opaque surface and calculated offsets win the cascade. */
    if (!document.querySelector('link[href*="sticky-layout.css"]')) {
      const stickyCss = document.createElement("link");
      stickyCss.rel = "stylesheet";
      stickyCss.href = _P + "assets/css/sticky-layout.css";
      document.head.appendChild(stickyCss);
    }

    const sharedComponents = [
      "assets/js/ngis-copy.js",
      "assets/js/error-messages.js",
      "assets/js/error-boundary.js",
      "assets/components/skeleton.js",
      "assets/components/error-state.js",
      "assets/components/empty-state.js",
      "assets/components/primary-button.js",
      "assets/components/cancel-dialog.js",
      "assets/components/onboarding-layout.js",
      "assets/components/ngis-ui-kit.js",
      "assets/js/ui-states.js",
      "assets/js/action-icons.js?v=1.13.2",
      "assets/js/semantic-states.js",
      "assets/js/ngis-search.js",
      "assets/js/sticky-layout.js"
    ];

    sharedComponents.forEach(scriptPath => {
      if (document.querySelector('script[src*="' + scriptPath + '"]')) return;
      const scriptTag = document.createElement("script");
      scriptTag.src = _P + scriptPath;
      scriptTag.defer = true;
      document.body.appendChild(scriptTag);
    });
  }

  window.toast = function(msg, kind, detail, options) {

    kind = kind || "info";

    if (window.NGISUI && window.NGISUI.toast) {

      /* Full async lifecycle: window.toast('Saving…', 'loading', '', { promise }) */
      if (kind === "loading" && options && options.promise) {
        const p = window.NGISUI.toast.operation(msg, options.promise, options);
        p.catch(() => { /* state already rendered by the feedback row */ });
        return p;
      }
      if (kind === "loading") {
        return window.NGISUI.toast.loading(msg, detail || "");
      }

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


/* =========================================================================
   NGIS SIDEBAR SYSTEM v2 — shared enhancement layer
   -------------------------------------------------------------------------
   Runs once per document, after the legacy shell mounts. No framework, no
   extra network call per interaction, no duplicate listeners, no re-render:

     - removes duplicate sidebars / scrims / hamburger ids
     - keeps the current portal's identity (never renders two global navs)
     - enriches rows with accessible tooltips, aria-current, aria-expanded
     - gives the mobile drawer dialog semantics, a focus trap and focus restore
     - filters navigation by the SERVER-evaluated access document
     - gates the current direct URL through the same server resolver

   Shared by all portals: portal-specific navigation content still comes from
   /api/nav/published; only the shell behaviour lives here.
   ========================================================================= */
(function (window, document) {
  'use strict';
  if (window.__NGIS_SIDEBAR_V2__) return;
  window.__NGIS_SIDEBAR_V2__ = true;

  var ACCESS_CACHE_KEY = 'ngis-nav-access-v2';
  var sidebar = null;
  var stateObserver = null;
  var bodyObserver = null;
  var access = { hidden_pages: [], denied_pages: [], hidden_files: [],
                 hidden_keys: [], denied_keys: [] };

  /* Portal directory from the URL. Nav ids such as "dashboard" repeat in every
     portal, so access keys must always be qualified with the owning portal. */
  function portalDir() {
    var m = (window.location.pathname || '').toLowerCase().match(/\/pages\/([^/]+)\//);
    return m ? m[1] : '';
  }

  function navPortals() {
    var list = [];
    if (sidebar) {
      var role = (sidebar.getAttribute('data-portal-role') || '').toLowerCase();
      var pp = (sidebar.getAttribute('data-portal-path') || '').toLowerCase();
      if (role) list.push(role);
      if (pp && list.indexOf(pp) === -1) list.push(pp);
    }
    var dir = portalDir();
    if (dir && list.indexOf(dir) === -1) list.push(dir);
    return list;
  }
  var opener = null;
  var focusBeforeOpen = null;
  var drawerOpen = false;
  var attached = false;

  /* Keep the first-party identity cookie aligned with the client gate. HTML
     document requests cannot send X-Actor, so the server-side direct-URL gate
     reads this cookie instead. Passive demo sessions stay cookie-free. */
  function writeActorCookie(actor) {
    try {
      document.cookie = actor
        ? 'ngis_actor=' + encodeURIComponent(actor) + '; path=/; max-age=604800; SameSite=Lax'
        : 'ngis_actor=; path=/; max-age=0; SameSite=Lax';
    } catch (e) {}
  }

  /* localStorage is origin-wide, so this works on every page regardless of
     whether auth.js was loaded. That avoids one page erasing the identity
     cookie that another page established. */
  function actorHeader() {
    var value = '';
    try {
      var ls = window.localStorage;
      var passive = ls.getItem('ngis_session_mode') === 'passive';
      var u = null;
      try { u = JSON.parse(ls.getItem('ngis_user') || 'null'); } catch (e) { u = null; }
      if (!u) {
        try { u = JSON.parse(ls.getItem('auth_user') || 'null'); } catch (e) { u = null; }
      }
      var raw = u && (u.email || u.username);
      if (!passive && raw) value = String(raw).trim().toLowerCase();
    } catch (e) { value = ''; }
    writeActorCookie(value);
    return value;
  }

  function authHeaders() {
    var actor = actorHeader();
    return actor ? { 'X-Actor': actor } : {};
  }

  function dedupeShell() {
    ['#sidebar', '#scrim', '#htbHamburger'].forEach(function (selector) {
      var nodes = document.querySelectorAll(selector);
      for (var i = 1; i < nodes.length; i++) {
        if (nodes[i].parentNode) nodes[i].parentNode.removeChild(nodes[i]);
      }
    });
  }

  function labelOf(node) {
    var label = node.querySelector('.nav-link-label, .nav-group-label-text');
    return String((label ? label.textContent : node.textContent) || '').replace(/\s+/g, ' ').trim();
  }

  /* Accessibility: tooltips for the collapsed rail, semantic states for
     active rows and expandable groups. Idempotent — safe after a re-render. */
  function decorate() {
    if (!sidebar) return;
    var rows = sidebar.querySelectorAll('.nav-link, .nav-subgroup-label, .nav-nested-label, .nav-group-label');
    Array.prototype.forEach.call(rows, function (row) {
      var text = labelOf(row);
      if (!text) return;
      if (!row.getAttribute('title')) row.setAttribute('title', text);
      if (/^(A|BUTTON)$/.test(row.tagName) && !row.getAttribute('aria-label')) {
        row.setAttribute('aria-label', text);
      }
      if (/^(A|BUTTON)$/.test(row.tagName) && row.tagName === 'BUTTON' && !row.hasAttribute('type')) {
        row.setAttribute('type', 'button');
      }
    });
    var active = sidebar.querySelector('.nav-link.active');
    if (active) active.setAttribute('aria-current', 'page');
    var toggles = sidebar.querySelectorAll('.nav-group.collapsible > .nav-group-label,' +
      '.nav-subgroup.collapsible > .nav-subgroup-label,' +
      '.nav-nested-group.collapsible > .nav-nested-label');
    Array.prototype.forEach.call(toggles, function (btn) {
      if (btn.tagName === 'BUTTON' && !btn.hasAttribute('aria-expanded')) {
        btn.setAttribute('aria-expanded', btn.parentNode.classList.contains('expanded') ? 'true' : 'false');
      }
    });
  }

  /* Permission-aware visibility. The list is computed by the server; the
     sidebar only reflects it. Direct-URL enforcement is independent. */
  function applyAccess() {
    if (!sidebar || !access) return;
    var ports = navPortals();
    var hasKeys = !!(access.hidden_keys || access.denied_keys);
    var blocked = {};
    /* Qualified keys (portal:id) are the source of truth. Raw ids are only a
       fallback for a legacy cached document, and are portal-scoped by the API. */
    (access.hidden_keys || []).concat(access.denied_keys || []).forEach(function (key) {
      blocked[String(key).toLowerCase()] = true;
    });
    var rawIds = {};
    if (!hasKeys) {
      (access.hidden_pages || []).concat(access.denied_pages || []).forEach(function (id) {
        rawIds[String(id).toLowerCase()] = true;
      });
    }
    var hiddenFiles = {};
    (access.hidden_files || []).forEach(function (f) { hiddenFiles[String(f).toLowerCase()] = true; });

    function isBlocked(id, file) {
      if (id && hasKeys) {
        for (var i = 0; i < ports.length; i++) {
          if (blocked[ports[i] + ':' + id]) return true;
        }
      }
      return (id && rawIds[id]) || (file && hiddenFiles[file]);
    }

    var nodes = sidebar.querySelectorAll('[data-id], [data-subgroup-id], [data-nested-id], [data-group-id]');
    Array.prototype.forEach.call(nodes, function (node) {
      var id = (node.getAttribute('data-id') || node.getAttribute('data-subgroup-id') ||
        node.getAttribute('data-nested-id') || node.getAttribute('data-group-id') || '').toLowerCase();
      var raw = node.getAttribute('data-raw-href') || '';
      var file = raw.split('?')[0].split('#')[0].split('/').pop().toLowerCase();
      if (isBlocked(id, file)) node.setAttribute('data-access-hidden', '1');
      else node.removeAttribute('data-access-hidden');
    });

    /* Collapse containers whose every leaf was removed. */
    var groups = sidebar.querySelectorAll('.nav-group, .nav-subgroup, .nav-nested-group');
    Array.prototype.forEach.call(groups, function (group) {
      var links = group.querySelectorAll('.nav-link');
      if (!links.length) return;
      var visible = 0;
      Array.prototype.forEach.call(links, function (link) {
        if (!link.closest('[data-access-hidden]')) visible++;
      });
      var gid = (group.getAttribute('data-group-id') || group.getAttribute('data-subgroup-id') || '').toLowerCase();
      if (!visible) group.setAttribute('data-access-hidden', '1');
      else if (!isBlocked(gid, '')) group.removeAttribute('data-access-hidden');
    });
  }

  function loadAccess(force) {
    try {
      if (!force) {
        var cached = window.sessionStorage.getItem(ACCESS_CACHE_KEY);
        if (cached) { access = JSON.parse(cached); applyAccess(); return; }
      }
    } catch (e) {}
    if (typeof window.fetch !== 'function') return;
    var query = portalDir() ? '?portal=' + encodeURIComponent(portalDir()) : '';
    window.fetch('/api/roles-mgmt/access' + query, { headers: authHeaders() })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) {
        if (!data || !data.success) return;
        access = {
          enforced: !!data.enforced,
          hidden_pages: data.hidden_pages || [],
          denied_pages: data.denied_pages || [],
          hidden_keys: data.hidden_keys || [],
          denied_keys: data.denied_keys || [],
          hidden_files: data.hidden_files || [],
        };
        try { window.sessionStorage.setItem(ACCESS_CACHE_KEY, JSON.stringify(access)); } catch (e) {}
        applyAccess();
      })
      .catch(function () { /* nav stays available if the API is offline */ });
  }

  function gateCurrentPage() {
    if (typeof window.fetch !== 'function') return;
    var PAGE = window.PAGE || {};
    var file = (window.location.pathname || '').split('/').pop();
    /* Filename + portal is unambiguous. PAGE.active alone is not: nav ids such
       as "dashboard" exist in every portal and would resolve to the wrong one. */
    var page = file || PAGE.active || '';
    if (!page) return;
    var query = '?page=' + encodeURIComponent(page) +
      '&portal=' + encodeURIComponent(portalDir()) +
      '&active=' + encodeURIComponent(PAGE.active || '');
    window.fetch('/api/roles-mgmt/my-access' + query, { headers: authHeaders() })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) {
        if (!data || !data.enforced || data.allowed !== false) return;
        var prefix = (window.location.pathname || '').indexOf('/pages/') !== -1 ? '../../' : '';
        window.location.href = prefix + 'pages/shared/access-denied.html?attempted=' +
          encodeURIComponent(window.location.pathname + window.location.search) +
          '&reason=access_denied';
      })
      .catch(function () {});
  }

  /* Drawer semantics + focus management. Only active in drawer widths. */
  function focusable() {
    if (!sidebar) return [];
    return Array.prototype.filter.call(
      sidebar.querySelectorAll('a[href], button:not([disabled]), input, [tabindex]:not([tabindex="-1"])'),
      function (el) { return el.offsetParent !== null; }
    );
  }

  function onDrawerOpen() {
    if (!sidebar) return;
    sidebar.setAttribute('role', 'dialog');
    sidebar.setAttribute('aria-modal', 'true');
    sidebar.setAttribute('aria-label', 'Navigation menu');
    focusBeforeOpen = opener || document.activeElement;
    window.setTimeout(function () {
      var items = focusable();
      if (items.length && document.activeElement && !sidebar.contains(document.activeElement)) {
        items[0].focus();
      }
    }, 60);
  }

  function onDrawerClose() {
    if (!sidebar) return;
    sidebar.setAttribute('role', 'navigation');
    sidebar.removeAttribute('aria-modal');
    if (focusBeforeOpen && document.contains(focusBeforeOpen) && focusBeforeOpen.focus) {
      try { focusBeforeOpen.focus(); } catch (e) {}
    }
    focusBeforeOpen = null;
  }

  function watchDrawer() {
    if (stateObserver || !sidebar) return;
    drawerOpen = sidebar.classList.contains('open');
    stateObserver = new MutationObserver(function () {
      var isOpen = sidebar.classList.contains('open');
      if (isOpen === drawerOpen) return;
      drawerOpen = isOpen;
      if (isOpen) onDrawerOpen(); else onDrawerClose();
    });
    stateObserver.observe(sidebar, { attributes: true, attributeFilter: ['class'] });
  }

  function attach() {
    if (attached) return;
    var found = document.getElementById('sidebar');
    if (!found) return;
    attached = true;
    dedupeShell();
    sidebar = document.getElementById('sidebar') || found;

    /* Portal identity: record the owning directory without overriding the
       resolved role (superadmin/staff previews remain intact). Dedupe above
       guarantees exactly one global navigation is rendered. */
    var pathMatch = (window.location.pathname || '').toLowerCase().match(/\/pages\/(admin|principal|teacher|student|shared)\//);
    if (pathMatch) sidebar.setAttribute('data-portal-path', pathMatch[1]);
    document.body.setAttribute('data-sidebar-system', 'v2');

    decorate();
    watchDrawer();
    loadAccess(false);
    gateCurrentPage();

    /* Re-apply cheap decorations after any nav re-render, without observing
       attribute churn (which would loop when we write attributes ourselves). */
    if (window.MutationObserver) {
      var navObserver = new MutationObserver(function (mutations) {
        var needsDecorate = false;
        for (var i = 0; i < mutations.length; i++) {
          if (mutations[i].addedNodes.length) { needsDecorate = true; break; }
        }
        if (needsDecorate) { decorate(); applyAccess(); }
      });
      var nav = sidebar.querySelector('.side-nav');
      if (nav) navObserver.observe(nav, { childList: true, subtree: true });
    }
  }

  /* One delegated opener tracker + one focus-trap listener for the whole app. */
  document.addEventListener('click', function (e) {
    var btn = e.target && e.target.closest ? e.target.closest(
      '#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, .hamburger-btn, [data-action="toggle-sidebar"]') : null;
    if (btn) opener = btn;
  }, true);

  document.addEventListener('keydown', function (e) {
    /* Escape / scrim / nav-click closing is already owned by layout.js; the
       class observer above performs the focus restore exactly once. */
    if (e.key !== 'Tab' || !sidebar || !sidebar.classList.contains('open')) return;
    var items = focusable();
    if (!items.length) return;
    var first = items[0], last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }, true);

  function start() {
    attach();
    if (attached) return;
    if (window.MutationObserver) {
      bodyObserver = new MutationObserver(function () {
        if (document.getElementById('sidebar')) { attach(); if (bodyObserver) bodyObserver.disconnect(); }
      });
      bodyObserver.observe(document.body, { childList: true, subtree: false });
    }
    /* layout.js waits up to 1200ms for the published nav; cover that window. */
    window.setTimeout(attach, 1400);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();

  /* Public, minimal API for the access-control workspace to invalidate the
     cached visibility document after a Save & Apply. */
  window.NGIS_SIDEBAR = {
    refreshAccess: function () { loadAccess(true); },
    element: function () { return sidebar; },
    apply: function () { decorate(); applyAccess(); },
  };

  /* Global Modal & Popup Controller bridge */
  if (!window.NGIS_MODAL) {
    var modalScript = document.createElement('script');
    modalScript.src = (function() {
      var currentScript = document.currentScript;
      if (currentScript && currentScript.src) {
        return currentScript.src.replace(/layout\.js.*$/, 'modal-system.js');
      }
      return '../../assets/js/modal-system.js';
    })();
    modalScript.defer = true;
    document.head.appendChild(modalScript);
  }

  /* Global Smart Content Display & Progressive Disclosure System bridge */
  if (!window.SmartDisclosure) {
    var disclosureScript = document.createElement('script');
    disclosureScript.src = (function() {
      var currentScript = document.currentScript;
      if (currentScript && currentScript.src) {
        return currentScript.src.replace(/layout\.js.*$/, 'smart-disclosure.js');
      }
      return '../../assets/js/smart-disclosure.js';
    })();
    disclosureScript.defer = true;
    document.head.appendChild(disclosureScript);
  }

  /* Global UX Copy & UI Kit System bridge (Rules 1-12) */
  if (!window.NGIS_COPY) {
    var copyScript = document.createElement('script');
    copyScript.src = (function() {
      var currentScript = document.currentScript;
      if (currentScript && currentScript.src) {
        return currentScript.src.replace(/layout\.js.*$/, 'ngis-copy.js');
      }
      return '../../assets/js/ngis-copy.js';
    })();
    copyScript.defer = true;
    document.head.appendChild(copyScript);
  }

  if (!window.NGISKit) {
    var kitScript = document.createElement('script');
    kitScript.src = (function() {
      var currentScript = document.currentScript;
      if (currentScript && currentScript.src) {
        return currentScript.src.replace(/js\/layout\.js.*$/, 'components/ngis-ui-kit.js');
      }
      return '../../assets/components/ngis-ui-kit.js';
    })();
    kitScript.defer = true;
    document.head.appendChild(kitScript);
  }

  /* Global Skeleton Loading System bridge */
  if (!window.NGIS_SKELETON) {
    var skScript = document.createElement('script');
    skScript.src = (function() {
      var currentScript = document.currentScript;
      if (currentScript && currentScript.src) {
        return currentScript.src.replace(/layout\.js.*$/, 'skeleton-system.js');
      }
      return '../../assets/js/skeleton-system.js';
    })();
    skScript.defer = true;
    document.head.appendChild(skScript);
  }

  /* Global Runtime UX Writing & State Normalizer (Rules 1–12) */
  function normalizeUXWritingAndStates() {
    try {
      // 1. Sanitize Toast Messages (Rule 12: eliminate filler words)
      if (typeof window.toast === 'function' && !window.toast.__ngisSanitized) {
        var origToast = window.toast;
        window.toast = function(msg, type) {
          if (typeof msg === 'string') {
            msg = msg.replace(/\b(successfully|has been successfully|was successfully)\b/gi, '')
                     .replace(/\bhas been\s+/gi, '')
                     .replace(/\bhave been\s+/gi, '')
                     .replace(/\bplease note that\s+/gi, '')
                     .replace(/\s{2,}/g, ' ')
                     .trim();
          }
          /* Forward every argument — detail and options (incl. {promise})
             must reach the underlying feedback engine untouched. */
          return origToast.apply(this, arguments);
        };
        window.toast.__ngisSanitized = true;
      }

      // 2. Normalize bare buttons (Rule 8: verb + noun, no bare 'Submit', 'OK', 'Yes', 'Next')
      document.querySelectorAll('button, a.btn, .btn').forEach(function(btn) {
        var txt = btn.textContent.trim();
        if (txt === 'Submit') {
          var isSearch = btn.closest('form') && (btn.closest('form').id.indexOf('search') !== -1 || btn.closest('form').id.indexOf('filter') !== -1);
          btn.textContent = isSearch ? 'Search Records' : 'Save Changes';
        } else if (txt === 'Next') {
          btn.textContent = 'Next Page';
        } else if (txt === 'OK' || txt === 'Ok') {
          btn.textContent = 'Confirm';
        } else if (txt === 'Yes') {
          btn.textContent = 'Confirm';
        } else if (txt === 'Learn More' || txt === 'Learn more') {
          btn.textContent = 'View Details';
        }
      });

      // 3. Normalize semantic badge colors (Rule 9)
      document.querySelectorAll('.badge, [class*="badge-"]').forEach(function(badge) {
        var text = (badge.textContent || '').trim().toLowerCase();
        if (text === 'urgent' || text === 'overdue' || text === 'failed' || text === 'expired' || text === 'rejected') {
          if (!badge.classList.contains('badge-danger') && !badge.classList.contains('red')) {
            badge.classList.add('badge-danger');
          }
        } else if (text === 'pending' || text === 'in progress' || text === 'review' || text === 'draft' || text === 'on hold') {
          if (!badge.classList.contains('badge-warning') && !badge.classList.contains('amber')) {
            badge.classList.add('badge-warning');
          }
        } else if (text === 'active' || text === 'published' || text === 'completed' || text === 'approved' || text === 'present') {
          if (!badge.classList.contains('badge-success') && !badge.classList.contains('green')) {
            badge.classList.add('badge-success');
          }
        }
      });
    } catch(err) {
      // safe fallback
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', normalizeUXWritingAndStates);
  } else {
    normalizeUXWritingAndStates();
  }
  window.setTimeout(normalizeUXWritingAndStates, 500);
})(window, document);

