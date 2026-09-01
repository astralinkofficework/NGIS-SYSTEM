/**
 * NGIS School ERP — Frontend Auth Helper
 * Handles login, token storage, and authenticated API requests.
 */

(function (window) {
  "use strict";

  const TOKEN_KEY = "ngis_token";
  const USER_KEY = "ngis_user";

  const Auth = {
    /** Save token + user after successful login */
    setSession(token, user) {
      localStorage.setItem(TOKEN_KEY, token);
      localStorage.setItem(USER_KEY, JSON.stringify(user));
    },

    /** Clear session (logout) */
    clearSession() {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
    },

    /** Get current JWT */
    getToken() {
      return localStorage.getItem(TOKEN_KEY);
    },

    /** Get current user object */
    getUser() {
      const raw = localStorage.getItem(USER_KEY);
      if (!raw) return null;
      try {
        return JSON.parse(raw);
      } catch {
        return null;
      }
    },

    /** Check if user is logged in */
    isAuthenticated() {
      return !!this.getToken();
    },

    /** Get current role */
    getRole() {
      const user = this.getUser();
      return user ? user.role : null;
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
      window.location.href = "/index.html";
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

      const res = await fetch(url, {
        ...options,
        headers,
      });

      // Auto logout on unauthorized
      if (res.status === 401) {
        this.clearSession();
        window.location.href = "/index.html";
        throw new Error("Session expired. Please login again.");
      }

      const json = await res.json();

      if (!res.ok) {
        throw new Error(json.error?.message || "Request failed");
      }

      return json;
    },

    /**
     * Require authentication + optional role check
     * Call this at the top of protected pages
     */
    requireAuth(allowedRoles = []) {
      if (!this.isAuthenticated()) {
        window.location.href = "/index.html";
        return false;
      }

      if (allowedRoles.length > 0) {
        const role = this.getRole();
        if (!allowedRoles.includes(role)) {
          // Redirect to correct portal
          const portals = {
            admin: "/pages/admin/admin.html",
            teacher: "/pages/teacher/teacher.html",
            student: "/pages/student/student.html",
            parent: "/pages/parent/parent.html",
          };
          window.location.href = portals[role] || "/index.html";
          return false;
        }
      }

      return true;
    },
  };

  window.NGISAuth = Auth;
})(window);
