/**
 * Teacher Portal — Auth Bootstrap
 */
(function () {
  "use strict";

  if (!window.NGISProtect || !NGISProtect.require(["teacher"])) {
    return;
  }

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
      console.error("[NGIS] Failed to load teacher data:", err.message);
    }
  });
})();
