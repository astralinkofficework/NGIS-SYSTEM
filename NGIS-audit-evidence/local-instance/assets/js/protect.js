/**
 * NGIS School ERP — Page Protection (Demo-First Mode)
 * Include this script on every protected portal page.
 */

(function (window) {
  "use strict";

  function normalizeRoleName(role) {
    const r = String(role || "").trim().toLowerCase();
    if (r === "super_admin" || r === "superadmin") return "superadmin";
    return r;
  }

  function redirectAccessDenied(role, neededRoles) {
    const pathname = (window.location.pathname || "").replace(/\\/g, "/");
    if (pathname.indexOf("/pages/shared/access-denied.html") !== -1) return false;
    const prefix = pathname.indexOf("/pages/") !== -1 ? "../../" : "";
    const attempted = encodeURIComponent(window.location.pathname + window.location.search);
    const needed = encodeURIComponent((neededRoles || []).join(","));
    const curRole = encodeURIComponent(role || "student");
    window.location.href = `${prefix}pages/shared/access-denied.html?attempted=${attempted}&role=${curRole}&needed=${needed}`;
    return false;
  }

  const Protect = {
    /**
     * Enforce role & portal boundaries when an explicit session is active.
     * In passive demo mode (unauthenticated fresh visits), adopts the contextual demo role.
     */
    require(allowedRoles = []) {
      if (!window.NGISAuth) {
        console.error("NGISAuth not loaded. Include auth.js before protect.js");
        return false;
      }

      const normalizedAllowed = (allowedRoles || []).map(normalizeRoleName);
      if (normalizedAllowed.includes("admin") && !normalizedAllowed.includes("superadmin")) {
        normalizedAllowed.push("superadmin");
      }

      const explicit = typeof NGISAuth.hasExplicitSession === "function" && NGISAuth.hasExplicitSession();
      const role = normalizeRoleName(NGISAuth.getRole());

      if (explicit) {
        if (typeof NGISAuth.isRoleAllowedForPath === "function" && !NGISAuth.isRoleAllowedForPath(role, window.location.pathname, window.location.search)) {
          return redirectAccessDenied(role, normalizedAllowed);
        }
        if (normalizedAllowed.length > 0 && !normalizedAllowed.includes(role)) {
          // Staff shares admin-school-information and principal-lost-found operational pages
          const pathAllowedForStaff = role === "staff" && typeof NGISAuth.isRoleAllowedForPath === "function" && NGISAuth.isRoleAllowedForPath("staff", window.location.pathname, window.location.search);
          if (!pathAllowedForStaff) {
            return redirectAccessDenied(role, normalizedAllowed);
          }
        }
        return true;
      }

      if (normalizedAllowed.length > 0 && !normalizedAllowed.includes(role)) {
        const targetRole = normalizedAllowed[0];
        if (targetRole && NGISAuth.DEMO_USERS && NGISAuth.DEMO_USERS[targetRole]) {
          NGISAuth.setDemoUser(targetRole);
          return true;
        }
      }

      return true;
    },

    /** Enforce portal directory boundary even on pages without inline Protect.require() */
    enforcePortalAccess() {
      if (!window.NGISAuth || typeof NGISAuth.hasExplicitSession !== "function") return true;
      if (!NGISAuth.hasExplicitSession()) return true;
      const role = normalizeRoleName(NGISAuth.getRole());
      if (typeof NGISAuth.isRoleAllowedForPath === "function" && !NGISAuth.isRoleAllowedForPath(role, window.location.pathname, window.location.search)) {
        return redirectAccessDenied(role, []);
      }
      return true;
    },

    /**
     * User Access & Visibility Control — direct-URL gate.
     * The server evaluates effective access (overrides, portals, roles); the
     * client only performs the redirect. Hiding a sidebar link is never the
     * security boundary. The shared sidebar shell already gates every page
     * that loads layout.js, so avoid a duplicate request when it is present.
     */
    async enforceUserAccess() {
      if (window.__NGIS_SIDEBAR_V2__) return true;
      // Prefer the filename: PAGE.active ids repeat across portals and would
      // resolve against the wrong portal's access rule.
      const file = (window.location.pathname || "").split("/").pop();
      const page = file || (window.PAGE && window.PAGE.active) || "";
      const portalMatch = (window.location.pathname || "").toLowerCase().match(/\/pages\/([^/]+)\//);
      const portal = portalMatch ? portalMatch[1] : "";
      let actor = "";
      try {
        // One identity source for both gates: an explicit session only.
        if (window.NGISAuth && typeof NGISAuth.actor === "function") {
          actor = NGISAuth.actor();
        } else {
          const u = (window.NGISAuth && typeof NGISAuth.getUser === "function" && NGISAuth.getUser()) ||
            JSON.parse(localStorage.getItem("auth_user") || "null");
          actor = u && (u.email || u.username) ? String(u.email || u.username).toLowerCase() : "";
        }
      } catch (_) { actor = ""; }
      try {
        const query = "?page=" + encodeURIComponent(page || "") +
          "&portal=" + encodeURIComponent(portal) +
          "&active=" + encodeURIComponent((window.PAGE && window.PAGE.active) || "");
        const res = await fetch("/api/roles-mgmt/my-access" + query,
          { headers: actor ? { "X-Actor": actor } : {} });
        const data = await res.json();
        if (data && data.enforced && data.allowed === false) {
          return redirectAccessDenied(
            (window.NGISAuth && typeof NGISAuth.getRole === "function" && NGISAuth.getRole()) || "",
            []);
        }
        return true;
      } catch (_) {
        return true; // offline / demo: keep the page available
      }
    },

    /**
     * Load current user into common profile elements on the page.
     * Looks for elements with data-user attributes.
     */
    async hydrateUser() {
      if (!window.NGISAuth) return null;

      try {
        const res = await NGISAuth.api("/api/auth/me");
        const user = res.data || NGISAuth.getUser();

        // Update common profile fields if present
        const nameEls = document.querySelectorAll("[data-user='name']");
        nameEls.forEach((el) => {
          el.textContent = `${user.firstName || ""} ${user.lastName || ""}`.trim();
        });

        const emailEls = document.querySelectorAll("[data-user='email']");
        emailEls.forEach((el) => {
          el.textContent = user.email || "";
        });

        const roleEls = document.querySelectorAll("[data-user='role']");
        roleEls.forEach((el) => {
          el.textContent = (user.role || "").toUpperCase();
        });

        return user;
      } catch (_) {
        const user = NGISAuth.getUser();
        if (user) {
          document.querySelectorAll("[data-user='name']").forEach((el) => {
            el.textContent = `${user.firstName || ""} ${user.lastName || ""}`.trim();
          });
          document.querySelectorAll("[data-user='email']").forEach((el) => {
            el.textContent = user.email || "";
          });
          document.querySelectorAll("[data-user='role']").forEach((el) => {
            el.textContent = (user.role || "").toUpperCase();
          });
        }
        return user;
      }
    },
  };

  window.NGISProtect = Protect;
  window.Protect = Protect;
  Protect.enforcePortalAccess();
  Protect.enforceUserAccess();
})(window);
