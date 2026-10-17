/**
 * Staff Portal — Auth Bootstrap
 * Hydrates staff session, enforces authorization, and initializes operational state.
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", async function () {
    try {
      if (window.NGISProtect && !NGISProtect.require(["staff", "admin", "super_admin"])) {
        return;
      }

      const res = await NGISAuth.api("/api/auth/me");
      const user = res.data;
      window.NGIS_CURRENT_USER = user;

      if (user) {
        document.querySelectorAll("[data-user='name']").forEach(el => {
          el.textContent = `${user.firstName || ""} ${user.lastName || ""}`.trim();
        });
        document.querySelectorAll("[data-user='email']").forEach(el => {
          el.textContent = user.email || "";
        });
        document.querySelectorAll("[data-user='role']").forEach(el => {
          el.textContent = (user.role || "staff").toUpperCase();
        });
      }

      console.log("[NGIS] Staff portal hydrated:", user?.email);
    } catch (err) {
      console.warn("[NGIS Demo] Using local demo session for staff hydration:", err.message);
      const user = (window.NGISAuth && NGISAuth.getUser()) || { firstName: "Ms. Sreymom", lastName: "Lim", email: "staff@ngis.edu.kh", role: "staff" };
      document.querySelectorAll("[data-user='name']").forEach(el => {
        el.textContent = `${user.firstName || ""} ${user.lastName || ""}`.trim();
      });
      document.querySelectorAll("[data-user='email']").forEach(el => {
        el.textContent = user.email || "";
      });
      document.querySelectorAll("[data-user='role']").forEach(el => {
        el.textContent = (user.role || "staff").toUpperCase();
      });
    }
  });
})();
