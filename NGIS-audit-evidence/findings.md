# NGIS-SYSTEM audit

Audit date: 2026-11-21 local time. The audit used the working-tree snapshot, including existing uncommitted changes. Existing screenshots and prior audit notes were used only to identify areas to inspect. Playwright Chromium used 1440 px desktop and 375 px mobile viewports. The Flask page sweep targeted localhost:3000. Sample writes and backend regression suites used a disposable copy on localhost:3017. The standalone Next.js timetable ran on localhost:3001.

A page shell check covers direct navigation, document response and title, rendered portal and header signals, document-level horizontal overflow, script errors and, where present, the mobile drawer control. It does not imply that every form or record on that page was exercised. An access-denied document returned with HTTP 200 is recorded as restricted, not as coverage of the intended page. The static design scanner examined 165 files and found signals in five of six applicable families. Four were inapplicable. Individual issues below distinguish reproduced behavior from source observations.

## Fix priority and findings

### F01. Principal adjustment actions claim cross-portal publication but persist only in the current browser

- **High · Browser-verified.** Principal Adjustment Requests and the Admin subject, faculty assignment and timetable review drawers.
- **Reproduce.** As Principal, open Adjustment Requests, select **Inspect** on a submitted record, then use **Request Clarification**, **Accept Request**, **Publish & Complete** and **Decline**. Refresh, then open the same request in a fresh browser context.
- **Expected.** Only the authorized reviewer can transition a request. History records the actual actor, enforces valid transitions and survives across sessions. Publication updates the official record.
- **Actual.** The Principal can invoke all four Admin actions, even decline after completion. History attributes the Principal's actions to a hard-coded Admin identity. The current browser retained five timeline entries and a Declined state after refresh. A fresh context showed the original Submitted state. The Publish handler updates only the request status and shows a cross-portal success message.
- **Source and evidence.** [Principal Inspect handler](pages/principal/principal-requests.html#L227) · [browser storage](assets/js/academic-requests.js#L10) · [transition handlers](assets/js/academic-requests.js#L737) · [actions screenshot](NGIS-audit-evidence/principal-inspect-actions.png) · [workflow results](NGIS-audit-evidence/workflow-results.json).
- **Priority.** Move transitions and history to server-backed, scoped actions. Derive authorship from the session and make publication contingent on updating the authoritative record.

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

### F10. Registration adjustment history wording obscures who is responsible

- **Low · UX observation.** Principal Adjustment Requests.
- **Reproduce.** Open an item via **Inspect** as Principal and read the drawer's actions and timeline.
- **Expected.** The drawer identifies whether an action is a review, a correction request or an audit detail, and shows who can perform it.
- **Actual.** The same Admin-oriented drawer opens on the Principal page. Clarification is entered in a native prompt with a prefilled example, which can be submitted as the actual rationale.
- **Source and evidence.** [Shared review labels and prompts](assets/js/academic-requests.js#L737) · [review screenshot](NGIS-audit-evidence/principal-inspect-actions.png).
- **Priority.** Use role-specific action labels and require an explicit rationale in a labeled input.


### F11. Clean dashboard aliases serve another portal's dashboard inside the signed-in user's shell

- **High · Browser-verified.** Public route aliases and the Admin, Teacher and Principal dashboards when visited from a Student session.
- **Reproduce.** Enter the Student demo and open the canonical Admin dashboard URL. Then navigate directly to /admin, /teacher and /principal.
- **Expected.** The canonical URLs and their aliases apply the same permission decision. The dashboard and shell belong to the same role.
- **Actual.** The canonical Admin path reached Access Restricted. The three aliases returned HTTP 200 and their own dashboard titles while the rendered shell stayed Student. The browser check established foreign dashboard HTML delivery. It did not establish unauthorized access to API records or write operations.
- **Source and evidence.** [Page access gate](server.py#L93) · [direct dashboard alias handlers](server.py#L9544) · [portal resolution](assets/js/layout.js#L836) · [signed-in route comparison](NGIS-audit-evidence/targeted-results.json).
- **Priority.** Have aliases redirect to canonical gated routes or invoke the same page authorization before rendering.

### F12. Identity regression tests still require the removed-overview contract

- **Low · Code-only, confirmed by backend test execution.** Admin User Management directory and CI.
- **Reproduce.** Run the user management regression suite against the working-tree snapshot.
- **Expected.** Tests and the intended Admin directory routes agree on whether the all-users overview exists.
- **Actual.** Two tests require admin-users.html to be absent, but the working tree includes and serves it. The test run also reported a separate overview metric mismatch. The metrics fixture includes existing locally provisioned accounts, so the mismatch requires a clean seed rerun before calling it an application defect.
- **Source and evidence.** [User Management suite](tests/test_user_management.py) · [Admin Users overview](pages/admin/admin-users.html) · [suite results](NGIS-audit-evidence/suite-results.json).
- **Priority.** Confirm the intended overview behavior and update the route contract and test fixture accordingly.

### F13. Student timetable reports missing enrollment during a service failure

- **Medium · Browser-verified.** Student Class Timetable.
- **Reproduce.** Open Class Timetable while its timetable state service responds with HTTP 503. The test injected that response locally.
- **Expected.** The timetable reports a temporary service failure and offers Retry while preserving the user's enrollment context.
- **Actual.** The page said “No enrollment record found” and displayed no Retry action. The enrollment resolver treats failed catalog loading as an empty result.
- **Source and evidence.** [Enrollment lookup and failure handling](pages/student/student-timetable.html#L233) · [empty-state rendering](pages/student/student-timetable.html#L428) · [browser screenshot](NGIS-audit-evidence/student-timetable-network.png) · [state results](NGIS-audit-evidence/states-results.json).
- **Priority.** Distinguish unavailable services from successful empty data and route failures to the retry state.

### F14. Student hub headers create competing primary headings and unnamed clear buttons

- **Low · Browser-verified markup observation.** Student Services Hub and Lost & Found Hub at desktop and mobile sizes.
- **Reproduce.** Open either hub and inspect its heading hierarchy and search controls. The page sweep recorded every rendered H1 and visible button naming attributes.
- **Expected.** The shell provides one clear primary page heading. The search clear button has an accessible name when shown.
- **Actual.** Each hub exposes both the shared hero title and a question as H1. The clear-search buttons have no text, title or ARIA name in the observed DOM.
- **Source and evidence.** [Services page heading and control](pages/student/student-services.html#L162) · [Lost & Found heading and control](pages/student/student-lost-found.html#L387) · [desktop and mobile DOM measurements](NGIS-audit-evidence/page-results.json).
- **Priority.** Preserve one primary heading and add a specific accessible name to each clear button.

### F15. Standalone timetable home still shows the scaffold landing page

- **Medium · Browser-verified.** Standalone timetable home.
- **Reproduce.** Start the standalone timetable using the documented dev command and open its root URL.
- **Expected.** The root introduces the timetable or routes to its first operational screen.
- **Actual.** The root renders the Create Next App starter with external Next.js and Vercel links and no entry to the local schedule.
- **Source and evidence.** [Root page](timetable/src/app/page.tsx#L26) · [rendered landing links](NGIS-audit-evidence/targeted-results.json).
- **Priority.** Replace the scaffold with a timetable entry route after the compile blockers are resolved.

### F16. A single-campus Admin can read campus and directory results outside the assigned campus

- **High · Browser-verified.** Admin Campus directory and Student Accounts data.
- **Reproduce.** In a disposable instance, create an Admin account scoped to one branch with the standard registration endpoint. Sign in as that account and compare the campus and student directory responses with the assigned campus.
- **Expected.** The account sees its assigned campus and in-scope student rows. The campus filter applies automatically based on the signed-in identity.
- **Actual.** The signed-in, single-campus fixture received three campus entries, including two outside its assignment. The student directory returned rows labeled with the assigned campus and Sensok. The test recorded counts and campus labels only. Out-of-scope writes were unverified.
- **Likely source.** The campus handler allows all entries when its account lookup yields no campus. The user directory applies request filters to the full row set without enforcing the actor's campus. In the department listing handler, the code initializes its result from the full departmental registry. The scoped Admin fixture had no configured single-department grant, so cross-department isolation remains unverified.
- **Source and evidence.** [Campus actor resolution](admin_operations_api.py#L227) · [department listing](admin_operations_api.py#L332) · [user directory](user_management_api.py#L719) · [signed-in scope comparison](NGIS-audit-evidence/targeted-results.json).
- **Priority.** Resolve scope from the authenticated account consistently and enforce it in both list queries and write guards. Verify each scoped route with a single-campus and single-department fixture.

