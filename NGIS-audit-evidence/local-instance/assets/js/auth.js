/**
 * NGIS School ERP — Frontend Auth Helper
 * Handles demo-first sessions, token storage, and authenticated API requests.
 */

(function (window) {
  "use strict";

  const TOKEN_KEY = "ngis_token";
  const USER_KEY = "ngis_user";
  const ACTOR_COOKIE = "ngis_actor";
  const ACTOR_MAX_AGE = 604800; // 7 days

  /**
   * Mirror the active identity into a first-party cookie. The server-side
   * direct-URL gate cannot read localStorage, so real browser navigation only
   * becomes enforceable once this cookie exists. Passive demo browsing (no
   * explicit login / portal choice) deliberately clears it, which keeps the
   * published demo navigation available and avoids silent lockouts.
   */
  function writeActorCookie(actor) {
    try {
      const value = actor ? String(actor).trim().toLowerCase() : "";
      document.cookie = value
        ? ACTOR_COOKIE + "=" + encodeURIComponent(value) +
          "; path=/; max-age=" + ACTOR_MAX_AGE + "; SameSite=Lax"
        : ACTOR_COOKIE + "=; path=/; max-age=0; SameSite=Lax";
    } catch (e) {}
  }

  /** Re-derive the cookie from localStorage. Safe to call on every page load. */
  function syncActorCookie() {
    try {
      if (localStorage.getItem("ngis_session_mode") === "passive") {
        writeActorCookie("");
        return;
      }
      const raw = localStorage.getItem(USER_KEY);
      const user = raw ? JSON.parse(raw) : null;
      writeActorCookie(user && (user.email || user.username));
    } catch (e) {
      writeActorCookie("");
    }
  }

  const DEMO_USERS = {
    superadmin: {
      id: "SUP-2024-001",
      firstName: "Sok Panha",
      lastName: "Heng",
      role: "superadmin",
      portal: "superadmin",
      email: "superadmin@ngis.edu.kh",
      title: "Super Administrator",
      avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=80&fit=crop&crop=face"
    },
    admin: {
      id: "ADM-2024-001",
      firstName: "Sok Panha",
      lastName: "Heng",
      role: "admin",
      portal: "admin",
      email: "admin@ngis.edu.kh",
      title: "School Administrator",
      avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=80&fit=crop&crop=face"
    },
    staff: {
      id: "STF-2024-018",
      firstName: "Chanthou",
      lastName: "Meas",
      role: "staff",
      portal: "staff",
      email: "staff@ngis.edu.kh",
      title: "Campus Operations Staff",
      avatar: "https://images.pexels.com/photos/3184339/pexels-photo-3184339.jpeg?auto=compress&cs=tinysrgb&w=80"
    },
    principal: {
      id: "PRN-2024-001",
      firstName: "Dr. Ly",
      lastName: "Bunheng",
      role: "principal",
      portal: "principal",
      email: "principal@ngis.edu.kh",
      title: "Campus Principal",
      avatar: "https://images.pexels.com/photos/3184339/pexels-photo-3184339.jpeg?auto=compress&cs=tinysrgb&w=80"
    },
    editor: {
      id: "USR-006",
      firstName: "Keo",
      lastName: "Sreymom",
      role: "editor",
      portal: "admin",
      email: "sreymom.keo@ngis.edu.kh",
      title: "Academic Configuration Editor",
      assignedCampus: "TK-MAIN",
      avatar: "https://images.pexels.com/photos/1181686/pexels-photo-1181686.jpeg?auto=compress&cs=tinysrgb&w=80"
    },
    teacher: {
      id: "TCH-2024-042",
      firstName: "Dr. Sarah",
      lastName: "Jenkins",
      role: "teacher",
      portal: "teacher",
      email: "teacher@ngis.edu.kh",
      title: "Mathematics Dept. Head",
      avatar: "https://images.pexels.com/photos/1181686/pexels-photo-1181686.jpeg?auto=compress&cs=tinysrgb&w=80"
    },
    student: {
      id: "STU-2024-089",
      firstName: "Nrinphouneta",
      lastName: "Hok",
      role: "student",
      portal: "student",
      email: "student@ngis.edu.kh",
      title: "Student · Grade 11-A",
      avatar: "https://images.pexels.com/photos/3785079/pexels-photo-3785079.jpeg?auto=compress&cs=tinysrgb&w=80"
    }
  };

  function normalizePortalName(role) {
    if (!role) return "";
    const r = String(role).trim().toLowerCase();
    if (r === "super_admin" || r === "superadmin") return "superadmin";
    return r;
  }

  function detectContextRole() {
    const path = (window.location.pathname || "").replace(/\\/g, "/").toLowerCase();
    const match = path.match(/\/pages\/(admin|teacher|student|principal|shared)\//);
    const pathSeg = match ? match[1] : null;
    const file = (path.split("/").pop() || "").toLowerCase();

    const params = new URLSearchParams(window.location.search || "");
    const qRole = normalizePortalName(params.get("portal") || params.get("role") || "");
    const staffFiles = ["admin-services.html", "principal-lost-found.html", "admin-campuses.html", "admin-school-information.html", "admin-settings.html"];
    // A portal directory owns its identity. Query-string previews are only for
    // superadmin / staff, which have no directory of their own, and only on the
    // directories their published navigation actually links into. This keeps
    // ?portal=admin from turning a Principal page into an Admin session.
    const ownedDir = ["admin", "teacher", "student", "principal"].includes(pathSeg) ? pathSeg : "";
    if (qRole && DEMO_USERS[qRole]) {
      if (qRole === "staff" && (pathSeg === "shared" || staffFiles.includes(file))) return "staff";
      if (qRole === "superadmin" && (pathSeg === "admin" || pathSeg === "shared")) return "superadmin";
      if (ownedDir && qRole !== ownedDir) { /* fall through to the directory role */ }
      else if (pathSeg === "shared" || pathSeg === qRole) return qRole;
    }

    if (pathSeg && pathSeg !== "shared" && DEMO_USERS[pathSeg]) return pathSeg;

    const pageRole = normalizePortalName(window.PAGE && window.PAGE.role);
    if (pageRole && DEMO_USERS[pageRole]) {
      return pageRole;
    }

    const stored = normalizePortalName(localStorage.getItem("ngis_active_portal") || "");
    if (stored && DEMO_USERS[stored]) {
      if (stored === "staff" && (pathSeg === "shared" || staffFiles.includes(file))) return "staff";
      if (stored === "superadmin" && (pathSeg === "admin" || pathSeg === "shared")) return "superadmin";
      if (!pathSeg || pathSeg === "shared" || pathSeg === stored) return stored;
    }

    return "student";
  }

  const Auth = {
    DEMO_USERS,

    /** Save token + user after successful login */
    setSession(token, user) {
      try {
        localStorage.setItem(TOKEN_KEY, token);
        localStorage.setItem(USER_KEY, JSON.stringify(user));
        localStorage.removeItem("ngis_session_mode");
        if (user && user.role) {
          const norm = normalizePortalName(user.portal || user.role);
          localStorage.setItem("ngis_active_portal", norm);
        }
        writeActorCookie(user && (user.email || user.username));
      } catch (e) {}
    },

    /** Activate a demo role and persist */
    setDemoUser(role) {
      const normalized = normalizePortalName(role);
      const targetRole = DEMO_USERS[normalized] ? normalized : detectContextRole();
      const user = DEMO_USERS[targetRole] || DEMO_USERS.student;
      this.setSession("mock-jwt-token-" + targetRole, user);
      return user;
    },

    /** Switch demo user and navigate to target portal */
    switchDemo(role, redirectUrl) {
      const normalized = normalizePortalName(role);
      this.setDemoUser(normalized);
      const rootPrefix = (window.location.pathname || "").indexOf("/pages/") !== -1 ? "../../" : "";
      const homeUrls = {
        superadmin: rootPrefix + "pages/admin/admin.html?portal=superadmin",
        admin: rootPrefix + "pages/admin/admin.html",
        staff: rootPrefix + "pages/admin/admin-services.html?portal=staff",
        teacher: rootPrefix + "pages/teacher/teacher.html",
        student: rootPrefix + "pages/student/student.html",
        principal: rootPrefix + "pages/principal/principal.html"
      };
      window.location.href = redirectUrl || homeUrls[normalized] || (rootPrefix + "index.html");
    },

    /** Clear session (logout) */
    clearSession() {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
      localStorage.removeItem("ngis_active_portal");
      localStorage.removeItem("ngis_session_mode");
      writeActorCookie("");
    },

    /**
     * Identity used by BOTH the client and server access gates.
     * Returns "" for passive demo browsing so no enforcement is applied;
     * an explicit login or explicit portal choice activates the real resolver.
     */
    actor() {
      try {
        if (localStorage.getItem("ngis_session_mode") === "passive") return "";
        const parsed = JSON.parse(localStorage.getItem(USER_KEY) || "null") ||
          JSON.parse(localStorage.getItem("auth_user") || "null");
        const value = parsed && (parsed.email || parsed.username);
        return value ? String(value).trim().toLowerCase() : "";
      } catch (e) {
        return "";
      }
    },

    /** Re-sync the identity cookie (also used after external localStorage writes). */
    syncActorCookie: syncActorCookie,

    /** True when the user signed in or explicitly selected a portal session */
    hasExplicitSession() {
      try {
        const raw = localStorage.getItem(USER_KEY);
        if (!raw) return false;
        if (localStorage.getItem("ngis_session_mode") === "passive") return false;
        const parsed = JSON.parse(raw);
        return Boolean(parsed && parsed.role);
      } catch (e) {
        return false;
      }
    },

    /** Check whether a role is allowed to access the given path/url */
    isRoleAllowedForPath(role, pathname, search) {
      const r = normalizePortalName(role);
      const p = (pathname || window.location.pathname || "").replace(/\\/g, "/").toLowerCase();
      const m = p.match(/\/pages\/(admin|teacher|student|principal|shared)\//);
      if (!m) return true;
      const seg = m[1];
      const file = (p.split("/").pop() || "").toLowerCase();
      if (seg === "shared") return true;
      if (r === "superadmin" || r === "admin") {
        return seg === "admin" || seg === "principal" || seg === "shared";
      }
      if (r === "editor") {
        return seg === "admin" || seg === "shared";
      }
      if (r === "principal") {
        if (seg === "principal" || seg === "shared") return true;
        return ["admin-school-information.html", "admin-dashboard-content.html", "admin-timetables.html"].includes(file);
      }
      if (r === "staff") {
        const staffAllowed = [
          "admin-services.html",
          "principal-lost-found.html",
          "admin-campuses.html",
          "admin-school-information.html",
          "admin-settings.html"
        ];
        return staffAllowed.includes(file);
      }
      return seg === r;
    },

    /** Get current JWT or generate demo token */
    getToken() {
      if (this.hasExplicitSession()) {
        const token = localStorage.getItem(TOKEN_KEY);
        if (token) return token;
      }
      const role = detectContextRole();
      const demoToken = "mock-jwt-token-" + role;
      try { localStorage.setItem(TOKEN_KEY, demoToken); } catch (e) {}
      return demoToken;
    },

    /** Get current user object or generate demo persona */
    getUser() {
      if (this.hasExplicitSession()) {
        try {
          const parsed = JSON.parse(localStorage.getItem(USER_KEY) || "null");
          if (parsed && parsed.role) return parsed;
        } catch (e) {}
      }
      // Passive demo-first fallback: resolve from current URL context without locking future portals
      const defaultRole = detectContextRole();
      const demoUser = DEMO_USERS[defaultRole] || DEMO_USERS.student;
      try {
        localStorage.setItem(USER_KEY, JSON.stringify(demoUser));
        localStorage.setItem(TOKEN_KEY, "mock-jwt-token-" + defaultRole);
        localStorage.setItem("ngis_session_mode", "passive");
      } catch (e) {}
      return demoUser;
    },

    /** Check if user is logged in (Always true in demo-first mode) */
    isAuthenticated() {
      return true;
    },

    /** Get current role */
    getRole() {
      const user = this.getUser();
      return normalizePortalName(user ? (user.portal || user.role) : detectContextRole());
    },

    /**
     * Login
     * @returns {Promise<{token, user}>}
     */
    async login(email, password) {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const json = await res.json();

      if (!res.ok) {
        throw new Error(json.error?.message || "Login failed");
      }

      this.setSession(json.data.token, json.data.user);
      return json.data;
    },

    /** Logout and redirect to home */
    logout() {
      this.clearSession();
      window.location.href = (window.location.pathname.indexOf("/pages/") !== -1 ? "../../" : "") + "index.html";
    },

    /**
     * Authenticated fetch wrapper
     * Automatically attaches Bearer token and handles 401
     */
    async api(url, options = {}) {
      const token = this.getToken();
      const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      };

      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      try {
        const res = await fetch(url, {
          ...options,
          headers,
        });

        if (res.status === 401) {
          console.warn("[NGIS Demo] 401 response — refreshing demo session token...");
          const wasExplicit = this.hasExplicitSession();
          let role;
          if (wasExplicit) {
            // An explicit session owns its identity. A background 401 must never
            // downgrade the signed-in role to the URL directory — a Super Admin
            // sitting on /pages/admin/* is still a Super Admin, not the plain
            // Admin persona. Directory precedence (e.g. a super_admin preview
            // landing on a Principal page) is already applied by
            // layout.js resolvePortalRole(), so the stored identity is kept.
            role = normalizePortalName(this.getRole()) || detectContextRole();
          } else {
            // Passive browsing follows the URL directory, not a cached persona.
            // A stale preview must not be re-persisted while sitting on another
            // portal's page.
            role = detectContextRole();
            this.setDemoUser(role);
            // A passive visitor must stay passive. Becoming an explicit session
            // merely because a demo endpoint returned 401 would write the
            // ngis_actor cookie, activate the server-side access gate and
            // silently lock the published demo out of the other portals.
            try { localStorage.setItem("ngis_session_mode", "passive"); } catch (e) {}
            writeActorCookie("");
          }
          headers["Authorization"] = `Bearer mock-jwt-token-${role}`;
          const retryRes = await fetch(url, { ...options, headers });
          return await retryRes.json();
        }

        const json = await res.json();
        if (!res.ok) {
          throw new Error(json.error?.message || "Request failed");
        }
        return json;
      } catch (err) {
        console.warn("[NGIS Demo] API fetch failed:", url, err.message);
        throw err;
      }
    },

    /**
     * Require authentication + optional role check
     */
    requireAuth(allowedRoles = []) {
      const role = this.getRole();
      if (allowedRoles.length > 0 && !allowedRoles.includes(role)) {
        // In demo mode, switch to the needed role seamlessly
        this.setDemoUser(allowedRoles[0]);
        return true;
      }
      return true;
    },
  };

  window.NGISAuth = Auth;

  // Identity may be written by index.html's portal picker or restored from a
  // previous tab, so re-derive the cookie on every script load rather than
  // trusting only setSession().
  syncActorCookie();
})(window);
