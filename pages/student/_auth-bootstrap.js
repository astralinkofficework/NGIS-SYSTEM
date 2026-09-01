/**
 * Student Portal — Auth Bootstrap
 * Include this at the top of every student page (before other scripts).
 *
 * <script src="../../assets/js/auth.js"></script>
 * <script src="../../assets/js/protect.js"></script>
 * <script src="_auth-bootstrap.js"></script>
 */

(function () {
  "use strict";

  // Require student role
  if (!window.NGISProtect || !NGISProtect.require(["student"])) {
    return; // Will redirect
  }

  // Hydrate profile data when DOM is ready
  document.addEventListener("DOMContentLoaded", async function () {
    try {
      const res = await NGISAuth.api("/api/student/dashboard");
      const data = res.data;
      const student = data.student;
      const user = data.user;

      // Update profile card if present
      const nameEl = document.querySelector(".ov-profile-name");
      if (nameEl) {
        nameEl.textContent = `${user.firstName || ""} ${user.lastName || ""}`.trim();
      }

      const gradeEl = document.querySelector(".ov-profile-grade");
      if (gradeEl && student) {
        gradeEl.innerHTML = `${student.grade || ""} &nbsp;·&nbsp; ${student.student_number || ""}`;
      }

      // Update email/phone if present
      const infoRows = document.querySelectorAll(".ov-info-row");
      if (infoRows.length >= 1 && user.email) {
        infoRows[0].innerHTML = `<span class="mi">mail</span>${user.email}`;
      }
      if (infoRows.length >= 2 && user.phone) {
        infoRows[1].innerHTML = `<span class="mi">phone</span>${user.phone}`;
      }

      // Update attendance percentage if present
      const attPct = document.querySelector(".att-pct");
      if (attPct && student) {
        attPct.textContent = `${Math.round(student.attendance_rate || 0)}%`;
      }

      // Store for other scripts
      window.NGIS_CURRENT_STUDENT = student;
      window.NGIS_CURRENT_USER = user;

      console.log("[NGIS] Student dashboard hydrated", user.firstName, student?.student_number);
    } catch (err) {
      console.error("[NGIS] Failed to load student dashboard:", err.message);
    }
  });
})();
