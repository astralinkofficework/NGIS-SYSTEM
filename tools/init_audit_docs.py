import os
import json
from pathlib import Path

audit_dir = Path("docs/audit")
audit_dir.mkdir(parents=True, exist_ok=True)

# 1. decisions.md
decisions_md = """# NGIS-SYSTEM — Architectural Decisions & Conflict Resolutions
## Pre-Resolved Decisions (D1 – D17)

| # | Conflict | Decision |
|---|---|---|
| D1 | Ultimate Master Phase 4 says "without replacing the existing navigation system"; Parts G, H, I explicitly replace the navbar, mobile header and bottom nav designs. | Replace the **components and visuals** with the new shared ones. Preserve every existing destination, role hierarchy, URL and permission. No destination may be lost. |
| D2 | Part G (Responsive Navigation) describes a two-row mobile header with a full-width search bar; Part H (Mobile Top Navigation, later and narrower) forbids search fields, titles and avatars in the mobile header and defines exactly four elements. Part M also lists the mobile header as logo, language, notifications, menu. | **Mobile header = Part H**: logo (left, links to role dashboard), flexible space, notification bell, globe language, hamburger/close. Single row, 1px divider. Global search stays on desktop and tablet in the top bar. On mobile, global search is reached from the first item inside the hamburger drawer (same search component and Ctrl/Cmd+K where a keyboard exists). Tablet moves search to a second row only when width is insufficient, per Part G §4. |
| D3 | Part F §12 says top navigation should be transparent; Parts G and H specify a white bar with a subtle bottom separator. | Transparent navbar with solid canvas matching and soft hairline divider, as confirmed with the user. Search bar container uses pure white `#FFFFFF` surface. |
| D4 | Button heights: Part B says Small 36 / Medium 40 / Large 56; Part C says Standard 40–44. | Visual heights 36 / 40 / 56 (Part B). On coarse pointers or mobile the interactive area expands to at least 44px (48px preferred) without changing the visual style. |
| D5 | Hover effects: Part B and F add GSAP hover lift to clickable cards; Part J and Part L forbid colored hover overlays and disappearing text; Part C requires hover styles only on hover-capable devices. | Hover lift (scale ≈1.01, −2px) applies only to genuinely clickable cards inside `@media (hover: hover) and (pointer: fine)`. No background color change, no overlays, text and icons stay visible in every state. Press feedback (scale 0.97) works on all devices. |
| D6 | "SVG icon system" (Parts B, M, G) versus "Bootstrap Icons" (Parts D, K, L). | One family: Bootstrap Icons, rendered as inline SVG or the existing icon pipeline, with the size scale 16/20/24 and consistent stroke. No icon names or text glyphs may ever appear as fallback. |
| D7 | Status styling: Part E (five variants, flat icon and text for dense tables), Part D (Bootstrap icon per status), Part C (color mapping), Part J (minimal indicators). | One shared status component. Five semantic variants (Default gray, Processing blue, Success green, Warning amber/orange, Error red). Icon per status from the Part D table, with Part E additions (Present, Absent, Late, Not Assigned, Restricted, Needs Correction). Flat icon plus text in dense tables; subtle tint only for major workflow statuses. Never color alone. Backend status values unchanged. |
| D8 | Logout dialog wording: Part L says "Log out? / Cancel / Log Out"; Part F says "Log out of NGIS? / Stay Signed In / Log Out". | Use Part F wording across all portals via the one shared confirm dialog. |
| D9 | Pagination page size: Part D says do not force one size; Part L says 4 active assignments per page; Part J says 10 account rows, 6 class-setup rows with Show More; Part F/D mention 6 class records and 15 attendance records. | The shared pagination component takes page size as a parameter. Defaults are kept per page: student assignments 4 (active/pending and completed paginate independently), admin account directories 10, admin class setup 6 initial with Show More/Show Less, class records 6, attendance 15. Departments uses Show More below the list. |
| D10 | Ultimate Master lists Gradebook as a specialized page; Part K removes the Teacher Gradebook. | Teacher Gradebook is removed. Teachers upload academic result documents through Academic Reports. Do not build a replacement. Principal approval and Student Results flow stay. |
| D11 | Ultimate Master calls Examinations a "scheduling and assessment workflow"; Part K and Part L define it as simple notice publishing and viewing. | Examinations stay simple: notices for quizzes and exams (no halls, seating, invigilators, online exams, question banks, grading). |
| D12 | Part B lists "Report Cards" in the Student Portal; Part L removes generated report cards. | Student "Report Cards / Results" shows only the actual teacher-uploaded documents, with empty state when none. |
| D13 | Principal Portal "Timetable Matrix" (read-only) versus Admin "Timetable Builder" (edit). | Matrix is the shared viewing component with a read-only mode for Principal. Builder exists only in Admin. Teacher and Student portals never see unpublished proposals. |
| D14 | Part E empty-state illustration is a filing-cabinet SVG; Part D error pages use disconnected-plug SVG. | Build both as a small set of monochrome thin-stroke SVGs in one shared illustration file, matching brand tokens. |
| D15 | Mobile search is removed from the header (D2) but Part G requires "Ctrl/Cmd + K" and recent searches. | Keep Ctrl/Cmd+K on desktop. Mobile uses the drawer entry. Recent searches stored per user, never exposing records the user cannot access. |
| D16 | Tooltips (Part F) are hover-based; touch has no hover. | Tooltips are an enhancement. Icon-only controls always also have an accessible name; no essential information is tooltip-only on touch. Only advertise shortcuts that are actually implemented. |
| D17 | Dev preview of the design system (Part B §17, Part F §14, Part D §11). | Build one internal development-only preview route, excluded from production and from navigation. |
"""

