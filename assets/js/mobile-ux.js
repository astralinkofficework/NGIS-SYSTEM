/**
 * ============================================================================
 * NGIS ERP — Master Mobile UX & Native Interaction Engine v1.0
 * New Gateway International School — Centralized Mobile UI/UX Engine
 *
 * Implements:
 * - Appropriate mobile keyboards (inputmode: email, tel, numeric, decimal, search)
 * - Email field sanitization (autocapitalize: none, spellcheck: false, autocorrect: off)
 * - OTP autofill & smart multi-box code pasting
 * - Contextual return keys (enterkeyhint: search, next, done, send, go)
 * - Keyboard navigation (Enter key automatically advances to next field)
 * - Scroll chaining lock on modal/drawer open
 * - Dynamic MutationObserver for AJAX/DOM-inserted forms & modals
 * ============================================================================
 */

(function (window, document) {
  "use strict";

  // Prevent double-initialization
  if (window.__NGIS_MOBILE_UX_INITIALIZED__) return;
  window.__NGIS_MOBILE_UX_INITIALIZED__ = true;

  /**
   * Determine the best inputmode, type, autocomplete and enterkeyhint for an input element
   */
  function enhanceInput(input) {
    if (!input || input.__ngis_mobile_enhanced__) return;
    input.__ngis_mobile_enhanced__ = true;

    var name = (input.name || "").toLowerCase();
    var id = (input.id || "").toLowerCase();
    var placeholder = (input.placeholder || "").toLowerCase();
    var type = (input.type || "text").toLowerCase();
    var cls = (input.className || "").toLowerCase();
    var form = input.form;

    // 1. Email Fields
    if (type === "email" || name.indexOf("email") !== -1 || id.indexOf("email") !== -1 || placeholder.indexOf("email") !== -1) {
      if (type !== "email") input.type = "email";
      if (!input.hasAttribute("autocomplete")) input.setAttribute("autocomplete", "email");
      input.setAttribute("autocapitalize", "none");
      input.setAttribute("autocorrect", "off");
      input.setAttribute("spellcheck", "false");
      if (!input.hasAttribute("inputmode")) input.setAttribute("inputmode", "email");
      if (!input.hasAttribute("enterkeyhint")) input.setAttribute("enterkeyhint", "next");
      return;
    }

    // 2. Phone / Tel Fields
    if (type === "tel" || name.indexOf("phone") !== -1 || id.indexOf("phone") !== -1 || name.indexOf("tel") !== -1 || id.indexOf("tel") !== -1 || placeholder.indexOf("phone") !== -1) {
      if (type !== "tel") input.type = "tel";
      if (!input.hasAttribute("inputmode")) input.setAttribute("inputmode", "tel");
      if (!input.hasAttribute("autocomplete")) input.setAttribute("autocomplete", "tel");
      if (!input.hasAttribute("enterkeyhint")) input.setAttribute("enterkeyhint", "next");
      return;
    }

    // 3. Search Fields
    if (type === "search" || name.indexOf("search") !== -1 || id.indexOf("search") !== -1 || cls.indexOf("search") !== -1 || placeholder.indexOf("search") !== -1 || placeholder.indexOf("filter") !== -1) {
      if (!input.hasAttribute("inputmode")) input.setAttribute("inputmode", "search");
      if (!input.hasAttribute("enterkeyhint")) input.setAttribute("enterkeyhint", "search");
      input.setAttribute("autocapitalize", "none");
      input.setAttribute("spellcheck", "false");
      return;
    }

    // 4. OTP / Verification Code Fields
    if (name.indexOf("otp") !== -1 || id.indexOf("otp") !== -1 || cls.indexOf("otp") !== -1 || name.indexOf("verify") !== -1 || placeholder.indexOf("verification code") !== -1 || (cls.indexOf("code-box") !== -1)) {
      if (!input.hasAttribute("inputmode")) input.setAttribute("inputmode", "numeric");
      if (!input.hasAttribute("autocomplete")) input.setAttribute("autocomplete", "one-time-code");
      if (!input.hasAttribute("pattern")) input.setAttribute("pattern", "[0-9]*");
      if (!input.hasAttribute("enterkeyhint")) input.setAttribute("enterkeyhint", "done");
      wireOtpBox(input);
      return;
    }

    // 5. Numeric / Digit-only Identifiers (Student ID, Room #, Bus #, Code)
    if (name.indexOf("student_id") !== -1 || id.indexOf("studentid") !== -1 || name.indexOf("national_id") !== -1 || name.indexOf("zip") !== -1 || (cls.indexOf("numeric-id") !== -1)) {
      // Keep type="text" to preserve leading zeros, but trigger numeric keypad!
      if (!input.hasAttribute("inputmode")) input.setAttribute("inputmode", "numeric");
      if (!input.hasAttribute("pattern")) input.setAttribute("pattern", "[0-9]*");
      if (!input.hasAttribute("enterkeyhint")) input.setAttribute("enterkeyhint", "next");
      return;
    }

    // 6. Decimal / Grade / Currency / Amount Fields
    if (name.indexOf("grade") !== -1 || id.indexOf("grade") !== -1 || name.indexOf("score") !== -1 || id.indexOf("score") !== -1 || name.indexOf("amount") !== -1 || id.indexOf("amount") !== -1 || name.indexOf("salary") !== -1 || name.indexOf("fee") !== -1 || cls.indexOf("grade-input") !== -1) {
      if (!input.hasAttribute("inputmode")) input.setAttribute("inputmode", "decimal");
      if (!input.hasAttribute("enterkeyhint")) input.setAttribute("enterkeyhint", "next");
      return;
    }

    // 7. Password Fields
    if (type === "password") {
      if (!input.hasAttribute("autocomplete")) {
        if (id.indexOf("new") !== -1 || name.indexOf("new") !== -1) {
          input.setAttribute("autocomplete", "new-password");
        } else {
          input.setAttribute("autocomplete", "current-password");
        }
      }
      if (!input.hasAttribute("enterkeyhint")) input.setAttribute("enterkeyhint", "done");
      return;
    }

    // 8. General intermediate vs final fields in a form
    if (form && !input.hasAttribute("enterkeyhint")) {
      var formInputs = Array.prototype.slice.call(form.querySelectorAll("input:not([type=hidden]):not([disabled]), select:not([disabled]), textarea:not([disabled])"));
      var idx = formInputs.indexOf(input);
      if (idx !== -1 && idx === formInputs.length - 1) {
        input.setAttribute("enterkeyhint", "done");
      } else {
        input.setAttribute("enterkeyhint", "next");
      }
    }
  }

  /**
   * Handle Enter Key navigation when enterkeyhint="next"
   */
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Enter" || e.shiftKey || e.altKey || e.ctrlKey || e.metaKey) return;
    var target = e.target;
    if (!target || target.tagName !== "INPUT" || target.type === "submit" || target.type === "button") return;

    var hint = target.getAttribute("enterkeyhint");
    if (hint === "next") {
      var form = target.form;
      if (form) {
        var focusables = Array.prototype.slice.call(
          form.querySelectorAll("input:not([type=hidden]):not([disabled]), select:not([disabled]), textarea:not([disabled])")
        ).filter(function (el) {
          return el.offsetParent !== null; // visible elements only
        });
        var currentIdx = focusables.indexOf(target);
        if (currentIdx !== -1 && currentIdx < focusables.length - 1) {
          e.preventDefault();
          focusables[currentIdx + 1].focus();
        }
      }
    } else if (hint === "search") {
      // If inside a form or table search, blur or trigger search event
      target.dispatchEvent(new Event("change", { bubbles: true }));
      target.dispatchEvent(new Event("input", { bubbles: true }));
    }
  });

  /**
   * Wire smart OTP / verification code multi-input pasting & auto-advancement
   */
  function wireOtpBox(input) {
    input.addEventListener("paste", function (e) {
      var pasteData = (e.clipboardData || window.clipboardData).getData("text").trim();
      if (!pasteData) return;
      var digits = pasteData.replace(/\D/g, "");
      if (digits.length >= 4) {
        e.preventDefault();
        var parent = input.parentElement;
        if (parent) {
          var siblingBoxes = Array.prototype.slice.call(parent.querySelectorAll("input"));
          if (siblingBoxes.length > 1) {
            siblingBoxes.forEach(function (box, idx) {
              if (idx < digits.length) {
                box.value = digits[idx];
                box.dispatchEvent(new Event("input", { bubbles: true }));
              }
            });
            var lastFilled = siblingBoxes[Math.min(digits.length - 1, siblingBoxes.length - 1)];
            if (lastFilled) lastFilled.focus();
            return;
          }
        }
        input.value = digits;
      }
    });

    input.addEventListener("input", function () {
      if (input.value.length === 1) {
        var next = input.nextElementSibling;
        while (next && next.tagName !== "INPUT") next = next.nextElementSibling;
        if (next) next.focus();
      }
    });

    input.addEventListener("keydown", function (e) {
      if (e.key === "Backspace" && !input.value) {
        var prev = input.previousElementSibling;
        while (prev && prev.tagName !== "INPUT") prev = prev.previousElementSibling;
        if (prev) {
          prev.focus();
          prev.value = "";
        }
      }
    });
  }

  /**
   * Modal & Drawer Background Scroll Lock
   */
  function lockBackgroundScroll(locked) {
    if (locked) {
      document.body.classList.add("modal-open");
      document.documentElement.classList.add("modal-open");
    } else {
      // Only unlock if no other active modals or drawers exist
      var openModals = document.querySelectorAll('.modal:not(.hidden):not([style*="display: none"]), [role="dialog"]:not(.hidden):not([style*="display: none"]), .mobile-drawer.open, body.sidebar-open');
      if (openModals.length <= 1) {
        document.body.classList.remove("modal-open");
        document.documentElement.classList.remove("modal-open");
      }
    }
  }

  // Hook into Bootstrap, Tailwind, or custom modal opens/closes
  document.addEventListener("click", function (e) {
    var trigger = e.target.closest('[data-modal-target], [data-action="open-modal"], [data-dismiss="modal"], [data-action="close-modal"], [data-action="toggle-sidebar"]');
    if (!trigger) return;

    var action = trigger.getAttribute("data-action") || "";
    if (action === "close-modal" || trigger.getAttribute("data-dismiss") === "modal") {
      setTimeout(function () { lockBackgroundScroll(false); }, 100);
    } else if (action === "open-modal" || trigger.getAttribute("data-modal-target")) {
      setTimeout(function () { lockBackgroundScroll(true); }, 50);
    } else if (action === "toggle-sidebar") {
      setTimeout(function () {
        var isExpanded = trigger.getAttribute("aria-expanded") === "true";
        if (isExpanded) {
          document.body.classList.add("sidebar-open");
        } else {
          document.body.classList.remove("sidebar-open");
        }
      }, 50);
    }
  });

  /**
   * Enhance all inputs currently on the page
   */
  function scanAndEnhance() {
    var inputs = document.querySelectorAll("input, select, textarea");
    for (var i = 0; i < inputs.length; i++) {
      enhanceInput(inputs[i]);
    }
  }

  // Initial scan on DOMContentLoaded and Load
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scanAndEnhance);
  } else {
    scanAndEnhance();
  }
  window.addEventListener("load", scanAndEnhance);

  // MutationObserver for dynamic DOM injections (AJAX modals, tab switches, dynamic tables)
  if (typeof MutationObserver !== "undefined") {
    var observer = new MutationObserver(function (mutations) {
      for (var i = 0; i < mutations.length; i++) {
        var added = mutations[i].addedNodes;
        for (var j = 0; j < added.length; j++) {
          var node = added[j];
          if (node.nodeType === 1) { // Element node
            if (node.tagName === "INPUT" || node.tagName === "SELECT" || node.tagName === "TEXTAREA") {
              enhanceInput(node);
            } else if (node.querySelectorAll) {
              var nested = node.querySelectorAll("input, select, textarea");
              for (var k = 0; k < nested.length; k++) {
                enhanceInput(nested[k]);
              }
            }
          }
        }
      }
    });

    observer.observe(document.documentElement, {
      childList: true,
      subtree: true
    });
  }

  // Export globally under window.NGIS_MOBILE_UX
  window.NGIS_MOBILE_UX = {
    enhance: scanAndEnhance,
    enhanceInput: enhanceInput,
    lockScroll: lockBackgroundScroll
  };

})(window, document);
