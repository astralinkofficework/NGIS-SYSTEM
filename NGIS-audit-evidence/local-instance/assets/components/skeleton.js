/**
 * ============================================================
 * NGIS ERP — Reusable Skeleton Component (Rule 1 Compliant)
 * Rule 1: No spinning loaders where the layout is known.
 * Skeletons reserve the EXACT space of final content so nothing
 * jumps when data arrives.
 * 
 * Provides layout skeletons for all 5 primary screen types:
 * 1. dashboard
 * 2. feed
 * 3. list
 * 4. detail
 * 5. profile
 * ============================================================
 */

(function (window, document) {
  "use strict";

  const NGISSkeleton = {
    // Generates the layout-accurate HTML for the 5 main screen templates
    templates: {
      /**
       * 1. DASHBOARD SKELETON
       * Matches hero header + 4 KPI stat cards + split columns (table & activity)
       */
      dashboard() {
        return `
          <div class="ngis-skeleton-screen ngis-skeleton-dashboard" aria-busy="true" aria-label="Loading dashboard...">
            <!-- Hero banner placeholder -->
            <div class="ngis-skel-banner ngis-skel-pulse" style="height:110px; border-radius:12px; margin-bottom:20px; background:#ECECED; border:1px solid #E5E5E8; padding:20px; display:flex; flex-direction:column; justify-content:center;">
              <div class="ngis-skel-line" style="width:240px; height:18px; margin-bottom:10px; background:#DFDFE2;"></div>
              <div class="ngis-skel-line" style="width:380px; height:13px; background:#DFDFE2;"></div>
            </div>

            <!-- 4 KPI stat cards -->
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:16px; margin-bottom:24px;">
              ${Array(4).fill(0).map(() => `
                <div class="ngis-skel-card ngis-skel-pulse" style="height:100px; background:#FFFFFF; border:1px solid #E5E5E8; border-radius:12px; padding:16px; display:flex; justify-content:space-between; align-items:center;">
                  <div style="flex:1;">
                    <div class="ngis-skel-line" style="width:70px; height:11px; margin-bottom:12px; background:#ECECED;"></div>
                    <div class="ngis-skel-line" style="width:90px; height:24px; background:#DFDFE2;"></div>
                  </div>
                  <div class="ngis-skel-circle" style="width:40px; height:40px; border-radius:50%; background:#ECECED; flex-shrink:0;"></div>
                </div>
              `).join("")}
            </div>

            <!-- Split Section: Main list & side card -->
            <div style="display:grid; grid-template-columns: 2fr 1fr; gap:20px;">
              <!-- Main table skeleton -->
              <div class="ngis-skel-card ngis-skel-pulse" style="background:#FFFFFF; border:1px solid #E5E5E8; border-radius:12px; padding:20px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:18px;">
                  <div class="ngis-skel-line" style="width:160px; height:16px; background:#DFDFE2;"></div>
                  <div class="ngis-skel-line" style="width:80px; height:16px; background:#ECECED;"></div>
                </div>
                ${Array(5).fill(0).map((_, i) => `
                  <div style="display:flex; align-items:center; gap:14px; padding:12px 0; border-top:1px solid #F3F3F5;">
                    <div class="ngis-skel-circle" style="width:36px; height:36px; border-radius:50%; background:#ECECED; flex-shrink:0;"></div>
                    <div style="flex:1;">
                      <div class="ngis-skel-line" style="width:${55 + (i % 3) * 15}%; height:13px; margin-bottom:6px; background:#DFDFE2;"></div>
                      <div class="ngis-skel-line" style="width:40%; height:10px; background:#ECECED;"></div>
                    </div>
                    <div class="ngis-skel-line" style="width:60px; height:20px; border-radius:6px; background:#ECECED;"></div>
                  </div>
                `).join("")}
              </div>

              <!-- Side panel skeleton -->
              <div class="ngis-skel-card ngis-skel-pulse" style="background:#FFFFFF; border:1px solid #E5E5E8; border-radius:12px; padding:20px;">
                <div class="ngis-skel-line" style="width:120px; height:16px; margin-bottom:18px; background:#DFDFE2;"></div>
                ${Array(4).fill(0).map(() => `
                  <div style="padding:10px 0; border-top:1px solid #F3F3F5;">
                    <div class="ngis-skel-line" style="width:80%; height:12px; margin-bottom:6px; background:#DFDFE2;"></div>
                    <div class="ngis-skel-line" style="width:50%; height:10px; background:#ECECED;"></div>
                  </div>
                `).join("")}
              </div>
            </div>
          </div>
        `;
      },

      /**
       * 2. FEED / ANNOUNCEMENTS SKELETON
       * Matches featured article (16:9) + news feed list
       */
      feed(count = 3) {
        return `
          <div class="ngis-skeleton-screen ngis-skeleton-feed" aria-busy="true" aria-label="Loading feed...">
            <!-- Featured hero card -->
            <div class="ngis-skel-card ngis-skel-pulse" style="background:#FFFFFF; border:1px solid #E5E5E8; border-radius:14px; overflow:hidden; margin-bottom:24px;">
              <div style="width:100%; height:220px; background:#ECECED;"></div>
              <div style="padding:20px;">
                <div style="display:flex; gap:10px; margin-bottom:12px;">
                  <div class="ngis-skel-line" style="width:70px; height:18px; border-radius:4px; background:#DFDFE2;"></div>
                  <div class="ngis-skel-line" style="width:90px; height:18px; background:#ECECED;"></div>
                </div>
                <div class="ngis-skel-line" style="width:85%; height:20px; margin-bottom:10px; background:#DFDFE2;"></div>
                <div class="ngis-skel-line" style="width:60%; height:14px; background:#ECECED;"></div>
              </div>
            </div>

            <!-- Feed list items -->
            <div style="display:flex; flex-direction:column; gap:16px;">
              ${Array(count).fill(0).map(() => `
                <div class="ngis-skel-card ngis-skel-pulse" style="background:#FFFFFF; border:1px solid #E5E5E8; border-radius:12px; padding:16px; display:flex; gap:16px; align-items:center;">
                  <div style="width:80px; height:80px; border-radius:10px; background:#ECECED; flex-shrink:0;"></div>
                  <div style="flex:1;">
                    <div class="ngis-skel-line" style="width:60px; height:10px; margin-bottom:8px; background:#ECECED;"></div>
                    <div class="ngis-skel-line" style="width:80%; height:14px; margin-bottom:6px; background:#DFDFE2;"></div>
                    <div class="ngis-skel-line" style="width:50%; height:11px; background:#ECECED;"></div>
                  </div>
                </div>
              `).join("")}
            </div>
          </div>
        `;
      },

      /**
       * 3. LIST / TABLE SKELETON
       * Matches Roster, User Directory, Class list, or Services table
       */
      list(count = 6) {
        return `
          <div class="ngis-skeleton-screen ngis-skeleton-list" aria-busy="true" aria-label="Loading list...">
            <div class="ngis-skel-card ngis-skel-pulse" style="background:#FFFFFF; border:1px solid #E5E5E8; border-radius:12px; overflow:hidden;">
              <!-- Table Header -->
              <div style="background:#F8F8FA; border-bottom:1px solid #E5E5E8; padding:14px 20px; display:flex; align-items:center; gap:16px;">
                <div class="ngis-skel-line" style="width:24px; height:12px; background:#DFDFE2;"></div>
                <div class="ngis-skel-line" style="width:160px; height:12px; background:#DFDFE2;"></div>
                <div class="ngis-skel-line" style="width:120px; height:12px; background:#DFDFE2;"></div>
                <div class="ngis-skel-line" style="width:100px; height:12px; background:#DFDFE2;"></div>
                <div class="ngis-skel-line" style="width:80px; height:12px; margin-left:auto; background:#DFDFE2;"></div>
              </div>

              <!-- Table Rows -->
              <div>
                ${Array(count).fill(0).map((_, i) => `
                  <div style="display:flex; align-items:center; gap:16px; padding:16px 20px; border-bottom:1px solid #F3F3F5;">
                    <div class="ngis-skel-line" style="width:20px; height:12px; background:#ECECED;"></div>
                    <div class="ngis-skel-circle" style="width:36px; height:36px; border-radius:50%; background:#ECECED; flex-shrink:0;"></div>
                    <div style="flex:1;">
                      <div class="ngis-skel-line" style="width:${45 + (i % 4) * 10}%; height:14px; margin-bottom:5px; background:#DFDFE2;"></div>
                      <div class="ngis-skel-line" style="width:30%; height:11px; background:#ECECED;"></div>
                    </div>
                    <div class="ngis-skel-line" style="width:90px; height:12px; background:#ECECED;"></div>
                    <div class="ngis-skel-line" style="width:70px; height:22px; border-radius:6px; background:#ECECED;"></div>
                    <div class="ngis-skel-line" style="width:50px; height:28px; border-radius:8px; background:#ECECED;"></div>
                  </div>
                `).join("")}
              </div>
            </div>
          </div>
        `;
      },

      /**
       * 4. DETAIL / DOCUMENT SKELETON
       * Matches Department details, Assignment dossiers, Transcript reports
       */
      detail() {
        return `
          <div class="ngis-skeleton-screen ngis-skeleton-detail" aria-busy="true" aria-label="Loading details...">
            <div class="ngis-skel-card ngis-skel-pulse" style="background:#FFFFFF; border:1px solid #E5E5E8; border-radius:14px; padding:28px;">
              <!-- Breadcrumb & Tag line -->
              <div style="display:flex; gap:12px; align-items:center; margin-bottom:16px;">
                <div class="ngis-skel-line" style="width:110px; height:12px; background:#ECECED;"></div>
                <div class="ngis-skel-line" style="width:60px; height:20px; border-radius:6px; background:#DFDFE2;"></div>
              </div>

              <!-- Main Title -->
              <div class="ngis-skel-line" style="width:70%; height:26px; margin-bottom:14px; background:#DFDFE2;"></div>
              <div class="ngis-skel-line" style="width:40%; height:14px; margin-bottom:28px; background:#ECECED;"></div>

              <div style="height:1px; background:#E5E5E8; margin-bottom:24px;"></div>

              <!-- Content Paragraphs -->
              <div style="display:flex; flex-direction:column; gap:10px; margin-bottom:28px;">
                <div class="ngis-skel-line" style="width:100%; height:14px; background:#ECECED;"></div>
                <div class="ngis-skel-line" style="width:96%; height:14px; background:#ECECED;"></div>
                <div class="ngis-skel-line" style="width:88%; height:14px; background:#ECECED;"></div>
                <div class="ngis-skel-line" style="width:65%; height:14px; background:#ECECED;"></div>
              </div>

              <!-- Sub-blocks grid -->
              <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:16px; margin-top:24px;">
                ${Array(3).fill(0).map(() => `
                  <div style="border:1px solid #E5E5E8; border-radius:10px; padding:16px;">
                    <div class="ngis-skel-line" style="width:80px; height:12px; margin-bottom:8px; background:#DFDFE2;"></div>
                    <div class="ngis-skel-line" style="width:120px; height:18px; background:#ECECED;"></div>
                  </div>
                `).join("")}
              </div>
            </div>
          </div>
        `;
      },

      /**
       * 5. PROFILE SKELETON
       * Matches User Profile, Student Profile, Teacher Profile
       */
      profile() {
        return `
          <div class="ngis-skeleton-screen ngis-skeleton-profile" aria-busy="true" aria-label="Loading profile...">
            <!-- Profile header card -->
            <div class="ngis-skel-card ngis-skel-pulse" style="background:#FFFFFF; border:1px solid #E5E5E8; border-radius:14px; padding:28px; margin-bottom:20px; display:flex; align-items:center; gap:20px;">
              <div class="ngis-skel-circle" style="width:80px; height:80px; border-radius:50%; background:#ECECED; flex-shrink:0;"></div>
              <div style="flex:1;">
                <div class="ngis-skel-line" style="width:200px; height:22px; margin-bottom:8px; background:#DFDFE2;"></div>
                <div class="ngis-skel-line" style="width:140px; height:14px; margin-bottom:12px; background:#ECECED;"></div>
                <div style="display:flex; gap:8px;">
                  <div class="ngis-skel-line" style="width:75px; height:22px; border-radius:6px; background:#ECECED;"></div>
                  <div class="ngis-skel-line" style="width:90px; height:22px; border-radius:6px; background:#ECECED;"></div>
                </div>
              </div>
            </div>

            <!-- Profile form blocks -->
            <div class="ngis-skel-card ngis-skel-pulse" style="background:#FFFFFF; border:1px solid #E5E5E8; border-radius:14px; padding:24px;">
              <!-- Tabs bar -->
              <div style="display:flex; gap:16px; border-bottom:1px solid #E5E5E8; padding-bottom:12px; margin-bottom:24px;">
                <div class="ngis-skel-line" style="width:80px; height:16px; background:#DFDFE2;"></div>
                <div class="ngis-skel-line" style="width:90px; height:16px; background:#ECECED;"></div>
                <div class="ngis-skel-line" style="width:70px; height:16px; background:#ECECED;"></div>
              </div>

              <!-- 2-column fields -->
              <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
                ${Array(4).fill(0).map(() => `
                  <div>
                    <div class="ngis-skel-line" style="width:90px; height:12px; margin-bottom:8px; background:#DFDFE2;"></div>
                    <div class="ngis-skel-line" style="width:100%; height:44px; border-radius:10px; background:#ECECED; border:1px solid #E5E5E8;"></div>
                  </div>
                `).join("")}
              </div>
            </div>
          </div>
        `;
      }
    },

    /**
     * Render a skeleton into a container element or selector
     */
    render(container, layout = "list", count = 5) {
      if (typeof container === "string") container = document.querySelector(container);
      if (!container) return;

      const templateFn = this.templates[layout] || this.templates.list;
      container.setAttribute("aria-busy", "true");
      container.innerHTML = templateFn(count);
    },

    /**
     * Remove skeleton and restore normal aria state
     */
    clear(container, contentHtml = "") {
      if (typeof container === "string") container = document.querySelector(container);
      if (!container) return;

      container.removeAttribute("aria-busy");
      if (contentHtml) {
        container.innerHTML = contentHtml;
      }
    }
  };

  // Custom Web Component: <ngis-skeleton layout="dashboard|feed|list|detail|profile" count="5">
  if (typeof customElements !== "undefined" && !customElements.get("ngis-skeleton")) {
    customElements.define("ngis-skeleton", class extends HTMLElement {
      connectedCallback() {
        const layout = this.getAttribute("layout") || "list";
        const count = parseInt(this.getAttribute("count") || "5", 10);
        NGISSkeleton.render(this, layout, count);
      }
    });
  }

  window.NGISSkeleton = NGISSkeleton;
})(window, document);