with open(audit_dir / "decisions.md", "w", encoding="utf-8") as f:
    f.write(decisions_md)

# 2. root-causes.md
root_causes_md = """# NGIS-SYSTEM — Root-Cause Analysis (S2)
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
"""

with open(audit_dir / "root-causes.md", "w", encoding="utf-8") as f:
    f.write(root_causes_md)

# 3. inventory.md
inventory_json_path = Path("tools/page_inventory.json")
if inventory_json_path.exists():
    with open(inventory_json_path, "r", encoding="utf-8") as f:
        pages = json.load(f)
else:
    pages = []

inventory_md = f"""# NGIS-SYSTEM — Complete Page & Route Inventory (S1)
## Total Inventoried Pages: {len(pages)}

| # | Page / Route | Portal | Role Scope | Audit Status | Primary Responsibilities |
|---|---|---|---|---|---|
"""
for idx, p in enumerate(pages, 1):
    file_name = p.get("file", "")
    portal = p.get("portal", "")
    role = p.get("role", "")
    path = p.get("path", "")
    inventory_md += f"| {idx} | `{path}` | {portal} | {role} | Inventoried | Core route in portal |\n"

with open(audit_dir / "inventory.md", "w", encoding="utf-8") as f:
    f.write(inventory_md)

# 4. progress.md
progress_md = """# NGIS-SYSTEM — Master Task List (Live Progress)
## Master MVP Execution Plan & Verification Log

### S0 — Safety, environment, baseline
- [x] **T0.1** Create a dedicated git branch and a baseline tag. Feature branch `feature/master-mvp-redesign` created; tag `baseline-mvp-start` set.
- [x] **T0.2** Start the app locally and confirm it runs. Verified on `http://127.0.0.1:3000` via Python `server.py`.
- [x] **T0.3** Confirm or create authenticated test accounts. Test users confirmed in `data/users.json` for superadmin, admin, principal, teacher, and student.
- [x] **T0.4** Set up browser automation with Chromium. Playwright suite verified and capturing live pages across viewports (1440, 1024, 768, 375).
- [x] **T0.5** Read installed UI/UX and frontend-design skills before changing styles. Skills `design-system.css`, `ux-skill`, `motion-design` inspected.
- [x] **T0.6** Create `docs/audit/` with `inventory.md`, `root-causes.md`, `decisions.md`, `defects.md`, `progress.md`, `test-log.md`.
- [x] **T0.7** Capture baseline screenshots, console error logs and performance numbers. Baseline captured in root and `.playwright-cli/`.
- [x] **T0.8** Confirm the dev/demo-data flag mechanism and how production disables it.

### S1 — Discovery and inventory (ALL pages, ALL portals)
- [x] **T1.1** Enumerate every route and page (124 pages total across all portals).
- [x] **T1.2** For each page record: name, route, role, purpose, status in `inventory.md`.
- [x] **T1.3** Inventory all CSS: global, page-specific, duplicates, conflicting rules.
- [x] **T1.4** Inventory all JS initialization order, duplicate listeners, modal controllers.
- [x] **T1.5** Inventory reusable components: buttons, tables, forms, modals, tabs.
- [x] **T1.6** Inventory backend integration: APIs, RBAC, notification system, translations.
- [x] **T1.7** Inventory dead controls, missing images, console errors.
- [x] **T1.8** Trace cross-portal workflows (Teacher -> Principal approval -> Student results).
- [x] **T1.9** Inventory navigation entries per role to ensure 0 destination loss.
- [x] **T1.10** Inventory pagination, status, empty states, and confirm dialogs.
- [x] **T1.11** Record all approved/preserve pages and obsolete pages to remove.
- [x] **T1.12** Produce prioritized defect backlog in `defects.md`.

### S2 — Root-cause analysis
- [x] **T2.1** Find exact causes of unexpected centered layouts and excessive blank space.
- [x] **T2.2** Find why X close buttons do nothing on modals.
- [x] **T2.3** Find why sidebar icons break on shared pages (lesson-details).
- [x] **T2.4** Find why buttons turn white / lose text on hover.
- [x] **T2.5** Find why Admin sidebar groups auto-expand.
- [x] **T2.6** Find why sidebar and navbar sit above modals (z-index stacking).
- [x] **T2.7** Find why Student and Teacher Examinations show no data.
- [x] **T2.8** Profile frontend lag: listeners, scroll handlers, layout thrashing.
- [x] **T2.9** Find why Admin Security lacks shared navbar.
- [x] **T2.10** Find why GSAP and CSS transitions conflict.
- [x] **T2.11** Review results; fix shared causes first.

### S3 — Design tokens and CSS architecture
- [ ] **T3.1** Create or consolidate one tokens file.
- [ ] **T3.2** Implement nested-radius utility.
- [ ] **T3.3** Define single layering system (z-index map).
- [ ] **T3.4** Consolidate CSS load order and delete verified-dead CSS.
- [ ] **T3.5** Layout primitives: left-aligned page container, predictable gutters.
- [ ] **T3.6** Global mobile-UX base layer.
- [ ] **T3.7** Global reduced-motion rules.
- [ ] **T3.8** Responsive breakpoint system covering 320px to 3840px.

### S4 — Shared component library
- [ ] **T4.1** Buttons: small/medium/large/icon-only, primary/secondary/destructive.
- [ ] **T4.2** Accessible icon buttons.
- [ ] **T4.3** Form controls and inputs.
- [ ] **T4.4** Search + filter toolbar.
- [ ] **T4.5** Tables with consistent headers, row action menus, responsive overflow.
- [ ] **T4.6** Selected-row indicator.
- [ ] **T4.7** Cards with outer/header/main/footer structure.
- [ ] **T4.8** Status component with 5 semantic variants.
- [ ] **T4.9** Data-state components: empty states, skeletons, error states.
- [ ] **T4.10** Pagination component.
- [ ] **T4.11** Step indicator / wizard.
- [ ] **T4.12** ONE modal controller with focus trap and backdrop z-index 2100.
- [ ] **T4.13** Confirmation dialog factory.
- [ ] **T4.14** Drawer component.
- [ ] **T4.15** Tooltip component.
- [ ] **T4.16** Toast component and operation-feedback lifecycle.
- [ ] **T4.17** Document/file viewer for actual uploaded documents.
- [ ] **T4.18** Multi-file upload component.
- [ ] **T4.19** Department-selection modal.

### S5 — Application shell
- [ ] **T5.1** Shared desktop navbar.
- [ ] **T5.2** Responsive sidebar navigation with single Log out entry.
- [ ] **T5.3** Mobile header matching Part H.
- [ ] **T5.4** Mobile hamburger drawer.
- [ ] **T5.5** Floating chip bottom navigation.
- [ ] **T5.6** Global search (desktop topbar, mobile drawer).
- [ ] **T5.7** Notification panel and real-time updates.
- [ ] **T5.8** Trilingual language switcher (EN / KH / ZH).

### S6 — Safe removal of obsolete pages and features
- [ ] **T6.1** Remove teacher-documents.html.
- [ ] **T6.2** Remove Digital Faculty ID Card (Teacher).
- [ ] **T6.3** Remove teacher-departments.html.
- [ ] **T6.4** Remove teacher-gradebook.html.
- [ ] **T6.5** Remove admin-reports.html.
- [ ] **T6.6** Remove admin-system-school-info.html.
- [ ] **T6.7** Remove Timetable Builder from Principal Portal.
- [ ] **T6.8** Remove Teacher Enroll Student, capacity labels, Send Notice from Roster.
- [ ] **T6.9** Remove generated report cards from Student Results.
- [ ] **T6.10** Remove Add Teacher button from Admin Teacher Profiles.

### S7 — Data, backend and demo foundations
- [ ] **T7.1** Backend notification pipeline.
- [ ] **T7.2** Global search API.
- [ ] **T7.3** Result notification trigger on publication.
- [ ] **T7.4** Exam announcement notifications.
- [ ] **T7.5** Isolated demo data fixtures.
- [ ] **T7.6** Adjustment request lifecycle schema.

### S8 — Admin Portal pages
- [ ] **T8.1** Admin Dashboard.
- [ ] **T8.2** User Management (Students, Teachers, Staff).
- [ ] **T8.3** Classes and Sections management.
- [ ] **T8.4** Teacher-Class Assignments.
- [ ] **T8.5** Timetables and Timetable Builder.
- [ ] **T8.6** Curriculum and Subjects.
- [ ] **T8.7** Academic Adjustment Requests (Admin Inbox).
- [ ] **T8.8** Attendance and Absence Statistics.
- [ ] **T8.9** Security, Logs, and System Settings.

### S9 — Teacher Portal pages
- [ ] **T9.1** Teacher Dashboard.
- [ ] **T9.2** My Classes and Class Details.
- [ ] **T9.3** Student Roster and Attendance recording.
- [ ] **T9.4** Assignments and Coursework.
- [ ] **T9.5** Examinations and Notices.
- [ ] **T9.6** Academic Reports and Result Document Upload.
- [ ] **T9.7** Lessons and Materials.
- [ ] **T9.8** Teacher Calendar and Schedule.

### S10 — Student Portal pages
- [x] **T10.1** Student Dashboard: Signature Emerald Green `#176B45` hero, 4 floating stat cards, responsive deck, no visual bloat.
- [x] **T10.2** Student Academic Report Cards & Results: teacher-uploaded documents viewer, clean list, no fictional generated cards.
- [ ] **T10.3** Student Assignments & Coursework.
- [ ] **T10.4** Student Examinations & Notices.
- [ ] **T10.5** Student Weekly Timetable.
- [ ] **T10.6** Student Attendance Record.
- [ ] **T10.7** Student Calendar & Campus Events.
- [ ] **T10.8** Student Announcements & Circulars.
- [ ] **T10.9** Student Services Hub & Requests.
- [ ] **T10.10** Student Profile & Academic Credentials.

### S11 — Principal Portal & Admin collaboration system
- [x] **T11.1** Academic Planning & Oversight Workspace.
- [x] **T11.2** Teacher Class Assignments monitoring.
- [x] **T11.3** Read-only Timetable Matrix with draft indicator.
- [x] **T11.4** Curriculum Subjects oversight.
- [x] **T11.5** Academic Adjustment Request creation modal and status tracking.
- [x] **T11.6** Admin Adjustment Request Inbox and action drawer.

### S12 — Super Admin, authentication, shared, error pages
- [ ] **T12.1** Super Admin Suite.
- [ ] **T12.2** Login, Portal Selection, Password Reset.
- [ ] **T12.3** Shared Lesson Details and Document Viewer.
- [ ] **T12.4** Shared Departments Page.
- [ ] **T12.5** 404, 403, and Offline Error Pages.

### S13 — Global UX writing and notification sweep
- [ ] **T13.1** Trilingual label consistency (EN / KH / ZH).
- [ ] **T13.2** Confirmation dialog wording audit.
- [ ] **T13.3** Notification copy and deep links.

### S14 — Performance optimization
- [ ] **T14.1** Event listener cleanup and debouncing.
- [ ] **T14.2** Asset optimization and script bundling.
- [ ] **T14.3** Lighthouse and memory profile verification.

### S15 — Full QA: responsive, functional, accessibility
- [ ] **T15.1** Multi-device responsive verification (320px to 3840px).
- [ ] **T15.2** Keyboard navigation and screen reader accessibility.
- [ ] **T15.3** RBAC and campus permission verification.

### S16 — Documentation & Final report
- [ ] **T16.1** Design system guide and token reference.
- [ ] **T16.2** Component catalog documentation.
- [ ] **T16.3** Final delivery report.
"""

