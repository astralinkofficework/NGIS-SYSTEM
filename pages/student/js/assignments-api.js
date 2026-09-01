/**
 * Student Assignments — load from real API
 * Include after auth.js + protect.js on student-assignments.html
 */
(function () {
  "use strict";

  async function loadAssignments() {
    const container = document.getElementById("assignmentsList") ||
                      document.querySelector(".assignments-list") ||
                      document.querySelector("[data-assignments]");

    // If no dedicated container, create a simple panel at top of main
    let target = container;
    if (!target) {
      const main = document.querySelector("main") || document.querySelector(".main") || document.body;
      target = document.createElement("div");
      target.id = "assignmentsList";
      target.style.cssText = "max-width:900px;margin:16px auto;padding:0 16px";
      main.insertBefore(target, main.firstChild?.nextSibling || null);
    }

    target.innerHTML = `<p style="color:#64748b;padding:12px">Loading assignments…</p>`;

    try {
      if (!window.NGISAuth || !NGISAuth.isAuthenticated()) {
        target.innerHTML = `<p style="color:#b91c1c;padding:12px">Please sign in to view assignments.</p>`;
        return;
      }

      const res = await NGISAuth.api("/api/assignments");
      const items = res.data || [];

      if (!items.length) {
        target.innerHTML = `
          <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:20px;text-align:center">
            <p style="margin:0;color:#64748b">No assignments yet.</p>
          </div>`;
        return;
      }

      target.innerHTML = `
        <div style="margin-bottom:12px;font-weight:700;font-size:18px;color:#0f172a">
          My Assignments <span style="color:#64748b;font-weight:500;font-size:14px">(${items.length})</span>
        </div>
        <div style="display:flex;flex-direction:column;gap:10px">
          ${items.map(a => {
            const status = a.submission_status || "pending";
            const statusColor = status === "graded" ? "#16a34a" : status === "submitted" || status === "late" ? "#2563eb" : "#d97706";
            const statusLabel = status.charAt(0).toUpperCase() + status.slice(1);
            return `
              <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px;display:flex;justify-content:space-between;align-items:flex-start;gap:12px">
                <div>
                  <div style="font-weight:700;color:#0f172a;margin-bottom:4px">${escapeHtml(a.title)}</div>
                  <div style="font-size:13px;color:#64748b;margin-bottom:6px">
                    ${escapeHtml(a.subject_name || "Subject")} · Due ${a.due_date || "—"}
                  </div>
                  <div style="font-size:13px;color:#475569">${escapeHtml((a.description || "").slice(0, 120))}${(a.description || "").length > 120 ? "…" : ""}</div>
                  ${a.score != null ? `<div style="margin-top:8px;font-size:13px;font-weight:600;color:#16a34a">Score: ${a.score}</div>` : ""}
                </div>
                <div style="display:flex;flex-direction:column;align-items:flex-end;gap:8px">
                  <span style="font-size:12px;font-weight:700;color:${statusColor};background:${statusColor}15;padding:4px 10px;border-radius:999px">${statusLabel}</span>
                  ${status === "pending" ? `
                    <button data-submit="${a.id}" style="border:none;background:#2563eb;color:#fff;padding:8px 14px;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer">
                      Submit
                    </button>` : ""}
                </div>
              </div>`;
          }).join("")}
        </div>`;

      // Wire submit buttons
      target.querySelectorAll("[data-submit]").forEach(btn => {
        btn.addEventListener("click", async () => {
          const id = btn.getAttribute("data-submit");
          btn.disabled = true;
          btn.textContent = "Submitting…";
          try {
            await NGISAuth.api(`/api/assignments/${id}/submit`, { method: "POST", body: "{}" });
            loadAssignments(); // refresh
          } catch (err) {
            alert(err.message || "Submit failed");
            btn.disabled = false;
            btn.textContent = "Submit";
          }
        });
      });
    } catch (err) {
      target.innerHTML = `<p style="color:#b91c1c;padding:12px">Failed to load assignments: ${escapeHtml(err.message)}</p>`;
    }
  }

  function escapeHtml(str) {
    return String(str || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", loadAssignments);
  } else {
    loadAssignments();
  }
})();
