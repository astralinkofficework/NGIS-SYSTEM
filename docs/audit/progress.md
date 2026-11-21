# NGIS-SYSTEM — Master Task List (Live Progress)
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
- [x] **T4.12** ONE modal controller with focus trap and backdrop z-index 2100.
- [ ] **T4.13** Confirmation dialog factory.
- [ ] **T4.14** Drawer component.
- [ ] **T4.15** Tooltip component.
- [ ] **T4.16** Toast component and operation-feedback lifecycle.
- [ ] **T4.17** Document/file viewer for actual uploaded documents.
- [ ] **T4.18** Multi-file upload component.
- [x] **T4.19** Department-selection modal.

### S5 — Application shell
- [x] **T5.1** Shared desktop navbar.
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
