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
      brand: "Admin", meta: "New Gateway International School",
      groups: [
        { id:"main", links:[
          { id:"dashboard", label:"Dashboard", icon:"dashboard", href:"pages/admin/admin.html" },
        ]},
        { id:"system", label:"ប្រព័ន្ធ", icon:"settings", collapsible:true, links:[
          { id:"school-info", label:"ព័ត៌មានសាលារៀន", href:"pages/admin/admin-settings.html?tab=school" },
          { id:"academic-structure", label:"កំណត់រចនាសម្ព័ន្ធឆ្នាំសិក្សា", collapsible:true, children:[
            { id:"academic-year", label:"ឆ្នាំសិក្សា", href:"pages/admin/admin-settings.html?tab=academic" },
            { id:"academic-weeks", label:"សប្តាហ៍", href:"pages/admin/admin-timetables.html?tab=weeks" },
            { id:"exam-structure", label:"កំណត់រចនាសម្ព័ន្ធការប្រឡង", href:"pages/admin/admin-exams.html" },
            { id:"score-locking", label:"ការកំណត់រចនាសម្ព័ន្ធចាក់សោពិន្ទុ", href:"pages/admin/admin-grades.html" },
            { id:"set-curriculum", label:"កំណត់កម្មវិធីសិក្សា", href:"pages/admin/admin-departments.html" },
            { id:"curriculum-design", label:"ការរចនាកម្មវិធីសិក្សា", href:"pages/admin/admin-lessons.html" },
            { id:"create-classes", label:"បង្កើតថ្នាក់រៀន", href:"pages/admin/admin-classes.html" },
            { id:"student-rollforward", label:"រៀបចំសិស្សឆ្នាំសិក្សាចាស់ទៅឆ្នាំសិក្សាថ្មី", href:"pages/admin/admin-users.html?role=students&action=rollforward" },
            { id:"assign-teachers", label:"ចាត់តាំងគ្រូបច្ចេកទេស និងគ្រូត្រួតពិនិត្យ", href:"pages/admin/admin-users.html?role=teachers&tab=assignment" },
          ]},
          { id:"account-management", label:"ការគ្រប់គ្រងគណនី", collapsible:true, children:[
            { id:"teacher-group-roles", label:"ការកំណត់តួនាទីលើក្រុមគណនីគ្រូ", href:"pages/admin/admin-settings.html?tab=roles" },
            { id:"teacher-accounts", label:"គណនីគ្រូ", href:"pages/admin/admin-users.html?role=teachers" },
            { id:"student-accounts", label:"គណនីសិស្ស", href:"pages/admin/admin-users.html?role=students" },
            { id:"guardian-accounts", label:"គណនីអាណាព្យាបាល", href:"pages/admin/admin-users.html?role=parents" },
          ]},
          { id:"system-timetable", label:"កាលវិភាគ", href:"pages/admin/admin-timetables.html" },
          { id:"general-settings", label:"ការកំណត់ទូទៅ", href:"pages/admin/admin-settings.html" },
        ]},
        { id:"users", label:"ការគ្រប់គ្រងរបស់គ្រូបង្រៀន", icon:"co_present", collapsible:true, links:[
          { id:"teachers",   label:"Teachers",   icon:"co_present",         href:"pages/admin/admin-users.html?role=teachers" },
          { id:"admins",     label:"Admins",     icon:"admin_panel_settings", href:"pages/admin/admin-users.html?role=admins" },
          { id:"principals", label:"Principals", icon:"military_tech",      href:"pages/admin/admin-users.html?role=principals" },
        ]},
        { id:"records", label:"ការគ្រប់គ្រងទិន្នន័យសិស្ស", icon:"school", collapsible:true, links:[
          { id:"students",   label:"Students",   icon:"school",             href:"pages/admin/admin-users.html?role=students" },
          { id:"parents",    label:"Parents",    icon:"family_restroom",    href:"pages/admin/admin-users.html?role=parents" },
          { id:"services",    label:"Student Services", icon:"assignment", href:"pages/admin/admin-services.html" },
          { id:"profiles",    label:"Student Profiles", icon:"badge",      href:"pages/admin/admin-users.html?role=students" },
        ]},
        { id:"academic", label:"ការបង្រៀន និងការវាយតម្លៃ", icon:"co_present", collapsible:true, links:[
          { id:"departments", label:"Departments", icon:"apartment",          href:"pages/admin/admin-departments.html" },
          { id:"campuses",    label:"Campuses",    icon:"location_city",      href:"pages/admin/admin-campuses.html" },
          { id:"classes",     label:"Classes",     icon:"school",             href:"pages/admin/admin-classes.html" },
          { id:"timetables",  label:"Timetable",   icon:"calendar_view_week", href:"pages/admin/admin-timetables.html" },
          { id:"lessons",     label:"Lessons",     icon:"menu_book",  href:"pages/admin/admin-lessons.html" },
          { id:"assignments", label:"Assignments", icon:"assignment", href:"pages/admin/admin-assignments.html" },
        ]},
        { id:"learning", label:"ការប្រឡង", icon:"edit_note", collapsible:true, links:[
          { id:"exams",       label:"Exams",       icon:"edit_note",  href:"pages/admin/admin-exams.html" },
          { id:"grades",      label:"Grades",      icon:"grade",      href:"pages/admin/admin-grades.html" },
        ]},
        { id:"reports-group", label:"របាយការណ៍ និងស្ថិតិ", icon:"query_stats", collapsible:true, links:[
          { id:"reports",     label:"Reports",         icon:"assessment", href:"pages/admin/admin-reports.html" },
          { id:"logs",        label:"Audit Logs",         icon:"history",     href:"pages/admin/admin-logs.html" },
        ]},
        { id:"messaging", label:"ប្រអប់សារ", icon:"mail", links:[
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
        { id:"administration", label:"កន្លែងផ្ទុកទិន្នន័យមេ", icon:"travel_explore", collapsible:true, links:[
          { id:"settings",    label:"System Settings",    icon:"settings",    href:"pages/admin/admin-settings.html" },
          { id:"roles",       label:"Roles & Permissions", icon:"shield_person", href:"pages/admin/admin-settings.html?tab=roles" },
          { id:"backup",      label:"Backup & Restore",   icon:"backup",      href:"pages/admin/admin-settings.html?tab=backup" },
        ]},
        { id:"moodle", label:"Moodle Extension", icon:"extension", collapsible:true, links:[
          { id:"moodle-courses", label:"Moodle Courses", icon:"school", href:"pages/admin/admin-lessons.html?src=moodle" },
          { id:"moodle-sync", label:"Moodle Sync", icon:"sync", href:"pages/admin/admin-settings.html?tab=moodle" },
        ]},
        { id:"elearning", label:"E-Learning", icon:"cast_for_education", links:[
          { id:"elearning-portal", label:"E-Learning Platform", icon:"cast_for_education", href:"pages/admin/admin-lessons.html" },
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
        { links:[
          { id:"dashboard", label:"Dashboard", icon:"home", href:"pages/teacher/teacher.html", chevron:false },
          { id:"classes",   label:"My Class",  icon:"school", href:"pages/teacher/teacher-classes.html" },
        ]},
        { id:"teaching", label:"TEACHING & LEARNING", links:[
          { id:"lessons",     label:"Lessons & Materials", icon:"menu_book", href:"pages/teacher/teacher-lessons.html" },
          { id:"assignments", label:"Assignments", icon:"assignment", href:"pages/teacher/teacher-assignments.html" },
          { id:"submissions", label:"Student Submissions", icon:"description", href:"pages/teacher/teacher-grades.html" },
          { id:"departments", label:"Class Resources", icon:"folder", href:"pages/teacher/teacher-departments.html" },
        ]},
        { id:"communication", label:"COMMUNICATION", links:[
          { id:"announcements", label:"Class Announcements", icon:"campaign", href:"pages/shared/announcements.html?portal=teacher" },
          { id:"class-chats",   label:"Class Chat", icon:"chat", href:"pages/messaging/class-chats.html" },
          { id:"chat",          label:"Student Feedback", icon:"person_search", href:"pages/shared/chat.html?portal=teacher" },
        ]},
        { id:"academic-tools", label:"ACADEMIC TOOLS", links:[
          { id:"gradebook", label:"Gradebook", icon:"grade", href:"pages/teacher/teacher-gradebook.html" },
          { id:"calendar", label:"Timetable", icon:"calendar_month", href:"pages/teacher/teacher-calendar.html" },
          { id:"reports",  label:"Class Reports", icon:"analytics", href:"pages/teacher/teacher-grades.html?tab=reports" },
          { id:"profile",  label:"Class Settings", icon:"settings", href:"pages/teacher/teacher-profile.html" },
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
          { id:"calendar",    label:"Calendar", icon:"calendar_month", href:"pages/student/student-calendar.html" },
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
    principal: {
      brand: "Principal", meta: "Executive Leadership · 2025–26",
      groups: [
        { label:"Overview", icon:"dashboard", links:[
          { id:"dashboard", label:"Executive Dashboard", icon:"dashboard", href:"pages/principal/principal.html" },
          { id:"approvals", label:"Executive Approvals", icon:"verified",  href:"pages/principal/principal-approvals.html" },
        ]},
        { id:"academic-oversight", label:"Academic Leadership", icon:"school", collapsible:true, links:[
          { id:"reports",     label:"Academic Reports",  icon:"assessment", href:"pages/principal/principal-reports.html" },
          { id:"classes",     label:"Classes & Cohorts", icon:"school",     href:"pages/admin/admin-classes.html" },
          { id:"departments", label:"Departments",        icon:"apartment",  href:"pages/admin/admin-departments.html" },
          { id:"campuses",    label:"Campuses",           icon:"location_city", href:"pages/admin/admin-campuses.html" },
          { id:"grades",      label:"Academic Grades",    icon:"grade",      href:"pages/admin/admin-grades.html" },
          { id:"exams",       label:"Examinations",       icon:"edit_note",  href:"pages/admin/admin-exams.html" },
        ]},
        { id:"faculty-students", label:"Faculty & Students", icon:"group", collapsible:true, links:[
          { id:"teachers",   label:"Teacher Oversight",  icon:"co_present", href:"pages/admin/admin-users.html?role=teachers" },
          { id:"students",   label:"Student Records",    icon:"school",     href:"pages/admin/admin-users.html?role=students" },
          { id:"attendance", label:"Attendance Summary", icon:"how_to_reg",  href:"pages/admin/admin-attendance.html" },
        ]},
        { id:"messaging", label:"Messaging", icon:"forum", links:[
          { id:"campus-announcements", label:"Campus Announcements", icon:"campaign", href:"pages/messaging/campus-announcements.html" },
          { id:"announcements",       label:"School Announcements", icon:"newspaper", href:"pages/shared/announcements.html", badge:"3" },
          { id:"chat",                label:"Direct Messages",      icon:"mail",      href:"pages/shared/chat.html", badge:"2" },
          { id:"group-chat",          label:"Leadership Forum",     icon:"groups",    href:"pages/shared/group-chat.html", badge:"3" },
        ]},
        { label:"Account", icon:"person", links:[
          { id:"profile",       label:"Executive Profile", icon:"person", href:"pages/principal/principal-profile.html" },
        ]},
      ],
    },
    staff: {
      brand: "Staff", meta: "Campus Operations · 2025–26",
      groups: [
        { label:"Main", icon:"home", links:[
          { id:"dashboard", label:"Operations Dashboard", icon:"dashboard", href:"pages/staff/staff.html" },
        ]},
        { id:"operations", label:"Services & Operations", icon:"room_service", collapsible:true, links:[
          { id:"services",    label:"Service Requests",     icon:"assignment",        href:"pages/staff/staff-services.html" },
          { id:"timetables",  label:"Facility Schedules",   icon:"calendar_view_week", href:"pages/admin/admin-timetables.html" },
          { id:"classes",     label:"Class Directory",      icon:"school",             href:"pages/admin/admin-classes.html" },
        ]},
        { id:"messaging", label:"Messaging", icon:"forum", links:[
          { id:"campus-announcements", label:"Campus Announcements", icon:"campaign",  href:"pages/messaging/campus-announcements.html" },
          { id:"announcements",       label:"School Announcements", icon:"newspaper", href:"pages/shared/announcements.html", badge:"2" },
          { id:"department-channels", label:"Department Channels",  icon:"apartment", href:"pages/messaging/department-channels.html" },
          { id:"chat",                label:"Direct Messages",      icon:"mail",       href:"pages/shared/chat.html", badge:"1" },
          { id:"group-chat",          label:"Staff Forum",          icon:"groups",     href:"pages/shared/group-chat.html", badge:"2" },
        ]},
        { label:"Account", icon:"person", links:[
          { id:"profile",       label:"Staff Profile", icon:"person", href:"pages/staff/staff-profile.html" },
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
      { id:"classes",    label:"My Class",   icon:"school",        href:"pages/teacher/teacher-classes.html" },
      { id:"notifications",label:"Alerts",   icon:"notifications", href:"pages/teacher/teacher-notifications.html", badge:"3" },
      { id:"profile",    label:"Profile",    icon:"person",        href:"pages/teacher/teacher-profile.html" },
    ],
    student: [
      { id:"dashboard",    label:"Home",       icon:"home",      href:"pages/student/student.html" },
      { id:"departments",  label:"Department", icon:"apartment", href:"pages/shared/departments.html" },
      { id:"announcements",label:"Alerts",     icon:"campaign",  href:"pages/shared/announcements.html", badge:"3" },
      { id:"profile",      label:"Profile",    icon:"person",    href:"pages/student/student-profile.html" },
    ],
    principal: [
      { id:"dashboard",  label:"Home",       icon:"home",           href:"pages/principal/principal.html" },
      { id:"reports",    label:"Reports",    icon:"assessment",     href:"pages/principal/principal-reports.html" },
      { id:"approvals",  label:"Approvals",  icon:"verified",       href:"pages/principal/principal-approvals.html" },
      { id:"profile",    label:"Profile",    icon:"person",         href:"pages/principal/principal-profile.html" },
    ],
    staff: [
      { id:"dashboard",  label:"Home",       icon:"home",           href:"pages/staff/staff.html" },
      { id:"services",   label:"Services",   icon:"assignment",     href:"pages/staff/staff-services.html" },
      { id:"announcements",label:"Alerts",   icon:"campaign",       href:"pages/shared/announcements.html", badge:"2" },
      { id:"profile",    label:"Profile",    icon:"person",         href:"pages/staff/staff-profile.html" },
    ],
  };

  /* Central quick-chat action shown between the left and right dock items */
  const CHAT = {
    admin:     { label:"Group Chat", href:"pages/shared/group-chat.html", badge:"4" },
    teacher:   { label:"Chat",       href:"pages/shared/chat.html", badge:"3" },
    student:   { label:"Chat",       href:"pages/shared/chat.html", badge:"3" },
    principal: { label:"Forum",      href:"pages/shared/group-chat.html", badge:"3" },
    staff:     { label:"Chat",       href:"pages/shared/chat.html", badge:"1" },
  };

  const DEFAULT_USER = {
    admin:     { name:"Sok Panha Heng",  role:"Super Administrator",  initials:"SH" },
    teacher:   { name:"Oudom Seila", role:"Teacher", initials:"OS" },
    student:   { name:"Nrinphouneta Hok", role:"Student · Grade 11-A", initials:"NH" },
    principal: { name:"Dr. Ly Bunheng",  role:"Campus Principal",     initials:"LB" },
    staff:     { name:"Ms. Sreymom Lim", role:"Operations Coordinator", initials:"SL" },
  };

  const PORTAL_HOME = {
    admin: "pages/admin/admin.html",
    teacher: "pages/teacher/teacher.html",
    student: "pages/student/student.html",
    principal: "pages/principal/principal.html",
    staff: "pages/staff/staff.html"
  };

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
    const match = path.match(/\/pages\/(admin|teacher|student|parent|staff|principal)\//);
    const pathRole = match ? match[1] : null;
    const sessionRole = getSessionRole();

    // Priority 1: Explicit non-student portal directory path
    if (pathRole && pathRole !== "student") {
      try { localStorage.setItem("ngis_active_portal", pathRole); } catch (e) {}
      return pathRole;
    }

    // Priority 2: Explicit URL query param
    const params = new URLSearchParams(window.location.search || "");
    const queryRole = (params.get("portal") || params.get("role") || "").toLowerCase();
    if (["admin", "teacher", "student", "staff", "principal"].includes(queryRole)) {
      try { localStorage.setItem("ngis_active_portal", queryRole); } catch (e) {}
      return queryRole;
    }

    // Priority 3: Visiting student directory — respect active staff/teacher/admin/principal session
    if (pathRole === "student") {
      if (sessionRole && sessionRole !== "student") {
        return sessionRole;
      }
      try { localStorage.setItem("ngis_active_portal", "student"); } catch (e) {}
      return "student";
    }

    // Priority 4: Stored portal preference
    const storedPortal = localStorage.getItem("ngis_active_portal");
    if (storedPortal && ["admin", "teacher", "student", "staff", "principal"].includes(storedPortal)) {
      if (sessionRole && storedPortal === "student" && sessionRole !== "student") {
        return sessionRole;
      }
      return storedPortal;
    }

    return normalizeRole(pageRole) || sessionRole || "student";
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

  function buildSidebar(cfg, active, user) {
    const role = (window.PAGE && window.PAGE.role) || "admin";
    const homeHref = PORTAL_HOME[role] ? `${_P}${PORTAL_HOME[role]}` : `${_P}index.html`;
    const currentUser = user || (window.PAGE && window.PAGE.user) || DEFAULT_USER[role] || DEFAULT_USER.teacher;

    function linkHasId(item, id) {
      if (!item) return false;
      if (item.id === id) return true;
      if (item.children && item.children.some(c => c.id === id)) return true;
      return false;
    }

    // Auto-detect active link if not set or doesn't match any link in this portal
    let effectiveActive = active;
    if (!effectiveActive || !cfg.groups.some(g => g.links.some(l => linkHasId(l, effectiveActive)))) {
      const curFile = (window.location.pathname || '').replace(/\\/g, '/').split('/').pop().toLowerCase();
      for (const g of cfg.groups) {
        for (const l of g.links) {
          if (l.children && l.children.length > 0) {
            for (const sub of l.children) {
              const linkFile = (sub.href || '').split('?')[0].split('/').pop().toLowerCase();
              if (linkFile && linkFile === curFile) {
                effectiveActive = sub.id;
                break;
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

    const groups = cfg.groups.map((g, gi) => {
      const links = g.links.map(l => {
        if (l.children && l.children.length > 0) {
          const sublinks = l.children.map(sub =>
            `<a class="nav-link nav-sub-link ${sub.id === effectiveActive ? "active" : ""}" href="${_P}${sub.href}"${sub.id===effectiveActive?' aria-current="page"':''} data-id="${sub.id}">
               ${sub.icon ? `<span class="material-symbols-outlined nav-link-icon">${sub.icon}</span>` : ""}
               <span class="nav-link-label">${esc(sub.label)}</span>
               ${sub.badge ? `<span class="pill">${sub.badge}</span>` : ""}
               ${sub.chevron !== false ? `<span class="material-symbols-outlined nav-link-chevron">chevron_right</span>` : ""}
             </a>`
          ).join("");
          const isSubActive = l.children.some(sub => sub.id === effectiveActive);
          return `
            <div class="nav-subgroup${l.collapsible ? ' collapsible' : ''}${isSubActive ? ' expanded' : ''}">
              <button type="button" class="nav-subgroup-label" aria-expanded="${isSubActive ? 'true' : 'false'}" title="${esc(l.label)}">
                <span>${esc(l.label)}</span>
                <span class="material-symbols-outlined ngl-subchevron">expand_more</span>
              </button>
              <div class="nav-subgroup-links">
                <div>${sublinks}</div>
              </div>
            </div>`;
        }
        return `<a class="nav-link ${l.icon ? '' : 'no-icon'} ${l.id === effectiveActive ? "active" : ""}" href="${_P}${l.href}"${l.id===effectiveActive?' aria-current="page"':''} data-id="${l.id}">
           ${l.icon ? `<span class="material-symbols-outlined nav-link-icon">${l.icon}</span>` : ""}
           <span class="nav-link-label">${esc(l.label)}</span>
           ${l.badge ? `<span class="pill">${l.badge}</span>` : ""}
           ${l.chevron !== false && l.id !== 'dashboard' ? `<span class="material-symbols-outlined nav-link-chevron">chevron_right</span>` : ""}
         </a>`;
      }).join("");
      const groupActive = g.id === effectiveActive || g.links.some(l => linkHasId(l, effectiveActive));
      const labelInner = `
        ${g.icon ? `<span class="material-symbols-outlined nav-group-icon">${g.icon}</span>` : ""}
        <span class="nav-group-label-text">${esc(g.label || "")}</span>
        <span class="nav-group-label-rule"></span>
        ${g.collapsible ? `<span class="material-symbols-outlined ngl-chevron">expand_more</span>` : ""}`;

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
        <header class="side-brand">
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
        </header>

        <div class="side-user-card" id="sideUserCard" data-purpose="user-profile-card">
          <div class="side-user-avatar">
            <span class="material-symbols-outlined side-user-icon">person</span>
            <span class="side-user-status" title="Online"></span>
          </div>
          <div class="side-user-info">
            <div class="side-user-name">${esc(currentUser.name)}</div>
            <div class="side-user-role">${esc(currentUser.role)}</div>
          </div>
          <span class="material-symbols-outlined side-user-caret">expand_more</span>
        </div>

        <nav class="side-nav custom-scrollbar" aria-label="Main Navigation">
          ${groups}
        </nav>

        <footer class="side-foot">
          <a class="nav-link side-foot-help" href="${_P}pages/teacher/teacher-profile.html?tab=help">
            <span class="material-symbols-outlined nav-link-icon">help_outline</span>
            <span class="nav-link-label">Help &amp; Support</span>
            <span class="material-symbols-outlined nav-link-chevron">chevron_right</span>
          </a>
          <a class="nav-link nav-link-danger side-foot-signout" href="${_P}index.html" data-purpose="sign-out-button">
            <span class="material-symbols-outlined nav-link-icon">logout</span>
            <span class="nav-link-label">Sign Out</span>
            <span class="material-symbols-outlined nav-link-chevron">chevron_right</span>
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

  const MOB_NAV_TABS = {
    student: [
      { id: "home", label: "Home", icon: "ph-fill ph-house-simple", href: "pages/student/student.html" },
      { id: "department", label: "Departments", icon: "ph-bold ph-buildings", href: "pages/shared/departments.html" },
      { id: "chat", label: "Chat", icon: "ph-fill ph-chat-circle-dots", href: "pages/student/student-chat.html", isCenter: true },
      { id: "alerts", label: "Alerts", icon: "ph-bold ph-bell", href: "pages/student/student-notifications.html", hasDot: true },
      { id: "profile", label: "Profile", icon: "ph-bold ph-user", href: "pages/student/student-profile.html" },
    ],
    teacher: [
      { id: "home", label: "Home", icon: "ph-fill ph-house-simple", href: "pages/teacher/teacher.html" },
      { id: "classes", label: "My Class", icon: "ph-bold ph-chalkboard-teacher", href: "pages/teacher/teacher-classes.html" },
      { id: "chat", label: "Chat", icon: "ph-fill ph-chat-circle-dots", href: "pages/shared/chat.html?portal=teacher", isCenter: true },
      { id: "alerts", label: "Alerts", icon: "ph-bold ph-bell", href: "pages/teacher/teacher-notifications.html", hasDot: true },
      { id: "profile", label: "Profile", icon: "ph-bold ph-user", href: "pages/teacher/teacher-profile.html" },
    ],
    admin: [
      { id: "home", label: "Home", icon: "ph-fill ph-house-simple", href: "pages/admin/admin.html" },
      { id: "users", label: "Users", icon: "ph-bold ph-users-four", href: "pages/admin/admin-users.html" },
      { id: "chat", label: "Chat", icon: "ph-fill ph-chat-circle-dots", href: "pages/shared/group-chat.html", isCenter: true },
      { id: "alerts", label: "Alerts", icon: "ph-bold ph-bell", href: "pages/admin/admin-logs.html", hasDot: true },
      { id: "settings", label: "Settings", icon: "ph-bold ph-gear", href: "pages/admin/admin-settings.html" },
    ],
    principal: [
      { id: "home", label: "Home", icon: "ph-fill ph-house-simple", href: "pages/principal/principal.html" },
      { id: "reports", label: "Reports", icon: "ph-bold ph-chart-line-up", href: "pages/admin/admin-reports.html" },
      { id: "chat", label: "Chat", icon: "ph-fill ph-chat-circle-dots", href: "pages/shared/group-chat.html", isCenter: true },
      { id: "alerts", label: "Alerts", icon: "ph-bold ph-bell", href: "pages/admin/admin-logs.html", hasDot: true },
      { id: "settings", label: "Settings", icon: "ph-bold ph-gear", href: "pages/admin/admin-settings.html" },
    ],
    staff: [
      { id: "home", label: "Home", icon: "ph-fill ph-house-simple", href: "pages/staff/staff.html" },
      { id: "services", label: "Services", icon: "ph-bold ph-stack", href: "pages/admin/admin-services.html" },
      { id: "chat", label: "Chat", icon: "ph-fill ph-chat-circle-dots", href: "pages/shared/chat.html", isCenter: true },
      { id: "alerts", label: "Alerts", icon: "ph-bold ph-bell", href: "pages/shared/announcements.html", hasDot: true },
      { id: "profile", label: "Profile", icon: "ph-bold ph-user", href: "pages/staff/staff-profile.html" },
    ],
  };

  function getRoleActiveTab(role, active) {
    const path = (window.location.pathname || '').toLowerCase();
    const file = (path.split('/').pop() || '').toLowerCase();
    if (file === `${role}.html` || (active === 'dashboard' && file.indexOf(`${role}-`) === -1)) return 'home';
    if (file.indexOf('chat') !== -1 || active === 'chat' || active === 'teacher-chat' || active === 'group-chat' || active === 'class-chats') return 'chat';
    if (file.indexOf('notification') !== -1 || file.indexOf('announcement') !== -1 || file.indexOf('log') !== -1 || active === 'notifications' || active === 'announcements' || active === 'alerts' || active === 'logs') return 'alerts';
    if (file.indexOf('profile') !== -1 || file.indexOf('setting') !== -1 || active === 'profile' || active === 'settings' || active === 'preferences') {
      return (role === 'admin' || role === 'principal') ? 'settings' : 'profile';
    }
    if (role === 'teacher' && (file.indexOf('class') !== -1 || active === 'classes')) return 'classes';
    if (role === 'admin' && (file.indexOf('user') !== -1 || active === 'users' || active === 'admins' || active === 'teachers' || active === 'students' || active === 'parents')) return 'users';
    if (role === 'principal' && (file.indexOf('report') !== -1 || active === 'reports')) return 'reports';
    if (role === 'staff' && (file.indexOf('service') !== -1 || active === 'services')) return 'services';
    if (role === 'student' && (file.indexOf('department') !== -1 || active === 'departments')) return 'department';
    return 'home';
  }

  function buildBottomNav(role, active) {
    const tabs = MOB_NAV_TABS[role] || MOB_NAV_TABS.student;
    const curTab = getRoleActiveTab(role, active);
    const itemsHtml = tabs.map(tab => {
      const isActive = tab.id === curTab;
      if (tab.isCenter) {
        return `
          <a href="${_P}${tab.href}" class="mob-bn-item mob-bn-chat ${isActive ? 'is-active' : ''}" data-tab="${tab.id}" aria-label="${esc(tab.label)}"${isActive ? ' aria-current="page"' : ''}>
            <span class="mob-bn-icon-row">
              <span class="mob-bn-chat-core">
                <i class="${tab.icon}"></i>
              </span>
            </span>
          </a>`;
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
        <button class="sidebar-expand-btn hamburger-btn" id="sidebarExpandBtn" title="Open navigation" aria-label="Open menu" data-action="toggle-sidebar" type="button">
          <svg class="side-expand-svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>`);
      sidebar.appendChild(expandBtn);
    } else if (expandBtn.parentElement !== sidebar) {
      sidebar.appendChild(expandBtn);
    }

    const COLLAPSED_KEY = 'ngis-sidebar-collapsed';
    function setSidebarCollapsed(collapsed) {
      const brandLogo = sidebar.querySelector('.side-brand-crest') || sidebar.querySelector('.side-brand-logo-img');
      if (collapsed) {
        sidebar.classList.add('collapsed');
        main.classList.add('sidebar-collapsed');
        document.body.classList.add('sidebar-collapsed');
        expandBtn.classList.add('visible');
        expandBtn.setAttribute('title', 'Open sidebar');
        expandBtn.setAttribute('aria-label', 'Open navigation');
        if (brandLogo && brandLogo.classList.contains('side-brand-logo-img')) {
          if (!brandLogo.dataset.origSrc) brandLogo.dataset.origSrc = brandLogo.src;
          brandLogo.src = _P + 'assets/images/moeys-sis-logo.png';
        }
        store.set(COLLAPSED_KEY, '1');
      } else {
        sidebar.classList.remove('collapsed');
        main.classList.remove('sidebar-collapsed');
        document.body.classList.remove('sidebar-collapsed');
        expandBtn.classList.add('visible');
        expandBtn.setAttribute('title', 'Collapse sidebar');
        expandBtn.setAttribute('aria-label', 'Collapse sidebar');
        if (brandLogo && brandLogo.classList.contains('side-brand-logo-img') && brandLogo.dataset.origSrc) {
          brandLogo.src = brandLogo.dataset.origSrc;
        }
        store.set(COLLAPSED_KEY, '0');
        setTimeout(() => scrollActiveItemIntoView(false), 160);
      }
      const isExpanded = !collapsed;
      document.querySelectorAll("#menuBtn, #htbHamburger, .htb-hamburger, .menu-btn, .hamburger-btn, [data-action='toggle-sidebar']").forEach(btn => {
        btn.setAttribute("aria-expanded", String(isExpanded));
      });
    }
    // Restore persisted state or default to collapsed on admin as requested
    const savedCollapsed = store.get(COLLAPSED_KEY);
    if (savedCollapsed === '1' || (savedCollapsed === null && PAGE.role === 'admin')) {
      setSidebarCollapsed(true);
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

    collapseBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      setSidebarCollapsed(true);
    });
    expandBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isCurrentlyCollapsed = sidebar.classList.contains('collapsed');
      setSidebarCollapsed(!isCurrentlyCollapsed);
    });

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
      if (sidebar.classList.contains("collapsed")) {
        sidebar.classList.remove("collapsed");
      }
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
