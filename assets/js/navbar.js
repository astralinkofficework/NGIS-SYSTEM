/**
 * ============================================================================
 * NGIS ERP — Master Global Responsive Navigation Controller v2.0
 * New Gateway International School — Centralized Responsive Enterprise Navbar
 * ============================================================================
 */
(function (window, document) {
  'use strict';

  if (window.__NGIS_NAVBAR_INITIALIZED__) return;
  window.__NGIS_NAVBAR_INITIALIZED__ = true;

  // Path resolution helpers
  var pathname = window.location.pathname || '';
  var isPages = pathname.indexOf('/pages/') !== -1;
  var rootPrefix = isPages ? '../../' : '';

  var DASHBOARDS = {
    student: rootPrefix + "pages/student/student.html",
    teacher: rootPrefix + "pages/teacher/teacher.html",
    principal: rootPrefix + "pages/principal/principal.html",
    admin: rootPrefix + "pages/admin/admin.html",
    superadmin: rootPrefix + "pages/admin/admin.html"
  };

  var PROFILES = {
    student: {
      name: "Nrinphouneta Hok",
      role: "Student",
      roleMeta: "Grade 10 · Term 2",
      id: "2026-STD-0142",
      email: "nrinphouneta.hok@ngis.edu.kh",
      avatar: "https://images.pexels.com/photos/3785079/pexels-photo-3785079.jpeg?auto=compress&cs=tinysrgb&w=80",
      profileUrl: rootPrefix + "pages/student/student-profile.html",
      settingsUrl: rootPrefix + "pages/student/student-settings.html",
      notifUrl: rootPrefix + "pages/student/student-notifications.html"
    },
    teacher: {
      name: "Dr. Sarah Jenkins",
      role: "Teacher",
      roleMeta: "Mathematics Lead",
      id: "TCH-2024-042",
      email: "sarah.jenkins@ngis.edu.kh",
      avatar: "https://images.pexels.com/photos/1181686/pexels-photo-1181686.jpeg?auto=compress&cs=tinysrgb&w=80",
      profileUrl: rootPrefix + "pages/teacher/teacher-profile.html",
      settingsUrl: rootPrefix + "pages/teacher/teacher-profile.html",
      notifUrl: rootPrefix + "pages/shared/announcements.html?portal=teacher"
    },
    principal: {
      name: "Dr. Ly Bunheng",
      role: "Principal",
      roleMeta: "Executive Principal",
      id: "PRN-2024-002",
      email: "ly.bunheng@ngis.edu.kh",
      avatar: "https://images.pexels.com/photos/2182970/pexels-photo-2182970.jpeg?auto=compress&cs=tinysrgb&w=80",
      profileUrl: rootPrefix + "pages/principal/principal-profile.html",
      settingsUrl: rootPrefix + "pages/principal/principal-profile.html",
      notifUrl: rootPrefix + "pages/shared/announcements.html?portal=principal"
    },
    admin: {
      name: "Sok Panha Heng",
      role: "Admin",
      roleMeta: "School Administrator",
      id: "ADM-2024-001",
      email: "admin@ngis.edu.kh",
      avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=80&fit=crop&crop=face",
      profileUrl: rootPrefix + "pages/admin/admin-security.html",
      settingsUrl: rootPrefix + "pages/admin/admin-system-general-setting.html",
      notifUrl: rootPrefix + "pages/shared/announcements.html?portal=admin"
    },
    superadmin: {
      name: "Sok Panha Heng",
      role: "Super Admin",
      roleMeta: "Super Administrator",
      id: "SUP-2024-001",
      email: "superadmin@ngis.edu.kh",
      avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=80&fit=crop&crop=face",
      profileUrl: rootPrefix + "pages/admin/admin-security.html",
      settingsUrl: rootPrefix + "pages/admin/admin-system-general-setting.html",
      notifUrl: rootPrefix + "pages/shared/announcements.html?portal=superadmin"
    }
  };

  // State
  var state = {
    role: "student",
    user: PROFILES.student,
    notifications: [],
    unreadCount: 0,
    notifFilter: "all",
    isNotifOpen: false,
    isLangOpen: false,
    isAccountOpen: false,
    isSearchOpen: false,
    lang: localStorage.getItem("ngis-lang") || "en",
    theme: localStorage.getItem("ngis-theme") || "light",
    searchIndex: -1,
    searchResults: []
  };

  /**
   * Detect current role
   */
  function detectRole() {
    var r = (document.body && (document.body.getAttribute("data-role") || document.body.getAttribute("data-portal"))) ||
            (window.PAGE && window.PAGE.role) || "student";
    state.role = String(r).toLowerCase();
    if (state.role === "editor") state.role = "admin";
    if (state.role === "staff") state.role = "admin";
    state.user = PROFILES[state.role] || PROFILES.student;
    return state.role;
  }

  /**
   * Render Official Bootstrap SVGs
   */
  function iconSvg(name) {
    if (name === "search") {
      return '<svg width="18" height="18" viewBox="0 0 16 16" fill="currentColor" class="bi"><path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/></svg>';
    }
    if (name === "bell") {
      return '<svg width="20" height="20" viewBox="0 0 16 16" fill="currentColor" class="bi"><path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2M8 1.918l-.797.161A4 4 0 0 0 4 6c0 .628-.134 2.197-.459 3.742-.16.767-.376 1.566-.663 2.258h10.244c-.287-.692-.502-1.49-.663-2.258C12.134 8.197 12 6.628 12 6a4 4 0 0 0-3.203-3.92zM14.22 12c.223.447.481.801.78 1H1c.299-.199.557-.553.78-1C2.68 10.2 3 6.88 3 6c0-2.42 1.72-4.44 4.005-4.901a1 1 0 1 1 1.99 0A5 5 0 0 1 13 6c0 .88.32 4.2 1.22 6"/></svg>';
    }
    if (name === "globe") {
      return '<svg width="20" height="20" viewBox="0 0 16 16" fill="currentColor" class="bi"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m7.5-6.923c-.67.204-1.335.82-1.887 1.855A8 8 0 0 0 5.145 4H7.5zM4.09 5a14 14 0 0 0-.27 2H1.054a7 7 0 0 1 1.057-2zm-.27 3a14 14 0 0 0 .27 2H2.11a7 7 0 0 1-1.057-2zm.88 3c.311.77.72 1.48 1.218 2.077A7.9 7.9 0 0 1 4.7 11zm1.48 0h3.62c.28 1.04.64 1.94 1.06 2.6A7.9 7.9 0 0 1 8 15a7.9 7.9 0 0 1-1.92-1.4c-.42-.66-.78-1.56-1.06-2.6M8 1a7 7 0 0 1 1.887 1.855A8 8 0 0 1 10.855 4H8zm2.855 4H8v2h3.91a14 14 0 0 0-.27-2M8 8v2h2.855c.135-.635.228-1.309.27-2zm-4.7 0H1.054a7 7 0 0 0 1.057 2H4.09A14 14 0 0 1 3.3 8M8 10v2.6c.42-.66.78-1.56 1.06-2.6zm0 3.923c.67-.204 1.335-.82 1.887-1.855A8 8 0 0 0 10.855 12H8z"/></svg>';
    }
    if (name === "menu") {
      return '<svg width="22" height="22" viewBox="0 0 16 16" fill="currentColor" class="bi"><path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5"/></svg>';
    }
    if (name === "close") {
      return '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" class="bi"><path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/></svg>';
    }
    if (name === "sidebar-toggle") {
      return '<svg width="18" height="18" viewBox="0 0 16 16" fill="currentColor" class="bi"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2z"/><path d="M5 2v12H2a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1z"/></svg>';
    }
    if (name === "chevron-down") {
      return '<svg width="13" height="13" viewBox="0 0 16 16" fill="currentColor" class="bi"><path fill-rule="evenodd" d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708"/></svg>';
    }
    if (name === "check") {
      return '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" class="bi"><path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425z"/></svg>';
    }
    if (name === "users") {
      return '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" class="bi"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6m-5.784 6A2.24 2.24 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.3 6.3 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1zM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5"/></svg>';
    }
    if (name === "teachers") {
      return '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" class="bi"><path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3a.5.5 0 0 0 .372 0L14 7.14V13a1 1 0 0 0-1 1v2h3v-2a1 1 0 0 0-1-1V6.739l.686-.275a.5.5 0 0 0 .025-.917z"/><path d="M4.179 8.88 1 7.428V11a.5.5 0 0 0 .265.44l3 1.5a.5.5 0 0 0 .47-.024l3-1.5A.5.5 0 0 0 8 11V7.428l-3.821 1.452z"/></svg>';
    }
    if (name === "book") {
      return '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" class="bi"><path d="M1 2.828c.885-.37 2.154-.769 3.388-.893 1.33-.134 2.458.063 3.112.752v9.746c-.935-.53-2.12-.603-3.213-.493-1.18.12-2.37.461-3.287.811zm7.5-.141c.654-.689 1.782-.886 3.112-.752 1.234.124 2.503.523 3.388.893v9.923c-.918-.35-2.107-.692-3.287-.81-1.094-.111-2.278-.039-3.213.492zM8 1.783C7.015.936 5.587.81 4.287.94c-1.514.153-3.042.672-3.994 1.105A.5.5 0 0 0 0 2.5v11a.5.5 0 0 0 .707.455c.882-.4 2.303-.881 3.68-1.02 1.409-.142 2.59.087 3.223.877a.5.5 0 0 0 .78 0c.633-.79 1.814-1.019 3.222-.877 1.378.139 2.8.62 3.681 1.02A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.293-.455c-.952-.433-2.48-.952-3.994-1.105C10.413.809 8.985.936 8 1.783"/></svg>';
    }
    if (name === "departments") {
      return '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" class="bi"><path d="M14.763.075A.5.5 0 0 1 15 .5v15a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5V14h-1v1.5a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V10a.5.5 0 0 1 .342-.474L6 7.64V4.5a.5.5 0 0 1 .276-.447l8-4a.5.5 0 0 1 .487.022M6 8.694 1 10.36V15h5zM7 15h2v-1.5a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 .5.5V15h2V1.309l-7 3.5z"/></svg>';
    }
    if (name === "exams") {
      return '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" class="bi"><path d="M14 0H2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2M1 3.857C1 3.384 1.448 3 2 3h12c.552 0 1 .384 1 .857v10.286c0 .473-.448.857-1 .857H2c-.552 0-1-.384-1-.857z"/></svg>';
    }
    if (name === "documents") {
      return '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" class="bi"><path d="M4 0h5.293A1 1 0 0 1 10 .293L13.707 4a1 1 0 0 1 .293.707V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2m5.5 1.5v2a1 1 0 0 0 1 1h2z"/></svg>';
    }
    if (name === "theme") {
      return '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" class="bi"><path d="M6 .278a.77.77 0 0 1 .08.858 7.2 7.2 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277q.792-.001 1.533-.16a.79.79 0 0 1 .81.316.73.73 0 0 1-.031.893A8.35 8.35 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.75.75 0 0 1 6 .278"/></svg>';
    }
    if (name === "settings") {
      return '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" class="bi"><path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492M5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0"/><path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115z"/></svg>';
    }
    if (name === "logout") {
      return '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" class="bi"><path fill-rule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0z"/><path fill-rule="evenodd" d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708z"/></svg>';
    }
    return '';
  }

  /**
   * Build the Master Navbar element
   */
  function buildNavbarElement() {
    var role = detectRole();
    var user = state.user;
    var dashUrl = DASHBOARDS[role] || DASHBOARDS.student;
    var logoUrl = rootPrefix + "assets/images/logo.png";

    var header = document.createElement("header");
    header.className = "ngis-navbar";
    header.id = "ngisGlobalNavbar";
    header.setAttribute("role", "banner");

    header.innerHTML =
      // ── DESKTOP ROW (Height 72px) ──────────────────────────────────────────
      '<div class="ngis-nav-row ngis-nav-desktop-row">' +
        // Left: Logo & Sidebar Toggle
        '<div class="ngis-nav-left">' +
          '<a href="' + dashUrl + '" class="ngis-nav-logo-link" aria-label="NGIS Dashboard">' +
            '<img src="' + logoUrl + '" alt="NGIS Logo" class="ngis-nav-logo" width="132" height="38">' +
          '</a>' +
          '<button type="button" class="ngis-nav-btn ngis-nav-collapse-btn" id="navSidebarCollapseBtn" data-action="toggle-sidebar-collapse" aria-label="Toggle sidebar">' +
            iconSvg("sidebar-toggle") +
          '</button>' +
        '</div>' +

        // Center: Long Global Search Bar (480-640px+)
        '<div class="ngis-nav-search-wrap" role="search" id="ngisDesktopSearchWrap">' +
          '<span class="ngis-nav-search-icon" aria-hidden="true">' + iconSvg("search") + '</span>' +
          '<input type="search" class="ngis-nav-search-input" id="ngisGlobalSearchInput" placeholder="Search students, classes, exams, departments, pages…" aria-label="Global Search" autocomplete="off" spellcheck="false">' +
          '<kbd class="ngis-nav-search-kbd">⌘ K</kbd>' +
          '<button type="button" class="ngis-nav-search-clear" id="ngisSearchClearBtn" aria-label="Clear search" style="display:none;">' + iconSvg("close") + '</button>' +
          '<div class="ngis-search-dropdown" id="ngisDesktopSearchDropdown" aria-hidden="true" style="display:none;"></div>' +
        '</div>' +

        // Right: Notifications, Language, Profile Chip
        '<div class="ngis-nav-right">' +
          '<button type="button" class="ngis-nav-btn ngis-nav-notif-btn" id="ngisDesktopNotifBtn" aria-label="Notifications" aria-expanded="false">' +
            iconSvg("bell") +
            '<span class="ngis-nav-notif-dot" id="ngisDesktopNotifDot" style="display:none;"></span>' +
          '</button>' +

          '<button type="button" class="ngis-nav-btn ngis-nav-lang-btn" id="ngisDesktopLangBtn" aria-label="Select Language" aria-expanded="false">' +
            iconSvg("globe") +
          '</button>' +

          '<div class="ngis-nav-divider-v" aria-hidden="true"></div>' +

          '<button type="button" class="ngis-nav-profile-chip" id="ngisNavProfileChip" aria-label="Account menu" aria-expanded="false">' +
            '<div class="ngis-profile-avatar-wrap">' +
              '<img src="' + user.avatar + '" alt="' + user.name + '" class="ngis-profile-avatar">' +
              '<span class="ngis-profile-pip"></span>' +
            '</div>' +
            '<div class="ngis-profile-meta">' +
              '<span class="ngis-profile-name">' + user.name + '</span>' +
              '<span class="ngis-profile-role">' + user.role + '</span>' +
            '</div>' +
            '<span class="ngis-profile-caret">' + iconSvg("chevron-down") + '</span>' +
          '</button>' +
        '</div>' +
      '</div>' +

      // ── MOBILE ROW 1 (Height 64px) ─────────────────────────────────────────
      '<div class="ngis-nav-row ngis-nav-mobile-row1">' +
        '<a href="' + dashUrl + '" class="ngis-nav-logo-link" aria-label="NGIS Dashboard">' +
          '<img src="' + logoUrl + '" alt="NGIS Logo" class="ngis-nav-logo" width="132" height="38">' +
        '</a>' +
        '<div class="ngis-nav-spacer"></div>' +
        '<div class="ngis-nav-actions">' +
          // 1. Notification Bell
          '<button type="button" class="ngis-nav-btn ngis-mobile-notif-btn" id="ngisMobileNotifBtn" aria-label="Notifications" aria-expanded="false">' +
            iconSvg("bell") +
            '<span class="ngis-nav-notif-dot" id="ngisMobileNotifDot" style="display:none;"></span>' +
          '</button>' +
          // 2. Globe Language Selector
          '<button type="button" class="ngis-nav-btn ngis-mobile-lang-btn" id="ngisMobileLangBtn" aria-label="Select Language" aria-expanded="false">' +
            iconSvg("globe") +
          '</button>' +
          // 3. Hamburger Menu
          '<button type="button" class="ngis-nav-btn ngis-mobile-menu-btn hamburger-btn mobile-hamburger-btn" id="ngisMobileMenuBtn" data-action="toggle-sidebar" aria-label="Open menu" aria-expanded="false">' +
            '<span class="ngis-menu-icon">' + iconSvg("menu") + '</span>' +
            '<span class="ngis-close-icon" style="display:none;">' + iconSvg("close") + '</span>' +
          '</button>' +
        '</div>' +
      '</div>' +

      // ── MOBILE ROW 2 (Height 56px, Full-Width Search) ───────────────────────
      '<div class="ngis-nav-row ngis-nav-mobile-row2">' +
        '<div class="ngis-nav-search-wrap" role="search" id="ngisMobileSearchWrap">' +
          '<span class="ngis-nav-search-icon" aria-hidden="true">' + iconSvg("search") + '</span>' +
          '<input type="search" class="ngis-nav-search-input" id="ngisMobileSearchInput" placeholder="Search students, classes, exams, pages…" aria-label="Search" autocomplete="off" spellcheck="false">' +
          '<button type="button" class="ngis-nav-search-clear" id="ngisMobileSearchClearBtn" aria-label="Clear search" style="display:none;">' + iconSvg("close") + '</button>' +
          '<div class="ngis-search-dropdown" id="ngisMobileSearchDropdown" aria-hidden="true" style="display:none;"></div>' +
        '</div>' +
      '</div>' +

      // ── BOTTOM DIVIDER (1px Hairline) ──────────────────────────────────────
      '<div class="ngis-nav-bottom-divider"></div>' +

      // ── FLOATING PANEL: NOTIFICATIONS ──────────────────────────────────────
      '<div class="ngis-nav-panel ngis-notif-panel" id="ngisNavNotifPanel" aria-hidden="true" style="display:none;">' +
        '<div class="ngis-notif-head">' +
          '<div class="ngis-notif-head-title-wrap">' +
            '<h3 class="ngis-notif-head-title">Notifications</h3>' +
            '<span class="ngis-notif-unread-badge" id="ngisNotifBadge">0 unread</span>' +
          '</div>' +
          '<button type="button" class="ngis-notif-mark-btn" id="ngisNotifMarkAllBtn">Mark all read</button>' +
        '</div>' +
        '<div class="ngis-notif-tabs" role="tablist">' +
          '<button type="button" class="ngis-notif-tab active" data-filter="all" id="ngisNotifTabAll">All (<span id="notifTotalNum">0</span>)</button>' +
          '<button type="button" class="ngis-notif-tab" data-filter="unread" id="ngisNotifTabUnread">Unread (<span id="notifUnreadNum">0</span>)</button>' +
        '</div>' +
        '<div class="ngis-notif-body" id="ngisNotifBody">' +
          '<div class="ngis-notif-empty"><p class="ngis-notif-empty-text">Loading notifications...</p></div>' +
        '</div>' +
        '<div class="ngis-notif-foot">' +
          '<a href="' + user.notifUrl + '" class="ngis-notif-foot-link" id="ngisNotifAllLink">View all notifications &rarr;</a>' +
        '</div>' +
      '</div>' +

      // ── FLOATING PANEL: LANGUAGE SELECTOR ──────────────────────────────────
      '<div class="ngis-nav-panel ngis-lang-panel" id="ngisNavLangPanel" aria-hidden="true" style="display:none;">' +
        '<button type="button" class="ngis-lang-item" data-lang="en">' +
          '<span>English</span>' +
          '<span class="ngis-lang-check">' + iconSvg("check") + '</span>' +
        '</button>' +
        '<button type="button" class="ngis-lang-item" data-lang="km">' +
          '<span>ភាសាខ្មែរ (Khmer)</span>' +
          '<span class="ngis-lang-check">' + iconSvg("check") + '</span>' +
        '</button>' +
        '<button type="button" class="ngis-lang-item" data-lang="zh">' +
          '<span>中文 (Chinese)</span>' +
          '<span class="ngis-lang-check">' + iconSvg("check") + '</span>' +
        '</button>' +
      '</div>' +

      // ── FLOATING PANEL: USER ACCOUNT MENU ──────────────────────────────────
      '<div class="ngis-nav-panel ngis-account-panel" id="ngisNavAccountPanel" aria-hidden="true" style="display:none;">' +
        '<div class="ngis-account-header">' +
          '<div class="ngis-account-name">' + user.name + '</div>' +
          '<div class="ngis-account-role">' + user.roleMeta + ' · ' + user.id + '</div>' +
        '</div>' +
        '<a href="' + user.profileUrl + '" class="ngis-account-link">' +
          iconSvg("users") + '<span>My Profile</span>' +
        '</a>' +
        '<a href="' + user.settingsUrl + '" class="ngis-account-link">' +
          iconSvg("settings") + '<span>Account Settings</span>' +
        '</a>' +
        '<button type="button" class="ngis-account-link" id="ngisThemeToggleBtn">' +
          iconSvg("theme") + '<span id="ngisThemeLabel">Dark Mode</span>' +
        '</button>' +
      '</div>';

    return header;
  }

  /**
   * Close all floating panels
   */
  function closeAllPanels() {
    var notifPanel = document.getElementById("ngisNavNotifPanel");
    var langPanel = document.getElementById("ngisNavLangPanel");
    var accountPanel = document.getElementById("ngisNavAccountPanel");
    var dSearchDrop = document.getElementById("ngisDesktopSearchDropdown");
    var mSearchDrop = document.getElementById("ngisMobileSearchDropdown");

    if (notifPanel) {
      notifPanel.style.display = "none";
      notifPanel.classList.remove("is-open");
      notifPanel.setAttribute("aria-hidden", "true");
    }
    if (langPanel) {
      langPanel.style.display = "none";
      langPanel.classList.remove("is-open");
      langPanel.setAttribute("aria-hidden", "true");
    }
    if (accountPanel) {
      accountPanel.style.display = "none";
      accountPanel.classList.remove("is-open");
      accountPanel.setAttribute("aria-hidden", "true");
    }
    if (dSearchDrop) {
      dSearchDrop.style.display = "none";
      dSearchDrop.classList.remove("is-open");
      dSearchDrop.setAttribute("aria-hidden", "true");
    }
    if (mSearchDrop) {
      mSearchDrop.style.display = "none";
      mSearchDrop.classList.remove("is-open");
      mSearchDrop.setAttribute("aria-hidden", "true");
    }

    state.isNotifOpen = false;
    state.isLangOpen = false;
    state.isAccountOpen = false;
    state.isSearchOpen = false;
  }

  /**
   * Dynamically position panel under anchor button
   */
  function positionDropdownPanel(panel, anchorBtn) {
    if (!panel || !anchorBtn) return;
    var nav = document.getElementById("ngisGlobalNavbar");
    if (!nav) return;
    var navRect = nav.getBoundingClientRect();
    var btnRect = anchorBtn.getBoundingClientRect();
    var panelW = panel.offsetWidth || (panel.id === "ngisNavNotifPanel" ? 380 : (panel.id === "ngisNavAccountPanel" ? 250 : 190));
    var rightDist = navRect.right - btnRect.right;
    var maxRight = Math.max(12, navRect.width - panelW - 12);
    var targetRight = Math.max(12, Math.min(rightDist - 8, maxRight));
    panel.style.setProperty("right", targetRight + "px", "important");
  }

  /**
   * Toggle Notifications Panel
   */
  function toggleNotifPanel(anchorBtn) {
    var panel = document.getElementById("ngisNavNotifPanel");
    if (!panel) return;
    if (state.isNotifOpen) {
      closeAllPanels();
    } else {
      closeAllPanels();
      panel.style.display = "flex";
      panel.classList.add("is-open");
      panel.setAttribute("aria-hidden", "false");
      state.isNotifOpen = true;
      if (anchorBtn) positionDropdownPanel(panel, anchorBtn);
      fetchNotifications();
    }
  }

  /**
   * Toggle Language Dropdown
   */
  function toggleLangPanel(anchorBtn) {
    var panel = document.getElementById("ngisNavLangPanel");
    if (!panel) return;
    if (state.isLangOpen) {
      closeAllPanels();
    } else {
      closeAllPanels();
      panel.style.display = "flex";
      panel.classList.add("is-open");
      panel.setAttribute("aria-hidden", "false");
      state.isLangOpen = true;
      if (anchorBtn) positionDropdownPanel(panel, anchorBtn);
      highlightActiveLanguage();
    }
  }

  /**
   * Toggle Account Dropdown
   */
  function toggleAccountPanel(anchorBtn) {
    var panel = document.getElementById("ngisNavAccountPanel");
    if (!panel) return;
    if (state.isAccountOpen) {
      closeAllPanels();
    } else {
      closeAllPanels();
      panel.style.display = "flex";
      panel.classList.add("is-open");
      panel.setAttribute("aria-hidden", "false");
      state.isAccountOpen = true;
      if (anchorBtn) positionDropdownPanel(panel, anchorBtn);
    }
  }

  /**
   * Highlight active language
   */
  function highlightActiveLanguage() {
    var cur = state.lang || "en";
    var items = document.querySelectorAll(".ngis-lang-item");
    for (var i = 0; i < items.length; i++) {
      if (items[i].getAttribute("data-lang") === cur) {
        items[i].classList.add("selected");
      } else {
        items[i].classList.remove("selected");
      }
    }
  }

  /**
   * Set language
   */
  function setLanguage(langCode) {
    state.lang = langCode;
    try { localStorage.setItem("ngis-lang", langCode); } catch (e) {}
    document.documentElement.setAttribute("lang", langCode);
    highlightActiveLanguage();
    closeAllPanels();
    window.dispatchEvent(new CustomEvent("ngis:lang-changed", { detail: { lang: langCode } }));
  }

  /**
   * Toggle Theme (Light / Dark)
   */
  function toggleTheme() {
    var next = state.theme === "dark" ? "light" : "dark";
    state.theme = next;
    try { localStorage.setItem("ngis-theme", next); } catch (e) {}
    document.documentElement.setAttribute("data-theme", next);
    var label = document.getElementById("ngisThemeLabel");
    if (label) label.textContent = next === "dark" ? "Light Mode" : "Dark Mode";
  }

  /**
   * Fetch Live Notifications
   */
  function fetchNotifications() {
    fetch("/api/notifications")
      .then(function (res) { return res.json(); })
      .then(function (json) {
        var items = json.data || json.notifications || [];
        state.notifications = items;
        renderNotifications();
      })
      .catch(function () {
        var body = document.getElementById("ngisNotifBody");
        if (body) body.innerHTML = '<div class="ngis-notif-empty"><p>Unable to load notifications.</p></div>';
      });
  }

  /**
   * Render notifications list
   */
  function renderNotifications() {
    var items = state.notifications || [];
    var unreadItems = items.filter(function (it) { return it.unread || it.read === false; });
    state.unreadCount = unreadItems.length;

    // Badges & Red Dots
    var dDot = document.getElementById("ngisDesktopNotifDot");
    var mDot = document.getElementById("ngisMobileNotifDot");
    var badge = document.getElementById("ngisNotifBadge");
    var tNum = document.getElementById("notifTotalNum");
    var uNum = document.getElementById("notifUnreadNum");

    var showDot = state.unreadCount > 0;
    if (dDot) dDot.style.display = showDot ? "block" : "none";
    if (mDot) mDot.style.display = showDot ? "block" : "none";
    if (badge) badge.textContent = state.unreadCount + " unread";
    if (tNum) tNum.textContent = items.length;
    if (uNum) uNum.textContent = state.unreadCount;

    var displayList = state.notifFilter === "unread" ? unreadItems : items;
    var body = document.getElementById("ngisNotifBody");
    if (!body) return;

    if (displayList.length === 0) {
      body.innerHTML = '<div class="ngis-notif-empty"><p class="ngis-notif-empty-text">No notifications to display.</p></div>';
      return;
    }

    var html = '';
    for (var i = 0; i < displayList.length; i++) {
      var n = displayList[i];
      var isUnread = n.unread || n.read === false;
      var icon = n.type === 'exam' ? 'exams' : (n.type === 'grade' ? 'book' : 'bell');
      html +=
        '<div class="ngis-notif-item ' + (isUnread ? 'unread' : '') + '" data-id="' + n.id + '" role="button" tabindex="0">' +
          '<div class="ngis-notif-item-icon">' + iconSvg(icon) + '</div>' +
          '<div class="ngis-notif-item-content">' +
            '<div class="ngis-notif-item-title">' + (n.title || 'Notification') + '</div>' +
            '<div class="ngis-notif-item-msg">' + (n.message || n.summary || '') + '</div>' +
            '<div class="ngis-notif-item-date">' + (n.date || '') + ' ' + (n.time || '') + '</div>' +
          '</div>' +
        '</div>';
    }
    body.innerHTML = html;

    // Single click mark as read
    var rows = body.querySelectorAll('.ngis-notif-item');
    for (var j = 0; j < rows.length; j++) {
      rows[j].addEventListener('click', function () {
        var id = this.getAttribute('data-id');
        markSingleRead(id);
      });
    }
  }

  function markSingleRead(id) {
    fetch('/api/notifications/' + id + '/read', { method: 'POST' })
      .then(function () {
        for (var i = 0; i < state.notifications.length; i++) {
          if (String(state.notifications[i].id) === String(id)) {
            state.notifications[i].read = true;
            state.notifications[i].unread = false;
          }
        }
        renderNotifications();
      })
      .catch(function () {});
  }

  function markAllRead() {
    fetch('/api/notifications/read-all', { method: 'POST' })
      .then(function () {
        for (var i = 0; i < state.notifications.length; i++) {
          state.notifications[i].read = true;
          state.notifications[i].unread = false;
        }
        renderNotifications();
      })
      .catch(function () {});
  }

  /**
   * Search Engine: Query Backend
   */
  var searchTimer = null;
  function performSearch(query, dropdownEl) {
    clearTimeout(searchTimer);
    if (!dropdownEl) return;

    var trimmed = String(query || '').trim();
    if (!trimmed) {
      renderRecentSearches(dropdownEl);
      return;
    }

    dropdownEl.style.display = "block";
    dropdownEl.classList.add("is-open");
    dropdownEl.setAttribute("aria-hidden", "false");
    dropdownEl.innerHTML = '<div class="ngis-search-empty">Searching records…</div>';

    searchTimer = setTimeout(function () {
      var url = '/api/search?q=' + encodeURIComponent(trimmed) + '&role=' + encodeURIComponent(state.role);
      fetch(url)
        .then(function (res) { return res.json(); })
        .then(function (data) {
          renderSearchResults(data, trimmed, dropdownEl);
        })
        .catch(function () {
          dropdownEl.innerHTML = '<div class="ngis-search-empty">Failed to load search results.</div>';
        });
    }, 180);
  }

  /**
   * Save recent search query
   */
  function saveRecentSearch(q) {
    if (!q || q.length < 2) return;
    try {
      var list = JSON.parse(localStorage.getItem('ngis-recent-searches') || '[]');
      list = list.filter(function (item) { return item.toLowerCase() !== q.toLowerCase(); });
      list.unshift(q);
      if (list.length > 5) list = list.slice(0, 5);
      localStorage.setItem('ngis-recent-searches', JSON.stringify(list));
    } catch (e) {}
  }

  function renderRecentSearches(dropdownEl) {
    var list = [];
    try { list = JSON.parse(localStorage.getItem('ngis-recent-searches') || '[]'); } catch (e) {}
    if (!list || !list.length) {
      dropdownEl.innerHTML =
        '<div class="ngis-search-empty">' +
          '<p style="margin:0 0 4px;font-weight:500;">Quick Search</p>' +
          '<p style="margin:0;font-size:12px;color:#94A3B8;">Type to search students, classes, exams, departments and system pages.</p>' +
        '</div>';
      dropdownEl.style.display = "block";
      dropdownEl.classList.add("is-open");
      dropdownEl.setAttribute("aria-hidden", "false");
      return;
    }

    var html = '<div class="ngis-search-section">' +
      '<div class="ngis-search-section-header"><span>Recent Searches</span><button type="button" id="clearRecentBtn" style="background:none;border:none;color:#94A3B8;cursor:pointer;font-size:11px;">Clear</button></div>';

    for (var i = 0; i < list.length; i++) {
      html +=
        '<button type="button" class="ngis-search-item recent-query" data-query="' + list[i] + '">' +
          '<div class="ngis-search-item-left">' +
            '<span class="ngis-search-item-icon">' + iconSvg("search") + '</span>' +
            '<span class="ngis-search-item-title">' + list[i] + '</span>' +
          '</div>' +
        '</button>';
    }
    html += '</div>';
    dropdownEl.innerHTML = html;
    dropdownEl.style.display = "block";
    dropdownEl.classList.add("is-open");
    dropdownEl.setAttribute("aria-hidden", "false");

    var clearBtn = dropdownEl.querySelector('#clearRecentBtn');
    if (clearBtn) {
      clearBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        try { localStorage.removeItem('ngis-recent-searches'); } catch (e) {}
        renderRecentSearches(dropdownEl);
      });
    }

    var items = dropdownEl.querySelectorAll('.recent-query');
    for (var j = 0; j < items.length; j++) {
      items[j].addEventListener('click', function () {
        var query = this.getAttribute('data-query');
        var dInput = document.getElementById("ngisGlobalSearchInput");
        var mInput = document.getElementById("ngisMobileSearchInput");
        if (dInput) dInput.value = query;
        if (mInput) mInput.value = query;
        performSearch(query, dropdownEl);
      });
    }
  }

  function renderSearchResults(data, query, dropdownEl) {
    var categories = (data && data.categories) || [];
    state.searchResults = [];

    if (!categories.length || data.total === 0) {
      dropdownEl.innerHTML =
        '<div class="ngis-search-empty">' +
          '<p style="margin:0 0 4px;font-weight:500;">No results found</p>' +
          '<p style="margin:0;font-size:12px;color:#94A3B8;">No records matched "' + query + '". Try another keyword.</p>' +
        '</div>';
      dropdownEl.style.display = "block";
      dropdownEl.classList.add("is-open");
      dropdownEl.setAttribute("aria-hidden", "false");
      return;
    }

    var html = '';
    var qLower = query.toLowerCase();

    for (var i = 0; i < categories.length; i++) {
      var cat = categories[i];
      html += '<div class="ngis-search-section">' +
        '<div class="ngis-search-section-header">' + cat.name + ' (' + cat.items.length + ')</div>';

      for (var j = 0; j < cat.items.length; j++) {
        var it = cat.items[j];
        var itemIdx = state.searchResults.length;
        state.searchResults.push(it);

        // Highlight matched text
        var title = it.title || '';
        var highlightedTitle = title;
        var matchPos = title.toLowerCase().indexOf(qLower);
        if (matchPos !== -1) {
          highlightedTitle = title.substring(0, matchPos) +
            '<mark>' + title.substring(matchPos, matchPos + qLower.length) + '</mark>' +
            title.substring(matchPos + qLower.length);
        }

        var iconName = it.icon || 'book';
        html +=
          '<a href="' + (rootPrefix + it.url.replace(/^\/+/, '')) + '" class="ngis-search-item" data-idx="' + itemIdx + '">' +
            '<div class="ngis-search-item-left">' +
              '<div class="ngis-search-item-icon">' + iconSvg(iconName) + '</div>' +
              '<div class="ngis-search-item-text">' +
                '<span class="ngis-search-item-title">' + highlightedTitle + '</span>' +
                '<span class="ngis-search-item-meta">' + (it.meta || '') + '</span>' +
              '</div>' +
            '</div>' +
          '</a>';
      }
      html += '</div>';
    }

    dropdownEl.innerHTML = html;
    dropdownEl.style.display = "block";
    dropdownEl.classList.add("is-open");
    dropdownEl.setAttribute("aria-hidden", "false");

    // Bind click to record search history
    var links = dropdownEl.querySelectorAll('.ngis-search-item');
    for (var k = 0; k < links.length; k++) {
      links[k].addEventListener('click', function () {
        saveRecentSearch(query);
      });
    }
  }

  /**
   * Toggle Sidebar Collapse (Desktop)
   */
  function toggleSidebarCollapse() {
    var sidebar = document.getElementById("sidebar");
    var main = document.querySelector(".main");
    if (!sidebar) return;

    var isCollapsed = sidebar.classList.contains("collapsed");
    var next = !isCollapsed;

    if (next) {
      sidebar.classList.add("collapsed");
      if (main) main.classList.add("sidebar-collapsed");
      document.body.classList.add("sidebar-collapsed");
    } else {
      sidebar.classList.remove("collapsed");
      if (main) main.classList.remove("sidebar-collapsed");
      document.body.classList.remove("sidebar-collapsed");
    }

    try { localStorage.setItem("ngis-sidebar-collapsed", String(next)); } catch (e) {}

    // Dispatch resize event so charts/tables re-render
    window.dispatchEvent(new Event("resize"));
  }

  /**
   * Toggle Sidebar Mobile Drawer
   */
  function toggleMobileDrawer() {
    closeAllPanels();
    if (typeof window.toggleSidebar === "function") {
      window.toggleSidebar();
    } else if (typeof window.openNav === "function") {
      var isSidebarOpen = document.body.classList.contains("sidebar-open");
      if (isSidebarOpen) {
        if (typeof window.closeNav === "function") window.closeNav();
      } else {
        window.openNav();
      }
    }
  }

  /**
   * Mount Navbar into DOM
   */
  function mountNavbar() {
    if (document.body.dataset.ngisNavbar === "page" || document.getElementById("ngisGlobalNavbar")) return;

    var oldMobile = document.getElementById("ngisMobileHeader");
    if (oldMobile && oldMobile.parentNode) oldMobile.parentNode.removeChild(oldMobile);

    var navbar = buildNavbarElement();

    // Insert at the top level of document.body before shell
    var shell = document.querySelector(".shell");
    if (shell && shell.parentNode === document.body) {
      document.body.insertBefore(navbar, shell);
    } else if (document.body.firstChild) {
      document.body.insertBefore(navbar, document.body.firstChild);
    } else {
      document.body.appendChild(navbar);
    }

    // ── Bind Desktop Controls ──
    var dCollapseBtn = document.getElementById("navSidebarCollapseBtn");
    if (dCollapseBtn) {
      dCollapseBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        toggleSidebarCollapse();
      });
    }

    var dNotifBtn = document.getElementById("ngisDesktopNotifBtn");
    if (dNotifBtn) {
      dNotifBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        toggleNotifPanel(this);
      });
    }

    var dLangBtn = document.getElementById("ngisDesktopLangBtn");
    if (dLangBtn) {
      dLangBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        toggleLangPanel(this);
      });
    }

    var dProfileChip = document.getElementById("ngisNavProfileChip");
    if (dProfileChip) {
      dProfileChip.addEventListener("click", function (e) {
        e.stopPropagation();
        toggleAccountPanel(this);
      });
    }

    // ── Bind Mobile Controls ──
    var mNotifBtn = document.getElementById("ngisMobileNotifBtn");
    if (mNotifBtn) {
      mNotifBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        toggleNotifPanel(this);
      });
    }

    var mLangBtn = document.getElementById("ngisMobileLangBtn");
    if (mLangBtn) {
      mLangBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        toggleLangPanel(this);
      });
    }

    var mMenuBtn = document.getElementById("ngisMobileMenuBtn");
    if (mMenuBtn) {
      mMenuBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        e.preventDefault();
        toggleMobileDrawer();
      });
    }

    // ── Bind Notification Tabs & Mark Read ──
    var markAllBtn = document.getElementById("ngisNotifMarkAllBtn");
    if (markAllBtn) {
      markAllBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        markAllRead();
      });
    }

    var tabAll = document.getElementById("ngisNotifTabAll");
    var tabUnread = document.getElementById("ngisNotifTabUnread");
    if (tabAll && tabUnread) {
      tabAll.addEventListener("click", function (e) {
        e.stopPropagation();
        state.notifFilter = "all";
        tabAll.classList.add("active");
        tabUnread.classList.remove("active");
        renderNotifications();
      });
      tabUnread.addEventListener("click", function (e) {
        e.stopPropagation();
        state.notifFilter = "unread";
        tabUnread.classList.add("active");
        tabAll.classList.remove("active");
        renderNotifications();
      });
    }

    // ── Bind Language Items ──
    var langItems = document.querySelectorAll(".ngis-lang-item");
    for (var i = 0; i < langItems.length; i++) {
      langItems[i].addEventListener("click", function (e) {
        e.stopPropagation();
        var code = this.getAttribute("data-lang");
        setLanguage(code);
      });
    }

    // ── Bind Theme Switcher ──
    var themeBtn = document.getElementById("ngisThemeToggleBtn");
    if (themeBtn) {
      themeBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        toggleTheme();
      });
    }

    // ── Bind Search Inputs (Desktop & Mobile) ──
    var dSearchInput = document.getElementById("ngisGlobalSearchInput");
    var dSearchClear = document.getElementById("ngisSearchClearBtn");
    var dSearchDrop = document.getElementById("ngisDesktopSearchDropdown");

    var mSearchInput = document.getElementById("ngisMobileSearchInput");
    var mSearchClear = document.getElementById("ngisMobileSearchClearBtn");
    var mSearchDrop = document.getElementById("ngisMobileSearchDropdown");

    function setupSearchField(input, clearBtn, dropdown) {
      if (!input || !dropdown) return;

      input.addEventListener("focus", function () {
        closeAllPanels();
        performSearch(input.value, dropdown);
      });

      input.addEventListener("input", function () {
        if (clearBtn) clearBtn.style.display = input.value ? "inline-flex" : "none";
        performSearch(input.value, dropdown);
      });

      if (clearBtn) {
        clearBtn.addEventListener("click", function (e) {
          e.stopPropagation();
          input.value = "";
          clearBtn.style.display = "none";
          input.focus();
          performSearch("", dropdown);
        });
      }

      // Keyboard navigation (ArrowDown, ArrowUp, Enter, Esc)
      input.addEventListener("keydown", function (e) {
        var items = dropdown.querySelectorAll(".ngis-search-item");
        if (e.key === "Escape") {
          dropdown.style.display = "none";
          input.blur();
          return;
        }
        if (e.key === "ArrowDown") {
          e.preventDefault();
          state.searchIndex = Math.min(state.searchIndex + 1, items.length - 1);
          updateSearchHighlight(items);
          return;
        }
        if (e.key === "ArrowUp") {
          e.preventDefault();
          state.searchIndex = Math.max(state.searchIndex - 1, 0);
          updateSearchHighlight(items);
          return;
        }
        if (e.key === "Enter") {
          if (state.searchIndex >= 0 && items[state.searchIndex]) {
            e.preventDefault();
            items[state.searchIndex].click();
          }
        }
      });
    }

    function updateSearchHighlight(items) {
      for (var i = 0; i < items.length; i++) {
        if (i === state.searchIndex) {
          items[i].classList.add("highlighted");
          items[i].scrollIntoView({ block: "nearest" });
        } else {
          items[i].classList.remove("highlighted");
        }
      }
    }

    setupSearchField(dSearchInput, dSearchClear, dSearchDrop);
    setupSearchField(mSearchInput, mSearchClear, mSearchDrop);

    // Global Hotkey: Ctrl+K / Cmd+K
    window.addEventListener("keydown", function (e) {
      if ((e.ctrlKey || e.metaKey) && (e.key === "k" || e.key === "K")) {
        e.preventDefault();
        var target = window.innerWidth <= 768 ? mSearchInput : dSearchInput;
        if (target) {
          target.focus();
          target.select();
        }
      }
    });

    // Global outside click dismissal
    document.addEventListener("click", function (e) {
      if (!e.target.closest("#ngisGlobalNavbar")) {
        closeAllPanels();
      }
    });

    // Mobile Hamburger dynamic cross-fade observer
    var observer = new MutationObserver(function () {
      var isOpen = document.body.classList.contains("sidebar-open");
      var menuIcon = document.querySelector("#ngisMobileMenuBtn .ngis-menu-icon");
      var closeIcon = document.querySelector("#ngisMobileMenuBtn .ngis-close-icon");
      if (menuIcon) menuIcon.style.display = isOpen ? "none" : "";
      if (closeIcon) closeIcon.style.display = isOpen ? "" : "none";
      if (mMenuBtn) mMenuBtn.setAttribute("aria-expanded", String(isOpen));
    });
    observer.observe(document.body, { attributes: true, attributeFilter: ["class"] });

    // Initial background fetch
    fetchNotifications();
  }

  // Auto-mount on DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mountNavbar);
  } else {
    mountNavbar();
  }

})(window, document);
