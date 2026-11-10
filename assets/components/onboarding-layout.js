/**
 * ============================================================
 * NGIS ERP — Reusable OnboardingLayout Component (Rule 4 Compliant)
 * Rule 4: Primary buttons stay in one fixed place during onboarding.
 * - Continue/Next button sits in the exact same fixed position on
 *   every screen (bottom, pinned above safe area & keyboard).
 * - Same size, same label style, same color across every step.
 * - Secondary actions (Back, Skip) maintain fixed positions.
 * - Scrollable middle body container so button NEVER shifts with content height.
 * - Progress indicator does not shift the layout.
 * ============================================================
 */

(function (window, document) {
  "use strict";

  const NGISOnboarding = {
    /**
     * Mount an onboarding wizard container
     */
    init(container, options = {}) {
      if (typeof container === "string") container = document.querySelector(container);
      if (!container) return;

      const {
        steps = [],
        onComplete = null,
        onSkip = null,
        initialStep = 0
      } = options;

      let currentStepIndex = initialStep;

      const render = () => {
        const step = steps[currentStepIndex] || {};
        const isFirst = currentStepIndex === 0;
        const isLast = currentStepIndex === steps.length - 1;
        const total = steps.length;
        const progressPct = Math.round(((currentStepIndex + 1) / total) * 100);

        container.className = "ngis-onboarding-shell";
        container.innerHTML = `
          <!-- Fixed Top Header & Progress Bar -->
          <header class="ngis-onboarding-header" style="height:64px; border-bottom:1px solid #E5E5E8; background:#FFFFFF; display:flex; align-items:center; justify-content:space-between; padding:0 24px; position:sticky; top:0; z-index:20;">
            <div style="display:flex; align-items:center; gap:10px;">
              <div style="width:32px; height:32px; border-radius:8px; background:#202F63; display:grid; place-items:center; color:#FFFFFF; font-size:12px; font-weight:500;">
                NGIS
              </div>
              <span style="font-size:13.5px; font-weight:500; color:#000000;">Campus Onboarding</span>
            </div>
            <div style="display:flex; align-items:center; gap:12px;">
              <span style="font-size:12px; color:#555555; font-weight:500;">Step ${currentStepIndex + 1} of ${total}</span>
              <div style="width:90px; height:6px; background:#F3F3F5; border-radius:99px; overflow:hidden; border:1px solid #E5E5E8;">
                <div style="width:${progressPct}%; height:100%; background:#202F63; transition:width 0.25s ease;"></div>
              </div>
            </div>
          </header>

          <!-- Middle Scrollable Content Container (Button never shifts with height) -->
          <main class="ngis-onboarding-body" style="flex:1; overflow-y:auto; padding:32px 24px; max-width:680px; width:100%; margin:0 auto; box-sizing:border-box;">
            <div class="ngis-onboarding-step-content" style="animation:fadeIn 0.2s ease;">
              <div style="margin-bottom:24px;">
                <span style="font-size:11px; text-transform:uppercase; letter-spacing:0.08em; color:#555555; background:#F3F3F5; border:1px solid #E5E5E8; padding:3px 10px; border-radius:999px; font-weight:500;">
                  ${step.badge || "Step " + (currentStepIndex + 1)}
                </span>
                <h1 style="font-size:22px; font-weight:500; color:#000000; margin:12px 0 6px 0; line-height:1.25;">
                  ${step.title || "Onboarding Step"}
                </h1>
                <p style="font-size:14px; color:#555555; margin:0; line-height:1.5;">
                  ${step.description || ""}
                </p>
              </div>

              <div class="ngis-step-custom-slot" style="min-height:220px;">
                ${step.content || ""}
              </div>
            </div>
          </main>

          <!-- Fixed Pinned Bottom Footer (Absolute consistency across all steps) -->
          <footer class="ngis-onboarding-footer" style="position:sticky; bottom:0; background:#FFFFFF; border-top:1px solid #E5E5E8; padding:16px 24px; padding-bottom:max(16px, env(safe-area-inset-bottom)); z-index:20;">
            <div style="max-width:680px; margin:0 auto; display:flex; align-items:center; justify-content:space-between; gap:16px;">
              <div>
                ${!isFirst ? `
                  <button type="button" id="ngisObBackBtn" class="ngis-btn-secondary" style="min-height:44px; min-width:96px; padding:0 18px; border-radius:10px; font-size:13px; font-weight:500; border:1px solid #E5E5E8; background:#FFFFFF; color:#333333; cursor:pointer;">
                    Back
                  </button>
                ` : (onSkip ? `
                  <button type="button" id="ngisObSkipBtn" class="ngis-btn-ghost" style="min-height:44px; padding:0 16px; font-size:13px; color:#666666; background:transparent; border:none; cursor:pointer;">
                    Skip for now
                  </button>
                ` : "<div></div>")}
              </div>

              <div style="display:flex; align-items:center; gap:10px;">
                <button type="button" id="ngisObNextBtn" class="ngis-btn-primary" style="min-height:44px; min-width:140px; padding:0 24px; border-radius:10px; font-size:13px; font-weight:500; background:#202F63; border:1px solid #18234D; color:#FFFFFF; display:inline-flex; align-items:center; justify-content:center; gap:8px; cursor:pointer;">
                  <span>${isLast ? (step.completeText || "Complete Setup") : "Continue"}</span>
                  <i class="ph ${isLast ? 'ph-check' : 'ph-arrow-right'}"></i>
                </button>
              </div>
            </div>
          </footer>
        `;

        // Wire handlers
        const nextBtn = container.querySelector("#ngisObNextBtn");
        const backBtn = container.querySelector("#ngisObBackBtn");
        const skipBtn = container.querySelector("#ngisObSkipBtn");

        if (nextBtn) {
          nextBtn.addEventListener("click", async () => {
            if (typeof step.validate === "function") {
              const valid = await step.validate();
              if (!valid) return;
            }

            if (isLast) {
              if (typeof onComplete === "function") onComplete();
            } else {
              currentStepIndex++;
              render();
            }
          });
        }

        if (backBtn) {
          backBtn.addEventListener("click", () => {
            if (currentStepIndex > 0) {
              currentStepIndex--;
              render();
            }
          });
        }

        if (skipBtn && onSkip) {
          skipBtn.addEventListener("click", onSkip);
        }
      };

      render();
    }
  };

  // Custom Web Component: <ngis-onboarding></ngis-onboarding>
  if (typeof customElements !== "undefined" && !customElements.get("ngis-onboarding")) {
    customElements.define("ngis-onboarding", class extends HTMLElement {
      connectedCallback() {
        this.style.display = "flex";
        this.style.flexDirection = "column";
        this.style.minHeight = "100vh";
      }
    });
  }

  window.NGISOnboarding = NGISOnboarding;
})(window, document);

