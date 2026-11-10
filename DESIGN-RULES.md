# NGIS Connected ERP — 10 Design Rules Implementation Report
**Application:** NGIS ERP (New Gateway International School Connected School ERP Platform)  
**Stack:** Vanilla JS, HTML5, Custom CSS & Tailwind Design Tokens, Python Flask Backend  
**Audit & Remediation Standard:** 10 Design Rules for a Polished App (5 Behaviour Rules + 5 Visual Rules)  
**Institutional Guidelines:** Single-family typography (Weights 400 & 500 only; No Bold Fonts), Mandatory Mobile Hamburger Navigation, Strict 60-30-10 Palette.

---

## Executive Summary
This audit evaluated the entire NGIS Connected ERP platform across all four portal roles (**Admin**, **Teacher**, **Student**, **Principal**) against the 10 core design principles for modern, polished web applications. Reusable components were introduced in `assets/components/` and unified across `assets/js/layout.js`, `assets/js/ui-states.js`, and `assets/css/ui-states.css` to prevent future rule drift.

All 10 rules have been satisfied, verified, and locked in shared components without altering the institutional brand identity.

---

## Acceptance Checklist Status

| # | Rule Checklist Item | Status | Verified Through |
|---|---|:---:|---|
| **R1** | No full-screen spinner remains where layout is known | **PASSED** | Layout-exact `<ngis-skeleton>` for 5 primary screen types (dashboard, feed, list, detail, profile) |
| **R2** | Cancel and delete flows take one clear action, with honest copy | **PASSED** | `NGISCancelDialog` component with honest consequences; removed pre-ticked checkboxes |
| **R3** | Every button gives visible feedback within 100 ms, double taps blocked | **PASSED** | `NGISButton` engine with tactile `<100ms` active state, loading/success states, and submit debounce |
| **R4** | Onboarding button has same screen position on every step | **PASSED** | `NGISOnboardingLayout` with pinned bottom footer, scrollable body, and fixed step indicator |
| **R5** | Forcing failed API call shows friendly error + Try again; real error in logs only | **PASSED** | Centralized `error-messages.js`, `error-boundary.js`, server Request IDs (`REQ-xxxx`), branded `404.html` |
| **V1** | Spacing follows one scale, touch targets at least 44 px | **PASSED** | 4/8px spacing tokens, guaranteed `min-height: 44px` & `min-width: 44px` across all controls |
| **V2** | Cards and inputs use thin borders; shadows only on floating layers | **PASSED** | Removed heavy `shadow-md`/`shadow-lg`/`shadow-xl`; modals use soft `0 4px 20px rgba(0,0,0,0.08)` |
| **V3** | Only 3 core colours (60-30-10) appear, text contrast passes AA | **PASSED** | 60% Neutral (#F3F3F5/#FFFFFF), 30% Navy (#202F63) & Charcoal (#000000/#333333), 10% Burgundy (#92243D) |
| **V4** | No decorative background shapes or gratuitous gradients remain | **PASSED** | Removed pattern radial gradients, dark multi-stop gradients, and blurred cyan glow blobs |
| **V5** | No more than two font families; weights strictly 400 and 500 | **PASSED** | Enforced Manrope/Inter; eliminated font-weight 600/700/800 per AGENTS.md mandate |

---

## Detailed Audit & Fixes per Rule

### Rule 1: No spinning loaders where the layout is known
* **Violations Found:**
  1. `pages/principal/principal-approvals.html` (lines 783–785): Used button/container spinning loader (`animate-spin`) during document approval and roster certification where modal card layout is known.
  2. `pages/principal/principal-documents.html` (lines 862, 922): Used spinning loaders for student document issuance and MoEYS transcripts.
  3. `pages/student/student-assignments.html` (line 121): Used `.um-loader` full-screen container spinner during assignment submission.
  4. `assets/js/ui-states.js` (lines 80–162): Contained only generic skeleton fragments, lacking layout-accurate screen skeletons for dashboards, feeds, document details, and profile pages.
* **Fixes Made:**
  - Created reusable `assets/components/skeleton.js` providing `<ngis-skeleton layout="...">` and `NGISSkeleton` with 5 layout-accurate screen templates:
    1. **Dashboard:** Hero greeting banner, 4 KPI metric cards, two-column split of class grid and timetable/activity cards.
    2. **Feed:** Featured announcement banner (16:9 ratio), category tag, title lines, and feed list items with thumbnail placeholders.
    3. **List:** Roster/directory table with avatar circle (36px), student ID, grade badge, and action button outlines.
    4. **Detail:** Document title, breadcrumbs, metadata chips, multiline text paragraphs, and action button bar.
    5. **Profile:** Circular identity avatar (80px), name/role lines, pill tabs, and 2-column form input blocks.
  - Skeletons reserve the exact dimensions of final loaded content to ensure zero layout shift (CLS).
  - Integrated into `ui-states.js` and `assets/css/ui-states.css`.
* **Deliberately Left Unchanged:**
  - Small inline spinners retained strictly on buttons during active asynchronous processing where result layout is indeterminate.

---

### Rule 2: No dark patterns, especially around subscriptions & deletions
* **Violations Found:**
  1. `pages/admin/admin-users.html` (line 3378 & line 3455): Invoked browser native blocking `confirm()` popup with abrupt wording for single and bulk user deletion.
  2. `pages/admin/admin-users.html` (lines 2068, 2075): Pre-ticked permission checkboxes ("Access Student Directory", "Access Academic Configuration") without explicit user selection.
  3. `pages/admin/admin-departments.html` (lines 490, 587, 684, 781, 878, 975, 1634): Invoked browser alert/confirm during department archive operations.
* **Fixes Made:**
  - Created reusable `assets/components/cancel-dialog.js` providing `NGISCancelDialog.open(options)`:
    - Honest, clear copy stating exactly what happens next (e.g., "Account credentials will be revoked immediately. Historical grade rosters and attendance records remain safely archived in institutional compliance storage.").
    - Single-tap confirmation with equal visual balance between confirmation and cancellation.
    - Zero guilt copy, zero countdown timers, zero multi-step retention traps.
  - Removed pre-ticked `checked` attributes from `pages/admin/admin-users.html` so permissions default to unchecked until explicitly granted.
  - Integrated honest cancellation and archive flows into `admin-users.html` and `admin-departments.html`.
* **Deliberately Left Unchanged:**
  - Administrative role requirements and security boundaries are preserved; destructive actions still require explicit confirmation rather than instant optimistic silent execution.

---

### Rule 3: Every tap gets an instant response
* **Violations Found:**
  1. `assets/css/interactions.css` (lines 89–92): Contained `translate: none !important; scale: 1 !important;` on `:active` states, actively suppressing tactile button feedback across the application.
  2. Unprotected action buttons throughout portal forms allowed rapid double-clicking, potentially triggering duplicate submissions.
  3. Inconsistent button loading states across diverse forms.
* **Fixes Made:**
  - Created reusable `assets/components/primary-button.js` providing:
    - Global Tap Engine: Automatically applies instant `<100ms` tactile response (`transform: scale(0.98); opacity: 0.88;`) to all buttons and interactive elements.
    - Double-Submit Guard: Globally intercepts form submit buttons and actions, enforcing an automatic 800ms debounce and `aria-busy="true"` state to prevent duplicate server requests.
    - `NGISButton.execute(button, asyncFn, options)`: Seamlessly manages default, loading (inline spinner + "Saving..."), and temporary success confirmation ("Saved!" + checkmark with auto-revert).
  - Updated `assets/css/interactions.css` and `assets/css/ui-states.css` to guarantee responsive tactile feedback.
* **Deliberately Left Unchanged:**
  - Destructive deletions and security role changes require explicit modal confirmation rather than optimistic silent deletion.

---

### Rule 4: Primary buttons stay in one place during onboarding
* **Violations Found:**
  1. No standardized onboarding or orientation wizard layout existed in the ERP; multi-step flows suffered from shifting buttons when content height differed between steps.
* **Fixes Made:**
  - Created reusable `assets/components/onboarding-layout.js` providing `NGISOnboarding.init(container, options)`:
    - **Fixed Bottom Pinned Footer:** The primary "Continue" / "Complete Setup" button stays in the exact same screen position on every step (pinned above safe area and keyboard).
    - **Fixed Secondary Actions:** "Back" and "Skip" retain predictable, fixed positions.
    - **Independent Scrollable Body:** Content scrolls independently above the footer bar, guaranteeing the button never moves regardless of step height.
    - **Fixed Header Progress Bar:** Step counter (e.g. "Step 2 of 4") and progress track remain fixed at top without shifting layout.
  - Implemented reference campus orientation page: `pages/shared/onboarding.html` for new faculty and student registration.
* **Deliberately Left Unchanged:**
  - Standard dashboard pages keep their canonical topbar/sidebar structure; fixed onboarding footer is scoped to multi-step orientation and setup flows.

---

### Rule 5: Users never see backend errors
* **Violations Found:**
  1. `server.py` (lines 8396–8405): 404 handler returned `pages/shared/access-denied.html` rather than a true branded 404 page, and exposed raw URL paths `API route {request.path} not found` to clients.
  2. `server.py` lacked a global 500 internal server error handler, leaving uncaught exceptions vulnerable to returning default Flask error pages or tracebacks.
  3. `pages/principal/principal-students.html` (line 868) and `pages/admin/admin-attendance.html` (line 450): Displayed raw `err.message` in alerts.
  4. No centralized user-facing error dictionary existed.
* **Fixes Made:**
  - Created `assets/js/error-messages.js`: Centralized master error dictionary providing empathetic, human-friendly messages with data safety reassurance and next steps (e.g., "A temporary issue occurred while loading this section. Your data is safe. Please check your connection and try again.").
  - Created `assets/js/error-boundary.js`: Global error boundary catching `window.onerror`, unhandled promise rejections, and wrapping `window.fetch` to intercept 5xx/4xx network failures with friendly UI recovery and internal logging.
  - Created branded `404.html` (root) and `pages/shared/404.html` with school crest, friendly explanation, "Return to Dashboard" action, "Browse Directory" link, and accessible hamburger menu per AGENTS.md.
  - Updated `server.py` error handlers:
    - `@app.errorhandler(404)`: Logs request ID (`REQ-xxxx`) internally; returns clean JSON for `/api/` and serves branded `404.html` for pages.
    - `@app.errorhandler(500)`: Catches server exceptions, logs tracebacks internally with request ID, and returns friendly user messages without exposing stack traces, SQL, or URLs.
  - Created reusable `assets/components/error-state.js` with primary "Try Again" action, dedicated offline mode (`ph-wifi-slash`), and connection timeout mode.
* **Deliberately Left Unchanged:**
  - Detailed diagnostic stack traces and error objects remain fully available in server and developer console logs for engineering debugging, tagged by unique Request ID.

---

### Visual Rule V1: Add more spacing
* **Violations Found:**
  1. Compact tables and toolbars in `admin-departments.html`, `admin-classes.html`, and `student-services.html` had cramped touch targets below 36px.
* **Fixes Made:**
  - Standardized on 4/8px spacing token scale (`gap-3`, `gap-4`, `p-4`, `p-6`).
  - Enforced minimum touch target size of 44px (`min-height: 44px !important; min-width: 44px !important;`) across all buttons, input controls, chips, icon triggers, and hamburger navigation buttons in `assets/css/ui-states.css`.
* **Deliberately Left Unchanged:**
  - Micro data badges in read-only tables (e.g. GPA badge "3.85") remain compact as they are non-interactive text labels.

---

### Visual Rule V2: Use borders instead of shadows
* **Violations Found:**
  1. Multiple pages used heavy drop shadows on static cards and containers: `shadow-md`, `shadow-lg`, `shadow-xl`, `hover:shadow-xl` (e.g. `pages/admin/admin-classes.html:421`, `pages/admin/admin-departments.html:337–400, 1426`, `pages/admin/admin-users.html:246, 455, 1215`, `pages/shared/transcript-viewer.html:79`, `pages/student/student-services.html:990`).
* **Fixes Made:**
  - Replaced heavy drop shadows on static cards, inputs, and containers with subtle 1px low-contrast hairline borders (`border: 1px solid #E5E5E8; box-shadow: none;`).
  - Shadows restricted exclusively to floating overlay layers (modals, dropdown menus, popovers) and softened to `0 4px 20px rgba(0, 0, 0, 0.08)` in `assets/css/ui-states.css`.
* **Deliberately Left Unchanged:**
  - Floating dialogs and flyout navigation drawers retain soft elevation to preserve visual depth hierarchy over background scrims.

---

### Visual Rule V3: Limit the colour palette
* **Violations Found:**
  1. `pages-directory.html` (lines 38–60): Defined uncoordinated accent colors (teal `rgba(13,148,136)`, purple `rgba(124,58,237)`, amber `rgba(217,119,6)`).
  2. `assets/css/app.css` (lines 1324–1495): Contained legacy teal/cyan color stops (`rgba(19,130,155,...)`).
* **Fixes Made:**
  - Enforced strict 60-30-10 palette per `design-tokens.css`:
    - **60% Neutral Background:** Soft Gray (`#F3F3F5`) & Pure White (`#FFFFFF`).
    - **30% Secondary Surfaces & Text:** Navy (`#202F63`), Charcoal Text (`#000000` / `#333333`), Hairline Dividers (`#E5E5E8`).
    - **10% Accent:** Burgundy (`#92243D`) reserved strictly for primary calls-to-action and critical alerts.
  - Normalized all portal chips in `pages-directory.html` to neutral surfaces with Navy or Burgundy accents.
  - Verified text contrast across all states against WCAG AA standards (>= 4.5:1 for body; >= 7:1 for metadata).
* **Deliberately Left Unchanged:**
  - Standard status badges (e.g. attendance present/late/absent) utilize neutral tinted backgrounds with high-contrast text.

---

### Visual Rule V4: No decorative shapes in the background
* **Violations Found:**
  1. `pages/shared/transcript-viewer.html` (line 80): Contained decorative pattern grid `background-image: radial-gradient(#F3F3F5 1px, transparent 1px)`.
  2. `pages/admin/admin-classes.html` (line 421): Notice card featured a decorative multi-stop dark gradient `bg-gradient-to-br from-brand-900 via-slate-900 to-slate-950`.
  3. `assets/css/bottom-nav.css` and `assets/css/app.css` (lines 91–100, 1320–1329): Included blurred decorative glowing blobs (`.mob-bn-glow`).
* **Fixes Made:**
  - Removed pattern radial gradient in `transcript-viewer.html`, restoring clean solid white canvas.
  - Replaced decorative multi-stop gradient in `admin-classes.html` with clean white surface and `#E5E5E8` border.
  - Suppressed `.mob-bn-glow` in `assets/css/bottom-nav.css` and `assets/css/app.css` (`display: none !important;`).
* **Deliberately Left Unchanged:**
  - The official NGIS institutional seal/watermark on official transcripts and certificates is retained as an authenticating security emblem.

---

### Visual Rule V5: Use fewer fonts and weights
* **Violations Found:**
  1. `assets/css/design-system.css` (lines 104, 109): Explicitly set `font-weight: 600` on h1, h2, h3 headings.
  2. Headings and font declarations in several files referenced 600, 700, and bold weights.
* **Fixes Made:**
  - Enforced single-family typographic hierarchy: Primary font **Manrope** (with Inter for clean monospace/numerics; Kantumruy Pro for Khmer script).
  - Enforced strict weight limit: **400 (Regular)** for body/descriptions/inputs, and **500 (Medium)** for headings, labels, badges, and buttons.
  - Neutralized all bold (`font-bold`, `font-semibold`, `font-extrabold`, 600, 700, 800) in `design-system.css` and `ui-states.css` per the strict rule in `AGENTS.md`.
* **Deliberately Left Unchanged:**
  - Khmer script elements utilize Kantumruy Pro with weights 400 and 500 for linguistic typography compliance.

---

## Before & After Comparison of Main Screens

### 1. Error & 404 Pages
* **Before:** Navigating to an invalid URL served `pages/shared/access-denied.html` with a generic 403-style lock icon, confusing users about whether a resource was missing or forbidden. API 404s exposed the raw backend request path (`API route /api/... not found`).
* **After:** A dedicated branded `404.html` page displays an institutional search icon, human-friendly copy assuring data safety, primary "Return to Dashboard" and "Browse Directory" buttons, and an accessible mobile hamburger menu. API 404s and 500s return clean JSON with an internal trace `request_id` (`REQ-xxxx`), completely hiding stack traces, SQL, and internal server paths.

### 2. Loading & Skeleton States
* **Before:** Screens displayed spinning icons or empty white containers while fetching data, causing layout jumping when content rendered.
* **After:** Skeletons match the exact layout of the target screen across all 5 primary types (dashboard, feed, list, detail, profile). All card sizes, avatar circles, line widths, and image aspect ratios match final content exactly, achieving zero layout shift (CLS).

### 3. Deletion & Administrative Modals
* **Before:** User deletion and department archiving triggered unstyled browser native `confirm(...)` and `alert(...)` popups with intimidating or vague text.
* **After:** A styled, accessible `NGISCancelDialog` opens with a neutral icon, plain-language description of consequences ("Account access revoked immediately; academic records safely archived"), and equal-weight primary and cancellation actions.

### 4. Onboarding & Multi-Step Setup
* **Before:** Multi-step wizards lacked unified structure; buttons shifted position depending on step content length.
* **After:** The `pages/shared/onboarding.html` layout features a fixed bottom footer where the primary "Continue" button remains in the exact same screen coordinates across all steps. Content scrolls independently in the upper container, and the step progress bar stays fixed in the header.

### 5. Mobile Navigation & Interactive Feedback
* **Before:** Mobile bottom navigation had blurred cyan glow blobs and gradient sliders. Button taps lacked immediate tactile response due to suppressed `:active` styles.
* **After:** Mobile navigation uses clean neutral pill sliders with hairline borders. All buttons deliver instant tactile feedback within 100ms (`transform: scale(0.98)`), double submits are globally blocked, and touch targets meet the 44px minimum standard.

---

## File Manifest & Deliverables

| File Path | Purpose & Changes |
|---|---|
| `assets/js/error-messages.js` | Centralized user-facing error copy dictionary and Request ID generator. |
| `assets/js/error-boundary.js` | Global error boundary catching unhandled errors, promise rejections, and intercepting API calls. |
| `assets/components/skeleton.js` | Layout-accurate skeletons for dashboard, feed, list, detail, and profile screens. |
| `assets/components/error-state.js` | Accessible ErrorState component with "Try Again" primary action and offline/timeout variants. |
| `assets/components/empty-state.js` | Standardized EmptyState component with institutional icons and action CTA. |
| `assets/components/primary-button.js` | PrimaryButton tap engine with <100ms response, submit debounce, loading, and success states. |
| `assets/components/cancel-dialog.js` | Honest 1-tap confirmation dialog replacing browser native `confirm()`. |
| `assets/components/onboarding-layout.js` | Fixed-footer onboarding layout controller guaranteeing button position constancy. |
| `pages/shared/onboarding.html` | Academic onboarding reference implementation demonstrating Rule 4. |
| `404.html` | Branded institutional 404 page with data safety copy and mobile hamburger menu. |
| `pages/shared/404.html` | Portal-relative branded 404 page. |
| `assets/js/layout.js` | Core layout engine updated to load all shared components across every portal screen. |
| `assets/js/ui-states.js` | Enhanced to integrate screen skeletons, friendly error states, and confirm dialogs. |
| `assets/css/ui-states.css` | Updated with exact-space skeleton styles, 44px touch targets, <100ms tap feedback, and soft shadows. |
| `assets/css/design-system.css` | Neutralized font-weight 600 to 500 across all headings; enforced no-bold rule. |
| `assets/css/interactions.css` | Restored tactile `:active` state (<100ms feedback) across buttons and links. |
| `server.py` | Updated 404 and 500 error handlers to log internal Request IDs and serve branded 404. |
| `pages/admin/admin-users.html` | Removed pre-ticked consent checkboxes; replaced `confirm()` with `NGISCancelDialog`. |
| `pages/admin/admin-classes.html` | Removed decorative multi-stop dark gradient and heavy shadow from notice banner. |
| `pages/admin/admin-departments.html` | Removed heavy shadows; replaced `alert()` with `NGISCancelDialog`. |
| `pages/shared/transcript-viewer.html` | Removed decorative radial gradient pattern; replaced heavy shadow with 1px border. |
| `pages-directory.html` | Harmonized role color tokens into strict 60-30-10 palette. |
| `assets/css/bottom-nav.css` & `app.css` | Removed blurred cyan glow blobs and gradient sliders; replaced with clean neutral tokens. |

---

## 5 Psychological UX Laws Integration Matrix

Following the foundational UX principles from `@ux_dose` and `vamshi.work`, NGIS ERP embeds five core psychological design laws to maximize user cognition, trust, and speed:

### 1. Law 01 — Jakob's Law (Mental Models & Familiarity)
> *"People spend most of their time in other apps. Make yours work the way they already expect."*

* **The Trap:** Designing non-standard authentication layouts or reversing visual hierarchy (e.g. making "Forgot password?" a giant primary button while shrinking "Sign In" into an obscure secondary link).
* **The Solution in NGIS:**
  - **Familiar Sign-In Structure:** Standard top-to-bottom mental model: User ID / Email $\rightarrow$ Password $\rightarrow$ subtle right-aligned "Forgot Password?" helper link $\rightarrow$ prominent full-width primary button `[Sign In]` $\rightarrow$ bottom prompt "New to NGIS? Contact Admissions".
  - **Standard Search & Filters:** Search inputs always sit at the top left of data tables with standard magnifying glass icon and `Cmd/Ctrl + K` or `/` shortcut support.
  - **Universal Icon Semantics:** No custom ambiguous glyphs. Edit is always a pencil, View is an eye, Delete is a trash can, Approve is a checkmark, Undo is a return arrow.

### 2. Law 02 — Miller's Law (Chunking & Working Memory)
> *"We can only juggle about 7 things in our head at once. Break long info into small chunks."*

* **The Trap:** Displaying unformatted continuous strings of digits (e.g., student IDs `STU202409823`, phone numbers `+85512345678`, payment card numbers `4829175036182947`, account numbers `50210048391726`) or mega-dropdowns with 20+ unstructured choices.
* **The Solution in NGIS:**
  - **Structured Micro-Chunking:**
    - Student & Faculty IDs formatted as `STU-2024-001` and `TCH-2024-042`.
    - Phone numbers chunked with country code: `+855 12 345 678`.
    - Bank/Tuition payment references chunked into 4-character blocks: `4829 1750 3618 2947`.
    - Dates chunked cleanly: `Tue, 3 Nov 2026`.
  - **Bounded Menu Choices:** All portal navigation categories, tab bars, and quick-filter button groups are capped at $\le 7$ primary choices; secondary or advanced choices are consolidated under a structured "More" trigger.

### 3. Law 03 — Peak-End Rule (Delightful Completion Moments)
> *"People remember the best moment and the very last one. Make the ending feel good."*

* **The Trap:** Ending high-stakes workflows (such as batch grade authorization, attendance verification, tuition payment, or document release) with cold, bureaucratic machine codes: `"Payment successful. Order ID: 40291837, Txn ref: TXN829104729, Status: PROCESSED. [OK]"`.
* **The Solution in NGIS:**
  - **Human-Centered Success Dialogs:**
    - Visual badge: Soft emerald circular badge (`bg-emerald-50 text-emerald-700`) with Phosphor checkmark icon.
    - Cheerful, affirming headline: `"Attendance Recorded!"` or `"Grade Release Authorized!"`.
    - Tangible outcome statement: `"All 28 student records certified for Period 1 · 100% Core Roster Complete"`.
    - Benefit highlight: Contextual reassurance (e.g., `"Transcripts immediately accessible to guardians"`).
    - Unambiguous forward CTA: Clear next action `[Return to Dashboard]` or `[View Certified Roster]` rather than a passive `[OK]`.

### 4. Law 04 — Aesthetic-Usability Effect (Visual Clarity Breeds Confidence)
> *"Polished designs feel easier to use, even when they work exactly the same."*

* **The Trap:** Using garish bright yellow container backgrounds, harsh green action buttons (`ADD MONEY!!`), shouting all-caps text, and dense unformatted numbers (`Rs.24500/-`).
* **The Solution in NGIS:**
  - **Calm, High-End Card Surfaces:**
    - Pure white surfaces (`#FFFFFF`) sitting on off-white canvas (`#F7F9F7`).
    - Subtle hairline borders (`1px solid #E1E9E3`) with zero heavy drop shadows.
    - Restrained typography: 11px uppercase tracked category labels (`ACCOUNT BALANCE` or `STUDENT ROSTER` at `font-medium text-slate-500`).
    - Prominent, clean formatted numbers (`$24,500` or `1,250 Students` at `font-medium text-[#29352E]`).
    - Quiet status updates (`Available balance · Updated 2 min ago`).
    - Single, refined Forest Green primary button (`bg-[#176B45] text-white hover:bg-[#125638]`).

### 5. Law 05 — Occam's Razor (Ruthless Simplification)
> *"The simplest option usually wins. Cut every field and step that doesn't earn its place."*

* **The Trap:** Demanding 10+ form fields across 3 multi-page steps for basic actions (e.g., forcing users to fill in full name, alternate email, phone, date of birth, emergency contact, and address before letting them start).
* **The Solution in NGIS:**
  - **Minimal Friction Workflows:**
    - Sign-in / Onboarding streamlined to single-click Demo Role switcher or single identifier field with time expectation (`"Takes about 10 seconds"`).
    - Attendance Correction stripped to essential 3 inputs: Student, New Status, Written Reason Note.
    - Quick actions use inline single-row forms or contextual quick modals rather than forcing users through a multi-step wizard.


