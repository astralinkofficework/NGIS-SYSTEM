# NGIS-SYSTEM — Root-Cause Analysis (S2)
## Shared Architectural Defect Investigation

### T2.1 Unexpected Centered Layouts and Excessive Blank Space
- **Root Cause**: Inherited CSS rules on `.main-content`, `main`, and flex wrappers using `justify-content: center` and `align-items: center` indiscriminately across dashboard routes, combined with hardcoded `max-width: 1200px; margin: 0 auto;` on operational wide-table pages.
- **Resolution**: Removed centered wrappers. Applied left-aligned page container `.ngis-page-container` with predictable 24px desktop / 16px mobile gutters.

### T2.2 Dead 'X' Close Buttons on Modals
- **Root Cause**: Event listener collision between legacy vanilla click handlers, dynamically injected modal HTML, and competing event listeners calling `stopPropagation()` before document delegation could process `data-action="close"`. In several modals, duplicate element IDs `#closeModal` existed simultaneously in DOM.
- **Resolution**: Standardized on unified `NGIS.modal` controller with global event delegation on `[data-action="close-modal"]`, keyboard Esc listener, focus trap, and modal state management.

### T2.3 Broken Sidebar Icons on Shared Pages & Missing Navigation Items
- **Root Cause**: Relative asset path resolution failure for SVG icons (`../../assets/...` vs `../assets/...`) on shared pages like `lesson-details.html`, causing glyph fallback to raw text strings. Also, role parameter `?portal=` was not passed to sidebar engine on deep links.
- **Resolution**: Normalized asset paths using root-relative path resolution in `action-icons.js` and hydrated icons universally through `NGIS.icon()`.

### T2.4 Button Text/Icon Disappearing on Hover
- **Root Cause**: Unscoped CSS rule `:hover { color: #ffffff !important; }` applied to elements that had white backgrounds on hover, resulting in white-on-white invisible text.
- **Resolution**: Replaced with strict semantic button variants (`.btn-primary`, `.btn-secondary`, `.btn-outline`) with explicit text and icon contrast guarantees across all states.

### T2.5 Admin Sidebar Groups Auto-Expanding
- **Root Cause**: Duplicate `initSidebar()` calls on DOM ready and window load re-evaluating the active route and forcing every parent collapsible group open, overriding user state and local storage.
- **Resolution**: Made sidebar initialization strictly idempotent via `window.__NGIS_SIDEBAR_INIT__` guard and single state store.

### T2.6 Sidebar and Navbar Stacking Context Occluding Modals
- **Root Cause**: Fixed navbar `.ngis-navbar` set to `z-index: 1000` and mobile chip navigation set to `z-index: 1100`, while modal backdrops were set to generic Tailwind `z-50` (50).
- **Resolution**: Raised modal backdrop to `z-index: 2100 !important;` and modal dialog boxes to `z-index: 2101 !important;` across `assets/css/shared-components.css`.

### T2.7 Empty Data in Examinations and Announcements
- **Root Cause**: Frontend API client expecting specific snake_case payload fields (`exam_date`, `is_published`) while backend returned camelCase or filtered out records when user campus was not explicitly matched.
- **Resolution**: Normalized response parser and added explicit fallback to fixture data in development mode with clear console warnings.

### T2.8 Frontend Lag and Frame Drops
- **Root Cause**: Heavy GSAP timelines attached to window `scroll` and `mousemove` without passive flag or requestAnimationFrame debouncing, combined with Chart.js full canvas re-renders on every resize event.
- **Resolution**: Applied `passive: true` to scroll listeners, debounced resize with `requestAnimationFrame`, and lazy-loaded Chart.js instances only when in viewport.
