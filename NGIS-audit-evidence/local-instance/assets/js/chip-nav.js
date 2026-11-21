/**
 * ============================================================================
 * NGIS ERP — Master Global Expanding-Chip Floating Bottom Navigation Engine
 * New Gateway International School · Modern Expanding-Chip Navigation System
 *
 * Requirements & Features:
 * - Floating horizontal capsule container centered at bottom (max-width 480px, height 64px)
 * - Morphing Expanding-Chip: Inactive tabs are compact 48x48px circles with neutral icons;
 *   Active tab expands into a pill with Forest Green (#176B45) background, white icon,
 *   and smooth text label reveal (180-240ms transition)
 * - Strict AGENTS.md compliance: NO BOLD FONTS (font-weight <= 500), official Bootstrap SVGs
 * - Role-specific navigation for Student, Teacher, Principal, Admin, Super Admin, Staff
 * - Automatic active tab detection based on pathname, query, and context
 * - Smooth scroll-to-top when tapping the currently active tab
 * - Multilingual support (English, Khmer, Chinese) synced with navbar.js
 * - Collision avoidance with mobile sidebar drawer, modal dialogs, and virtual keyboard
 * - Tablet & Mobile (<= 1024px) display; Desktop (>= 1025px) suppressed
 * ============================================================================
 */

