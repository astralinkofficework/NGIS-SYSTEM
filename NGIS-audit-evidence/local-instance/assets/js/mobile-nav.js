/**
 * ============================================================================
 * NGIS ERP — Global Mobile Top Navigation Engine v1.0
 * New Gateway International School — Centralized Shared Mobile Header
 *
 * Implements:
 * - 4-Element Top Bar: Logo — (flexible space) — Bell — Globe — Hamburger
 * - Live Notification System connected to /api/notifications
 * - Language Selector (English, Khmer, Chinese) with persistence
 * - Hamburger toggle synchronization with layout.js sidebar
 * - Mutual exclusivity of header dropdowns/panels
 * - Keyboard accessibility & click-outside dismissal
 * ============================================================================
 */

(function (window, document) {
  "use strict";

  if (window.__NGIS_MOBILE_HEADER_INITIALIZED__ || window.__NGIS_NAVBAR_INITIALIZED__ || document.getElementById("ngisGlobalNavbar")) return;
  window.__NGIS_MOBILE_HEADER_INITIALIZED__ = true;

  // Resolve root prefix based on pathname
  var isSubpage = (window.location.pathname || "").indexOf("/pages/") !== -1;
  var rootPrefix = isSubpage ? "../../" : "";

  // Authorized Dashboard mapping
  var DASHBOARDS = {
    student: rootPrefix + "pages/student/student.html",
    teacher: rootPrefix + "pages/teacher/teacher.html",
    principal: rootPrefix + "pages/principal/principal.html",
    admin: rootPrefix + "pages/admin/admin.html",
    super_admin: rootPrefix + "pages/admin/admin.html"
  };

  // Full notifications destination mapping
  var NOTIF_PAGES = {
    student: rootPrefix + "pages/student/student-notifications.html",
    teacher: rootPrefix + "pages/teacher/teacher-notifications.html",
    principal: rootPrefix + "pages/principal/principal-activity.html",
    admin: rootPrefix + "pages/admin/admin-news.html",
    super_admin: rootPrefix + "pages/admin/admin-news.html"
  };

  // Notification item destination URL resolver
  function resolveNotifUrl(notif, role) {
    var type = (notif.type || "").toLowerCase();
    if (role === "student") {
      if (type === "assignment") return rootPrefix + "pages/student/student-assignments.html";
      if (type === "exam") return rootPrefix + "pages/student/student-exams.html";
      if (type === "grade") return rootPrefix + "pages/student/student-grades.html";
      return rootPrefix + "pages/student/student.html";
    }
    if (role === "teacher") {
      if (type === "assignment") return rootPrefix + "pages/teacher/teacher-submissions.html";
      if (type === "exam") return rootPrefix + "pages/teacher/teacher-exams.html";
      if (type === "grade") return rootPrefix + "pages/teacher/teacher-gradebook.html";
      return rootPrefix + "pages/teacher/teacher.html";
    }
    if (role === "principal") {
      return rootPrefix + "pages/principal/principal-activity.html";
    }
    return rootPrefix + "pages/admin/admin-news.html";
  }

  // Escape helper for safe text injection
  function esc(str) {
    return String(str == null ? "" : str).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // Active state
  var state = {
    role: "student",
    notifications: [],
    unreadCount: 0,
    filter: "all",
    isNotifOpen: false,
    isLangOpen: false,
    lang: localStorage.getItem("ngis-lang") || "en"
  };

  /**
   * Determine active role from body attributes or URL
   */
  function detectRole() {
    var r = (document.body && (document.body.getAttribute("data-role") || document.body.getAttribute("data-portal"))) ||
            (window.PAGE && window.PAGE.role) || "student";
    state.role = String(r).toLowerCase();
    return state.role;
  }

  /**
   * Render SVG icons with Bootstrap fallback
   */
  function iconSvg(name) {
    if (window.NGIS && typeof window.NGIS.icon === "function") {
      return window.NGIS.icon(name);
    }
    // Fallback official 16x16 Bootstrap paths
    if (name === "bell") {
      return '<svg width="24" height="24" viewBox="0 0 16 16" fill="currentColor" class="ngis-action-svg"><path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2M8 1.918l-.797.161A4 4 0 0 0 4 6c0 .628-.134 2.197-.459 3.742-.16.767-.376 1.566-.663 2.258h10.244c-.287-.692-.502-1.49-.663-2.258C12.134 8.197 12 6.628 12 6a4 4 0 0 0-3.203-3.92zM14.22 12c.223.447.481.801.78 1H1c.299-.199.557-.553.78-1C2.68 10.2 3 6.88 3 6c0-2.42 1.72-4.44 4.005-4.901a1 1 0 1 1 1.99 0A5 5 0 0 1 13 6c0 .88.32 4.2 1.22 6"/></svg>';
    }
    if (name === "globe") {
      return '<svg width="24" height="24" viewBox="0 0 16 16" fill="currentColor" class="ngis-action-svg"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m7.5-6.923c-.67.204-1.335.82-1.887 1.855A8 8 0 0 0 5.145 4H7.5zM4.09 5a14 14 0 0 0-.27 2H1.054a7 7 0 0 1 1.057-2zm-.27 3a14 14 0 0 0 .27 2H2.11a7 7 0 0 1-1.057-2zm.88 3c.311.77.72 1.48 1.218 2.077A7.9 7.9 0 0 1 4.7 11zm1.48 0h3.62c.28 1.04.64 1.94 1.06 2.6A7.9 7.9 0 0 1 8 15a7.9 7.9 0 0 1-1.92-1.4c-.42-.66-.78-1.56-1.06-2.6M8 1a7 7 0 0 1 1.887 1.855A8 8 0 0 1 10.855 4H8zm2.855 4H8v2h3.91a14 14 0 0 0-.27-2M8 8v2h2.855c.135-.635.228-1.309.27-2zm-4.7 0H1.054a7 7 0 0 0 1.057 2H4.09A14 14 0 0 1 3.3 8M8 10v2.6c.42-.66.78-1.56 1.06-2.6zm0 3.923c.67-.204 1.335-.82 1.887-1.855A8 8 0 0 0 10.855 12H8z"/></svg>';
    }
    if (name === "menu") {
      return '<svg width="24" height="24" viewBox="0 0 16 16" fill="currentColor" class="ngis-action-svg"><path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5"/></svg>';
    }
    if (name === "close") {
      return '<svg width="24" height="24" viewBox="0 0 16 16" fill="currentColor" class="ngis-action-svg"><path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/></svg>';
    }
    if (name === "check") {
      return '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" class="ngis-action-svg"><path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425z"/></svg>';
    }
    return '';
  }

  /**
   * Build the DOM markup for the Master Mobile Header
   */
  function createHeaderElement() {
    var role = detectRole();
    var dashUrl = DASHBOARDS[role] || DASHBOARDS.student;
    var logoUrl = rootPrefix + "assets/images/logo.png";
    var notifPageUrl = NOTIF_PAGES[role] || NOTIF_PAGES.student;

    var header = document.createElement("header");
    header.className = "ngis-mobile-header";
    header.id = "ngisMobileHeader";
    header.setAttribute("role", "banner");

    header.innerHTML =
      '<div class="ngis-mobile-header-inner">' +
        // Left: Official NGIS School Logo (links to authorized dashboard)
        '<a href="' + dashUrl + '" class="ngis-mobile-logo-link" aria-label="NGIS Dashboard">' +
          '<img src="' + logoUrl + '" alt="NGIS Logo" class="ngis-mobile-logo" width="132" height="38">' +
        '</a>' +

        // Flexible Center Space
        '<div class="ngis-mobile-header-spacer"></div>' +

        // Right Controls: Bell -> Globe -> Hamburger
        '<div class="ngis-mobile-header-actions">' +
          // 1. Notification Bell
          '<button type="button" class="ngis-mobile-btn ngis-mobile-notif-btn" id="ngisMobileNotifBtn" aria-label="Notifications" aria-expanded="false" title="Notifications">' +
            iconSvg("bell") +
            '<span class="ngis-notif-dot" id="ngisMobileNotifDot" style="display:none;"></span>' +
          '</button>' +

          // 2. Globe Language Selector
          '<button type="button" class="ngis-mobile-btn ngis-mobile-lang-btn" id="ngisMobileLangBtn" aria-label="Select Language" aria-expanded="false" title="Language">' +
            iconSvg("globe") +
          '</button>' +

          // 3. Hamburger Menu (Toggles to Close)
          '<button type="button" class="ngis-mobile-btn ngis-mobile-menu-btn hamburger-btn mobile-hamburger-btn" id="ngisMobileMenuBtn" data-action="toggle-sidebar" aria-label="Open menu" aria-expanded="false" title="Open navigation">' +
            '<span class="ngis-menu-icon">' + iconSvg("menu") + '</span>' +
            '<span class="ngis-close-icon" style="display:none;">' + iconSvg("close") + '</span>' +
          '</button>' +
        '</div>' +
      '</div>' +

      // Thin 1px bottom divider
      '<div class="ngis-mobile-header-divider"></div>' +

      // Responsive Notification Panel Dropdown
      '<div class="ngis-mobile-notif-panel" id="ngisMobileNotifPanel" aria-hidden="true" style="display:none;">' +
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
          '<a href="' + notifPageUrl + '" class="ngis-notif-foot-link" id="ngisNotifAllLink">View all notifications &rarr;</a>' +
        '</div>' +
      '</div>' +

      // Minimal Language Dropdown
      '<div class="ngis-mobile-lang-dropdown" id="ngisMobileLangDropdown" aria-hidden="true" style="display:none;">' +
        '<button type="button" class="ngis-lang-item" data-lang="en">' +
          '<span>English</span>' +
          '<span class="ngis-lang-check-icon">' + iconSvg("check") + '</span>' +
        '</button>' +
        '<button type="button" class="ngis-lang-item" data-lang="km">' +
          '<span>ភាសាខ្មែរ (Khmer)</span>' +
          '<span class="ngis-lang-check-icon">' + iconSvg("check") + '</span>' +
        '</button>' +
        '<button type="button" class="ngis-lang-item" data-lang="zh">' +
          '<span>中文 (Chinese)</span>' +
          '<span class="ngis-lang-check-icon">' + iconSvg("check") + '</span>' +
        '</button>' +
      '</div>';

    return header;
  }

  /**
   * Fetch live notification records from backend
   */
  function fetchNotifications() {
    var url = "/api/notifications";
    fetch(url)
      .then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status);
        return res.json();
      })
      .then(function (json) {
        var items = json.data || json.notifications || [];
        state.notifications = items;
        renderNotifications();
      })
      .catch(function () {
        // Fallback default mock notifications if offline / running without server
        if (!state.notifications.length) {
          state.notifications = [
            { id: 1, type: "assignment", title: "New Assignment: Mathematics Ch.8", message: "Mr. Sophea posted an assignment.", date: "2026-07-06", read: false },
            { id: 2, type: "exam", title: "Exam Tomorrow: Physics Mid-Term", message: "Physics exam scheduled at 8:00 AM.", date: "2026-07-05", read: false },
            { id: 3, type: "grade", title: "Grade Released: Chemistry Practical", message: "Score: 88% is published.", date: "2026-07-04", read: false },
            { id: 4, type: "system", title: "Campus Holiday Reminder", message: "Sen Sok Campus will observe holiday on Friday.", date: "2026-07-02", read: true }
          ];
          renderNotifications();
        }
      });
  }

  /**
   * Render notifications list in panel & update red dot
   */
  function renderNotifications() {
    var items = state.notifications || [];
    var unread = items.filter(function (n) { return !n.read; });
    state.unreadCount = unread.length;

    // Update Red Indicator Dot
    var dot = document.getElementById("ngisMobileNotifDot");
    if (dot) {
      dot.style.display = state.unreadCount > 0 ? "block" : "none";
    }

    // Update Head Badge
    var badge = document.getElementById("ngisNotifBadge");
    if (badge) {
      badge.textContent = state.unreadCount + " unread";
    }

    // Update Tab Counts
    var totalNum = document.getElementById("notifTotalNum");
    var unreadNum = document.getElementById("notifUnreadNum");
    if (totalNum) totalNum.textContent = items.length;
    if (unreadNum) unreadNum.textContent = state.unreadCount;

    // Filter Items
    var displayItems = state.filter === "unread" ? unread : items;

    // Render List Body
    var body = document.getElementById("ngisNotifBody");
    if (!body) return;

    if (!displayItems.length) {
      body.innerHTML =
        '<div class="ngis-notif-empty">' +
          '<p class="ngis-notif-empty-text">' +
            (state.filter === "unread" ? "No unread notifications" : "No notifications available") +
          '</p>' +
        '</div>';
      return;
    }

    var html = "";
    displayItems.forEach(function (n) {
      var notifUrl = resolveNotifUrl(n, state.role);
      var unreadCls = !n.read ? " unread" : "";
      var unreadDot = !n.read ? '<span class="ngis-notif-item-unread-dot"></span>' : '';

      html +=
        '<a href="' + notifUrl + '" class="ngis-notif-item' + unreadCls + '" data-id="' + esc(n.id) + '">' +
          '<div class="ngis-notif-icon-wrap">' + iconSvg("bell") + '</div>' +
          '<div class="ngis-notif-content">' +
            '<h4 class="ngis-notif-item-title">' + esc(n.title) + '</h4>' +
            '<p class="ngis-notif-item-msg">' + esc(n.message) + '</p>' +
            '<span class="ngis-notif-item-time">' + esc(n.date || "Recent") + '</span>' +
          '</div>' +
          unreadDot +
        '</a>';
    });

    body.innerHTML = html;

    // Wire individual item clicks to mark read
    var itemEls = body.querySelectorAll(".ngis-notif-item");
    for (var i = 0; i < itemEls.length; i++) {
      itemEls[i].addEventListener("click", function (e) {
        var id = this.getAttribute("data-id");
        if (id) markSingleRead(id);
      });
    }
  }

  /**
   * Mark all notifications as read
   */
  function markAllRead() {
    fetch("/api/notifications/read-all", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({})
    }).catch(function () {});

    state.notifications.forEach(function (n) { n.read = true; });
    renderNotifications();
  }

  /**
   * Mark a single notification as read
   */
  function markSingleRead(id) {
    fetch("/api/notifications/" + id + "/read", { method: "POST" }).catch(function () {});
    var item = state.notifications.find(function (n) { return String(n.id) === String(id); });
    if (item) item.read = true;
    renderNotifications();
  }

  /**
   * Close all panels (Notifications, Language, Sidebar)
   */
  function closeAllPanels() {
    var notifPanel = document.getElementById("ngisMobileNotifPanel");
    var langDropdown = document.getElementById("ngisMobileLangDropdown");
    var notifBtn = document.getElementById("ngisMobileNotifBtn");
    var langBtn = document.getElementById("ngisMobileLangBtn");
    var menuBtn = document.getElementById("ngisMobileMenuBtn");

    if (notifPanel) {
      notifPanel.style.display = "none";
      notifPanel.classList.remove("is-open");
      notifPanel.setAttribute("aria-hidden", "true");
    }
    if (langDropdown) {
      langDropdown.style.display = "none";
      langDropdown.classList.remove("is-open");
      langDropdown.setAttribute("aria-hidden", "true");
    }
    if (notifBtn) notifBtn.setAttribute("aria-expanded", "false");
    if (langBtn) langBtn.setAttribute("aria-expanded", "false");

    state.isNotifOpen = false;
    state.isLangOpen = false;
  }

  /**
   * Toggle Notifications Panel
   */
  function toggleNotifPanel() {
    var panel = document.getElementById("ngisMobileNotifPanel");
    var btn = document.getElementById("ngisMobileNotifBtn");
    if (!panel) return;

    if (state.isNotifOpen) {
      closeAllPanels();
    } else {
      closeAllPanels();
      // Also close sidebar if open
      if (typeof window.closeSidebar === "function") window.closeSidebar();
      panel.style.display = "flex";
      panel.classList.add("is-open");
      panel.setAttribute("aria-hidden", "false");
      if (btn) btn.setAttribute("aria-expanded", "true");
      state.isNotifOpen = true;
      fetchNotifications();
    }
  }

  /**
   * Toggle Language Dropdown
   */
  function toggleLangDropdown() {
    var dropdown = document.getElementById("ngisMobileLangDropdown");
    var btn = document.getElementById("ngisMobileLangBtn");
    if (!dropdown) return;

    if (state.isLangOpen) {
      closeAllPanels();
    } else {
      closeAllPanels();
      // Also close sidebar if open
      if (typeof window.closeSidebar === "function") window.closeSidebar();
      dropdown.style.display = "flex";
      dropdown.classList.add("is-open");
      dropdown.setAttribute("aria-hidden", "false");
      if (btn) btn.setAttribute("aria-expanded", "true");
      state.isLangOpen = true;
      highlightActiveLanguage();
    }
  }

  /**
   * Highlight the active language in the dropdown
   */
  function highlightActiveLanguage() {
    var cur = state.lang || "en";
    var items = document.querySelectorAll(".ngis-lang-item");
    for (var i = 0; i < items.length; i++) {
      var itemLang = items[i].getAttribute("data-lang");
      if (itemLang === cur) {
        items[i].classList.add("selected");
      } else {
        items[i].classList.remove("selected");
      }
    }
  }

  /**
   * Set and persist selected language
   */
  function setLanguage(langCode) {
    state.lang = langCode;
    try {
      localStorage.setItem("ngis-lang", langCode);
    } catch (e) {}
    document.documentElement.setAttribute("lang", langCode);
    highlightActiveLanguage();
    closeAllPanels();

    // Dispatch global event for application listeners
    window.dispatchEvent(new CustomEvent("ngis:lang-changed", { detail: { lang: langCode } }));
  }

  /**
   * Update Hamburger Menu Button Icon (Menu vs Close)
   */
  function syncHamburgerIcon(isOpen) {
    var menuBtn = document.getElementById("ngisMobileMenuBtn");
    if (!menuBtn) return;
    var menuIcon = menuBtn.querySelector(".ngis-menu-icon");
    var closeIcon = menuBtn.querySelector(".ngis-close-icon");

    menuBtn.setAttribute("aria-expanded", String(isOpen));
    if (menuIcon) menuIcon.style.display = isOpen ? "none" : "";
    if (closeIcon) closeIcon.style.display = isOpen ? "" : "none";

    if (isOpen) {
      closeAllPanels();
    }
  }

  /**
   * Mount the mobile header into the DOM
   */
  function mountMobileHeader() {
    if (document.getElementById("ngisMobileHeader")) return;

    var header = createHeaderElement();

    // Mount at the top level of document.body to span full viewport width
    var shell = document.querySelector(".shell");
    if (shell && shell.parentNode === document.body) {
      document.body.insertBefore(header, shell);
    } else if (document.body.firstChild) {
      document.body.insertBefore(header, document.body.firstChild);
    } else {
      document.body.appendChild(header);
    }

    // Wire Notification Bell
    var notifBtn = document.getElementById("ngisMobileNotifBtn");
    if (notifBtn) {
      notifBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        toggleNotifPanel();
      });
    }

    // Wire Mark All Read
    var markAllBtn = document.getElementById("ngisNotifMarkAllBtn");
    if (markAllBtn) {
      markAllBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        markAllRead();
      });
    }

    // Wire Filter Tabs
    var tabAll = document.getElementById("ngisNotifTabAll");
    var tabUnread = document.getElementById("ngisNotifTabUnread");
    if (tabAll && tabUnread) {
      tabAll.addEventListener("click", function (e) {
        e.stopPropagation();
        state.filter = "all";
        tabAll.classList.add("active");
        tabUnread.classList.remove("active");
        renderNotifications();
      });
      tabUnread.addEventListener("click", function (e) {
        e.stopPropagation();
        state.filter = "unread";
        tabUnread.classList.add("active");
        tabAll.classList.remove("active");
        renderNotifications();
      });
    }

    // Wire Language Button
    var langBtn = document.getElementById("ngisMobileLangBtn");
    if (langBtn) {
      langBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        toggleLangDropdown();
      });
    }

    // Wire Language Options
    var langItems = document.querySelectorAll(".ngis-lang-item");
    for (var i = 0; i < langItems.length; i++) {
      langItems[i].addEventListener("click", function (e) {
        e.stopPropagation();
        var code = this.getAttribute("data-lang");
        if (code) setLanguage(code);
      });
    }

    // Wire Hamburger Menu Button
    var menuBtn = document.getElementById("ngisMobileMenuBtn");
    if (menuBtn) {
      menuBtn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        closeAllPanels();
        if (typeof window.toggleSidebar === "function") {
          window.toggleSidebar();
        }
      });
    }

    // Global outside click dismissal
    document.addEventListener("click", function (e) {
      if (!e.target.closest("#ngisMobileHeader")) {
        closeAllPanels();
      }
    });

    // Global Escape key listener
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        closeAllPanels();
        if (typeof window.closeSidebar === "function") window.closeSidebar();
      }
    });

    // Observer for sidebar open/close state to switch hamburger icon
    var observer = new MutationObserver(function () {
      var isSidebarOpen = document.body.classList.contains("sidebar-open") ||
                          (document.getElementById("sidebar") && document.getElementById("sidebar").classList.contains("open"));
      syncHamburgerIcon(isSidebarOpen);
    });

    observer.observe(document.body, { attributes: true, attributeFilter: ["class"] });

    // Initial fetch of notifications
    fetchNotifications();
    highlightActiveLanguage();
  }

  // Mount on DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mountMobileHeader);
  } else {
    mountMobileHeader();
  }
  window.addEventListener("load", mountMobileHeader);

  // Export helper
  window.NGIS_MOBILE_HEADER = {
    mount: mountMobileHeader,
    fetchNotifications: fetchNotifications,
    closeAll: closeAllPanels
  };

})(window, document);
