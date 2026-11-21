/**
 * Admin Portal — Auth Bootstrap
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", async function () {
    try {
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
      }

      // Load student count for dashboard widgets if present
      try {
        const studentsRes = await NGISAuth.api("/api/admin/students");
        const totalEl = document.querySelector("[data-stat='total-students']");
        if (totalEl) {
          totalEl.textContent = studentsRes.meta?.total ?? studentsRes.data?.length ?? 0;
        }
      } catch (_) {}

      console.log("[NGIS] Admin portal hydrated", user?.firstName);
    } catch (err) {
      console.warn("[NGIS Demo] Using local demo session for admin hydration:", err.message);
      const user = (window.NGISAuth && NGISAuth.getUser()) || { firstName: "Sok Panha", lastName: "Heng", email: "admin@ngis.edu.kh" };
      document.querySelectorAll("[data-user='name']").forEach(el => {
        el.textContent = `${user.firstName || ""} ${user.lastName || ""}`.trim();
      });
      document.querySelectorAll("[data-user='email']").forEach(el => {
        el.textContent = user.email || "";
      });
    }
  });
})();
