motion_css = """
/* ==========================================================================
   NGIS GLOBAL MOTION DESIGN & MICRO-INTERACTION SYSTEM (2026)
   Tokens, Hardware-Accelerated Transforms, Card Lifts, Shake & Reduced Motion
   ========================================================================== */

:root {
  --ngis-motion-duration-press: 100ms;
  --ngis-motion-duration-hover: 180ms;
  --ngis-motion-duration-tooltip: 120ms;
  --ngis-motion-duration-dropdown: 180ms;
  --ngis-motion-duration-modal-enter: 240ms;
  --ngis-motion-duration-modal-exit: 180ms;
  --ngis-motion-duration-sidebar: 260ms;
  --ngis-motion-duration-height: 240ms;
  --ngis-motion-duration-shake: 300ms;
  --ngis-motion-duration-success: 400ms;
  --ngis-motion-scale-press: 0.97;
  --ngis-motion-scale-entrance: 0.97;
  --ngis-motion-card-lift: -2.5px;
  --ngis-motion-ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ngis-motion-ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ngis-motion-ease-spring: cubic-bezier(0.34, 1.4, 0.64, 1);
}

/* 1. Physical Press Feedback */
button:active:not(:disabled),
.btn:active:not(:disabled),
.icon-btn:active:not(:disabled),
.tab-btn:active,
.exw-tab:active,
.exw-roadmap-tab:active,
.hamburger-btn:active,
.mobile-hamburger-btn:active,
.htb-ctrl-btn:active,
.action-btn:active,
.pill-btn:active,
[data-action]:active {
  transform: scale(var(--ngis-motion-scale-press)) !important;
  transition: transform var(--ngis-motion-duration-press) var(--ngis-motion-ease-out) !important;
}

/* 2. Subtle Card Hover Lift (Disabled on touch-only devices) */
@media (hover: hover) and (pointer: fine) {
  .card-hover:hover,
  .ql-card:hover,
  .module-card:hover,
  .dept-card:hover,
  .task-card:hover,
  .ann-card:hover,
  .exam-card:hover,
  .subject-card:hover,
  .interactive-card:hover,
  .exw-timeline-card:hover,
  .ngis-card-lifted {
    transform: translateY(var(--ngis-motion-card-lift)) scale(1.007) !important;
    box-shadow: 0 8px 24px -4px rgba(15, 23, 20, 0.08), 0 2px 6px -2px rgba(15, 23, 20, 0.04) !important;
    transition: transform var(--ngis-motion-duration-hover) var(--ngis-motion-ease-out),
                box-shadow var(--ngis-motion-duration-hover) var(--ngis-motion-ease-out) !important;
  }
}

/* 3. Subtle Horizontal Error Shake (3-5px over 300ms) */
@keyframes ngis-error-shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-4px); }
  40%, 80% { transform: translateX(4px); }
}

.ngis-shake {
  animation: ngis-error-shake var(--ngis-motion-duration-shake) cubic-bezier(0.36, 0.07, 0.19, 0.97) both !important;
}

.ngis-error-static {
  outline: 2px solid #ef4444 !important;
  transition: outline 200ms ease;
}

/* 4. Scale 0.97 Entrances and Exits */
@keyframes ngis-scale-enter {
  0% { opacity: 0; transform: scale(var(--ngis-motion-scale-entrance)) translateY(6px); }
  100% { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes ngis-scale-exit {
  0% { opacity: 1; transform: scale(1) translateY(0); }
  100% { opacity: 0; transform: scale(var(--ngis-motion-scale-entrance)) translateY(6px); }
}

.ngis-scale-enter {
  animation: ngis-scale-enter var(--ngis-motion-duration-dropdown) var(--ngis-motion-ease-out) forwards !important;
}

.ngis-scale-exit {
  animation: ngis-scale-exit var(--ngis-motion-duration-dropdown) var(--ngis-motion-ease-in) forwards !important;
}

/* 5. Intelligent Tooltip Styling */
.ngis-motion-tooltip {
  position: fixed;
  z-index: 9999;
  pointer-events: none;
  background: #0f172a;
  color: #ffffff;
  font-size: 11.5px;
  font-weight: 500;
  padding: 5px 10px;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: none;
  white-space: nowrap;
  line-height: 1.3;
  letter-spacing: 0.01em;
}

[data-theme="dark"] .ngis-motion-tooltip {
  background: #1e293b;
  color: #f8fafc;
  border: 1px solid #334155;
}

/* 6. Success Feedback Toast & Animated Checkmark */
.ngis-success-toast {
  position: fixed;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10000;
  pointer-events: none;
}

.ngis-success-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: #ffffff;
  border: 1px solid #dcfce7;
  color: #166534;
  padding: 10px 18px;
  border-radius: 9999px;
  box-shadow: 0 10px 30px -4px rgba(22, 101, 52, 0.12), 0 2px 8px -2px rgba(0, 0, 0, 0.06);
  font-size: 13px;
  font-weight: 500;
}

[data-theme="dark"] .ngis-success-pill {
  background: #13241b;
  border-color: #1e3a29;
  color: #86efac;
}

.ngis-success-checkmark {
  color: #16a34a;
  flex-shrink: 0;
}

/* 7. Full Accessibility & Prefers-Reduced-Motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .ngis-shake {
    animation: none !important;
  }
  .card-hover:hover,
  .ql-card:hover,
  .interactive-card:hover,
  .exw-timeline-card:hover,
  .ngis-card-lifted {
    transform: none !important;
    box-shadow: none !important;
  }
}
"""

with open('assets/css/interactions.css', 'r', encoding='utf-8') as f:
    content = f.read()

mark = "/* ==========================================================================\n   NGIS GLOBAL MOTION DESIGN & MICRO-INTERACTION SYSTEM"
if mark in content:
    content = content[:content.find(mark)].rstrip()

content = content + "\n\n" + motion_css

with open('assets/css/interactions.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated assets/css/interactions.css successfully!")
