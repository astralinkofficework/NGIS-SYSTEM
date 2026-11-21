with open('assets/js/modal-system.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace in open:
old_open_anim = """      // Trigger smooth entrance animation
      backdropEl.classList.remove("ngis-modal-exit");
      backdropEl.classList.add("ngis-modal-enter");

      // Force layout reflow
      void backdropEl.offsetWidth;

      requestAnimationFrame(function () {
        backdropEl.classList.add("ngis-modal-active");
        backdropEl.classList.remove("ngis-modal-enter");

        // Focus first interactive element or close button
        if (modalBox) {
          var focusables = getFocusableElements(modalBox);
          var firstInput = modalBox.querySelector('input:not([type="hidden"]), select, textarea');
          if (firstInput && !options.noAutoFocus) {
            firstInput.focus();
          } else if (focusables.length) {
            focusables[0].focus();
          } else {
            modalBox.focus();
          }
        }
      });"""

new_open_anim = """      // Trigger smooth entrance animation with NGIS_MOTION or CSS fallback
      backdropEl.classList.remove("ngis-modal-exit");
      backdropEl.classList.add("ngis-modal-enter");

      if (window.NGIS_MOTION && typeof window.NGIS_MOTION.modalEnter === 'function') {
        window.NGIS_MOTION.modalEnter(backdropEl, modalBox, function () {
          backdropEl.classList.add("ngis-modal-active");
          backdropEl.classList.remove("ngis-modal-enter");
        });
      } else {
        void backdropEl.offsetWidth;
        requestAnimationFrame(function () {
          backdropEl.classList.add("ngis-modal-active");
          backdropEl.classList.remove("ngis-modal-enter");
        });
      }

      // Focus first interactive element or close button
      if (modalBox) {
        var focusables = getFocusableElements(modalBox);
        var firstInput = modalBox.querySelector('input:not([type="hidden"]), select, textarea');
        if (firstInput && !options.noAutoFocus) {
          firstInput.focus();
        } else if (focusables.length) {
          focusables[0].focus();
        } else {
          modalBox.focus();
        }
      }"""

# Replace in close:
old_close_anim = """      backdropEl.classList.remove("ngis-modal-active");
      backdropEl.classList.add("ngis-modal-exit");

      var prefersReducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      var duration = prefersReducedMotion ? 10 : 180;

      setTimeout(function () {
        if (backdropEl && backdropEl.parentNode) {
          backdropEl.parentNode.removeChild(backdropEl);
        }
        unlockScroll();

        // Restore focus
        if (lastActiveElement && typeof lastActiveElement.focus === "function") {
          try { lastActiveElement.focus(); } catch (err) {}
        }
      }, duration);"""

new_close_anim = """      backdropEl.classList.remove("ngis-modal-active");
      backdropEl.classList.add("ngis-modal-exit");

      var cleanup = function () {
        if (backdropEl && backdropEl.parentNode) {
          backdropEl.parentNode.removeChild(backdropEl);
        }
        unlockScroll();

        // Restore focus
        if (lastActiveElement && typeof lastActiveElement.focus === "function") {
          try { lastActiveElement.focus(); } catch (err) {}
        }
      };

      if (window.NGIS_MOTION && typeof window.NGIS_MOTION.modalExit === 'function') {
        window.NGIS_MOTION.modalExit(backdropEl, entry ? entry.box : null, cleanup);
      } else {
        var prefersReducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        var duration = prefersReducedMotion ? 10 : 180;
        setTimeout(cleanup, duration);
      }"""

if old_open_anim in text:
    text = text.replace(old_open_anim, new_open_anim, 1)
    print("Updated NGISModalSystem.open")
else:
    print("old_open_anim not found")

if old_close_anim in text:
    text = text.replace(old_close_anim, new_close_anim, 1)
    print("Updated NGISModalSystem.close")
else:
    print("old_close_anim not found")

with open('assets/js/modal-system.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved assets/js/modal-system.js successfully!")