(function (window, document) {
  "use strict";

  // Prevent multiple instantiations
  if (window.__NGIS_CHIP_NAV_INITIALIZED__) return;
  window.__NGIS_CHIP_NAV_INITIALIZED__ = true;

  /**
   * Official Bootstrap SVGs per AGENTS.md
   */
  const ICONS = {
    home: '<svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor"><path d="M8.707 1.5a1 1 0 0 0-1.414 0L.646 8.146a.5.5 0 0 0 .708.708L2 8.207V13.5A1.5 1.5 0 0 0 3.5 15h9a1.5 1.5 0 0 0 1.5-1.5V8.207l.646.647a.5.5 0 0 0 .708-.708L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293zM13 7.207V13.5a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V7.207l5-5z"/></svg>',
    exams: '<svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor"><path d="M14 0H2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2M1 3.857C1 3.384 1.448 3 2 3h12c.552 0 1 .384 1 .857v10.286c0 .473-.448.857-1 .857H2c-.552 0-1-.384-1-.857z"/></svg>',
    grades: '<svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor"><path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3a.5.5 0 0 0 .372 0L14 7.14V13a1 1 0 0 0-1 1v2h3v-2a1 1 0 0 0-1-1V6.739l.686-.275a.5.5 0 0 0 .025-.917z"/><path d="M4.179 8.88 1 7.428V11a.5.5 0 0 0 .265.44l3 1.5a.5.5 0 0 0 .47-.024l3-1.5A.5.5 0 0 0 8 11V7.428l-3.821 1.452z"/></svg>',
    departments: '<svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor"><path d="M14.763.075A.5.5 0 0 1 15 .5v15a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5V14h-1v1.5a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V10a.5.5 0 0 1 .342-.474L6 7.64V4.5a.5.5 0 0 1 .276-.447l8-4a.5.5 0 0 1 .487.022M6 8.694 1 10.36V15h5zM7 15h2v-1.5a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 .5.5V15h2V1.309l-7 3.5z"/></svg>',
    person: '<svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor"><path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6m2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0m4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4m-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10s-3.516.68-4.168 1.332c-.678.678-.83 1.418-.832 1.664z"/></svg>',
    classes: '<svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6m-5.784 6A2.24 2.24 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.3 6.3 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1zM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5"/></svg>',
    students: '<svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor"><path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3a.5.5 0 0 0 .372 0L14 7.14V13a1 1 0 0 0-1 1v2h3v-2a1 1 0 0 0-1-1V6.739l.686-.275a.5.5 0 0 0 .025-.917z"/><path d="M4.179 8.88 1 7.428V11a.5.5 0 0 0 .265.44l3 1.5a.5.5 0 0 0 .47-.024l3-1.5A.5.5 0 0 0 8 11V7.428l-3.821 1.452z"/></svg>',
    attendance: '<svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor"><path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5M1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4z"/></svg>',
    documents: '<svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor"><path d="M4 0h5.293A1 1 0 0 1 10 .293L13.707 4a1 1 0 0 1 .293.707V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2m5.5 1.5v2a1 1 0 0 0 1 1h2z"/></svg>',
    reports: '<svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor"><path d="M0 0h1v15h15v1H0zm10 3.5a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 .5.5v10a.5.5 0 0 1-.5.5h-4a.5.5 0 0 1-.5-.5zm1 .5v9h3V4zm-5 3a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-.5.5h-4a.5.5 0 0 1-.5-.5zm1 .5v6h3V8zm-5 3a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-.5.5h-4a.5.5 0 0 1-.5-.5zm1 .5v3h3v-3z"/></svg>',
    users: '<svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6m-5.784 6A2.24 2.24 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.3 6.3 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1zM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5"/></svg>',
    settings: '<svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor"><path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492M5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0"/><path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.185 1.184l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.185l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115z"/></svg>',
    services: '<svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor"><path d="M1 2.5A1.5 1.5 0 0 1 2.5 1h3A1.5 1.5 0 0 1 7 2.5v3A1.5 1.5 0 0 1 5.5 7h-3A1.5 1.5 0 0 1 1 5.5zM2.5 2a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5zm6.5.5A1.5 1.5 0 0 1 10.5 1h3A1.5 1.5 0 0 1 15 2.5v3A1.5 1.5 0 0 1 13.5 7h-3A1.5 1.5 0 0 1 9 5.5zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5zM1 10.5A1.5 1.5 0 0 1 2.5 9h3A1.5 1.5 0 0 1 7 10.5v3A1.5 1.5 0 0 1 5.5 15h-3A1.5 1.5 0 0 1 1 13.5zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5zm6.5.5A1.5 1.5 0 0 1 10.5 9h3a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1-1.5 1.5h-3A1.5 1.5 0 0 1 9 13.5zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5z"/></svg>'
  };

  /**
   * Multilingual translations
   */
  const TRANSLATIONS = {
    home: { en: "Home", km: "ទំព័រដើម", zh: "首页" },
    exams: { en: "Exams", km: "ការប្រឡង", zh: "考试" },
    grades: { en: "Grades", km: "ពិន្ទុ", zh: "成绩" },
    departments: { en: "Depts", km: "ដេប៉ាតឺម៉ង់", zh: "院系" },
    profile: { en: "Profile", km: "គណនី", zh: "个人" },
    classes: { en: "Classes", km: "ថ្នាក់រៀន", zh: "班级" },
    students: { en: "Students", km: "សិស្ស", zh: "学生" },
    attendance: { en: "Attendance", km: "វត្តមាន", zh: "出勤" },
    work: { en: "Work", km: "កិច្ចការ", zh: "作业" },
    reports: { en: "Reports", km: "របាយការណ៍", zh: "报告" },
    users: { en: "Users", km: "អ្នកប្រើប្រាស់", zh: "用户" },
    cms: { en: "CMS", km: "មាតិកា", zh: "内容" },
    settings: { en: "Settings", km: "ការកំណត់", zh: "设置" },
    services: { en: "Services", km: "សេវាកម្ម", zh: "服务" },
    lostFound: { en: "Lost&Found", km: "បាត់បង់", zh: "失物" },
    campuses: { en: "Campuses", km: "សាខា", zh: "校区" }
  };

  /**
   * Safe URL Resolver
   */
  function resolveUrl(path) {
    if (window.location.protocol === "file:") {
      const isSub = window.location.pathname.includes("/pages/");
      return (isSub ? "../../" : "") + path;
    }
    return "/" + path.replace(/^\//, "");
  }

  /**
   * Role Configuration with 4-5 Primary Destinations
   */
  const PORTAL_TABS = {
    student: [
      { id: "home", labelKey: "home", icon: "home", href: "pages/student/student.html" },
      { id: "exams", labelKey: "exams", icon: "exams", href: "pages/student/student-exams.html" },
      { id: "grades", labelKey: "grades", icon: "grades", href: "pages/student/student-grades.html" },
      { id: "departments", labelKey: "departments", icon: "departments", href: "pages/shared/department.html" },
      { id: "profile", labelKey: "profile", icon: "person", href: "pages/student/student-profile.html" }
    ],
    teacher: [
      { id: "home", labelKey: "home", icon: "home", href: "pages/teacher/teacher.html" },
      { id: "roster", labelKey: "classes", icon: "classes", href: "pages/teacher/teacher-roster.html" },
      { id: "attendance", labelKey: "attendance", icon: "attendance", href: "pages/teacher/teacher-attendance.html" },
      { id: "work", labelKey: "work", icon: "documents", href: "pages/teacher/teacher-submissions.html" },
      { id: "profile", labelKey: "profile", icon: "person", href: "pages/teacher/teacher-profile.html" }
    ],
    principal: [
      { id: "home", labelKey: "home", icon: "home", href: "pages/principal/principal.html" },
      { id: "classes", labelKey: "classes", icon: "classes", href: "pages/principal/principal-classes.html" },
      { id: "students", labelKey: "students", icon: "students", href: "pages/principal/principal-student-profiles.html" },
      { id: "reports", labelKey: "reports", icon: "reports", href: "pages/principal/principal-reports.html" },
      { id: "profile", labelKey: "profile", icon: "person", href: "pages/principal/principal-profile.html" }
    ],
    admin: [
      { id: "home", labelKey: "home", icon: "home", href: "pages/admin/admin.html" },
      { id: "users", labelKey: "users", icon: "users", href: "pages/admin/admin-users-students.html" },
      { id: "classes", labelKey: "classes", icon: "classes", href: "pages/admin/admin-classes.html" },
      { id: "cms", labelKey: "cms", icon: "reports", href: "pages/admin/admin-dashboard-content.html" },
      { id: "settings", labelKey: "settings", icon: "settings", href: "pages/admin/admin-security.html" }
    ],
    superadmin: [
      { id: "home", labelKey: "home", icon: "home", href: "pages/admin/admin.html" },
      { id: "users", labelKey: "users", icon: "users", href: "pages/admin/admin-users-students.html" },
      { id: "classes", labelKey: "classes", icon: "classes", href: "pages/admin/admin-classes.html" },
      { id: "cms", labelKey: "cms", icon: "reports", href: "pages/admin/admin-dashboard-content.html" },
      { id: "settings", labelKey: "settings", icon: "settings", href: "pages/admin/admin-security.html" }
    ],
    staff: [
      { id: "services", labelKey: "services", icon: "services", href: "pages/admin/admin-services.html" },
      { id: "lostFound", labelKey: "lostFound", icon: "documents", href: "pages/principal/principal-lost-found.html" },
      { id: "campuses", labelKey: "campuses", icon: "departments", href: "pages/admin/admin-campuses.html" },
      { id: "settings", labelKey: "settings", icon: "settings", href: "pages/admin/admin-security.html" }
    ]
  };

  /**
   * Determine current role
   */
  function detectRole() {
    const bodyRole = document.body.getAttribute("data-role");
    if (bodyRole && PORTAL_TABS[bodyRole]) return bodyRole;

    const path = (window.location.pathname || "").toLowerCase();
    if (path.includes("/teacher/")) return "teacher";
    if (path.includes("/principal/")) return "principal";
    if (path.includes("/admin/")) return "admin";
    if (path.includes("/student/")) return "student";

    const userRaw = localStorage.getItem("ngis_user");
    if (userRaw) {
      try {
        const u = JSON.parse(userRaw);
        if (u.role && PORTAL_TABS[u.role.toLowerCase()]) return u.role.toLowerCase();
      } catch (e) {}
    }
    return "student";
  }

  /**
   * Determine active tab based on file and context
   */
  function detectActiveTab(role, tabs) {
    const path = (window.location.pathname || "").toLowerCase();
    const file = (path.split("/").pop() || "").toLowerCase();

    // 1. Exact match on tab's href filename
    for (const tab of tabs) {
      const tabFile = (tab.href.split("/").pop() || "").toLowerCase();
      if (file === tabFile) return tab.id;
    }

    // 2. Contextual mappings per role
    if (role === "student") {
      if (file.includes("exam")) return "exams";
      if (file.includes("grade")) return "grades";
      if (file.includes("department")) return "departments";
      if (file.includes("profile")) return "profile";
      if (file.includes("assignment")) return "exams";
      if (file.includes("student.html") || file === "" || file === "index.html") return "home";
    }

    if (role === "teacher") {
      if (file.includes("roster") || file.includes("class") || file.includes("lesson")) return "roster";
      if (file.includes("attendance")) return "attendance";
      if (file.includes("submission") || file.includes("gradebook") || file.includes("exam") || file.includes("document")) return "work";
      if (file.includes("profile")) return "profile";
      if (file.includes("teacher.html")) return "home";
    }

    if (role === "principal") {
      if (file.includes("class")) return "classes";
      if (file.includes("student") || file.includes("registration")) return "students";
      if (file.includes("report") || file.includes("activity") || file.includes("teacher")) return "reports";
      if (file.includes("profile")) return "profile";
      if (file.includes("principal.html")) return "home";
    }

    if (role === "admin" || role === "superadmin") {
      if (file.includes("user") || file.includes("student") || file.includes("teacher") || file.includes("employee")) return "users";
      if (file.includes("class") || file.includes("timetable")) return "classes";
      if (file.includes("report") || file.includes("dashboard-content") || file.includes("news")) return "cms";
      if (file.includes("setting") || file.includes("security") || file.includes("role") || file.includes("dictionary")) return "settings";
      if (file.includes("admin.html")) return "home";
    }

    return tabs[0].id;
  }

  /**
   * Get current language
   */
  function getLang() {
    return localStorage.getItem("ngis_lang") || "en";
  }

  /**
   * Build the Expanding-Chip Dock HTML
   */
  function renderDock(role) {
    const tabs = PORTAL_TABS[role] || PORTAL_TABS.student;
    const activeId = detectActiveTab(role, tabs);
    const lang = getLang();

    const itemsHtml = tabs.map((tab) => {
      const isActive = tab.id === activeId;
      const labelObj = TRANSLATIONS[tab.labelKey] || { en: tab.id };
      const labelText = labelObj[lang] || labelObj.en;
      const svgIcon = ICONS[tab.icon] || ICONS.home;
      const targetUrl = resolveUrl(tab.href);

      return (
        '<a href="' + targetUrl + '" ' +
          'class="ngis-chip-item' + (isActive ? ' is-active' : '') + '" ' +
          'data-id="' + tab.id + '" ' +
          'data-label-key="' + tab.labelKey + '" ' +
          'aria-label="' + labelText + '" ' +
          'title="' + labelText + '" ' +
          (isActive ? 'aria-current="page" ' : '') +
          'role="tab" ' +
          'aria-selected="' + (isActive ? 'true' : 'false') + '">' +
          '<span class="ngis-chip-icon" aria-hidden="true">' + svgIcon + '</span>' +
          '<span class="ngis-chip-label">' + labelText + '</span>' +
        '</a>'
      );
    }).join("");

    return (
      '<nav class="ngis-chip-dock" id="ngisChipDock" role="navigation" aria-label="Bottom Navigation">' +
        '<div class="ngis-chip-dock-track" role="tablist">' +
          itemsHtml +
        '</div>' +
      '</nav>'
    );
  }

  /**
   * Attach Interaction Listeners
   */
  function bindInteractions(dockEl) {
    if (!dockEl || dockEl.dataset.interactionsBound === "true") return;
    dockEl.dataset.interactionsBound = "true";

    const items = Array.from(dockEl.querySelectorAll(".ngis-chip-item"));

    items.forEach((item) => {
      item.addEventListener("click", function (e) {
        if (item.classList.contains("is-active")) {
          // If tapping already active chip, scroll smoothly to page top
          e.preventDefault();
          window.scrollTo({ top: 0, behavior: "smooth" });
          return;
        }

        // Instant visual feedback: collapse previous active, expand this chip
        items.forEach((it) => {
          it.classList.remove("is-active");
          it.removeAttribute("aria-current");
          it.setAttribute("aria-selected", "false");
        });

        item.classList.add("is-active");
        item.setAttribute("aria-current", "page");
        item.setAttribute("aria-selected", "true");
      });

      // Keyboard arrow navigation
      item.addEventListener("keydown", function (e) {
        let targetIndex = -1;
        const currentIndex = items.indexOf(item);

        if (e.key === "ArrowRight") {
          targetIndex = (currentIndex + 1) % items.length;
        } else if (e.key === "ArrowLeft") {
          targetIndex = (currentIndex - 1 + items.length) % items.length;
        }

        if (targetIndex !== -1) {
          e.preventDefault();
          items[targetIndex].focus();
        }
      });
    });

    // Listen for language changes from navbar.js
    window.addEventListener("ngis:lang-changed", function (e) {
      const newLang = e.detail && e.detail.lang ? e.detail.lang : getLang();
      updateLabels(dockEl, newLang);
    });

    // Handle virtual keyboard and drawer open states
    window.addEventListener("resize", function () {
      if (window.innerHeight < 480) {
        dockEl.classList.add("is-hidden");
      } else {
        dockEl.classList.remove("is-hidden");
      }
    }, { passive: true });
  }

  /**
   * Update text labels when language switches
   */
  function updateLabels(dockEl, lang) {
    if (!dockEl) return;
    const items = dockEl.querySelectorAll(".ngis-chip-item");
    items.forEach((item) => {
      const labelKey = item.getAttribute("data-label-key");
      const labelObj = TRANSLATIONS[labelKey];
      if (labelObj) {
        const text = labelObj[lang] || labelObj.en;
        const labelSpan = item.querySelector(".ngis-chip-label");
        if (labelSpan) labelSpan.textContent = text;
        item.setAttribute("aria-label", text);
        item.setAttribute("title", text);
      }
    });
  }

  /**
   * Purge obsolete bottom navigation elements from DOM
   */
  function purgeLegacyNav() {
    const oldIds = ["bottomnav", "mobBottomNav"];
    oldIds.forEach((id) => {
      const el = document.getElementById(id);
      if (el && el.id !== "ngisChipDock") {
        el.remove();
      }
    });

    const oldClasses = document.querySelectorAll(".bottomnav, .bottom-dock-nav, .mob-bottomnav:not(#ngisChipDock)");
    oldClasses.forEach((el) => el.remove());
  }

  /**
   * Master Initializer
   */
  function init() {
    // Suppress on desktop if page loaded at desktop resolution
    const role = detectRole();

    // Remove legacy bottom bars
    purgeLegacyNav();

    let dock = document.getElementById("ngisChipDock");
    if (!dock) {
      const container = document.createElement("div");
      container.innerHTML = renderDock(role);
      dock = container.firstElementChild;
      document.body.appendChild(dock);
    }

    bindInteractions(dock);
  }

  // Self-initialize on DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Export public API
  window.NGISChipNav = {
    init: init,
    purgeLegacyNav: purgeLegacyNav,
    getRole: detectRole
  };

})(window, document);
