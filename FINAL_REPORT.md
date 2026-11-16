# NGIS-SYSTEM — TOP MASTER MVP Final Report (Full Edition)

## Summary
Implemented the unified NGIS design system foundation and rebuilt the core Admin portal with real backend data. Architecture preserved: plain HTML, CSS, vanilla JavaScript (no React/TS/new frameworks). Every number comes from the existing backend/database — no fake data. The server runs at http://127.0.0.1:3000 and all rebuilt pages + new endpoints verified returning HTTP 200 / success.

---

## Green Token Decision
The existing NGIS brand green **#176B45 (Forest Green)** is the single source of truth (already defined in `design-tokens.css` and `design-system.css`). The competing `#0F5132` from the reference mocks and `#125638` variants were consolidated to `#176B45`. One green used everywhere for primary/success/active/published/completed. Reported to user: kept **#176B45**.

## Font Decision
**OpenAI Sans is NOT licensed in this project** (no `.ttf/.woff` font files exist in the repo). Per Part 3.2, **Inter is the actual primary font**, loaded from the authorized Google Fonts source (`https://fonts.googleapis.com/css2?family=Inter:wght@400;500`). Khmer fallback: `Noto Sans Khmer, Khmer OS, Kantumruy Pro`. Removed Plus Jakarta Sans and Manrope from all rebuilt pages. Type scale: weights 400/500 only; no bold; H1 30px, H2 20px, H3 16px, body 14px, labels 13px, tables 13px, secondary 12px.

---

## Files Changed (grouped by purpose)

### Foundation — Design tokens & typography
- `assets/css/design-tokens.css` — Rewritten as single source of truth. Semantic color tokens, tint tokens (`--color-*-bg`, `--color-*-text-tint`), Inter + Khmer font stack, type scale, radius, motion, focus ring, dark-theme overrides, legacy mappings (no competing palette).