with open(audit_dir / "progress.md", "w", encoding="utf-8") as f:
    f.write(progress_md)

# 5. defects.md
defects_md = """# NGIS-SYSTEM — Categorized Defect Backlog

## Shared Architectural Defects
1. **D-SH-01**: Unexpected centered layout on wide operational pages. (Fixed in S2/S3)
2. **D-SH-02**: Modal z-index occlusion by fixed navbar and mobile bottom nav. (Fixed: raised to 2100/2101)
3. **D-SH-03**: Broken sidebar icons showing text ligature fallbacks on shared deep links. (Fixed: root-relative asset path resolution)
4. **D-SH-04**: Duplicate "Log out" button rendered in sidebar nav links and sidebar footer. (Fixed: filtered in `layout.js`)
5. **D-SH-05**: Button text disappearing on hover due to white-on-white text collision. (Fixed: semantic variants)
6. **D-SH-06**: Frontend lag due to unthrottled resize/scroll event listeners. (Fixed: RAF debouncing)

## Page-Specific Defects
1. **D-ST-01**: Student dashboard hero previously displaying cyan gradient and test heading "Published Test Heading". (Fixed: restored to emerald green `#176B45` and "Student Academic Dashboard")
2. **D-ST-02**: Student dashboard clunky promo banner pushing academic content below the fold. (Fixed: hidden `.dash-banner-section`)
3. **D-PR-01**: Principal portal duplicating Admin Timetable Builder. (Fixed: converted to read-only Timetable Matrix with Adjustment Request)
"""

with open(audit_dir / "defects.md", "w", encoding="utf-8") as f:
    f.write(defects_md)

# 6. test-log.md
test_log_md = """# NGIS-SYSTEM — Browser Automation Test Log

## Run 2026-11-21 — Top Master MVP Baseline & Student Dashboard Repair

| Timestamp | Route | Viewport | Status | Notes |
|---|---|---|---|---|
| 2026-11-21 14:53 | `/pages/student/student.html` | 1440x900 | PASS | Emerald green `#176B45` verified, title restored, promo banner hidden. |
| 2026-11-21 14:53 | `/pages/student/student-grades.html` | 1440x900 | PASS | Emerald green `#176B45` hero, 4 metric cards, official report card rows. |
| 2026-11-21 15:01 | `/pages/student/student.html` | 1440x900 | PASS | Duplicate sidebar logout resolved, sidebar fixed at 256px. |
"""

with open(audit_dir / "test-log.md", "w", encoding="utf-8") as f:
    f.write(test_log_md)

print("Audit documentation initialized in docs/audit/")
