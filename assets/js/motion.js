/**
 * ============================================================================
 * NGIS-SYSTEM — GLOBAL MOTION DESIGN, ANIMATION & MICRO-INTERACTION ENGINE
 * Enterprise School Management System · 2026
 *
 * Integrates official GSAP (Core, Flip, Draggable, Inertia, CustomEase, ScrollTo)
 * with GPU-accelerated CSS fallbacks.
 *
 * Core Features:
 *  1. Physical press feedback (scale: 0.97 with spring recovery)
 *  2. Subtle card hover lift (-2.5px, scale: 1.007, soft elevation shadow)
 *  3. Scale-from-0.97 entrances (modals, dropdowns, popovers, context menus)
 *  4. Directional slide animations (sidebars, mobile drawers, bottom sheets)
 *  5. Smooth automatic height transitions for collapsible groups
 *  6. Horizontal error shake (3-5px over 300ms) with message pairing
 *  7. Intelligent tooltip delays (350ms first, 0ms warm group, 100ms exit)
 *  8. Velocity-based springs and subtle rubber-banding
 *  9. Animated success feedback (crisp vector checkmark draw)
 * 10. Strict accessibility & prefers-reduced-motion compliance
 * ============================================================================
 */

(function (window, document) {
  "use strict";

  // Prevent duplicate initialization
  if (window.NGIS_MOTION && window.NGIS_MOTION._initialized) return;

  /* ── 1. MOTION DESIGN TOKENS (Mirrored from CSS Custom Properties) ── */
  var TOKENS = {
    duration: {
      press: 0.1,        // 100ms
      hover: 0.18,       // 180ms
      tooltip: 0.12,     // 120ms
      dropdown: 0.18,    // 180ms
      modalEnter: 0.24,  // 240ms
      modalExit: 0.18,   // 180ms
      sidebar: 0.26,     // 260ms
      height: 0.24,      // 240ms
      shake: 0.3,        // 300ms
      success: 0.4       // 400ms
    },
    scale: {
      press: 0.97,
      entrance: 0.97,
      cardLift: 1.007
    },
    liftY: -2.5,
    ease: {
      out: "power2.out",
      in: "power2.in",
      spring: "back.out(1.4)",
      sharp: "power3.out"
    }
  };

  /* ── 2. ACCESSIBILITY CHECK (Prefers-Reduced-Motion) ── */
  function prefersReducedMotion() {
    try {
      return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    } catch (e) {
      return false;
    }
  }

  /* ── 3. DYNAMIC GSAP LOADER & VENDOR REGISTRATION ── */
  var gsapReady = false;
  var gsapQueue = [];
  var gsapLoadStarted = false;

  function onGSAPReady(fn) {
    if (gsapReady && window.gsap) {
      fn(window.gsap);
    } else {
      gsapQueue.push(fn);
      ensureGSAP();
    }
  }

  /* Lazy GSAP: nothing on any page registers GSAP callbacks up-front, and
     every consumer of window.gsap is feature-guarded with a CSS fallback,
     so the 172KB core + 6 plugins are only fetched when something actually
     asks for them. Previously this fired eagerly on every page load. */
  function ensureGSAP() {
    if (gsapReady || gsapLoadStarted) return;
    gsapLoadStarted = true;
    initGSAP();
  }

  function flushGSAPQueue() {
    gsapReady = true;
    while (gsapQueue.length) {
      var fn = gsapQueue.shift();
      try { fn(window.gsap); } catch (err) { console.warn("[NGIS Motion] Queue error:", err); }
    }
  }

  function resolveScriptPath(relPath) {
    // Determine relative depth to assets/
    var scripts = document.querySelectorAll("script[src]");
    var prefix = "";
    for (var i = 0; i < scripts.length; i++) {
      var src = scripts[i].getAttribute("src") || "";
      if (src.indexOf("assets/") !== -1) {
        prefix = src.substring(0, src.indexOf("assets/"));
        break;
      }
    }
    return prefix + relPath;
  }

  function loadVendorScript(src, cb) {
    var s = document.createElement("script");
    s.src = resolveScriptPath(src);
    s.async = false;
    s.onload = function () { cb(null); };
    s.onerror = function (e) { cb(e); };
    document.head.appendChild(s);
  }

  function initGSAP() {
    if (window.gsap) {
      registerPlugins();
      flushGSAPQueue();
      return;
    }

    // Load GSAP Core
    loadVendorScript("assets/vendor/gsap/gsap.min.js", function (err) {
      if (err) {
        console.warn("[NGIS Motion] Local GSAP vendor failed to load; using native CSS transitions fallback.");
        return;
      }

      // Load plugins sequentially or in parallel
      var plugins = [
        "assets/vendor/gsap/Flip.min.js",
        "assets/vendor/gsap/CustomEase.min.js",
        "assets/vendor/gsap/ScrollToPlugin.min.js",
        "assets/vendor/gsap/Draggable.min.js",
        "assets/vendor/gsap/InertiaPlugin.min.js",
        "assets/vendor/gsap/Observer.min.js"
      ];

      var loaded = 0;
      plugins.forEach(function (path) {
        loadVendorScript(path, function () {
          loaded++;
          if (loaded === plugins.length) {
            registerPlugins();
            flushGSAPQueue();
          }
        });
      });
    });
  }

  function registerPlugins() {
    if (!window.gsap) return;
    try {
      var pluginsToRegister = [];
      if (window.Flip) pluginsToRegister.push(window.Flip);
      if (window.CustomEase) pluginsToRegister.push(window.CustomEase);
      if (window.ScrollToPlugin) pluginsToRegister.push(window.ScrollToPlugin);
      if (window.Draggable) pluginsToRegister.push(window.Draggable);
      if (window.InertiaPlugin) pluginsToRegister.push(window.InertiaPlugin);
      if (window.Observer) pluginsToRegister.push(window.Observer);

      if (pluginsToRegister.length) {
        window.gsap.registerPlugin.apply(window.gsap, pluginsToRegister);
      }

      // Create Custom Eases matching Apple / Linear motion standards
      if (window.CustomEase) {
        window.CustomEase.create("ngisDecel", "M0,0 C0.16,1 0.3,1 1,1");
        window.CustomEase.create("ngisSpring", "M0,0 C0.34,1.4 0.64,1 1,1");
        window.CustomEase.create("ngisAccel", "M0,0 C0.4,0 1,1 1,1");
        TOKENS.ease.out = "ngisDecel";
        TOKENS.ease.spring = "ngisSpring";
        TOKENS.ease.in = "ngisAccel";
      }
    } catch (e) {
      console.warn("[NGIS Motion] Plugin registration note:", e);
    }
  }

  /* ── 4. PHYSICAL BUTTON / CONTROL PRESS FEEDBACK ── */
  function pressFeedback(el) {
    if (!el || prefersReducedMotion()) return;
    if (el.disabled || el.getAttribute("aria-disabled") === "true") return;

    if (window.gsap) {
      window.gsap.to(el, {
        scale: TOKENS.scale.press,
        duration: TOKENS.duration.press,
        ease: "power1.out",
        overwrite: "auto"
      });
    } else {
      el.style.transform = "scale(" + TOKENS.scale.press + ")";
      el.style.transition = "transform " + (TOKENS.duration.press * 1000) + "ms cubic-bezier(0.16, 1, 0.3, 1)";
    }
  }

  function releaseFeedback(el) {
    if (!el || prefersReducedMotion()) return;

    var isCard = el.matches && (el.matches(".hub-card, .portal-card, .dept-card, .module-card, .lesson-card, .card-hover, .interactive-card, [class*='card']") || el._isHovered);
    var targetScale = (isCard && el._isHovered) ? TOKENS.scale.cardLift : 1.0;
    var targetY = (isCard && el._isHovered) ? TOKENS.liftY : 0;

    if (window.gsap) {
      window.gsap.to(el, {
        scale: targetScale,
        y: targetY,
        duration: 0.16,
        ease: TOKENS.ease.spring,
        overwrite: "auto",
        clearProps: (isCard && el._isHovered) ? "" : "transform"
      });
    } else {
      el.style.transform = (isCard && el._isHovered) ? "translateY(" + TOKENS.liftY + "px) scale(" + TOKENS.scale.cardLift + ")" : "scale(1)";
      setTimeout(function () {
        if (el && el.style && (!isCard || !el._isHovered)) el.style.transform = "";
      }, 180);
    }
  }

  /* ── 5. SUBTLE CARD HOVER LIFT ── */
  function cardHoverEnter(card) {
    if (!card || prefersReducedMotion()) return;
    // Strictly disable on touch-only devices
    if (window.matchMedia && !window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;

    if (window.gsap) {
      window.gsap.to(card, {
        y: TOKENS.liftY,
        scale: TOKENS.scale.cardLift,
        duration: TOKENS.duration.hover,
        ease: TOKENS.ease.out,
        boxShadow: "0 8px 24px -4px rgba(15, 23, 20, 0.08), 0 2px 6px -2px rgba(15, 23, 20, 0.04)",
        overwrite: "auto"
      });
    } else {
      card.classList.add("ngis-card-lifted");
    }
  }

  function cardHoverLeave(card) {
    if (!card || prefersReducedMotion()) return;

    if (window.gsap) {
      window.gsap.to(card, {
        y: 0,
        scale: 1.0,
        duration: TOKENS.duration.hover,
        ease: TOKENS.ease.out,
        boxShadow: "",
        clearProps: "y,scale,boxShadow",
        overwrite: "auto"
      });
    } else {
      card.classList.remove("ngis-card-lifted");
    }
  }

  /* ── 6. ERROR SHAKE ANIMATION ── */
  function errorShake(el, options) {
    if (!el) return;
    options = options || {};
    var distance = options.distance || 4; // 3-5px
    var duration = options.duration || TOKENS.duration.shake;

    // Accessibility: Reduced motion replaces shake with subtle highlight pulse
    if (prefersReducedMotion()) {
      el.classList.add("ngis-error-static");
      setTimeout(function () { el.classList.remove("ngis-error-static"); }, 400);
      return;
    }

    if (window.gsap) {
      var tl = window.gsap.timeline({
        onComplete: function () {
          window.gsap.set(el, { clearProps: "x" });
          if (options.onComplete) options.onComplete();
        }
      });
      tl.to(el, { x: -distance, duration: duration * 0.2, ease: "power1.out" })
        .to(el, { x: distance, duration: duration * 0.2, ease: "power1.inOut" })
        .to(el, { x: -distance * 0.7, duration: duration * 0.2, ease: "power1.inOut" })
        .to(el, { x: distance * 0.7, duration: duration * 0.2, ease: "power1.inOut" })
        .to(el, { x: 0, duration: duration * 0.2, ease: "power1.in" });
    } else {
      el.classList.add("ngis-shake");
      setTimeout(function () {
        el.classList.remove("ngis-shake");
        if (options.onComplete) options.onComplete();
      }, 320);
    }
  }

  /* ── 7. SCALE FROM 0.97 ENTRANCE (Modals, Dropdowns, Popovers) ── */
  function scaleEntrance(el, options) {
    if (!el) return;
    options = options || {};
    var startScale = options.scale || TOKENS.scale.entrance;
    var duration = options.duration || TOKENS.duration.dropdown;
    var startY = options.y !== undefined ? options.y : 6;

    if (prefersReducedMotion()) {
      el.style.opacity = "1";
      el.style.transform = "none";
      if (options.onComplete) options.onComplete();
      return;
    }

    if (window.gsap) {
      window.gsap.fromTo(el,
        { scale: startScale, y: startY, opacity: 0 },
        {
          scale: 1.0,
          y: 0,
          opacity: 1,
          duration: duration,
          ease: TOKENS.ease.out,
          overwrite: "auto",
          clearProps: options.clearProps !== false ? "transform" : "",
          onComplete: options.onComplete
        }
      );
    } else {
      el.style.opacity = "0";
      el.style.transform = "scale(" + startScale + ") translateY(" + startY + "px)";
      void el.offsetWidth;
      el.style.transition = "opacity " + (duration * 1000) + "ms cubic-bezier(0.16, 1, 0.3, 1), transform " + (duration * 1000) + "ms cubic-bezier(0.16, 1, 0.3, 1)";
      el.style.opacity = "1";
      el.style.transform = "scale(1) translateY(0)";
      if (options.onComplete) setTimeout(options.onComplete, duration * 1000);
    }
  }

  function scaleExit(el, options) {
    if (!el) return;
    options = options || {};
    var endScale = options.scale || TOKENS.scale.entrance;
    var duration = options.duration || TOKENS.duration.modalExit;
    var endY = options.y !== undefined ? options.y : 6;

    if (prefersReducedMotion()) {
      el.style.opacity = "0";
      if (options.onComplete) options.onComplete();
      return;
    }

    if (window.gsap) {
      window.gsap.to(el, {
        scale: endScale,
        y: endY,
        opacity: 0,
        duration: duration,
        ease: TOKENS.ease.in,
        overwrite: "auto",
        onComplete: options.onComplete
      });
    } else {
      el.style.transition = "opacity " + (duration * 1000) + "ms cubic-bezier(0.4, 0, 1, 1), transform " + (duration * 1000) + "ms cubic-bezier(0.4, 0, 1, 1)";
      el.style.opacity = "0";
      el.style.transform = "scale(" + endScale + ") translateY(" + endY + "px)";
      if (options.onComplete) setTimeout(options.onComplete, duration * 1000);
    }
  }

  /* ── 8. MODAL COORDINATED TIMELINE (Backdrop + Box) ── */
  function modalEnter(backdropEl, boxEl, onComplete) {
    if (!backdropEl) return;
    boxEl = boxEl || backdropEl.querySelector(".smx-modal, .rp-modal, .ngis-modal, .ngis-modal-box, .modal-box, [role='dialog']");

    if (prefersReducedMotion()) {
      backdropEl.style.opacity = "1";
      if (boxEl) {
        boxEl.style.opacity = "1";
        boxEl.style.transform = "none";
      }
      if (onComplete) onComplete();
      return;
    }

    if (window.gsap) {
      var tl = window.gsap.timeline({ onComplete: onComplete });
      tl.fromTo(backdropEl,
        { opacity: 0, backdropFilter: "blur(0px)" },
        { opacity: 1, backdropFilter: "blur(6px)", duration: TOKENS.duration.modalEnter, ease: "power1.out" },
        0
      );
      if (boxEl) {
        tl.fromTo(boxEl,
          { scale: TOKENS.scale.entrance, y: 12, opacity: 0 },
          { scale: 1.0, y: 0, opacity: 1, duration: TOKENS.duration.modalEnter, ease: TOKENS.ease.out },
          0.02
        );
      }
    } else {
      scaleEntrance(boxEl, { duration: TOKENS.duration.modalEnter, onComplete: onComplete });
    }
  }

  function modalExit(backdropEl, boxEl, onComplete) {
    if (!backdropEl) return;
    boxEl = boxEl || backdropEl.querySelector(".smx-modal, .rp-modal, .ngis-modal, .ngis-modal-box, .modal-box, [role='dialog']");

    if (prefersReducedMotion()) {
      backdropEl.style.opacity = "0";
      if (onComplete) onComplete();
      return;
    }

    if (window.gsap) {
      var tl = window.gsap.timeline({ onComplete: onComplete });
      if (boxEl) {
        tl.to(boxEl, { scale: TOKENS.scale.entrance, y: 8, opacity: 0, duration: TOKENS.duration.modalExit, ease: TOKENS.ease.in }, 0);
      }
      tl.to(backdropEl, { opacity: 0, backdropFilter: "blur(0px)", duration: TOKENS.duration.modalExit, ease: "power1.in" }, 0.02);
    } else {
      scaleExit(boxEl, { duration: TOKENS.duration.modalExit, onComplete: onComplete });
    }
  }

  /* ── 9. SMOOTH AUTOMATIC HEIGHT (Collapsible Groups / Accordions) ── */
  function expandHeight(el, isOpening, onComplete) {
    if (!el) return;
    if (prefersReducedMotion()) {
      el.style.height = isOpening ? "auto" : "0px";
      el.style.overflow = isOpening ? "visible" : "hidden";
      if (onComplete) onComplete();
      return;
    }

    if (isOpening) {
      el.style.display = "block";
      el.style.height = "auto";
      var targetH = el.scrollHeight;
      el.style.height = "0px";
      el.style.overflow = "hidden";

      if (window.gsap) {
        window.gsap.to(el, {
          height: targetH,
          duration: TOKENS.duration.height,
          ease: TOKENS.ease.out,
          overwrite: "auto",
          onComplete: function () {
            el.style.height = "auto";
            el.style.overflow = "";
            if (onComplete) onComplete();
          }
        });
      } else {
        void el.offsetWidth;
        el.style.transition = "height " + (TOKENS.duration.height * 1000) + "ms cubic-bezier(0.16, 1, 0.3, 1)";
        el.style.height = targetH + "px";
        setTimeout(function () {
          el.style.height = "auto";
          el.style.overflow = "";
          if (onComplete) onComplete();
        }, TOKENS.duration.height * 1000);
      }
    } else {
      var currentH = el.offsetHeight;
      el.style.height = currentH + "px";
      el.style.overflow = "hidden";

      if (window.gsap) {
        window.gsap.to(el, {
          height: 0,
          duration: TOKENS.duration.height * 0.85,
          ease: TOKENS.ease.in,
          overwrite: "auto",
          onComplete: function () {
            el.style.display = "none";
            if (onComplete) onComplete();
          }
        });
      } else {
        void el.offsetWidth;
        el.style.transition = "height " + (TOKENS.duration.height * 850) + "ms cubic-bezier(0.4, 0, 1, 1)";
        el.style.height = "0px";
        setTimeout(function () {
          el.style.display = "none";
          if (onComplete) onComplete();
        }, TOKENS.duration.height * 850);
      }
    }
  }

  /* ── 10. TOOLTIP DECOMMISSIONED (Zero Hover Popups) ── */
  function showTooltip() {}
  function hideTooltip() {}

  /* ── 11. ANIMATED SUCCESS CONFIRMATION ── */
  function showSuccessFeedback(container, message, onComplete) {
    if (!container) container = document.body;
    var el = document.createElement("div");
    el.className = "ngis-success-toast";
    el.innerHTML =
      '<div class="ngis-success-pill">' +
        '<svg class="ngis-success-checkmark" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">' +
          '<path class="ngis-check-path" d="M20 6L9 17L4 12"></path>' +
        '</svg>' +
        '<span class="ngis-success-text">' + (message || "Operation Completed Successfully") + '</span>' +
      '</div>';
    document.body.appendChild(el);

    scaleEntrance(el, { duration: 0.25, y: 8, scale: 0.96 });

    // Animate checkmark draw
    var path = el.querySelector(".ngis-check-path");
    if (path) {
      var len = path.getTotalLength ? path.getTotalLength() : 30;
      path.style.strokeDasharray = len;
      path.style.strokeDashoffset = len;
      path.getBoundingClientRect(); // reflow
      path.style.transition = "stroke-dashoffset 280ms cubic-bezier(0.16, 1, 0.3, 1) 120ms";
      path.style.strokeDashoffset = "0";
    }

    setTimeout(function () {
      scaleExit(el, {
        duration: 0.2,
        y: -4,
        onComplete: function () {
          if (el.parentNode) el.parentNode.removeChild(el);
          if (onComplete) onComplete();
        }
      });
    }, 2400);
  }

  /* ── 12. GLOBAL EVENT DELEGATION & REUSABLE BINDINGS ── */
  function initGlobalDelegates() {
    // A. Physical Press Feedback on interactive controls & cards
    var pressSelector = [
      "button:not([disabled])",
      ".btn",
      ".icon-btn",
      ".tab-btn",
      ".exw-tab",
      ".exw-roadmap-tab",
      ".card-clickable",
      ".hub-card",
      ".portal-card",
      ".dept-card",
      ".module-card",
      ".lesson-card",
      ".interactive-card",
      ".card-hover",
      ".exw-roadmap-row",
      "a[class*='card']:not(.stat-card):not(.telemetry-card)",
      ".nav-link",
      ".hamburger-btn",
      ".mobile-hamburger-btn",
      ".htb-ctrl-btn",
      ".action-btn",
      "[data-action]",
      ".pill-btn"
    ].join(", ");

    document.addEventListener("pointerdown", function (e) {
      var target = e.target.closest(pressSelector);
      if (!target || target.disabled || target.getAttribute("aria-disabled") === "true") return;
      pressFeedback(target);

      var onUp = function () {
        releaseFeedback(target);
        window.removeEventListener("pointerup", onUp);
        window.removeEventListener("pointercancel", onUp);
      };
      window.addEventListener("pointerup", onUp);
      window.addEventListener("pointercancel", onUp);
    }, { passive: true });

    // B. Subtle Card Lift on interactive cards
    var cardSelector = [
      ".card-hover",
      ".hub-card",
      ".portal-card",
      ".dept-card",
      ".module-card",
      ".lesson-card",
      ".ql-card",
      ".task-card",
      ".ann-card",
      ".exam-card",
      ".interactive-card",
      ".sh-card",
      ".exw-timeline-card",
      ".exw-roadmap-row",
      "a[class*='card']:not(.stat-card):not(.telemetry-card)"
    ].join(", ");

    document.addEventListener("mouseover", function (e) {
      var card = e.target.closest(cardSelector);
      if (card && !card._isHovered) {
        card._isHovered = true;
        cardHoverEnter(card);
      }
    }, { passive: true });

    document.addEventListener("mouseout", function (e) {
      var card = e.target.closest(cardSelector);
      if (card && card._isHovered) {
        var related = e.relatedTarget;
        if (!related || !card.contains(related)) {
          card._isHovered = false;
          cardHoverLeave(card);
        }
      }
    }, { passive: true });


    // D. Dropdown / Menu 0.97 Entrance detection
    document.addEventListener("click", function (e) {
      var toggle = e.target.closest("[data-toggle='dropdown'], [data-dropdown-toggle], .dropdown-trigger, .hpd-ctrl-btn");
      if (toggle) {
        var menu = toggle.nextElementSibling || document.querySelector(toggle.getAttribute("data-target"));
        if (menu && menu.classList.contains("open")) {
          scaleEntrance(menu, { duration: TOKENS.duration.dropdown, y: -4 });
        }
      }
    }, { passive: true });
  }

  /* ── 13. PUBLIC API EXPOSURE ── */
  var NGIS_MOTION = {
    _initialized: true,
    tokens: TOKENS,
    prefersReducedMotion: prefersReducedMotion,
    onReady: onGSAPReady,
    press: pressFeedback,
    release: releaseFeedback,
    cardLiftEnter: cardHoverEnter,
    cardLiftLeave: cardHoverLeave,
    shake: errorShake,
    scaleEntrance: scaleEntrance,
    scaleExit: scaleExit,
    modalEnter: modalEnter,
    modalExit: modalExit,
    expandHeight: expandHeight,
    showTooltip: showTooltip,
    hideTooltip: hideTooltip,
    success: showSuccessFeedback
  };

  // Expose globally
  window.NGIS_MOTION = NGIS_MOTION;
  if (!window.NGIS) window.NGIS = {};
  window.NGIS.motion = NGIS_MOTION;

  // Initialize global delegations when DOM is ready.
  // GSAP is lazy: see ensureGSAP() — it loads only when onGSAPReady()
  // is called by a real consumer (nothing does today).
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      initGlobalDelegates();
    });
  } else {
    initGlobalDelegates();
  }

})(window, document);
