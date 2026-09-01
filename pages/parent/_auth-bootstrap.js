/**
 * Parent Portal — Auth Bootstrap
 */
(function () {
  "use strict";

  if (!window.NGISProtect || !NGISProtect.require(["parent"])) {
    return;
  }

  document.addEventListener("DOMContentLoaded", async function () {
    try {
      const res = await NGISAuth.api("/api/parent/children");
      const children = res.data || [];

      window.NGIS_CHILDREN = children;
      window.NGIS_CURRENT_USER = NGISAuth.getUser();

      // If page has a children list container, populate it
      const listEl = document.getElementById("childrenList");
      if (listEl && children.length) {
        listEl.innerHTML = children.map(c => `
          <div class="child-card" data-id="${c.id}">
            <div class="child-name">${c.first_name || ""} ${c.last_name || ""}</div>
            <div class="child-meta">${c.grade || ""} · ${c.student_number || ""}</div>
          </div>
        `).join("");
      }

      // Update any profile name elements
      const user = NGISAuth.getUser();
      if (user) {
        document.querySelectorAll("[data-user='name']").forEach(el => {
          el.textContent = `${user.firstName || ""} ${user.lastName || ""}`.trim();
        });
      }

      console.log("[NGIS] Parent portal hydrated", children.length, "children");
    } catch (err) {
      console.error("[NGIS] Failed to load parent data:", err.message);
    }
  });
})();