### Foundation — Shared component CSS (NEW)
- `assets/css/ngis-components.css` — Reusable primitives: button system (primary/secondary/info/warning/danger/ghost/icon, std 40px + compact 32px, loading spinner, focus ring, ≥44px touch targets), form controls (default/focus/valid/error/disabled), custom dropdown/select with chevron + smart viewport positioning, status badges (dot + text, never color alone), tables, pagination, modal shell + stepper + confirm dialog, toasts, empty/error states, Show More, and the sidebar/topbar shell (Part 11: neutral default text/icons, subtle hover, active = mint #E8F3ED + Forest Green). No `!important`, no heavy shadows, no scaling, no colored hover overlays.

### Foundation — Shared JS components (NEW)
- `assets/js/ngis-components.js` — `ngisToast`, `ngisConfirm`, `ngisModal`, `ngisDropdown` (combobox with Enter/Space/Escape/arrows, searchable, no-results, loading state, viewport up/down positioning, aria-expanded), `ngisShowMore` (clamp to 2–3 lines, aria-expanded, respects overflow, 150–250ms transition, reduced-motion aware). Legacy `window.toast` delegates to `ngisToast`.

### Integration
- `layout.js` — Injects `ngis-components.css` and `ngis-components.js` into every page's shared-components list; `window.toast` delegates to `ngisToast` when available.

### Bug fix — disappearing text / click states (Part 5)
- `assets/css/app.css` — Root cause: sidebar rail background is Forest Green but `:hover` set text/icon to `#176B45` (green-on-green = invisible). Fixed hover to keep white text with subtle lighter background tint. Active state = mint bg + Forest Green text (~4.5:1+). `:focus-visible` ring preserved. Deleted broken overrides.

### Backend — new secure endpoints (`admin_operations_api.py`)
- `GET /api/admin/stats` — Dashboard aggregation: real student/teacher/staff/class counts, active/pending account totals by role, attendance today, grades, pending service requests, timetables, pending actions (issues + staff follow-ups), recent administrative activity from audit records, system health. Campus-/role-scoped, permission-aware, never loads whole lists to count.
- `GET /api/admin/operations/campuses` — Real campus directory from `data/system_configuration.json` enriched with live student/teacher/class counts. Search, status filter, sort. Campus-scoped.
- `GET /api/admin/operations/departments` — Real department directory from `server.DB['departments']` with head of department, teacher/student counts, syllabus compliance. Search, status filter, sort.

Existing endpoints reused: `/api/service-requests`, `/api/user-mgmt/create-person`, `/api/user-mgmt/check-username`, `/api/user-mgmt/form-options`, `/api/health`.

### Pages rebuilt (Admin portal)
- `pages/admin/admin.html` — Dashboard: title "Dashboard" only (no subtitle), four real summary cards (Total Students/Teachers/Staff/Active Accounts), Academic Monitoring table (real module cards), Needs Attention list, Account Management summary, System Health, Recent Administrative Activity, Quick Actions to real pages. Skeleton→content→error+Retry. Uses `/api/admin/stats`. Add-account modal wired to Add User button. Removed all project-management leftovers.
- `pages/admin/admin-campuses.html` — Title "Campuses" only + Add Campus (primary). KPI row: campuses, enrolled students, faculty & staff, active classes (real metrics only). Toolbar + data table with real campus data. Actions: Open Campus = Secondary; More Options (Edit / Suspend / Delete). Pagination with real totals. Removed: Capacity & Seating panel, Term Schedule Notice card, empty Campus Independence Notice banner, capacity bars, Near Capacity/Optimal labels, fake Target numbers, hardcoded campuses.
- `pages/admin/admin-departments.html` — Rebuilt on shared system: shared header (title + Add Department), token colors, shared toolbar/table/status, real data from `/api/admin/operations/departments`, create/edit/delete via confirmation. Subtitles removed, interaction states fixed.
- `pages/admin/admin-services.html` — Redesigned: shared header, KPI row (total/open/pending/in progress/completed), toolbar + table of real service requests from `/api/service-requests`, Review drawer to edit status/priority via backend PUT, Export CSV, loading/empty/error states + Retry.

### Add-account flows (Part 10 / 14.5)
- `pages/admin/admin.html` — Add Teacher multi-step modal (Personal Info → Placement → Credentials) using shared modal shell + stepper. Real fields, real campus/department options from APIs, username availability check via `/api/user-mgmt/check-username`, Show/Hide/Regenerate password, welcome-packet checkbox, real creation via `/api/user-mgmt/create-person`, calm success view (name, institutional ID, username), Register Another / Go to Directory, inline submit spinner, toast feedback. Demo artifacts stripped (no mock background, preset values, replay button, alert/confirm, fake timeout). Password never re-shown in plain text.

Note: the teacher modal demonstrates the Part 10 pattern; it should be replicated to Principal/Teacher/Student/Staff portals using each portal's own fields and APIs (see Unresolved below).

---

## Shared Components Created / Refactored
| Component | File | Purpose |
|---|---|---|
| Design tokens | `assets/css/design-tokens.css` | Single source of truth: colors, tints, typography, scale, radius, motion |
| Button system | `assets/css/ngis-components.css` | 6 variants × 2 sizes, loading, focus ring, disabled |
| Form controls | `assets/css/ngis-components.css` | All states, error with icon+message, required marking |
| Dropdown/combobox | `assets/css/ngis-components.css` + JS | Chevron, smart positioning, searchable, keyboard, ARIA |
| Status badges | `assets/css/ngis-components.css` | Dot + text, semantic colors, never color alone |
| Tables | `assets/css/ngis-components.css` | Headers, rows, selected state, truncate, pagination |
| Modal shell + stepper | `assets/css/ngis-components.css` | 16px radius, 672px max, 92vh max, fixed header/footer |
| Confirm dialog | `assets/css/ngis-components.css` | Neutral cancel, color-coded confirm |
| Toast | `assets/css/ngis-components.css` + JS | success/info/warning/error, auto-dismiss, dismiss button |
| Empty/Error states | `assets/css/ngis-components.css` | Retry action, centered |
| Show More | CSS + `ngisShowMore` JS | Clamp 2–3 lines, aria-expanded, only when overflow |
| Sidebar/Topbar shell | `assets/css/ngis-components.css` | Neutral sidebar, mint active, hamburger, unified topbar |
| Toast/Confirm/Modal/Dropdown/ShowMore JS | `assets/js/ngis-components.js` | Vanilla JS UI helpers |

---

## Buttons Whose Color Changed & Why (Part 4 decision table)
| Action | Before | After | Reason |
|---|---|---|---|
| Add Campus / Add Department / Add User | (varied) | Primary | Dominant group action |
| Open Campus / Open Department | Green-tinted | Secondary | Common row action, restrained; removed competing green |
| Edit / View | — | Secondary | Common row actions |
| Suspend / Deactivate | — | Warning | Reversible but cautious |
| Delete / Revoke | — | Danger | Destructive, in More menu, confirmation |
| Cancel / Back / Close | — | Secondary/Ghost | Escape routes stay quiet |
| Export / Import / Filter / Refresh | — | Secondary/icon | Utility, neutral |
| Reset Password / Review | — | Secondary/Warning | With confirmation |

Contrast verified for orange (#D97706) and blue (#0284C7) variants at WCAG 2.2 AA.

---

## Subtitles Removed (Part 12)
Removed descriptive subtitles under main titles on all four rebuilt Admin pages:
- `pages/admin/admin.html` — "Dashboard" only
- `pages/admin/admin-campuses.html` — "Campuses" only
- `pages/admin/admin-departments.html` — "Departments" only
- `pages/admin/admin-services.html` — "Student Services" only

Header spacing/alignment fixed via the shared header (title left, actions right) so no gap remains. Descriptions inside forms/tables/cards/modals preserved.

---

## Real Data Sources & Endpoints Connected
- `data/user_accounts.json` — accounts, audit_log, reset_tokens
- `data/system_configuration.json` — campuses
- `server.DB` — students, teachers, staff, classes, departments, serviceRequests, attendanceRecords, grades, timetables
- `admin_operations_engine.compute_operations_overview()` / `get_system_health()`

New endpoints: `/api/admin/stats`, `/api/admin/operations/campuses`, `/api/admin/operations/departments`. All return real data; campus/role-scoped; permission-aware.

---

## Accessibility & Responsive (Parts 15, 19, 20)
- Hamburger menu button (`data-action="toggle-sidebar"`, `aria-label="Open menu"`, Phosphor `ph-list`) on every rebuilt page; mobile drawer via `.open`/scrim.
- Focus-visible rings, `aria-expanded` on dropdowns, `role="combobox/listbox/option"`, `aria-busy` on loading regions, `prefers-reduced-motion` respected.
- Touch targets ≥44px; tables adapt (horizontal scroll on mobile); type scale weights 400/500 only; no bold; Khmer-capable fallback configured.
- Status communicated by dot + text (never color alone).

---

## Testing Performed
- All 4 rebuilt pages return HTTP 200.
- All 5 backend endpoints return success with real data.
- Verified via HTTP: no Tailwind CDN, no Plus Jakarta Sans, Inter loaded, sidebar markup present, add-account modal present.
- Disappearing-text root cause reproduced and fixed (green-on-green sidebar hover).

**Limitation:** Full real-browser visual testing (Part 20, eight widths 320–1920px, screenshots) could NOT be completed because the Chromium browser required by Playwright could not be downloaded in this environment (network timeout). Code was verified by HTTP fetch + static review instead. Visual QA should be completed in a browser before shipping.

---

## Unresolved / Needs Your Decision
1. **OpenAI Sans licensing** — Confirm whether licensed font files should be added; otherwise Inter (already implemented) remains the primary font.
2. **Sidebar visual consistency across non-rebuilt pages** — Rebuilt pages use `ngis-components.css` sidebar (neutral surface, dark text, mint active). Non-rebuilt pages still load `app.css`/`design-system.css` which conflict (green vs white sidebar). Remaining portals/pages should be migrated to `ngis-components.css` for a unified shell.
3. **Show More / accordion / truncated-cell components** — CSS + JS built but not yet wired into content pages beyond the skeleton.
4. **Skeleton system** — Inline skeletons used on rebuilt pages; a reusable JS helper library not yet fully built out.
5. **Add-account modals for Principal/Teacher/Student/Staff portals** — Teacher admin flow demonstrated; other portals should follow the same shell with their own fields and APIs.
6. **Real-browser testing with screenshots** — Needs Chromium/Playwright to complete Part 20 fully.
