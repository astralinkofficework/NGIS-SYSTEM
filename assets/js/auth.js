/**
 * NGIS School ERP — Frontend Auth Helper
 * Handles demo-first sessions, token storage, and authenticated API requests.
 */

(function (window) {
  "use strict";

  const TOKEN_KEY = "ngis_token";
  const USER_KEY = "ngis_user";

  const DEMO_USERS = {
    admin: {
      id: "ADM-2024-001",
      firstName: "Sok Panha",
      lastName: "Heng",
      role: "admin",
      portal: "admin",
      email: "admin@ngis.edu.kh",
      title: "Super Administrator",
      avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=80&fit=crop&crop=face"
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
    staff: {
      id: "STF-2024-015",
      firstName: "Ms. Sreymom",
      lastName: "Lim",
      role: "staff",
      portal: "staff",
      email: "staff@ngis.edu.kh",
      title: "Operations Coordinator",
      avatar: "https://images.pexels.com/photos/1181519/pexels-photo-1181519.jpeg?auto=compress&cs=tinysrgb&w=80"
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

  function detectContextRole() {
    const path = (window.location.pathname || "").toLowerCase();
    const match = path.match(/\/pages\/(admin|teacher|student|staff|principal)\//);
    if (match && DEMO_USERS[match[1]]) return match[1];

    const params = new URLSearchParams(window.location.search || "");
    const qRole = (params.get("portal") || params.get("role") || "").toLowerCase();
    if (DEMO_USERS[qRole]) return qRole;

    const stored = (localStorage.getItem("ngis_active_portal") || "").toLowerCase();
    if (DEMO_USERS[stored]) return stored;

    if (window.PAGE && window.PAGE.role && DEMO_USERS[window.PAGE.role]) {
      return window.PAGE.role;
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
        if (user && user.role) {
          localStorage.setItem("ngis_active_portal", user.role);
          localStorage.setItem("ngis_chat_user", JSON.stringify({
            id: user.id,
            name: `${user.firstName || ""} ${user.lastName || ""}`.trim(),
            role: user.role,
            avatar: user.avatar || ""
          }));
        }
      } catch (e) {}
    },

    /** Activate a demo role and persist */
    setDemoUser(role) {
      const targetRole = DEMO_USERS[role] ? role : detectContextRole();
      const user = DEMO_USERS[targetRole] || DEMO_USERS.student;
      this.setSession("mock-jwt-token-" + targetRole, user);
      return user;
    },

    /** Switch demo user and navigate to target portal */
    switchDemo(role, redirectUrl) {
      this.setDemoUser(role);
      const rootPrefix = (window.location.pathname || "").indexOf("/pages/") !== -1 ? "../../" : "";
      const homeUrls = {
        admin: rootPrefix + "pages/admin/admin.html",
        teacher: rootPrefix + "pages/teacher/teacher.html",
        student: rootPrefix + "pages/student/student.html",
        principal: rootPrefix + "pages/principal/principal.html",
        staff: rootPrefix + "pages/staff/staff.html"
      };
      window.location.href = redirectUrl || homeUrls[role] || (rootPrefix + "index.html");
    },

    /** Clear session (logout) */
    clearSession() {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
      localStorage.removeItem("ngis_active_portal");
    },

    /** Get current JWT or generate demo token */
    getToken() {
      const token = localStorage.getItem(TOKEN_KEY);
      if (token) return token;
      const role = detectContextRole();
      const demoToken = "mock-jwt-token-" + role;
      try { localStorage.setItem(TOKEN_KEY, demoToken); } catch (e) {}
      return demoToken;
    },

    /** Get current user object or generate demo persona */
    getUser() {
      const raw = localStorage.getItem(USER_KEY);
      if (raw) {
        try {
          const parsed = JSON.parse(raw);
          if (parsed && parsed.role) return parsed;
        } catch (e) {}
      }
      // Demo-first fallback: auto-provision demo user matching context
      const defaultRole = detectContextRole();
      const demoUser = DEMO_USERS[defaultRole] || DEMO_USERS.student;
      try {
        localStorage.setItem(USER_KEY, JSON.stringify(demoUser));
        localStorage.setItem(TOKEN_KEY, "mock-jwt-token-" + defaultRole);
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
      return user ? user.role : detectContextRole();
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
          const role = this.getRole() || detectContextRole();
          this.setDemoUser(role);
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
})(window);
