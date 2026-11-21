# NGIS icon and accent refinement

## Inventory and root causes

The source sweep covered 123 portal HTML files (53 Admin, 26 Principal, 17 Teacher, 12 Student and 15 Shared), with supporting CSS, templates and JavaScript reviewed for the relevant component families. A broad markup heuristic flagged 64 pages for inspection. The flag includes legitimate controls and status surfaces. Earlier Playwright evidence contains 324 desktop and mobile route attempts and helped establish the navigation baseline.

| Pattern | Source and reason it recurred | Treatment |
| --- | --- | --- |
| Workspace and timetable metrics | The [Student workspace renderer](assets/js/ngis-student-workspace.js#L72), [Teacher workspace renderer](assets/js/ngis-teacher-workspace.js#L57) and [Khmer suite renderer](assets/js/khmer-suite-ui.js#L228) emit alignment slots whose styles supplied independent green, orange and red fills. | Keep the dimensions. Use neutral icons for ordinary metrics and semantic foreground tokens for significant warning or error metrics. |
| Notification lists | [Desktop](assets/js/navbar.js#L541) and [mobile](assets/js/mobile-nav.js#L287) render separate bell wrappers with painted CSS blocks. The unread dot and row already convey unread state. | Use neutral glyphs in both wrappers. Preserve the unread cue and row interaction. |
| Sidebar and bottom navigation | [Shared mobile CSS](assets/css/shared-components.css) set a background on every span in the active item. [Sidebar rules](assets/css/app.css) recolored hovered labels and explicitly suppressed keyboard outlines. | Apply accent to the glyph. Retain selected label weight and aria-current. Restore the inset sidebar focus outline. |
| Ordinary card and heading icons | Several component templates and 23 page files gave isolated glyphs tint, radius, borders or shadows through Tailwind utilities. Chromium identified a shared telemetry rule that reapplied mint to any 40-by-40 descendant in a telemetry card. Removing that size-based rule eliminated the Principal dashboard regression. Student and Teacher quick links also used inline backgrounds. | Migrate 62 isolated glyph wrappers to the shared alignment pattern. Retain per-context spacing. Use the shared quick-link CSS after removing its inline fills. |
| Disclosure and empty states | [Disclosure markup](assets/js/smart-disclosure.js#L342) emitted a painted square. [UI state markup](assets/js/ui-states.js) got a colored circular base from overlapping styles, with error sometimes drawn in brand green. | Remove the ornamental surfaces, use neutral foregrounds by default and derive error, warning and success glyph colors from semantic tokens. |
| Competing action colors | [Design system](assets/css/design-system.css) and [cleanup stylesheet](assets/css/ui-cleanup.css) treated legacy accent action classes as orange primary buttons. | Map the legacy accent action to Forest Green and keep explicit warning and destructive variants. |

The shared Bootstrap icon engine still determines each glyph's rendering. The notification wrapper no longer forces an SVG fill. Scope guards in the migration limited changes to plain single-glyph wrappers. Timetable subject coding, actual notification counts, confirmation severity, destructive controls and academic statuses retain their respective treatments.

## Files modified

- **Standards:** AGENTS.md and DESIGN-RULES.md.
- **Shared CSS:** app.css, design-system.css, design-tokens.css, khmer-suite.css, mobile-header.css, navbar.css, ngis-components.css, shared-components.css, smart-disclosure.css, ui-cleanup.css and ui-states.css, under assets/css.
- **Admin:** admin-absence-stats, admin-campuses, admin-classes, admin-department-detail, admin-lost-found, admin-services, admin-subjects, admin-teacher-class-assignment and admin-timetables.
- **Principal:** principal, principal-activity, principal-attendance, principal-classes, principal-departments, principal-lost-found, principal-profile and principal-services.
- **Student:** student, student-assignments, student-grades and css/quicklinks.css. **Teacher:** teacher and teacher-reports. **Shared:** departments. Page names above refer to the corresponding HTML files.
- **Verification:** tests/icon-surfaces.test.cjs and NGIS-audit-evidence/icon-design.py and NGIS-audit-evidence/icon-verify.cjs.

## Verification

- The [targeted regression check](tests/icon-surfaces.test.cjs) passed. It checks ordinary icon-slot declarations and markup for painted wrappers. Its scope excludes status, selection and functional button surfaces.
- Calculated token contrast: neutral glyph on white 4.94:1, Forest Green on white 6.51:1, dark neutral glyph on dark surface 10.77:1, and active glyph on dark surface 10.62:1. Warning and error glyph tokens on white measure 5.02:1 and 6.50:1. These measurements apply to the token pairs.
- The design-audit scanner completed its static pass over 165 page files. Its existing focus and motion findings extend beyond this change.
- Node Playwright Chromium checked the local frontend files at 1440, 768 and 375 px with intercepted, empty API fixtures. The run covers 24 page routes and all migrated ordinary-icon wrappers. Comparison screenshots use the committed CSS as the baseline for the shared fixture. See [browser measurements](NGIS-audit-evidence/icon-browser-verification.json), [baseline fixture](NGIS-audit-evidence/icon-components-git-baseline.png) and [refined fixture](NGIS-audit-evidence/icon-components-refined-light.png).

## Remaining coverage

Live authenticated data, real interaction flows, a comprehensive dark-mode page sweep, and browser engines beyond Chromium remain unverified. The loopback Flask port was inaccessible in the managed shell, so the browser suite intercepted requests. Parent has no reachable portal in the prior audit, authenticated Super Admin coverage is incomplete, and the separate Next.js timetable failed to render its schedule in the prior browser sweep. Page-owned colors that encode application state or are embedded in bespoke templates require component-specific review before migration. The [functional audit](NGIS-SYSTEM-AUDIT.md) records the earlier navigation and workflow findings.

