/**
 * NGIS School ERP — Page Protection
 * Include this script on every protected portal page.
 *
 * Usage:
 *   <script src="../../assets/js/auth.js"></script>
 *   <script src="../../assets/js/protect.js"></script>
 *   <script>
 *     NGISProtect.require(['student']); // or ['admin'], ['teacher'], ['parent']
 *   </script>
 */

(function (window) {
  "use strict";

  const Protect = {
    /**
     * Require authentication and optionally specific roles.
     * Redirects to login or correct portal if not allowed.
     */
    require(allowedRoles = []) {
      if (!window.NGISAuth) {
        console.error("NGISAuth not loaded. Include auth.js before protect.js");
        return false;
      }

      if (!NGISAuth.isAuthenticated()) {
        window.location.href = "/index.html";
        return false;
      }

      const role = NGISAuth.getRole();

      if (allowedRoles.length > 0 && !allowedRoles.includes(role)) {
        // Redirect to the correct portal for this user's role
        const portals = {
          admin: "/pages/admin/admin.html",
          teacher: "/pages/teacher/teacher.html",
          student: "/pages/student/student.html",
          parent: "/pages/parent/parent.html",
        };
        window.location.href = portals[role] || "/index.html";
        return false;
      }

      return true;
    },

    /**
     * Load current user into common profile elements on the page.
     * Looks for elements with data-user attributes.
     */
    async hydrateUser() {
      if (!window.NGISAuth || !NGISAuth.isAuthenticated()) return null;

      try {
        const res = await NGISAuth.api("/api/auth/me");
        const user = res.data;

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
          el.textContent = (user.role || "").charAt(0).toUpperCase() + (user.role || "").slice(1);
        });

        return user;
      } catch (err) {
        console.error("Failed to hydrate user:", err);
        return null;
      }
    },
  };

  window.NGISProtect = Protect;
})(window);
