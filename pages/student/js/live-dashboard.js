/**
 * Student dashboard — hydrate live widgets from connected APIs
 */
(function () {
  function esc(s) {
    return String(s || "")
      .replace(/&/g, "&")
      .replace(/</g, "<")
      .replace(/>/g, ">");
  }

  async function hydrate() {
    if (!window.NGISAuth) return;

    // Profile header
    try {
      const me = await NGISAuth.api("/api/auth/me");
      const u = me.data || {};
      const s = u.student || {};
      const name = ((u.firstName || u.first_name || "") + " " + (u.lastName || u.last_name || "")).trim();
      const nameEl = document.querySelector(".ov-profile-name");
      const gradeEl = document.querySelector(".ov-profile-grade");
      const rows = document.querySelectorAll(".ov-info-row");
      if (nameEl) nameEl.textContent = name || "Student";
      if (gradeEl) gradeEl.textContent = (s.grade || "—") + (s.class_id ? " · " + s.class_id : "");
      if (rows[0]) rows[0].innerHTML = '<span class="mi">mail</span>' + esc(u.email || "—");
      if (rows[1]) rows[1].innerHTML = '<span class="mi">phone</span>' + esc(u.phone || "—");

      // Attendance %
      const pct = document.querySelector(".att-pct");
      if (pct && s.attendance_rate != null) {
        pct.textContent = Math.round(s.attendance_rate) + "%";
      }
    } catch (_) {}

    // Assignments → upcoming panel
    try {
      const res = await NGISAuth.api("/api/assignments");
      const items = (res.data || []).slice(0, 3);
      const panel = document.querySelector(".ov-upcoming .ov-inner-panel:nth-child(2)");
      if (panel && items.length) {
        panel.innerHTML =
          '<div class="ov-inner-head"><span class="mi" style="color:#16a34a">assignment</span>Assignments</div>' +
          items
            .map(
              (a) =>
                `<div class="ov-inner-item"><div class="ov-inner-item-t">${esc(a.title)}</div><div class="ov-inner-item-s">Due ${esc(
                  (a.due_date || "").slice(0, 10)
                )}</div></div>`
            )
            .join("");
      }

      const deadPanel = document.querySelector(".ov-deadline-panel");
      if (deadPanel && items.length) {
        deadPanel.innerHTML =
          '<div class="ov-deadline-head"><span class="mi" style="color:#e11d48">assignment</span>Assessments</div>' +
          items
            .map(
              (a) =>
                `<div class="ov-deadline-item"><div class="ov-deadline-dot" style="background:#e11d48"></div><div><div class="ov-deadline-item-t">${esc(
                  a.title
                )}</div><div class="ov-deadline-item-s">Due ${esc((a.due_date || "").slice(0, 10))}</div></div></div>`
            )
            .join("");
      }
    } catch (_) {}

    // Announcements
    try {
      const res = await NGISAuth.api("/api/announcements");
      const items = (res.data || []).slice(0, 3);
      const list = document.querySelector(".ann-list");
      if (list && items.length) {
        list.innerHTML = items
          .map(
            (a) => `
          <div class="ann-item">
            <div class="ann-body">
              <div class="ann-title">${esc(a.title)}</div>
              <div class="ann-desc">${esc((a.body || "").slice(0, 120))}${(a.body || "").length > 120 ? "…" : ""}</div>
              <div class="ann-time">${esc((a.created_at || "").slice(0, 10))}</div>
            </div>
          </div>`
          )
          .join("");
      }
    } catch (_) {}
  }

  // Wait for auth bootstrap
  setTimeout(hydrate, 400);
})();
