/**
 * NGIS School ERP — Page Protection (Demo-First Mode)
 * Include this script on every protected portal page.
 */

(function (window) {
  "use strict";

  const Protect = {
    /**
     * Require authentication and optionally specific roles.
     * In Demo-First mode: seamlessly auto-adopts the demo role for the page
     * so that all users can explore and test every portal immediately.
     */
    require(allowedRoles = []) {
      if (!window.NGISAuth) {
        console.error("NGISAuth not loaded. Include auth.js before protect.js");
        return false;
      }

      const role = NGISAuth.getRole();

      if (allowedRoles.length > 0 && !allowedRoles.includes(role)) {
        // Demo first: auto-adopt role for this page rather than locking out
        const targetRole = allowedRoles[0];
        if (targetRole && NGISAuth.DEMO_USERS && NGISAuth.DEMO_USERS[targetRole]) {
          console.info(`[NGIS Demo] Auto-activating demo persona '${targetRole}' for page access.`);
          NGISAuth.setDemoUser(targetRole);
          return true;
        }
      }

      return true;
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
})(window);
