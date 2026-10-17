/**
 * Teacher Portal — Auth Bootstrap
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", async function () {
    try {
      const res = await NGISAuth.api("/api/teacher/me");
      const data = res.data;

      window.NGIS_CURRENT_TEACHER = data.teacher;
      window.NGIS_CURRENT_USER = data.user;

      const user = data.user;
      if (user) {
        document.querySelectorAll("[data-user='name']").forEach(el => {
          el.textContent = `${user.firstName || ""} ${user.lastName || ""}`.trim();
        });
        document.querySelectorAll("[data-user='email']").forEach(el => {
          el.textContent = user.email || "";
        });
      }

      console.log("[NGIS] Teacher portal hydrated", user?.firstName);
    } catch (err) {
      console.warn("[NGIS Demo] Using local demo session for teacher hydration:", err.message);
      const user = (window.NGISAuth && NGISAuth.getUser()) || { firstName: "Dr. Sarah", lastName: "Jenkins", email: "teacher@ngis.edu.kh" };
      document.querySelectorAll("[data-user='name']").forEach(el => {
        el.textContent = `${user.firstName || ""} ${user.lastName || ""}`.trim();
      });
      document.querySelectorAll("[data-user='email']").forEach(el => {
        el.textContent = user.email || "";
      });
    }
  });
})();
