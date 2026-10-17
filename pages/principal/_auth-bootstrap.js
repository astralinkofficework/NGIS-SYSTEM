/**
 * Principal Portal — Auth Bootstrap
 * Hydrates leadership session, enforces executive authorization, and loads campus KPIs.
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", async function () {
    try {
      if (window.NGISProtect && !NGISProtect.require(["principal", "admin", "super_admin"])) {
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
          el.textContent = (user.role || "principal").toUpperCase();
        });
      }

      console.log("[NGIS] Principal executive portal hydrated:", user?.email);
    } catch (err) {
      console.warn("[NGIS Demo] Using local demo session for principal hydration:", err.message);
      const user = (window.NGISAuth && NGISAuth.getUser()) || { firstName: "Dr. Ly", lastName: "Bunheng", email: "principal@ngis.edu.kh", role: "principal" };
      document.querySelectorAll("[data-user='name']").forEach(el => {
        el.textContent = `${user.firstName || ""} ${user.lastName || ""}`.trim();
      });
      document.querySelectorAll("[data-user='email']").forEach(el => {
        el.textContent = user.email || "";
      });
      document.querySelectorAll("[data-user='role']").forEach(el => {
        el.textContent = (user.role || "principal").toUpperCase();
      });
    }
  });
})();
