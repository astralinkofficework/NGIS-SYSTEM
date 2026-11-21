# NGIS-SYSTEM audit

Audit date: 2026-11-21 local time. The audit used the working-tree snapshot, including existing uncommitted changes. Existing screenshots and prior audit notes were used only to identify areas to inspect. Playwright Chromium used 1440 px desktop and 375 px mobile viewports. The Flask page sweep targeted localhost:3000. Sample writes and backend regression suites used a disposable copy on localhost:3017. The standalone Next.js timetable ran on localhost:3001.

A page shell check covers direct navigation, document response and title, rendered portal and header signals, document-level horizontal overflow, script errors and, where present, the mobile drawer control. It does not imply that every form or record on that page was exercised. An access-denied document returned with HTTP 200 is recorded as restricted, not as coverage of the intended page. The static design scanner examined 165 files and found signals in five of six applicable families. Four were inapplicable. Individual issues below distinguish reproduced behavior from source observations.

## Fix priority and findings

### F16. A single-campus Admin can read campus and directory results outside the assigned campus

- **High · Browser-verified.** Admin Campus directory and Student Accounts data.
- **Reproduce.** In a disposable instance, create an Admin account scoped to one branch with the standard registration endpoint. Sign in as that account and compare the campus and student directory responses with the assigned campus.
- **Expected.** The account sees its assigned campus and in-scope student rows. The campus filter applies automatically based on the signed-in identity.
- **Actual.** The signed-in, single-campus fixture received three campus entries, including two outside its assignment. The student directory returned rows labeled with the assigned campus and Sensok. The test recorded counts and campus labels only. Out-of-scope writes were unverified.
- **Likely source.** The campus handler allows all entries when its account lookup yields no campus. The user directory applies request filters to the full row set without enforcing the actor's campus. In the department listing handler, the code initializes its result from the full departmental registry. The scoped Admin fixture had no configured single-department grant, so cross-department isolation remains unverified.
- **Source and evidence.** [Campus actor resolution](admin_operations_api.py#L227) · [department listing](admin_operations_api.py#L332) · [user directory](user_management_api.py#L719) · [signed-in scope comparison](NGIS-audit-evidence/targeted-results.json).
- **Priority.** Resolve scope from the authenticated account consistently and enforce it in both list queries and write guards. Verify each scoped route with a single-campus and single-department fixture.

### F01. Principal adjustment actions claim cross-portal publication but persist only in the current browser

- **High · Browser-verified.** Principal Adjustment Requests and the Admin subject, faculty assignment and timetable review drawers.
- **Reproduce.** As Principal, open Adjustment Requests, select **Inspect** on a submitted record, then use **Request Clarification**, **Accept Request**, **Publish & Complete** and **Decline**. Refresh, then open the same request in a fresh browser context.
- **Expected.** Only the authorized reviewer can transition a request. History records the actual actor, enforces valid transitions and survives across sessions. Publication updates the official record.
- **Actual.** The Principal can invoke all four Admin actions, even decline after completion. History attributes the Principal's actions to a hard-coded Admin identity. The current browser retained five timeline entries and a Declined state after refresh. A fresh context showed the original Submitted state. The Publish handler updates only the request status and shows a cross-portal success message.
- **Source and evidence.** [Principal Inspect handler](pages/principal/principal-requests.html#L227) · [browser storage](assets/js/academic-requests.js#L10) · [transition handlers](assets/js/academic-requests.js#L737) · [actions screenshot](NGIS-audit-evidence/principal-inspect-actions.png) · [workflow results](NGIS-audit-evidence/workflow-results.json).
- **Priority.** Move transitions and history to server-backed, scoped actions. Derive authorship from the session and make publication contingent on updating the authoritative record.

### F11. Clean dashboard aliases serve another portal's dashboard inside the signed-in user's shell

- **High · Browser-verified.** Public route aliases and the Admin, Teacher and Principal dashboards when visited from a Student session.
- **Reproduce.** Enter the Student demo and open the canonical Admin dashboard URL. Then navigate directly to /admin, /teacher and /principal.
- **Expected.** The canonical URLs and their aliases apply the same permission decision. The dashboard and shell belong to the same role.
- **Actual.** The canonical Admin path reached Access Restricted. The three aliases returned HTTP 200 and their own dashboard titles while the rendered shell stayed Student. The browser check established foreign dashboard HTML delivery. It did not establish unauthorized access to API records or write operations.
- **Source and evidence.** [Page access gate](server.py#L93) · [direct dashboard alias handlers](server.py#L9544) · [portal resolution](assets/js/layout.js#L836) · [signed-in route comparison](NGIS-audit-evidence/targeted-results.json).
- **Priority.** Have aliases redirect to canonical gated routes or invoke the same page authorization before rendering.

### F02. Parent accounts have no reachable Parent portal

- **High · Browser-verified.** Parent sign-in, landing and navigation.
- **Reproduce.** Sign in with the local Parent fixture and open the Parent landing route. Also request the expected role page directly.
- **Expected.** A Parent session reaches its own dashboard, top bar, sidebar and mobile navigation.
- **Actual.** Sign-in returns role Parent. The Parent landing and conventional role page both returned 404. The homepage offers no Parent portal link. The Flask API defines Parent data and authentication, while the shared layout omits Parent from its portal list.
- **Source and evidence.** [Layout portal list](assets/js/layout.js#L692) · [landing cards](index.html#L172) · [Parent dashboard API branch](server.py#L3030) · [Parent 404](NGIS-audit-evidence/parent-page-missing.png) · [signed-in test](NGIS-audit-evidence/targeted-results.json).
- **Priority.** Give Parent a registered landing route and a complete role-scoped shell.

### F03. Standalone timetable schedule fails to compile

- **High · Browser-verified.** Users of the standalone Next.js timetable, on desktop and mobile.
- **Reproduce.** Run the timetable's dev script and open /schedule directly.
- **Expected.** The schedule renders or reports its data connection state.
- **Actual.** Both viewports returned HTTP 500. Next.js rejects the route's force-dynamic segment with cache components enabled. The server also reports an invalid Print import from lucide-react.
- **Source and evidence.** [Schedule segment](<timetable/src/app/(app)/schedule/page.tsx#L5>) · [shell import](<timetable/src/app/(app)/layout.tsx#L5>) · [Next config](timetable/next.config.ts) · [browser sweep](NGIS-audit-evidence/page-results.json).
- **Priority.** Fix both build errors before testing schedule interactions. The compiler error precedes the upstream timetable data dependency.

### F04. The mobile landing sidebar intercepts portal cards

- **High · Browser-verified.** Public landing and entry to Student, Teacher, Principal and Admin at 375 px.
- **Reproduce.** Open the mobile homepage, scroll a portal card into view and tap it. Try closing the sidebar and tapping again.
- **Expected.** The closed drawer leaves the cards tappable. Only an intentionally opened drawer intercepts taps.
- **Actual.** Playwright timed out on each portal card. A center hit test identified the sidebar as the element receiving the tap, and the card did not become hittable after using the visible close control. The mobile route sweep established the demo session at desktop width before switching to mobile width.
- **Source and evidence.** [Landing drawer wiring](index.html#L304) · [landing sidebar markup](index.html#L356) · [shared sidebar rules](assets/css/app.css) · [mobile landing screenshot](NGIS-audit-evidence/landing-mobile.png) · [hit-test results](NGIS-audit-evidence/targeted-results.json).
- **Priority.** Fix the landing drawer's closed state and verify hit testing and keyboard reachability before and after opening.

### F05. Selecting or clearing a registration photo discards typed identity fields

- **Medium · Browser-verified.** Staff Add User, with the same photo component shared by the five role directories.
- **Reproduce.** Open Staff Accounts → Add User. Enter first name, last name and contact email, then choose a small PNG. Remove the photo and continue.
- **Expected.** Preview and removal preserve all other form values.
- **Actual.** The preview and removal worked, but the wizard cleared the names and email and then reported “First name is required.” The shared photo callbacks rerender the full pane without synchronizing the current inputs.
- **Source and evidence.** [Photo upload and clearing callbacks](assets/js/ngis-register.js#L1203) · [cleared registration form](NGIS-audit-evidence/add-staff-blocked.png).
- **Priority.** Synchronize pane values before rerendering and add a regression check for upload, removal and oversized files.

### F06. Inspect adds a colored hover and pressed surface, and navigation recolors text

- **Medium · Browser-verified.** Principal Adjustment Requests and shared sidebar styles.
- **Reproduce.** Hover and press the first **Inspect** button. Move the pointer away and reach it with the keyboard. Hover an inactive sidebar link.
- **Expected.** Hover, press and selected states preserve a white or transparent surface and change only the icon color. Keyboard focus stays visible.
- **Actual.** Inspect changed from transparent to #e8f3ed on hover and press. Its keyboard focus retained a solid 2 px outline. The sidebar link label changed from rgb(41, 53, 46) to rgb(23, 107, 69) on hover, and dashboard active links measured a solid rgb(23, 107, 69) background.
- **Source and evidence.** [Inspect utility classes](pages/principal/principal-requests.html#L219) · [shared navigation states](assets/css/app.css#L852) · [shared keyboard focus](assets/css/app.css#L271) · [hover](NGIS-audit-evidence/principal-inspect-hover.png) · [keyboard](NGIS-audit-evidence/principal-inspect-keyboard.png) · [computed styles](NGIS-audit-evidence/targeted-results.json).
- **Priority.** Remove surface and label changes at the shared style and component layers, keeping the measured focus treatment.

### F07. Shared Academic Departments has no visible mobile hamburger

- **Medium · Browser-verified.** Shared Academic Departments when loaded directly with its Student shell at 375 px.
- **Reproduce.** Load the shared Departments URL directly at 375 px and look for a visible control to open the sidebar.
- **Expected.** A visible and named hamburger opens the role-specific drawer.
- **Actual.** The rendered Student shell included a sidebar, but none of the standard hamburger selectors resolved to a visible target.
- **Source and evidence.** [Shared department markup](pages/shared/departments.html) · [shared shell](assets/js/layout.js#L2135) · [375 px screenshot](NGIS-audit-evidence/shared-375-pages-shared-departments-html.png) · [page metrics](NGIS-audit-evidence/page-results.json).
- **Priority.** Provide the standard trigger via the shared shell. Check the scoped portal variants and the accessible expanded state.

### F08. Registration image chooser lacks a native keyboard focus target

- **Medium · Code-only.** All five Add User directories.
- **Inspect.** In the identity step, compare the visible **Choose File** label and its associated input. The file input is display:none and the standalone styled label has no native tab stop or equivalent keyboard handler.
- **Expected.** Keyboard users can focus and activate the chooser and see a focus indicator.
- **Actual in source.** Both the hidden native control and the visible label are absent from ordinary keyboard tab order. Programmatic file selection was checked separately.
- **Source.** [Registration photo control](assets/js/ngis-register.js#L214).
- **Priority.** Make the native file input focusable or use a real button wired to the chooser.

### F09. Standalone timetable declares seven sidebar destinations without matching pages

- **Medium · Browser-verified routes.** Timetable Assign, Teachers, Classes, Subjects, Overtime, Now and Print.
- **Inspect.** Compare the sidebar links with the Next app directory.
- **Expected.** Each visible destination resolves to a working route.
- **Actual.** All seven direct route checks returned HTTP 404. The schedule compile failure blocks the sidebar. Source review also found that its transform remains off-canvas at mobile widths regardless of sidebarOpen, which controls only the scrims.
- **Source.** [Timetable sidebar links](<timetable/src/app/(app)/layout.tsx#L7>) · [drawer class and conditional scrim](<timetable/src/app/(app)/layout.tsx#L51>) · [HTTP 404 results](NGIS-audit-evidence/states-results.json).
- **Priority.** Wire the mobile drawer state's transform and ship only reachable destinations.

### F13. Student timetable reports missing enrollment during a service failure

- **Medium · Browser-verified.** Student Class Timetable.
- **Reproduce.** Open Class Timetable while its timetable state service responds with HTTP 503. The test injected that response locally.
- **Expected.** The timetable reports a temporary service failure and offers Retry while preserving the user's enrollment context.
- **Actual.** The page said “No enrollment record found” and displayed no Retry action. The enrollment resolver treats failed catalog loading as an empty result.
- **Source and evidence.** [Enrollment lookup and failure handling](pages/student/student-timetable.html#L233) · [empty-state rendering](pages/student/student-timetable.html#L428) · [browser screenshot](NGIS-audit-evidence/student-timetable-network.png) · [state results](NGIS-audit-evidence/states-results.json).
- **Priority.** Distinguish unavailable services from successful empty data and route failures to the retry state.

### F15. Standalone timetable home still shows the scaffold landing page

- **Medium · Browser-verified.** Standalone timetable home.
- **Reproduce.** Start the standalone timetable using the documented dev command and open its root URL.
- **Expected.** The root introduces the timetable or routes to its first operational screen.
- **Actual.** The root renders the Create Next App starter with external Next.js and Vercel links and no entry to the local schedule.
- **Source and evidence.** [Root page](timetable/src/app/page.tsx#L26) · [rendered landing links](NGIS-audit-evidence/targeted-results.json).
- **Priority.** Replace the scaffold with a timetable entry route after the compile blockers are resolved.

### F10. Registration adjustment history wording obscures who is responsible

- **Low · UX observation.** Principal Adjustment Requests.
- **Reproduce.** Open an item via **Inspect** as Principal and read the drawer's actions and timeline.
- **Expected.** The drawer identifies whether an action is a review, a correction request or an audit detail, and shows who can perform it.
- **Actual.** The same Admin-oriented drawer opens on the Principal page. Clarification is entered in a native prompt with a prefilled example, which can be submitted as the actual rationale.
- **Source and evidence.** [Shared review labels and prompts](assets/js/academic-requests.js#L737) · [review screenshot](NGIS-audit-evidence/principal-inspect-actions.png).
- **Priority.** Use role-specific action labels and require an explicit rationale in a labeled input.

### F12. Identity regression tests still require the removed-overview contract

- **Low · Code-only, confirmed by backend test execution.** Admin User Management directory and CI.
- **Reproduce.** Run the user management regression suite against the working-tree snapshot.
- **Expected.** Tests and the intended Admin directory routes agree on whether the all-users overview exists.
- **Actual.** Two tests require admin-users.html to be absent, but the working tree includes and serves it. The test run also reported a separate overview metric mismatch. The metrics fixture includes existing locally provisioned accounts, so the mismatch requires a clean seed rerun before calling it an application defect.
- **Source and evidence.** [User Management suite](tests/test_user_management.py) · [Admin Users overview](pages/admin/admin-users.html) · [suite results](NGIS-audit-evidence/suite-results.json).
- **Priority.** Confirm the intended overview behavior and update the route contract and test fixture accordingly.

### F14. Student hub headers create competing primary headings and unnamed clear buttons

- **Low · Browser-verified markup observation.** Student Services Hub and Lost & Found Hub at desktop and mobile sizes.
- **Reproduce.** Open either hub and inspect its heading hierarchy and search controls. The page sweep recorded every rendered H1 and visible button naming attributes.
- **Expected.** The shell provides one clear primary page heading. The search clear button has an accessible name when shown.
- **Actual.** Each hub exposes both the shared hero title and a question as H1. The clear-search buttons have no text, title or ARIA name in the observed DOM.
- **Source and evidence.** [Services page heading and control](pages/student/student-services.html#L162) · [Lost & Found heading and control](pages/student/student-lost-found.html#L387) · [desktop and mobile DOM measurements](NGIS-audit-evidence/page-results.json).
- **Priority.** Preserve one primary heading and add a specific accessible name to each clear button.

## Coverage and evidence

**162 page and route contexts received a browser document response** across 324 viewport attempts. This includes aliases, negative routes, shared portal variants and the two separately hosted timetable pages. The sweep considered **127 distinct Flask HTML page paths**. The Flask runtime inventory contains **388 registered URL rules**, including static routing and APIs.

[Page measurements and HTTP responses](NGIS-audit-evidence/page-results.json) · [Flask route inventory with methods and source lines](NGIS-audit-evidence/server-routes.json) · [Playwright workflow results](NGIS-audit-evidence/workflow-results.json) · [Targeted browser results](NGIS-audit-evidence/targeted-results.json) · [Regression suites](NGIS-audit-evidence/suite-results.json).

### Every discovered application page and route context

| Portal or host | Page or route | 1440 px | 375 px |
|---|---|---|---|
| Public / routing | `/` | 200 | 200 |
| Public / routing | `/404.html` | 200 | 200 |
| Public / routing | `/access-denied` | 200 | 200 |
| Public / routing | `/admin` | 200 · admin | 200 · admin, drawer check failed |
| Public / routing | `/audit-missing.html` | HTTP 404 | HTTP 404 |
| Public / routing | `/index.html` | 200 | 200 |
| Public / routing | `/pages-directory.html` | 200 | 200 |
| Public / routing | `/parent` | HTTP 404 | HTTP 404 |
| Public / routing | `/principal` | 200 · principal | 200 · principal, drawer opened |
| Public / routing | `/sitemap.html` | 200 · redirected | 200 · redirected |
| Public / routing | `/staff` | 200 · staff, redirected | 200 · staff, redirected, drawer check failed |
| Public / routing | `/student` | 200 · student | 200 · student, hamburger missing |
| Public / routing | `/superadmin` | HTTP 404 | HTTP 404 |
| Public / routing | `/teacher` | 200 · teacher | 200 · teacher, drawer opened |
| Student | `/pages/shared/announcements.html?portal=student` | 200 · student | 200 · student, drawer opened |
| Student | `/pages/shared/departments.html?portal=student` | 200 · student | 200 · student, drawer opened |
| Student | `/pages/shared/exams.html?portal=student` | 200 · student | 200 · student, drawer opened |
| Student | `/pages/shared/lessons.html?portal=student` | 200 · student, redirected | 200 · student, redirected, drawer opened |
| Student | `/pages/student/student-announcements.html` | 200 · student, redirected | 200 · student, redirected, drawer opened |
| Student | `/pages/student/student-assignments.html` | 200 · student | 200 · student, drawer opened |
| Student | `/pages/student/student-attendance.html` | 200 · student | 200 · student, drawer opened |
| Student | `/pages/student/student-calendar.html` | 200 · student | 200 · student, drawer opened |
| Student | `/pages/student/student-exams.html` | 200 · student | 200 · student, drawer opened |
| Student | `/pages/student/student-grades.html` | 200 · student | 200 · student, drawer opened |
| Student | `/pages/student/student-lost-found.html` | 200 · student | 200 · student, drawer check failed |
| Student | `/pages/student/student-notifications.html` | 200 · student | 200 · student, drawer opened |
| Student | `/pages/student/student-profile.html` | 200 · student | 200 · student, drawer opened |
| Student | `/pages/student/student-services.html` | 200 · student | 200 · student, drawer opened |
| Student | `/pages/student/student-timetable.html` | 200 · student | 200 · student, drawer opened |
| Student | `/pages/student/student.html` | 200 · student | 200 · student, drawer opened |
| Teacher | `/pages/shared/announcements.html?portal=teacher` | 200 · teacher | 200 · teacher, drawer opened |
| Teacher | `/pages/shared/departments.html?portal=teacher` | 200 · redirected | 200 · teacher, redirected, drawer opened |
| Teacher | `/pages/shared/exams.html?portal=teacher` | 200 · teacher | 200 · teacher, drawer opened |
| Teacher | `/pages/shared/lessons.html?portal=teacher` | 200 · teacher, redirected | 200 · teacher, redirected, drawer opened |
| Teacher | `/pages/teacher/teacher-announcements.html` | 200 · teacher, redirected | 200 · teacher, redirected, drawer opened |
| Teacher | `/pages/teacher/teacher-attendance.html` | 200 · teacher | 200 · teacher, drawer check failed |
| Teacher | `/pages/teacher/teacher-calendar.html` | 200 · teacher | 200 · teacher, drawer opened |
| Teacher | `/pages/teacher/teacher-departments.html` | 200 · teacher, redirected | 200 · teacher, redirected, drawer opened |
| Teacher | `/pages/teacher/teacher-documents.html` | 200 · teacher, redirected | 200 · teacher, redirected, drawer opened |
| Teacher | `/pages/teacher/teacher-exams.html` | 200 · teacher | 200 · teacher, drawer opened |
| Teacher | `/pages/teacher/teacher-gradebook.html` | 200 · teacher, redirected | 200 · teacher, redirected, drawer opened |
| Teacher | `/pages/teacher/teacher-lessons.html` | 200 · teacher | 200 · teacher, drawer opened |
| Teacher | `/pages/teacher/teacher-lost-found.html` | 200 · teacher | 200 · teacher, drawer opened |
| Teacher | `/pages/teacher/teacher-notifications.html` | 200 · teacher | 200 · teacher, drawer opened |
| Teacher | `/pages/teacher/teacher-profile.html` | 200 · teacher | 200 · teacher, drawer opened |
| Teacher | `/pages/teacher/teacher-reports.html` | 200 · teacher | 200 · teacher, drawer opened |
| Teacher | `/pages/teacher/teacher-roster.html` | 200 · teacher | 200 · teacher, drawer opened |
| Teacher | `/pages/teacher/teacher-services.html` | 200 · teacher | 200 · teacher, drawer check failed |
| Teacher | `/pages/teacher/teacher-submissions.html` | 200 · teacher | 200 · teacher, drawer check failed |
| Teacher | `/pages/teacher/teacher-timetable.html` | 200 · teacher | 200 · teacher, drawer opened |
| Teacher | `/pages/teacher/teacher.html` | 200 · teacher | 200 · teacher, drawer opened |
| Parent | `/pages/parent/parent.html` | HTTP 404 · targeted check | No mobile portal to open |
| Principal | `/pages/principal/principal-academic-workspace.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-activity.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-attendance.html` | 200 · principal | 200 · principal, drawer check failed |
| Principal | `/pages/principal/principal-classes.html` | 200 · principal | 200 · principal, drawer check failed |
| Principal | `/pages/principal/principal-data-dictionary.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-departments.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-dictionary-additional.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-dictionary-school.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-dictionary-students.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-dictionary-teachers.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-dictionary-timetable.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-exams.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-lost-found.html` | Restricted | Restricted |
| Principal | `/pages/principal/principal-profile.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-registration-approve.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-reports.html` | 200 · principal | 200 · principal, drawer check failed |
| Principal | `/pages/principal/principal-requests.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-school-information.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-services.html` | 200 · principal | 200 · principal, drawer check failed |
| Principal | `/pages/principal/principal-student-profiles.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-subjects.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-teacher-class-assignment.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal-teacher-profiles.html` | 200 · principal | 200 · principal, drawer check failed |
| Principal | `/pages/principal/principal-timetable-builder.html` | 200 · redirected | 200 · principal, drawer check failed |
| Principal | `/pages/principal/principal-timetables.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/principal/principal.html` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/shared/announcements.html?portal=principal` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/shared/departments.html?portal=principal` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/shared/exams.html?portal=principal` | 200 · principal | 200 · principal, drawer opened |
| Principal | `/pages/shared/lessons.html?portal=principal` | 200 · principal, redirected | 200 · principal, redirected, drawer opened |
| Admin | `/pages/admin/admin-absence-stats.html` | 200 · admin | 200 · admin, drawer check failed |
| Admin | `/pages/admin/admin-assignments.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-attendance.html` | 200 · admin | 200 · admin, drawer check failed |
| Admin | `/pages/admin/admin-campus.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-campuses.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-classes.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-dashboard-content.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-data-dictionary.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-department-detail.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-departments.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-dictionary-additional.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-dictionary-school.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-dictionary-students.html` | 200 · admin | 200 · admin, drawer check failed |
| Admin | `/pages/admin/admin-dictionary-teachers.html` | 200 · admin | 200 · admin, drawer check failed |
| Admin | `/pages/admin/admin-dictionary-timetable.html` | 200 · admin | 200 · admin, drawer check failed |
| Admin | `/pages/admin/admin-exams.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-grade-release.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-grades.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-lessons.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-logs.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-lost-found.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-modal-add-subject.html` | 200 | 200 |
| Admin | `/pages/admin/admin-news.html` | 200 · admin | 200 · admin, drawer check failed |
| Admin | `/pages/admin/admin-roles-permissions.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-school-information.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-security.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-services.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-settings.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-student-assign.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-student-profiles.html` | 200 · admin | 200 · admin, drawer check failed |
| Admin | `/pages/admin/admin-student-verify.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-subjects.html` | 200 · admin | 200 · admin, drawer check failed |
| Admin | `/pages/admin/admin-system-employee-accounts.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-system-employee-group.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-system-exam-config.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-system-general-setting.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-system-parent-accounts.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-system-schedule.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-system-school-week.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-system-school-year.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-system-student-accounts.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-teacher-class-assignment.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-teacher-profiles.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-teacher-verify.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-timetable-management.html` | 200 · admin, redirected | 200 · admin, redirected, drawer opened |
| Admin | `/pages/admin/admin-timetables.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-users-admins.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-users-principals.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-users-staff.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-users-students.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-users-teachers.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/admin/admin-users.html` | 200 · admin, redirected | 200 · admin, redirected, drawer opened |
| Admin | `/pages/admin/admin.html` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/shared/announcements.html?portal=admin` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/shared/departments.html?portal=admin` | 200 · admin | 200 · admin, drawer opened |
| Admin | `/pages/shared/exams.html?portal=admin` | Blocked · timeout or navigation error | 200 · admin, drawer opened |
| Admin | `/pages/shared/lessons.html?portal=admin` | 200 · admin, redirected | 200 · admin, redirected, drawer opened |
| Super Admin preview | `/pages/admin/admin.html?portal=superadmin` | 200 · superadmin | 200 · superadmin, drawer opened |
| Super Admin preview | `/pages/shared/announcements.html?portal=superadmin` | 200 · superadmin | 200 · superadmin, drawer opened |
| Super Admin preview | `/pages/shared/departments.html?portal=superadmin` | 200 · superadmin | 200 · superadmin, drawer opened |
| Super Admin preview | `/pages/shared/exams.html?portal=superadmin` | 200 · superadmin | 200 · superadmin, drawer opened |
| Super Admin preview | `/pages/shared/lessons.html?portal=superadmin` | 200 · superadmin, redirected | 200 · superadmin, redirected, drawer opened |
| Shared | `/pages/shared/404.html` | 200 | 200 |
| Shared | `/pages/shared/access-denied.html` | 200 | 200 |
| Shared | `/pages/shared/announcements.html` | 200 · student | 200 · student, drawer opened |
| Shared | `/pages/shared/department.html` | 200 · student | 200 · student, drawer opened |
| Shared | `/pages/shared/department.html?id=dept-mat` | 200 · admin | 200 · admin, drawer opened |
| Shared | `/pages/shared/departments.html` | 200 · student | 200 · student, hamburger missing |
| Shared | `/pages/shared/design-system-preview.html` | 200 · student | 200 · admin |
| Shared | `/pages/shared/empty-states-demo.html` | 200 · admin | 200 · admin, drawer opened |
| Shared | `/pages/shared/error.html` | 200 | 200 |
| Shared | `/pages/shared/exams.html` | 200 · admin | 200 · admin, drawer opened |
| Shared | `/pages/shared/lesson-details.html` | 200 · admin | 200 · admin, drawer opened |
| Shared | `/pages/shared/lesson-details.html?id=1` | 200 · admin | 200 · admin, drawer opened |
| Shared | `/pages/shared/lessons.html` | 200 · admin, redirected | 200 · admin, redirected, drawer check failed |
| Shared | `/pages/shared/news.html` | 200 · admin | 200 · admin, drawer check failed |
| Shared | `/pages/shared/onboarding.html` | 200 | 200 |
| Shared | `/pages/shared/transcript-viewer.html` | 200 | 200 |
| Shared | `/pages/shared/ux-demo.html` | 200 · admin | 200 · admin, drawer opened |
| Standalone timetable | `/` | 200 | 200 |
| Standalone timetable | `/schedule` | HTTP 500 | HTTP 500 |
| Standalone timetable | `/assign` | HTTP 404 | Schedule shell blocked |
| Standalone timetable | `/teachers` | HTTP 404 | Schedule shell blocked |
| Standalone timetable | `/classes` | HTTP 404 | Schedule shell blocked |
| Standalone timetable | `/subjects` | HTTP 404 | Schedule shell blocked |
| Standalone timetable | `/overtime` | HTTP 404 | Schedule shell blocked |
| Standalone timetable | `/now` | HTTP 404 | Schedule shell blocked |
| Standalone timetable | `/print` | HTTP 404 | Schedule shell blocked |

### Major workflow coverage

| ID | Portal | Workflow | Result and boundary |
|---|---|---|---|
| W01 | Public | Landing and portal entry | Four staff and learner cards reached on desktop. Mobile tap interception reproduced (F04). |
| W02 | Shared | Own-portal shell and mobile drawer | Direct-load shell metrics for each page. Dashboard refresh sampled. Scope and drawer exceptions are in the page table. |
| W03 | Shared | Cross-portal direct route isolation | Student was denied the canonical Admin page. Clean aliases returned foreign dashboard HTML with a Student shell (F11). |
| W04 | Parent | Sign-in, landing and account navigation | Fixture sign-in succeeded. Parent landing and role page returned 404. Remaining Parent workflows blocked (F02). |
| W05 | Super Admin | Dashboard and shared navigation | Query-based preview and refresh exercised. Fixture sign-in was rejected and privileged browser workflows were blocked. |
| W06 | Student | Assignments, submission upload and resubmission | Assignment shell checked. Submission persistence and upload paths not exercised. |
| W07 | Student | Report cards, grade visibility and attendance | Grade and attendance shells checked. Backend suite exited successfully. Ran 4 tests in 0.314s |
| W08 | Student | Published timetable, day filters and export | Network failure injected and misclassified as no enrollment (F13). The loading indicator was not conclusively observed. |
| W09 | Student | Calendar, announcements, notification read state and profile | Page shells checked. Calendar event action, read persistence and profile save unverified. |
| W10 | Student / Teacher / Admin / Principal | Services and lost-and-found submission, fulfillment, claims and return | Page shells checked. Account-specific submission, upload and fulfillment unverified. |
| W11 | Student / Teacher / Shared | Department context, lessons, exam materials and lesson detail | Shared portal variants and detail routes checked for direct-load shell. Materials upload and student assessment lifecycle unverified. |
| W12 | Teacher | Roster and homeroom workflows | Shell checked. Backend suite exited successfully. Ran 5 tests in 0.248s |
| W13 | Teacher | Gradebook and attendance editing, submissions and feedback | Page shells checked. Backend suite exited successfully. Ran 4 tests in 0.314s Browser saves, grading and feedback unverified. |
| W14 | Teacher | Teaching materials, exams, documents and reports | Page shells checked. File CRUD, assessment publication and report generation unverified. |
| W15 | Teacher | Timetable, calendar, news, notifications and profile | Page shells checked. Per-record actions unverified. |
| W16 | Admin | Add student from scratch | Wizard created a new person and account (201), login succeeded (200), and success screen returned to the directory. |
| W17 | Admin | Add teacher from scratch | Wizard created a new person and account (201), login succeeded (200), and success screen returned to the directory. |
| W18 | Admin | Add staff from scratch | Wizard created a new person and account (201), login succeeded (200), and success screen returned to the directory. |
| W19 | Admin | Add principal from scratch | Wizard created a new person and account (201), login succeeded (200), and success screen returned to the directory. |
| W20 | Admin | Add admin from scratch | Wizard created a new person and account (201), login succeeded (200), and success screen returned to the directory. |
| W21 | Admin | Registration photo and form feedback | PNG preview and removal exercised. Typed field loss and required-field feedback reproduced (F05). |
| W22 | Admin | Identity provisioning, status, audit trail and credential handling | Backend suite had failures or errors. Ran 24 tests in 6.854s Browser end-to-end status and reset flows unverified. |
| W23 | Principal | Academic adjustment review, clarification, acceptance, decline, publication and history | All four actions executed on sample record. Actual cross-session history and publication failed (F01). New request creation and correction resubmission unverified. |
| W24 | Principal | Registration, approvals, roster, classes, service and activity oversight | Backend suite exited successfully.  Registration decision UI and feed history not fully exercised. |
| W25 | Principal / Admin | School information and configuration | Backend suite had failures or errors. Ran 10 tests in 5.075s School year, calendar week and other system-setting mutations not individually exercised. |
| W26 | Principal / Admin | Timetable draft, validation, preview and publish | Backend suite had failures or errors. Ran 12 tests in 9.468s Backend tests ran. Standalone Next.js schedule blocked. Direct browser timetable writes unverified. |
| W27 | Principal / Admin | Timetable replacement and import | Backend suite exited successfully. Ran 6 tests in 0.779s Browser choose-file/import screens unverified. |
| W28 | Principal / Admin | Timetable monitoring and oversight | Backend suite exited successfully. Ran 13 tests in 2.044s Browser monitoring interactions unverified. |
| W29 | Admin / Principal | Campus and department permission boundaries | Scoped Admin read requests returned out-of-campus entries (F16). Department grants, out-of-scope writes and other role combinations unverified. |
| W30 | Admin / Super Admin | Roles, access, delegated permissions, visibility overrides and audit | Backend suite exited successfully. Ran 31 tests in 3.574s Backend tests ran. Full signed-in Super Admin browser session unverified. |
| W31 | Admin / Super Admin | Legacy route enforcement, hidden-only policy and scope resolver | Backend suite had failures or errors. Ran 37 tests in 1.501s Code and backend suite, plus browser alias checks under Student. |
| W32 | Admin | Sidebar navigation management | Backend suite had failures or errors. Ran 11 tests in 0.518s Published nav consumed during sweep. Admin editing and rollback UI unverified. |
| W33 | Admin | Dashboard page content, banners and publishing | Backend suite had failures or errors. Ran 9 tests in 0.793s Browser content editing and rollback unverified. |
| W34 | Admin / Principal / Teacher / Student | Exam administration and published exam data | Backend suite exited successfully. Ran 12 tests in 1.575s Browser exam creation, publish and students taking exams unverified. |
| W35 | Admin / Principal | Grade release, overrides, attendance correction, report-card and transcript upload/download | Shells inventoried. Transcript upload, grade release UI and override mutations not verified in a browser. |
| W36 | Admin | Account security, logs, system configuration, campus pages and organization management | Shells inspected. Security controls, private audit exports, department and campus mutation and restoring settings not exercised. |
| W37 | Admin / Principal | Data dictionary records, subjects, faculty assignments and school-year settings | Route coverage and code inspection. Full create/edit/delete/import/export combinations unverified. |
| W38 | Shared | Error, access denied, empty-state demonstrations, onboarding and design previews | Direct shells and a missing route exercised. Individual examples and onboarding progression unverified. |
| W39 | Shared | Keyboard focus and surface state | Inspect default, hover, press and keyboard focus measured. Sidebar label and active surface sampled (F06). |
| W40 | Standalone timetable | Home, schedule, mobile drawer and linked destinations | Home returned 200 with starter content. Schedule returned 500. Upstream timetable actions and mobile drawer blocked (F03). |

**31 of 40 workflow groups had a browser interaction or backend test execution.** Shell-only groups are shown separately in the table. A group can include a failed check or remaining scenario gaps.

### Backend regression evidence

| Suite | Exit | Observed summary |
|---|---:|---|
| `test_user_management.py` | 1 | FAIL: test_01_overview_metrics_derived_from_store (test_user_management.UserManagementTest.test_01_overview_metrics_derived_from_store) / FAIL: test_13_five_pages_exist_with_canonical_wiring (test_user_management.UserManagementTest.test_13_five_pages_exist_with_canonical_wiring) / FAIL: test_13b_no_live_references_to_removed_overview (test_user_management.UserManagementTest.test_13b_no_live_references_to_removed_overview) / Ran 24 tests in 6.854s / FAILED (failures=3) |
| `test_roles_access_v3.py` | 0 | Ran 31 tests in 3.574s / OK |
| `test_timetable_publication.py` | 1 | FAIL: test_11_builder_pages_load_publication_assets (test_timetable_publication.TimetablePublicationTest.test_11_builder_pages_load_publication_assets) / FAIL: test_12_ui_implementation_covers_workflow (test_timetable_publication.TimetablePublicationTest.test_12_ui_implementation_covers_workflow) / Ran 12 tests in 9.468s / FAILED (failures=2) |
| `test_roles_permissions.py` | 1 | ERROR: test_hidden_only_is_not_treated_as_access_deny (test_roles_permissions.TestResolutionAndEnforcement.test_hidden_only_is_not_treated_as_access_deny) / ERROR: test_hide_and_deny_blocks_direct_url (test_roles_permissions.TestResolutionAndEnforcement.test_hide_and_deny_blocks_direct_url) / FAIL: test_layout_copies_are_byte_identical (test_roles_permissions.TestFrontendWiring.test_layout_copies_are_byte_identical) / Ran 37 tests in 1.501s / FAILED (failures=1, errors=2) |
| `test_timetable_replacement.py` | 0 | Ran 6 tests in 0.779s / OK |
| `test_timetable_monitoring.py` | 0 | Ran 13 tests in 2.044s / OK |
| `test_simplified_exams.py` | 0 | Ran 12 tests in 1.575s / OK |
| `test_sidebar_manager.py` | 1 | FAIL: test_09_mobile_hamburger_compliance (test_sidebar_manager.TestSidebarManager.test_09_mobile_hamburger_compliance) / Ran 11 tests in 0.518s / FAILED (failures=1) |
| `test_dashboard_cms.py` | 1 | FAIL: test_01_runtime_content_endpoint (test_dashboard_cms.TestDashboardCMS.test_01_runtime_content_endpoint) / Ran 9 tests in 0.793s / FAILED (failures=1) |
| `test_khmer_suite.py` | 1 | ERROR: test_04_locked_subject_excluded_from_auto_assign (test_khmer_suite.TestKhmerSuite.test_04_locked_subject_excluded_from_auto_assign) / FAIL: test_09_subject_crud_and_cascade (test_khmer_suite.TestKhmerSuite.test_09_subject_crud_and_cascade) / FAIL: test_16_all_ten_page_shells_exist_and_wire_the_shared_ui (test_khmer_suite.TestKhmerSuite.test_16_all_ten_page_shells_exist_and_wire_the_shared_ui) (role='principal', module='wizard') / FAIL: test_16_all_ten_page_shells_exist_and_wire_the_shared_ui (test_khmer_suite.TestKhmerSuite.test_16_all_ten_page_shells_exist_and_wire_the_shared_ui) (role='principal', module='builder') / FAIL: test_16_all_ten_page_shells_exist_and_wire_the_shared_ui (test_khmer_suite.TestKhmerSuite.test_16_all_ten_page_shells_exist_and_wire_the_shared_ui) (role='principal', module='viewer') / FAIL: test_16_all_ten_page_shells_exist_and_wire_the_shared_ui (test_khmer_suite.TestKhmerSuite.test_16_all_ten_page_shells_exist_and_wire_the_shared_ui) (role='principal', module='subjects') / FAIL: test_19_pages_use_master_design_tokens_and_dark_theme (test_khmer_suite.TestKhmerSuite.test_19_pages_use_master_design_tokens_and_dark_theme) (role='principal', slug='teacher-class-assignment') / FAIL: test_19_pages_use_master_design_tokens_and_dark_theme (test_khmer_suite.TestKhmerSuite.test_19_pages_use_master_design_tokens_and_dark_theme) (role='principal', slug='timetable-builder') / FAIL: test_19_pages_use_master_design_tokens_and_dark_theme (test_khmer_suite.TestKhmerSuite.test_19_pages_use_master_design_tokens_and_dark_theme) (role='principal', slug='timetables') / FAIL: test_19_pages_use_master_design_tokens_and_dark_theme (test_khmer_suite.TestKhmerSuite.test_19_pages_use_master_design_tokens_and_dark_theme) (role='principal', slug='subjects') / FAIL: test_19_pages_use_master_design_tokens_and_dark_theme (test_khmer_suite.TestKhmerSuite.test_19_pages_use_master_design_tokens_and_dark_theme) (role='admin', slug='timetables') / Ran 19 tests in 2.313s |
| `test_ui_states_mvp.py` | 5 | Ran 0 tests in 0.000s |
| `tests/academic-mvp.test.py` | 0 | Ran 4 tests in 0.314s / OK |
| `tests/academic-architecture.test.py` | 0 | Ran 6 tests in 0.422s / OK |
| `tests/teacher-my-class.test.py` | 0 | Ran 5 tests in 0.248s / OK |
| `test_principal_e2e.py` | 0 | PASS: Page Load: /pages/principal/principal.html / PASS: Page Load: /pages/principal/principal-classes.html / PASS: Page Load: /pages/principal/principal-departments.html / PASS: Page Load: /pages/principal/principal-timetables.html / PASS: Page Load: /pages/principal/principal-attendance.html / PASS: Page Load: /pages/principal/principal-services.html / PASS: Page Load: /pages/principal/principal-lost-found.html / PASS: Page Load: /pages/principal/principal-teacher-profiles.html / PASS: Page Load: /pages/principal/principal-student-profiles.html / PASS: Page Load: /pages/principal/principal-reports.html / PASS: Page Load: /pages/principal/principal-activity.html / PASS: GET /api/classes returns 200 |
| `test_school_information_e2e.py` | 1 | FAIL: test_10_browser_views (__main__.SchoolInformationE2ETest.test_10_browser_views) / Ran 10 tests in 5.075s / FAILED (failures=1) |

### Remaining coverage gaps

- Parent portal is missing. Super Admin preview was reachable but the local Super Admin sign-in fixture was rejected. No staging identity was used.
- The standalone Next.js timetable returned 500 before its schedule and drawer could render. Its downstream MCP data flows were unverified.
- Browser verification used Chromium at 375 and 1440 px. Tablet breakpoints, other engines, physical devices, full keyboard traversal, screen-reader behavior and systematic color-contrast coverage remain open.
- Only the selected interactions and regression suites described above ran. Full data-state, cross-campus and cross-department write permutations, production configuration, email delivery, generated documents and hands-on browser end-to-end checks for all workflows remain open.
- The current snapshot contains pre-existing uncommitted changes. No prior build was executed for a binary regression comparison. Regression signals refer to the current repository test contracts.
