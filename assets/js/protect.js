/**
 * NGIS School ERP — Page Protection
 * Soft mode: if not authenticated, allow page view (for static Netlify demo).
 * Role mismatch still redirects when a session exists.
 */

(function (window) {
  "use strict";

  const Protect = {
    require(allowedRoles = []) {
      if (!window.NGISAuth) {
        console.warn("NGISAuth not loaded — allowing page view");
        return true;
      }

      // No session: allow static demo browsing (do not force login modal)
      if (!NGISAuth.isAuthenticated()) {
        return true;
      }

      const role = NGISAuth.getRole();

      if (allowedRoles.length > 0 && !allowedRoles.includes(role)) {
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

    async hydrateUser() {
      if (!window.NGISAuth || !NGISAuth.isAuthenticated()) return null;

      try {
        const res = await NGISAuth.api("/api/auth/me");
        const user = res.data;

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
